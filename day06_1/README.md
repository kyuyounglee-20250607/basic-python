 # 암호화폐 시세 조회 웹 애플리케이션

Flask로 구현된 실시간 암호화폐 가격 조회 및 차트 생성 웹 애플리케이션입니다.

## 주요 기능

- 🪙 다양한 암호화폐 실시간 가격 조회
- 📊 일별/시간별 가격 변화 차트 생성
- 🌍 다국가 통화 지원 (KRW, USD, EUR, JPY)
- 📱 반응형 웹 디자인
- ⚡ RESTful API 제공

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 애플리케이션 실행
```bash
python app.py
```

### 3. 웹 브라우저에서 접속
```
http://localhost:5000
```

## API 엔드포인트

### 가격 데이터 조회
```
POST /api/price
Content-Type: application/json

{
    "crypto_id": "bitcoin",
    "currency": "krw",
    "days": "7",
    "interval": "daily"
}
```

### 현재 가격 조회
```
GET /api/current-price/{crypto_id}/{currency}
```

## 지원하는 암호화폐

- Bitcoin (BTC)
- Ethereum (ETH)
- Binance Coin (BNB)
- Cardano (ADA)
- Solana (SOL)
- Ripple (XRP)
- Dogecoin (DOGE)
- Polkadot (DOT)

## 기술 스택

- **Backend**: Flask, Python
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **차트**: Matplotlib
- **API**: CoinGecko API
- **데이터 처리**: Requests, JSON

## 프로젝트 구조

```
day06_1/
├── app.py              # Flask 애플리케이션 메인 파일
├── templates/
│   └── index.html      # 웹 인터페이스 템플릿
├── requirements.txt    # Python 의존성 패키지
└── README.md          # 프로젝트 설명서
```

## 리팩토링 개선사항

### 기존 노트북 코드 대비 개선점:

1. **코드 구조화**
   - 클래스 기반 설계로 코드 재사용성 향상
   - `CryptoPriceService` 클래스로 API 로직 분리
   - `ChartGenerator` 클래스로 차트 생성 로직 분리

2. **에러 처리 개선**
   - API 요청 실패 시 적절한 에러 메시지 제공
   - 타임아웃 설정으로 안정성 향상
   - 예외 처리 강화

3. **API 호출 최적화**
   - User-Agent 헤더 추가로 401 오류 해결
   - Session 객체 사용으로 연결 재사용
   - 요청 타임아웃 설정

4. **사용자 인터페이스**
   - 웹 기반 인터페이스로 접근성 향상
   - 반응형 디자인으로 모바일 지원
   - 실시간 데이터 조회 및 차트 표시

5. **한글 폰트 문제 해결**
   - matplotlib 폰트 설정 개선
   - 여러 폰트 옵션 제공

6. **기능 확장**
   - 현재 가격 조회 기능 추가
   - 다양한 암호화폐 및 통화 지원
   - RESTful API 제공

## 라이선스

MIT License