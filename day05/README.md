# 📈 실시간 주가 조회 프로그램

한국 주식 시장의 실시간 주가 정보를 조회할 수 있는 웹 애플리케이션입니다.

## 🚀 주요 기능

- **실시간 주가 조회**: 종목 코드를 입력하여 실시간 주가 정보 확인
- **인기 주식 목록**: 주요 기업들의 주가 정보를 한눈에 확인
- **캔들스틱 차트**: 주가 변동을 시각적으로 확인
- **상세 정보**: 시가총액, PER, 배당수익률 등 종목 상세 정보 제공
- **반응형 디자인**: 모바일과 데스크톱에서 모두 사용 가능

## 📋 지원 종목

- 한국 주식 시장(KOSPI, KOSDAQ) 상장 기업
- 종목 코드로 검색 (예: 삼성전자 = 005930)

## 🛠️ 설치 및 실행

### 1. 필요한 패키지 설치

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

## 📱 사용법

1. **종목 검색**: 검색창에 종목 코드를 입력하고 "검색" 버튼 클릭
2. **인기 주식 확인**: 하단의 인기 주식 카드를 클릭하여 해당 종목 정보 확인
3. **차트 확인**: 주가 차트를 통해 가격 변동 추이 확인
4. **상세 정보**: 거래량, 시가총액, PER, 배당수익률 등 확인

## 🎯 주요 종목 코드 예시

- **005930**: 삼성전자
- **000660**: SK하이닉스
- **035420**: NAVER
- **051910**: LG화학
- **006400**: 삼성SDI

## 🔧 기술 스택

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript, jQuery
- **차트**: Plotly.js
- **데이터**: Yahoo Finance API (yfinance)
- **스타일링**: CSS3 (그라데이션, 애니메이션)

## 📊 데이터 제공

- **Yahoo Finance**: 실시간 주가 데이터
- **업데이트**: 실시간 (API 호출 시)

## ⚠️ 주의사항

- 이 프로그램은 교육 및 개인적인 용도로만 사용하세요
- 투자 결정은 충분한 분석과 전문가 상담 후 진행하세요
- 주식 투자는 원금 손실의 위험이 있습니다

## 🐛 문제 해결

### 패키지 설치 오류
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 포트 충돌
다른 포트를 사용하려면 `app.py` 파일에서 포트 번호를 변경하세요:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여

버그 리포트나 기능 제안은 언제든 환영합니다! 