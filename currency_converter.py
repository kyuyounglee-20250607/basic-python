# 실시간 환율 정보를 웹에서 수집하여 지폐 단위로 환전하는 환율 변환기
# pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup

# 국가별 통화 코드 매핑
country_currency = {
    '한국': 'KRW',
    '미국': 'USD',
    '일본': 'JPY',
    '유럽연합': 'EUR',
    '중국': 'CNY',
    '영국': 'GBP',
    '호주': 'AUD',
    '캐나다': 'CAD',
    '스위스': 'CHF',
    '홍콩': 'HKD',
    # 필요시 추가
}

# 환율 정보 크롤링 함수 (frankfurter.app API 사용)
def get_exchange_rate(src_code, target_code):
    if src_code == target_code:
        return 1.0
    url = f'https://api.frankfurter.app/latest?from={src_code}&to={target_code}'
    print(f'환율 정보 요청: {url}')
    resp = requests.get(url)
    data = resp.json()
    rates = data.get('rates', {})
    rate = rates.get(target_code)
    if rate is None:
        print('API 응답:', data)
        raise Exception('환율 정보를 찾을 수 없습니다.')
    return rate

# 네이버 금융에서 현찰 살 때/팔 때 환율을 크롤링하는 함수
# return: {'현찰살때': float, '현찰팔때': float}
def get_cash_rates(target_code):
    url = 'https://finance.naver.com/marketindex/exchangeList.naver'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    rows = soup.select('table.tbl_exchange > tbody > tr')
    for row in rows:
        tds = row.find_all('td')
        if not tds or len(tds) < 5:
            continue
        code = tds[0].text.strip()
        # 코드가 USD(미국), JPY(일본), EUR(유럽연합) 등과 일치하는지 확인
        if target_code in code:
            cash_buy = tds[2].text.replace(',', '').strip()
            cash_sell = tds[3].text.replace(',', '').strip()
            try:
                return {
                    '현찰살때': float(cash_buy) if cash_buy != '-' else None,
                    '현찰팔때': float(cash_sell) if cash_sell != '-' else None
                }
            except:
                continue
    raise Exception(f'{target_code}에 대한 현찰 환율 정보를 찾을 수 없습니다.')

# 환전 함수
def exchange_money(amount, src_country, target_country):
    src_code = country_currency.get(src_country)
    target_code = country_currency.get(target_country)
    if not src_code or not target_code:
        raise Exception('지원하지 않는 국가입니다.')
    if src_code == target_code:
        return amount, 0  # 같은 통화면 그대로 반환
    # 원화를 외화로 환전: 현찰 살 때 환율 적용
    if src_code == 'KRW':
        rates = get_cash_rates(target_code)
        rate = rates['현찰살때']
        if not rate:
            raise Exception('현찰 살 때 환율 정보를 찾을 수 없습니다.')
        exchanged_float = amount / rate  # 소수점까지 환전 금액
        exchanged = int(exchanged_float)  # 지폐 단위(버림)
        remain = int(round(amount - (exchanged * rate)))  # 남은 돈(정확하게)
        return exchanged, remain
    # 외화를 원화로 환전: 현찰 팔 때 환율 적용
    elif target_code == 'KRW':
        rates = get_cash_rates(src_code)
        rate = rates['현찰팔때']
        if not rate:
            raise Exception('현찰 팔 때 환율 정보를 찾을 수 없습니다.')
        exchanged_float = amount * rate  # 소수점까지 환전 금액
        exchanged = int(exchanged_float)  # 지폐 단위(버림)
        remain = 0
        return exchanged, remain
    else:
        # src -> KRW -> target
        rates1 = get_cash_rates(src_code)
        rate1 = rates1['현찰팔때']
        rates2 = get_cash_rates(target_code)
        rate2 = rates2['현찰살때']
        if not rate1 or not rate2:
            raise Exception('중간 환율 정보를 찾을 수 없습니다.')
        krw = amount * rate1
        exchanged_float = krw / rate2
        exchanged = int(exchanged_float)
        remain = int(round(krw - (exchanged * rate2)))
        return exchanged, remain

# 사용 예시
if __name__ == '__main__':
    src = '한국'
    target = '미국'
    amount = 1000000  # 100만원
    exchanged, remain = exchange_money(amount, src, target)
    print(f'{src} {amount}원을 {target} 화폐로 환전하면 {exchanged} {country_currency[target]} 지폐, 남은 돈은 {remain} {country_currency[src]} 입니다.')
