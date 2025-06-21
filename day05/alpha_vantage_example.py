import requests
import json
from datetime import datetime

class AlphaVantageAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
    
    def get_quote(self, symbol):
        """실시간 주식 가격 조회"""
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if "Global Quote" in data:
                quote = data["Global Quote"]
                return {
                    "symbol": quote.get("01. symbol"),
                    "price": float(quote.get("05. price", 0)),
                    "change": float(quote.get("09. change", 0)),
                    "change_percent": quote.get("10. change percent", "0%").replace("%", ""),
                    "volume": int(quote.get("06. volume", 0)),
                    "high": float(quote.get("03. high", 0)),
                    "low": float(quote.get("04. low", 0)),
                    "open": float(quote.get("02. open", 0))
                }
            else:
                print(f"Error: {data.get('Note', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def get_daily_data(self, symbol):
        """일별 주식 데이터 조회"""
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if "Time Series (Daily)" in data:
                time_series = data["Time Series (Daily)"]
                dates = list(time_series.keys())[:30]  # 최근 30일
                
                chart_data = {
                    "labels": dates,
                    "prices": [float(time_series[date]["4. close"]) for date in dates],
                    "volumes": [int(time_series[date]["5. volume"]) for date in dates]
                }
                return chart_data
            else:
                print(f"Error: {data.get('Note', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

# 사용 예제
if __name__ == "__main__":
    # API 키를 여기에 입력하세요 (https://www.alphavantage.co/support/#api-key 에서 무료로 발급 가능)
    API_KEY = "YOUR_API_KEY_HERE"
    
    api = AlphaVantageAPI(API_KEY)
    
    # 실시간 가격 조회
    quote = api.get_quote("AAPL")
    if quote:
        print(f"애플 실시간 가격: ${quote['price']}")
        print(f"변동: ${quote['change']} ({quote['change_percent']}%)")
    
    # 일별 데이터 조회
    daily_data = api.get_daily_data("AAPL")
    if daily_data:
        print(f"차트 데이터: {len(daily_data['prices'])}개 데이터포인트") 