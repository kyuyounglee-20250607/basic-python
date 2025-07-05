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

# ✅ 사용자 업로드 파일 로드 함수
@st.cache_data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df.columns = ['date', 'sales']
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values('date')

# ✅ 날짜 기반 특성 생성
def create_features(df):
    df["dayofweek"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    return df

# ✅ 학습용 데이터 분리
def prepare_data(df):
    features = ["dayofweek", "month", "day"]
    X = df[features]
    y = df["sales"]
    return train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ 모델 학습
def train_model(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

# ✅ 미래 날짜 생성
def create_future_dates(start_date, days=30):
    future_dates = pd.date_range(start=start_date, periods=days, freq='D')
    future_df = pd.DataFrame({'date': future_dates})
    return create_features(future_df)

# ✅ Streamlit 앱 시작
def main():
    st.title("📈 판매량 예측 대시보드")
    st.markdown("CSV 파일을 업로드하면 AI 모델이 향후 판매량을 예측합니다.")

    # 🔽 CSV 업로드 받기
    uploaded_file = st.file_uploader("📂 CSV 파일을 업로드하세요", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = load_data(uploaded_file)
            df = create_features(df)

            X_train, X_test, y_train, y_test = prepare_data(df)
            model = train_model(X_train, y_train)

            # MAE 평가
            preds = model.predict(X_test)
            mae = mean_absolute_error(y_test, preds)
            st.success(f"✅ 테스트 평균 오차 (MAE): {mae:.2f}")

            # 예측일 설정 슬라이더
            forecast_days = st.slider("예측 기간 (일)", min_value=7, max_value=365, step=7, value=90)

            # 예측 수행
            last_date = df["date"].max()
            future_df = create_future_dates(last_date + pd.Timedelta(days=1), days=forecast_days)
            future_df["predicted_sales"] = model.predict(future_df[["dayofweek", "month", "day"]]).astype(int)

            # 예측 결과 출력
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

        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")

    else:
        st.info("👈 왼쪽 사이드바 또는 위에서 CSV 파일을 업로드하세요.")
        st.markdown("""
        #### 샘플 CSV 형식
        ```
        date,sales  
        2024-01-01,120  
        2024-01-02,130  
        ...
        ```
        """)

if __name__ == "__main__":
    main()
