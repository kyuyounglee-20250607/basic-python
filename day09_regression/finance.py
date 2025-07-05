import yfinance as yf
import pandas as pd

# 삼성전자 ticker
ticker = "005930.KS"

# 최근 60 거래일 데이터 조회
df = yf.Ticker(ticker).history(period="60d")

# date와 종가만 추출
df = df.reset_index()[["Date", "Close"]]
df.columns = ["date", "sales"]

# 날짜 포맷 변경
df["date"] = df["date"].dt.strftime("%Y-%m-%d")

# CSV로 저장
df.to_csv("samsung_recent_2months.csv", index=False)
print(df.head())
