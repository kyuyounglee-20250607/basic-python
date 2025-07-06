import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import yfinance as yf
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

@st.cache_data
def get_krx_stock_list():
    url = "https://kind.krx.co.kr/corpgeneral/corpList.do?method=download"
    resp = requests.get(url)
    resp.encoding = 'euc-kr'
    df = pd.read_html(resp.text, header=0)[0]
    df["종목코드"] = df["종목코드"].astype(str).str.zfill(6)
    df["ticker"] = df["종목코드"] + ".KS"
    return df[["회사명", "ticker"]]

@st.cache_data
def load_stock_data(ticker: str, period="60d"):
    df = yf.Ticker(ticker).history(period=period)
    df = df.reset_index()[["Date", "Close"]]
    df.columns = ["date", "sales"]
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date")

def create_features(df):
    df["dayofweek"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    return df

def prepare_data(df):
    features = ["dayofweek", "month", "day"]
    X = df[features]
    y = df["sales"]
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def create_future_dates(start_date, days=30):
    future_dates = pd.date_range(start=start_date, periods=days, freq='D')
    future_df = pd.DataFrame({"date": future_dates})
    return create_features(future_df)

def main():
    st.title("📈 KRX 주가 예측 대시보드")
    st.markdown("한국거래소 상장 종목을 검색하고 선택해 향후 주가를 예측합니다.")

    try:
        stock_list = get_krx_stock_list()
    except Exception as e:
        st.error(f"상장 종목 리스트 로드 오류: {e}")
        return

    # 검색어 입력
    search_term = st.text_input("종목명 검색 (예: 삼성)")

    # 필터링: 검색어가 포함된 종목명만 표시, 없으면 전체 표시
    if search_term:
        filtered_df = stock_list[stock_list["회사명"].str.contains(search_term, case=False, na=False)]
    else:
        filtered_df = stock_list

    if filtered_df.empty:
        st.warning("검색 결과가 없습니다. 다른 검색어를 입력하세요.")
        return

    selected_name = st.selectbox("종목 선택", filtered_df["회사명"])
    selected_ticker = filtered_df[filtered_df["회사명"] == selected_name]["ticker"].values[0]
    st.info(f"선택된 종목: {selected_name} ({selected_ticker})")

    period_days = st.slider("학습용 과거 기간 (일)", 30, 120, step=30, value=60)

    try:
        df = load_stock_data(selected_ticker, period=f"{period_days}d")
        if df.empty:
            st.error("주가 데이터를 불러올 수 없습니다. 다른 종목을 선택해 주세요.")
            return
    except Exception as e:
        st.error(f"주가 데이터 로드 오류: {e}")
        return

    df_feat = create_features(df)
    X_train, X_test, y_train, y_test = prepare_data(df_feat)
    model = train_model(X_train, y_train)

    mae = mean_absolute_error(y_test, model.predict(X_test))
    st.success(f"테스트 평균 오차 (MAE): {mae:.2f}")

    forecast_days = st.slider("예측 기간 (일)", 7, 90, step=7, value=30)
    last_date = df["date"].max()
    future_df = create_future_dates(last_date + pd.Timedelta(days=1), days=forecast_days)
    future_df["predicted_sales"] = model.predict(future_df[["dayofweek", "month", "day"]]).astype(int)

    st.subheader(f"📅 향후 {forecast_days}일간 예측 주가")
    st.dataframe(future_df[["date", "predicted_sales"]].reset_index(drop=True))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["date"], df["sales"], label="과거 종가")
    ax.plot(future_df["date"], future_df["predicted_sales"], linestyle="--", marker="o", label="예측 종가")
    ax.legend()
    ax.set_title(f"{selected_name} 주가 예측")
    ax.set_xlabel("날짜")
    ax.set_ylabel("종가")
    ax.grid(True)
    st.pyplot(fig)

if __name__ == "__main__":
    main()
