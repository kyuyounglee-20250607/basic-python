# 📊 AI 기반 판매량 예측 프로그램

이 프로젝트는 머신러닝을 활용하여 **과거 판매 데이터를 기반으로 미래 7일간의 판매량을 예측**하는 프로그램입니다.  
무료 라이브러리만을 사용하며, 실무에 사용할 수 있을 정도의 성능을 목표로 구성되어 있습니다.

---

## ✅ 주요 기능

- CSV 파일로부터 날짜별 판매량 데이터 로드
- 날짜 정보를 기반으로 한 **특성 생성 (요일, 월, 일)**
- **Random Forest** 회귀 모델을 이용한 학습
- 미래 7일간의 판매량 예측
- 실제 vs 예측 결과를 시각적으로 비교 (Matplotlib 그래프)

---

## 🛠 사용된 라이브러리

| 라이브러리 | 설명 |
|------------|------|
| pandas     | 데이터 처리 및 날짜 변환 |
| numpy      | 수치 계산 지원 |
| scikit-learn | 머신러닝 모델 학습 (RandomForestRegressor) |
| matplotlib | 판매량 시각화 |
| joblib _(옵션)_ | 모델 저장/불러오기 가능 |

> ⚠️ 모두 **무료 오픈소스** 라이브러리입니다.
| numpy      | 수치 계산 지원 |
pip install scikit-learn pandas matplotlib joblib streamlit
---

## 📁 입력 데이터 형식 (`sales_data.csv`)

```csv
date,sales
2025-06-01,120
2025-06-02,150
2025-06-03,170
...

streamlit run 002.py
