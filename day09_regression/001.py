

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import OneHotEncoder
import matplotlib.font_manager as fm

# Windows용 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # 또는 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False     # 마이너스 기호 깨짐 방지


file_path = 'https://raw.githubusercontent.com/kyuyounglee-20250607/basic-python/refs/heads/main/day09_regression/clean_sales_data.csv'
# 1. 데이터 로드
def load_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = ['date','sales']
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    return df

# 2. 특성 엔지니어링
def create_features(df):
    df["dayofweek"] = df["date"].dt.dayofweek  # 요일 (0=월 ~ 6=일)
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    return df

# 3. 데이터 준비
def prepare_data(df):
    features = ["dayofweek", "month", "day"]
    target = "sales"

    X = df[features]
    y = df[target]

    return train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 모델 학습
def train_model(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

# 5. 미래 예측용 데이터 생성
def create_future_dates(start_date, days=7):
    future_dates = pd.date_range(start=start_date, periods=days, freq="D")
    future_df = pd.DataFrame({"date": future_dates})
    return create_features(future_df)

# 6. 전체 파이프라인
def main():
    # CSV 파일 예시: columns=['date', 'sales']
    # file_path = "sales_data.csv"  # 사용자 파일
    df = load_data(file_path)
    df = create_features(df)

    # 학습 데이터 준비
    X_train, X_test, y_train, y_test = prepare_data(df)

    # 모델 학습
    model = train_model(X_train, y_train)

    # 정확도 확인
    preds = model.predict(X_test)
    error = mean_absolute_error(y_test, preds)
    print(f"[테스트 MAE] 평균 오차: {error:.2f}")

    # 미래 예측
    last_date = df["date"].max()
    future_df = create_future_dates(last_date + pd.Timedelta(days=1), days=365)
    future_preds = model.predict(future_df[["dayofweek", "month", "day"]])

    # 결과 출력
    future_df["predicted_sales"] = future_preds.astype(int)
    print("\n📈 향후 365일간 예측 판매량:")
    print(future_df[["date", "predicted_sales"]])

    # 그래프 출력 (옵션)
    plt.figure(figsize=(10, 5))
    plt.plot(df["date"], df["sales"], label="과거 판매량")
    plt.plot(future_df["date"], future_df["predicted_sales"], label="예측 판매량", linestyle='--', marker='o')
    plt.legend()
    plt.title("판매량 예측")
    plt.xlabel("날짜")
    plt.ylabel("판매량")
    plt.grid(True)
    plt.tight_layout()

    # 저장
    plt.savefig("forecast.png", dpi=150)
    plt.close()  # 그래프 메모리 닫기
    print("✅ 그래프가 forecast.png 로 저장되었습니다.")

if __name__ == "__main__":
    main()
