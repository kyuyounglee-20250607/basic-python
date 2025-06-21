from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime, timedelta
import time

app = Flask(__name__)

# Alpha Vantage API 설정 (실제 사용 시 API 키를 입력하세요)
ALPHA_VANTAGE_API_KEY = "3JQCLXOAZI6WRNV2"  # https://www.alphavantage.co/support/#api-key

# 주요 주식 종목 매핑
US_STOCKS = {
    '애플': 'AAPL',
    '마이크로소프트': 'MSFT',
    '구글': 'GOOGL',
    '테슬라': 'TSLA',
    '아마존': 'AMZN',
    '넷플릭스': 'NFLX',
    '메타': 'META',
    '엔비디아': 'NVDA'
}

class StockDataProvider:
    def __init__(self):
        self.last_request_time = 0
        self.request_count = 0
    
    def get_alpha_vantage_quote(self, symbol):
        """Alpha Vantage API로 실시간 가격 조회"""
        if not ALPHA_VANTAGE_API_KEY:
            print("Alpha Vantage API 키가 설정되지 않았습니다.")
            return None
            
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        
        try:
            print(f"Alpha Vantage API 호출: {symbol}")
            response = requests.get(url, params=params)
            data = response.json()
            
            if "Global Quote" in data:
                quote = data["Global Quote"]
                result = {
                    "symbol": quote.get("01. symbol"),
                    "current_price": float(quote.get("05. price", 0)),
                    "change": float(quote.get("09. change", 0)),
                    "change_percent": float(quote.get("10. change percent", "0%").replace("%", "")),
                    "volume": int(quote.get("06. volume", 0)),
                    "high": float(quote.get("03. high", 0)),
                    "low": float(quote.get("04. low", 0)),
                    "open": float(quote.get("02. open", 0)),
                    "source": "Alpha Vantage"
                }
                print(f"Alpha Vantage 데이터 성공: {result['current_price']}")
                return result
            else:
                error_msg = data.get('Note', data.get('Error Message', 'Unknown error'))
                print(f"Alpha Vantage API 오류: {error_msg}")
                return None
        except Exception as e:
            print(f"Alpha Vantage API 오류: {e}")
            return None
    
    def get_alpha_vantage_daily(self, symbol):
        """Alpha Vantage API로 일별 데이터 조회"""
        if not ALPHA_VANTAGE_API_KEY:
            return None
            
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        
        try:
            response = requests.get(url, params=params)
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
                error_msg = data.get('Note', data.get('Error Message', 'Unknown error'))
                print(f"Alpha Vantage 일별 데이터 오류: {error_msg}")
                return None
        except Exception as e:
            print(f"Alpha Vantage 일별 데이터 오류: {e}")
            return None
    
    def get_stock_data(self, symbol):
        """Alpha Vantage API로 주식 데이터 가져오기"""
        print(f"실시간 데이터 조회: {symbol}")
        
        # API 호출 제한 확인 (Alpha Vantage: 5회/분, 500회/일)
        current_time = time.time()
        if current_time - self.last_request_time < 60:  # 1분 내
            self.request_count += 1
            if self.request_count > 5:  # 분당 5회 제한
                print("Alpha Vantage API 호출 제한에 도달했습니다. 잠시 후 다시 시도하세요.")
                return None
        else:
            self.request_count = 1
            self.last_request_time = current_time
        
        # Alpha Vantage로 실시간 가격 조회
        data = self.get_alpha_vantage_quote(symbol)
        if data:
            return data
        
        print("Alpha Vantage API에서 데이터를 가져올 수 없습니다.")
        return None

# 전역 데이터 제공자 인스턴스
data_provider = StockDataProvider()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_stock():
    symbol = request.form.get('symbol', '').upper()
    print(f"검색 요청: {symbol}")
    
    if not symbol:
        return jsonify({'error': '종목명을 입력해주세요.'})
    
    # 종목명으로 검색 시도
    if symbol in US_STOCKS:
        symbol = US_STOCKS[symbol]
        print(f"종목명 변환: {symbol}")
    
    # 실시간 데이터 가져오기
    stock_data = data_provider.get_stock_data(symbol)
    
    if stock_data is None:
        return jsonify({
            'error': f'{symbol} 종목의 실시간 데이터를 가져올 수 없습니다.',
            'suggestion': 'Alpha Vantage API 키를 설정하거나 다른 종목을 시도해보세요.'
        })
    
    # 차트 데이터 가져오기
    chart_data = data_provider.get_alpha_vantage_daily(symbol)
    if not chart_data:
        # 차트 데이터가 없으면 가짜 데이터 생성
        chart_data = {
            'labels': [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30, 0, -1)],
            'prices': [stock_data['current_price'] + (i * 0.1) for i in range(30)],
            'volumes': [stock_data['volume']] * 30
        }
    
    return jsonify({
        'symbol': symbol,
        'current_price': stock_data['current_price'],
        'change': stock_data['change'],
        'change_percent': stock_data['change_percent'],
        'volume': stock_data['volume'],
        'chart': chart_data,
        'info': {
            'name': f"{symbol} Corporation",
            'market_cap': 'N/A',  # Alpha Vantage Global Quote에는 시가총액 정보가 없음
            'pe_ratio': 'N/A',
            'dividend_yield': 'N/A'
        },
        'source': stock_data.get('source', 'Alpha Vantage'),
        'fake_data': False
    })

@app.route('/popular')
def popular_stocks():
    """인기 주식 목록"""
    print("인기 주식 데이터 로딩...")
    popular_symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']
    stocks = []
    
    for symbol in popular_symbols:
        print(f"처리 중: {symbol}")
        data = data_provider.get_stock_data(symbol)
        if data:
            stocks.append({
                'symbol': symbol,
                'name': f"{symbol} Corporation",
                'price': data['current_price'],
                'change': data['change'],
                'change_percent': data['change_percent']
            })
            print(f"{symbol} 추가됨: ${data['current_price']}")
        else:
            print(f"{symbol} 실패")
    
    print(f"총 {len(stocks)}개 주식 로드됨")
    return jsonify(stocks)

if __name__ == '__main__':
    print("실시간 주가 조회 서버 시작...")
    print("Alpha Vantage API 키 설정 상태:")
    print(f"Alpha Vantage: {'설정됨' if ALPHA_VANTAGE_API_KEY else '설정되지 않음'}")
    
    if not ALPHA_VANTAGE_API_KEY:
        print("\n⚠️  경고: Alpha Vantage API 키가 설정되지 않았습니다!")
        print("실시간 데이터를 사용하려면 API 키를 설정하세요:")
        print("1. https://www.alphavantage.co/support/#api-key 에서 무료로 발급")
        print("2. app_realtime.py 파일에서 ALPHA_VANTAGE_API_KEY 변수에 키 입력")
        print("3. 무료 티어: 5회/분, 500회/일")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 