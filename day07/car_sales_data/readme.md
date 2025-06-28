# 🚗 자동차 판매량 데이터 수집 프로그램

네이버 자동차 판매량 정보를 수집하여 데이터베이스에 저장하는 프로그램입니다.

---

## 🏁 실행 방법 (Step by Step)

### 1. 폴더 이동

```bash
cd car_sales_data
```

### 2. 필수 라이브러리 설치

아래 명령어를 터미널(명령 프롬프트)에서 실행하세요.

```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 초기화 (최초 1회)

```bash
python database_setup.py
```

- 데이터베이스와 테이블이 생성되고, 샘플 데이터가 입력됩니다.

### 4. 데이터 수집 프로그램 실행

```bash
python car_sales_crawler.py
```

- 메뉴가 나오면 원하는 기능을 숫자로 선택하세요.
- 예시: 1번(특정 월 데이터 수집) → 연도/월 입력 → 데이터 저장 및 조회

### 5. 데이터 분석 도구 실행 (선택)

```bash
python data_analyzer.py
```

- 다양한 통계, 차트, 보고서 생성 기능을 사용할 수 있습니다.

### 6. 간단 버전 실행 (학습용)

```bash
python simple_car_crawler.py
```

- 파이썬/DB 기초 학습에 적합한 아주 쉬운 버전입니다.

---

## 📁 파일 구조
- `car_sales_crawler.py`: 메인 크롤링 프로그램
- `database_setup.py`: 데이터베이스 설정
- `data_analyzer.py`: 데이터 분석 도구
- `simple_car_crawler.py`: 기초 학습용 간단 버전
- `car_sales.db`: SQLite 데이터베이스 파일
- `requirements.txt`: 필요한 라이브러리 목록

## 📊 수집 데이터
- 차량명
- 판매 대수
- 해당 월
- 수집 시간

## ⚠️ 주의사항
- 웹 크롤링 시 해당 웹사이트의 이용약관을 준수하세요
- 과도한 요청은 피해주세요
- 수집된 데이터는 개인 학습 목적으로만 사용하세요