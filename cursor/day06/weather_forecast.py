import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any

def get_weather(city: str, country_code: str = "KR") -> Optional[Dict[str, Any]]:
    """
    현재 날씨 정보를 조회합니다.
    
    Args:
        city: 도시명
        country_code: 국가 코드 (기본값: "KR")
        
    Returns:
        날씨 정보 딕셔너리 또는 None (오류 시)
    """
    # API 키 (실제 사용 시 config.json에서 로드하거나 환경변수 사용)
    API_KEY = "cb9a8cbc6c0ca6f050057f8b496292fb"
    
    try:
        # API 요청
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": f"{city},{country_code}",
            "appid": API_KEY,
            "lang": "kr",
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API 오류: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ 요청 시간 초과")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ 네트워크 오류: {e}")
        return None
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return None

def get_forecast(city: str, country_code: str = "KR", days: int = 5) -> Optional[Dict[str, Any]]:
    """
    날씨 예보 정보를 조회합니다.
    
    Args:
        city: 도시명
        country_code: 국가 코드 (기본값: "KR")
        days: 예보 일수 (기본값: 5)
        
    Returns:
        예보 정보 딕셔너리 또는 None (오류 시)
    """
    API_KEY = "cb9a8cbc6c0ca6f050057f8b496292fb"
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": f"{city},{country_code}",
            "appid": API_KEY,
            "lang": "kr",
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API 오류: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 예보 조회 오류: {e}")
        return None

def format_current_weather(data: Dict[str, Any]) -> str:
    """현재 날씨 정보를 포맷팅"""
    try:
        city = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        
        # 일출/일몰 시간
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
        sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
        
        return (
            f"📍 {city}, {country}\n"
            f"🌤️  {description}\n"
            f"🌡️  온도: {temp:.1f}°C\n"
            f"🌡️  체감온도: {feels_like:.1f}°C\n"
            f"💧 습도: {humidity}%\n"
            f"🌪️  바람: {wind_speed:.1f}m/s\n"
            f"🌅 일출: {sunrise}\n"
            f"🌇 일몰: {sunset}"
        )
    except KeyError as e:
        return f"❌ 데이터 파싱 오류: {e}"

def format_forecast(data: Dict[str, Any], days: int = 5) -> str:
    """예보 정보를 포맷팅"""
    try:
        city = data['city']['name']
        result = [f"📅 {city} {days}일 예보"]
        
        # 날짜별로 데이터 그룹화
        daily_data = {}
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%m/%d')
            if date not in daily_data:
                daily_data[date] = []
            daily_data[date].append(item)
        
        # 각 날짜별 평균 계산
        for i, (date, items) in enumerate(list(daily_data.items())[:days], 1):
            avg_temp = sum(item['main']['temp'] for item in items) / len(items)
            avg_humidity = sum(item['main']['humidity'] for item in items) / len(items)
            description = items[0]['weather'][0]['description']
            
            result.append(
                f"\n📅 {i}일 후 ({date})\n"
                f"🌤️  {description}\n"
                f"🌡️  온도: {avg_temp:.1f}°C\n"
                f"💧 습도: {avg_humidity:.0f}%"
            )
        
        return "\n".join(result)
        
    except KeyError as e:
        return f"❌ 예보 데이터 파싱 오류: {e}"

def main():
    """메인 함수"""
    print("=" * 50)
    print("🌤️  날씨 정보 조회")
    print("=" * 50)
    
    # 현재 날씨 조회
    print("\n📍 현재 날씨")
    current_weather = get_weather("Seoul")
    if current_weather:
        print(format_current_weather(current_weather))
    else:
        print("❌ 현재 날씨 정보를 가져올 수 없습니다.")
    
    # 날씨 예보 조회
    print("\n" + "=" * 50)
    print("📅 5일 예보")
    print("=" * 50)
    
    forecast = get_forecast("Seoul", days=5)
    if forecast:
        print(format_forecast(forecast, 5))
    else:
        print("❌ 날씨 예보를 가져올 수 없습니다.")

if __name__ == "__main__":
    main() 