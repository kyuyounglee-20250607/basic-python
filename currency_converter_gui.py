import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup

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
}

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

def exchange_money(amount, src_country, target_country):
    src_code = country_currency.get(src_country)
    target_code = country_currency.get(target_country)
    if not src_code or not target_code:
        raise Exception('지원하지 않는 국가입니다.')
    if src_code == target_code:
        return amount, 0
    if src_code == 'KRW':
        rates = get_cash_rates(target_code)
        rate = rates['현찰살때']
        if not rate:
            raise Exception('현찰 살 때 환율 정보를 찾을 수 없습니다.')
        exchanged_float = amount / rate
        exchanged = int(exchanged_float)
        remain = int(round(amount - (exchanged * rate)))
        return exchanged, remain
    elif target_code == 'KRW':
        rates = get_cash_rates(src_code)
        rate = rates['현찰팔때']
        if not rate:
            raise Exception('현찰 팔 때 환율 정보를 찾을 수 없습니다.')
        exchanged_float = amount * rate
        exchanged = int(exchanged_float)
        remain = 0
        return exchanged, remain
    else:
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

def run_converter():
    try:
        src = src_var.get()
        target = target_var.get()
        amount = int(amount_var.get())
        exchanged, remain = exchange_money(amount, src, target)
        result = f'{src} {amount}원을 {target} 화폐로 환전하면\n{exchanged} {country_currency[target]} 지폐, 남은 돈은 {remain} {country_currency[src]} 입니다.'
        result_var.set(result)
    except Exception as e:
        messagebox.showerror('오류', str(e))

root = tk.Tk()
root.title('환율 변환기')
root.geometry('420x250')

src_var = tk.StringVar(value='한국')
target_var = tk.StringVar(value='미국')
amount_var = tk.StringVar(value='1000000')
result_var = tk.StringVar()

# 입력 UI
ttk.Label(root, text='보유 국가:').grid(row=0, column=0, padx=10, pady=10, sticky='e')
ttk.Combobox(root, textvariable=src_var, values=list(country_currency.keys()), width=10).grid(row=0, column=1)
ttk.Label(root, text='환전 국가:').grid(row=1, column=0, padx=10, pady=10, sticky='e')
ttk.Combobox(root, textvariable=target_var, values=list(country_currency.keys()), width=10).grid(row=1, column=1)
ttk.Label(root, text='금액:').grid(row=2, column=0, padx=10, pady=10, sticky='e')
tk.Entry(root, textvariable=amount_var, width=15).grid(row=2, column=1)

# 변환 버튼
ttk.Button(root, text='환전하기', command=run_converter).grid(row=3, column=0, columnspan=2, pady=15)

# 결과 출력
ttk.Label(root, textvariable=result_var, wraplength=400, foreground='blue').grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
