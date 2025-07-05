import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# CSV 파일 경로
file_path = 'https://raw.githubusercontent.com/kyuyounglee-20250607/basic-python/refs/heads/main/day09_regression/clean_sales_data.csv'

# 데이터 불러오기
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = ['date', 'sales']
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values('date')

# 특성 생성
def create_features(df):
    df["dayofweek"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    return df

# 학습용 데이터셋
def prepare_data(df):
    features = ["dayofweek", "month", "day"]
    X = df[features]
    y = df["sales"]
    return train_test_split(X, y, test_size=0.2, random_state=42)

# 모델 학습
def train_model(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

# 미래 날짜 생성
def create_future_dates(start_date, days=30):
    future_dates = pd.date_range(start=start_date, periods=days, freq='D')
    future_df = pd.DataFrame({'date': future_dates})
    return create_features(future_df)

# Streamlit 앱 시작
def main():
    st.title("📈 판매량 예측 대시보드")
    st.markdown("AI 모델을 활용한 향후 판매량 예측")

    df = load_data(file_path)
    df = create_features(df)

    X_train, X_test, y_train, y_test = prepare_data(df)
    model = train_model(X_train, y_train)

    # 모델 평가
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    st.success(f"✅ 테스트 평균 오차 (MAE): {mae:.2f}")

    # 예측일 수 선택
    forecast_days = st.slider("예측 기간 (일)", min_value=7, max_value=365, step=7, value=90)

    # 미래 예측
    last_date = df["date"].max()
    future_df = create_future_dates(last_date + pd.Timedelta(days=1), days=forecast_days)
    future_df["predicted_sales"] = model.predict(future_df[["dayofweek", "month", "day"]]).astype(int)

    # 예측 결과 표
    st.subheader(f"📅 향후 {forecast_days}일간 예측 판매량")
    st.dataframe(future_df[["date", "predicted_sales"]].reset_index(drop=True))

    # 시각화
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["date"], df["sales"], label="과거 판매량")
    ax.plot(future_df["date"], future_df["predicted_sales"], label="예측 판매량", linestyle='--', marker='o')
    ax.set_title("판매량 예측")
    ax.set_xlabel("날짜")
    ax.set_ylabel("판매량")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

if __name__ == "__main__":
    main()
