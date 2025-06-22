# 🌤️ 간단한 날씨 예보 프로그램

OpenWeatherMap API를 사용하여 현재 날씨와 5일 예보를 조회하는 간단한 Python 프로그램입니다.

## ✨ 주요 기능

- **현재 날씨 조회**: 온도, 체감온도, 습도, 바람, 일출/일몰 시간
- **5일 예보**: 향후 5일간의 날씨 예보 정보
- **한국어 지원**: 한국어로 날씨 정보 표시
- **간단한 사용법**: 함수 호출만으로 쉽게 사용

## 🚀 설치 및 실행

### 1. 필요한 패키지 설치
```bash
pip install requests
```

### 2. API 키 설정
OpenWeatherMap에서 무료 API 키를 발급받아 `weather_forecast.py` 파일의 `API_KEY` 변수에 입력하세요.

### 3. 프로그램 실행
```bash
python weather_forecast.py
```

## 📖 사용법

### 기본 사용법
```python
from weather_forecast import get_weather, get_forecast, format_current_weather, format_forecast

# 현재 날씨 조회
weather_data = get_weather("Seoul")
if weather_data:
    print(format_current_weather(weather_data))

# 5일 예보 조회
forecast_data = get_forecast("Seoul", days=5)
if forecast_data:
    print(format_forecast(forecast_data, 5))
```

### 다른 도시 조회
```python
# 부산 날씨 조회
busan_weather = get_weather("Busan")

# 뉴욕 날씨 조회 (미국)
ny_weather = get_weather("New York", "US")
```

## 📊 출력 예시

```
==================================================
🌤️  날씨 정보 조회
==================================================

📍 현재 날씨
📍 Seoul, KR
🌤️  맑음
🌡️  온도: 25.8°C
🌡️  체감온도: 26.0°C
💧 습도: 61%
🌪️  바람: 2.6m/s
🌅 일출: 05:11
🌇 일몰: 19:56

==================================================
📅 5일 예보
==================================================
📅 Seoul 5일 예보

📅 1일 후 (06/22)
🌤️  맑음
🌡️  온도: 25.9°C
💧 습도: 56%

📅 2일 후 (06/23)
🌤️  맑음
🌡️  온도: 25.5°C
💧 습도: 55%
```

## 🔧 주요 함수

### `get_weather(city, country_code="KR")`
현재 날씨 정보를 조회합니다.

**매개변수:**
- `city`: 도시명 (예: "Seoul", "Busan")
- `country_code`: 국가 코드 (기본값: "KR")

**반환값:**
- 날씨 정보 딕셔너리 또는 None (오류 시)

### `get_forecast(city, country_code="KR", days=5)`
날씨 예보 정보를 조회합니다.

**매개변수:**
- `city`: 도시명
- `country_code`: 국가 코드 (기본값: "KR")
- `days`: 예보 일수 (기본값: 5)

**반환값:**
- 예보 정보 딕셔너리 또는 None (오류 시)

### `format_current_weather(data)`
현재 날씨 정보를 보기 좋게 포맷팅합니다.

### `format_forecast(data, days=5)`
예보 정보를 보기 좋게 포맷팅합니다.

## ⚠️ 주의사항

1. **API 키 필요**: OpenWeatherMap에서 무료 API 키를 발급받아야 합니다.
2. **인터넷 연결**: 실시간 데이터 조회를 위해 인터넷 연결이 필요합니다.
3. **요청 제한**: 무료 API는 분당 60회 요청 제한이 있습니다.
4. **도시명 정확성**: 정확한 도시명을 입력해야 합니다.

## 🔗 관련 링크

- [OpenWeatherMap API](https://openweathermap.org/api)
- [API 키 발급](https://home.openweathermap.org/users/sign_up)

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 