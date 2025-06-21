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

# 환율 정보 크롤링 함수 (네이버 환율)
def get_exchange_rate(src_code, target_code):
    url = f'https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_{src_code}{target_code}'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    rate_tag = soup.select_one('span.value')
    if not rate_tag:
        raise Exception('환율 정보를 찾을 수 없습니다.')
    rate = float(rate_tag.text.replace(',', ''))
    return rate

# 환전 함수
def exchange_money(amount, src_country, target_country):
    src_code = country_currency.get(src_country)
    target_code = country_currency.get(target_country)
    if not src_code or not target_code:
        raise Exception('지원하지 않는 국가입니다.')
    if src_code == target_code:
        return amount, 0  # 같은 통화면 그대로 반환
    # 환율 방향에 따라 계산
    if src_code == 'KRW':
        rate = get_exchange_rate(src_code, target_code)
        exchanged = int(amount // rate)
        remain = int(amount - exchanged * rate)
        return exchanged, remain
    elif target_code == 'KRW':
        rate = get_exchange_rate(target_code, src_code)
        exchanged = int(amount * rate)
        remain = 0
        return exchanged, remain
    else:
        # src -> KRW -> target
        rate1 = get_exchange_rate(src_code, 'KRW')
        rate2 = get_exchange_rate('KRW', target_code)
        krw = amount * rate1
        exchanged = int(krw // rate2)
        remain = int(krw - exchanged * rate2)
        return exchanged, remain

# 사용 예시
if __name__ == '__main__':
    src = '한국'
    target = '미국'
    amount = 1000000  # 100만원
    exchanged, remain = exchange_money(amount, src, target)
    print(f'{src} {amount}원을 {target} 화폐로 환전하면 {exchanged} {country_currency[target]} 지폐, 남은 돈은 {remain} {country_currency[src]} 입니다.')
