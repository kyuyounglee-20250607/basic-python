import requests
import json
from datetime import datetime

class IEXCloudAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://cloud.iexapis.com/stable"
    
    def get_quote(self, symbol):
        """실시간 주식 가격 조회"""
        url = f"{self.base_url}/stock/{symbol}/quote"
        params = {"token": self.api_key}
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            return {
                "symbol": data.get("symbol"),
                "price": data.get("latestPrice", 0),
                "change": data.get("change", 0),
                "change_percent": data.get("changePercent", 0) * 100,
                "volume": data.get("latestVolume", 0),
                "high": data.get("high", 0),
                "low": data.get("low", 0),
                "open": data.get("open", 0),
                "market_cap": data.get("marketCap", 0),
                "pe_ratio": data.get("peRatio", 0)
            }
                
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def get_chart_data(self, symbol, range="1m"):
        """차트 데이터 조회"""
        url = f"{self.base_url}/stock/{symbol}/chart/{range}"
        params = {"token": self.api_key}
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            chart_data = {
                "labels": [item["date"] for item in data],
                "prices": [item["close"] for item in data],
                "volumes": [item["volume"] for item in data]
            }
            return chart_data
                
        except Exception as e:
            print(f"Error fetching chart data: {e}")
            return None

# 사용 예제
if __name__ == "__main__":
    # API 키를 여기에 입력하세요 (https://iexcloud.io/cloud-login#/register 에서 무료로 발급 가능)
    API_KEY = "YOUR_API_KEY_HERE"
    
    api = IEXCloudAPI(API_KEY)
    
    # 실시간 가격 조회
    quote = api.get_quote("AAPL")
    if quote:
        print(f"애플 실시간 가격: ${quote['price']}")
        print(f"변동: ${quote['change']} ({quote['change_percent']:.2f}%)")
    
    # 차트 데이터 조회
    chart_data = api.get_chart_data("AAPL")
    if chart_data:
        print(f"차트 데이터: {len(chart_data['prices'])}개 데이터포인트") 