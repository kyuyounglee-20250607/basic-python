# 🚗 자동차 판매량 데이터 수집 프로그램

네이버 자동차 판매량 정보를 수집하여 데이터베이스에 저장하고 분석하는 프로그램입니다.

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

**설치되는 라이브러리:**
- requests==2.32.3 (웹 요청)
- beautifulsoup4==4.13.4 (HTML 파싱)
- pandas==2.3.0 (데이터 처리)
- matplotlib==3.10.3 (차트 생성)
- seaborn==0.13.2 (고급 차트)
- numpy==2.3.1 (수치 계산)

### 3. 데이터베이스 초기화 (최초 1회)

```bash
python database_setup.py
```

- ✅ SQLite 데이터베이스 생성
- ✅ 테이블 생성 (car_sales, brand_stats, monthly_stats)
- ✅ 샘플 데이터 입력 (2024년 5월 데이터)
- ✅ 데이터베이스 구조 확인

### 4. 데이터 수집 프로그램 실행

```bash
python car_sales_crawler.py
```

**메뉴 옵션:**
- 1️⃣ 특정 월 데이터 수집
- 2️⃣ 저장된 데이터 조회
- 3️⃣ CSV 파일로 내보내기
- 4️⃣ 데이터베이스 통계 확인
- 5️⃣ 프로그램 종료

### 5. 데이터 분석 도구 실행

```bash
python data_analyzer.py
```

**분석 기능:**
- 📊 기본 통계 정보
- 🚙 차종 카테고리별 분석
- 🏭 브랜드별 상세 분석
- 📈 트렌드 분석
- 📊 판매량 차트 생성
- 🍰 브랜드별 파이 차트
- 📄 분석 보고서 내보내기

### 6. 간단 버전 실행 (학습용)

```bash
python simple_car_crawler.py
```

- 파이썬/DB 기초 학습에 적합한 아주 쉬운 버전입니다.

---

## 📁 파일 구조

```
car_sales_data/
├── car_sales_crawler.py      # 메인 크롤링 프로그램
├── database_setup.py         # 데이터베이스 설정
├── data_analyzer.py          # 데이터 분석 도구
├── simple_car_crawler.py     # 기초 학습용 간단 버전
├── car_sales.db             # SQLite 데이터베이스 파일
├── requirements.txt          # 필요한 라이브러리 목록
└── readme.md                # 이 파일
```

## 📊 데이터베이스 구조

### car_sales 테이블 (개별 차량 판매량)
- id: 고유 번호
- car_name: 차량명
- sales_count: 판매 대수
- year: 연도
- month: 월
- rank_position: 순위
- category: 차종 카테고리
- brand: 브랜드
- collected_at: 수집 시간

### brand_stats 테이블 (브랜드별 통계)
- brand: 브랜드명
- year: 연도
- month: 월
- total_sales: 총 판매량
- car_count: 등록 차량 수
- collected_at: 수집 시간

### monthly_stats 테이블 (월별 전체 통계)
- year: 연도
- month: 월
- total_sales: 총 판매량
- car_count: 등록 차량 수
- top_brand: 1위 브랜드
- top_car: 1위 차량
- collected_at: 수집 시간

## 🎯 주요 기능

### 데이터 수집
- 네이버 자동차 판매량 정보 수집
- 자동 데이터베이스 저장
- 중복 데이터 방지

### 데이터 분석
- 실시간 통계 계산
- 브랜드별/카테고리별 분석
- 시각적 차트 생성
- CSV 보고서 내보내기

### 사용자 친화적 인터페이스
- 메뉴 기반 쉬운 조작
- 한글 지원
- 상세한 안내 메시지

## ⚠️ 주의사항

- 웹 크롤링 시 해당 웹사이트의 이용약관을 준수하세요
- 과도한 요청은 피해주세요
- 수집된 데이터는 개인 학습 목적으로만 사용하세요
- matplotlib 한글 폰트 설정이 필요할 수 있습니다

## 🔧 문제 해결

### 라이브러리 설치 오류
```bash
# conda 사용 시
conda install matplotlib seaborn pandas requests beautifulsoup4

# pip 사용 시
pip install --upgrade pip
pip install -r requirements.txt
```

### 한글 폰트 문제
- Windows: 기본적으로 'Malgun Gothic' 사용
- 다른 OS: matplotlib 폰트 설정 필요

---

## 📞 지원

문제가 발생하면 다음을 확인해주세요:
1. Python 버전 (3.8 이상 권장)
2. 라이브러리 설치 상태
3. 데이터베이스 파일 존재 여부
4. 인터넷 연결 상태