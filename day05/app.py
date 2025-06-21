from flask import Flask, render_template, request, jsonify
import yfinance as yf
from datetime import datetime, timedelta
import json
import requests
import random

app = Flask(__name__)

# 주요 한국 주식 종목 매핑
KOREAN_STOCKS = {
    '삼성전자': '005930',
    'SK하이닉스': '000660',
    'NAVER': '035420',
    'LG화학': '051910',
    '삼성SDI': '006400',
    '현대차': '005380',
    '기아': '000270',
    'POSCO홀딩스': '005490',
    'KB금융': '105560',
    '신한지주': '055550'
}

# 미국 주식 종목 매핑 (테스트용)
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

def get_fake_stock_data(symbol):
    """가짜 주식 데이터 생성 (yfinance가 작동하지 않을 때 사용)"""
    print(f"Generating fake data for: {symbol}")
    
    # 기본 가격 설정
    base_prices = {
        'AAPL': 180.0,
        'MSFT': 400.0,
        'GOOGL': 150.0,
        'TSLA': 250.0,
        'AMZN': 180.0,
        'NFLX': 600.0,
        'META': 500.0,
        'NVDA': 1200.0
    }
    
    base_price = base_prices.get(symbol, 100.0)
    current_price = base_price + random.uniform(-10, 10)
    change = random.uniform(-5, 5)
    change_percent = (change / current_price) * 100
    
    # 가짜 히스토리 데이터 생성
    dates = []
    prices = []
    for i in range(30):
        date = datetime.now() - timedelta(days=29-i)
        dates.append(date.strftime('%Y-%m-%d'))
        price = current_price + random.uniform(-20, 20)
        prices.append(price)
    
    return {
        'history': None,  # 실제 히스토리는 없음
        'info': {
            'longName': f'{symbol} Corporation',
            'marketCap': random.randint(1000000000, 5000000000),
            'trailingPE': random.uniform(10, 30),
            'dividendYield': random.uniform(0, 3)
        },
        'current_price': current_price,
        'change': change,
        'change_percent': change_percent,
        'fake_data': True
    }

def get_stock_data(symbol, period='5d'):
    """주식 데이터를 가져오는 함수"""
    try:
        print(f"Fetching data for: {symbol}")
        
        # 미국 주식인지 확인
        if symbol in US_STOCKS.values() or any(us_symbol in symbol for us_symbol in US_STOCKS.values()):
            print(f"Detected US stock: {symbol}")
            stock = yf.Ticker(symbol)
        else:
            # 한국 주식 시도
            print(f"Trying Korean stock: {symbol}")
            if not symbol.endswith('.KS'):
                symbol_with_ks = symbol + '.KS'
            else:
                symbol_with_ks = symbol
            stock = yf.Ticker(symbol_with_ks)
        
        # 여러 기간으로 시도
        periods_to_try = ['5d', '1mo', '3mo', '1d']
        
        for period in periods_to_try:
            print(f"Trying period: {period}")
            try:
                hist = stock.history(period=period)
                if not hist.empty:
                    print(f"Success with period: {period}")
                    break
            except Exception as e:
                print(f"Failed with period {period}: {e}")
                continue
        else:
            print(f"No data found for {symbol} with any period, using fake data")
            return get_fake_stock_data(symbol)
        
        print(f"Successfully fetched data for {symbol}")
        info = stock.info
        
        return {
            'history': hist,
            'info': info,
            'current_price': hist['Close'].iloc[-1] if not hist.empty else None,
            'change': hist['Close'].iloc[-1] - hist['Open'].iloc[0] if len(hist) > 0 else 0,
            'change_percent': ((hist['Close'].iloc[-1] - hist['Open'].iloc[0]) / hist['Open'].iloc[0] * 100) if len(hist) > 0 else 0
        }
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}, using fake data")
        return get_fake_stock_data(symbol)

def create_simple_chart_data(hist_data, fake_data=None):
    """간단한 차트 데이터 생성"""
    if fake_data:
        # 가짜 데이터용 차트 생성
        return {
            'labels': fake_data['dates'],
            'prices': fake_data['prices'],
            'volumes': [1000000] * len(fake_data['dates'])  # 고정 거래량
        }
    
    if hist_data is None or hist_data.empty:
        return None
    
    # 최근 30일 데이터만 사용
    recent_data = hist_data.tail(30)
    
    chart_data = {
        'labels': [str(date.date()) for date in recent_data.index],
        'prices': recent_data['Close'].tolist(),
        'volumes': recent_data['Volume'].tolist()
    }
    
    return chart_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_stock():
    symbol = request.form.get('symbol', '').upper()
    print(f"Searching for stock: {symbol}")
    
    if not symbol:
        return jsonify({'error': '종목 코드를 입력해주세요.'})
    
    # 종목명으로 검색 시도 (한국 주식)
    if symbol in KOREAN_STOCKS:
        symbol = KOREAN_STOCKS[symbol]
        print(f"Found Korean stock name, using code: {symbol}")
    
    # 종목명으로 검색 시도 (미국 주식)
    if symbol in US_STOCKS:
        symbol = US_STOCKS[symbol]
        print(f"Found US stock name, using code: {symbol}")
    
    stock_data = get_stock_data(symbol)
    
    if stock_data is None:
        return jsonify({
            'error': f'{symbol} 종목을 찾을 수 없습니다. yfinance API에서 해당 주식 데이터를 가져올 수 없습니다.',
            'suggestion': '미국 주식으로 테스트해보세요: AAPL, MSFT, GOOGL, TSLA 등'
        })
    
    # 간단한 차트 데이터 생성
    if stock_data.get('fake_data'):
        # 가짜 데이터인 경우
        fake_data = {
            'dates': [f"{(datetime.now() - timedelta(days=29-i)).strftime('%Y-%m-%d')}" for i in range(30)],
            'prices': [stock_data['current_price'] + random.uniform(-20, 20) for _ in range(30)]
        }
        chart_data = create_simple_chart_data(None, fake_data)
    else:
        chart_data = create_simple_chart_data(stock_data['history'])
    
    return jsonify({
        'symbol': symbol,
        'current_price': stock_data['current_price'],
        'change': stock_data['change'],
        'change_percent': stock_data['change_percent'],
        'volume': stock_data['history']['Volume'].iloc[-1] if stock_data['history'] and not stock_data['history'].empty else 1000000,
        'chart': chart_data,
        'info': {
            'name': stock_data['info'].get('longName', 'N/A'),
            'market_cap': stock_data['info'].get('marketCap', 'N/A'),
            'pe_ratio': stock_data['info'].get('trailingPE', 'N/A'),
            'dividend_yield': stock_data['info'].get('dividendYield', 'N/A')
        },
        'fake_data': stock_data.get('fake_data', False)
    })

@app.route('/popular')
def popular_stocks():
    """인기 주식 목록 (미국 주식으로 대체)"""
    print("Loading popular stocks (US stocks)...")
    popular_symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']  # 미국 주요 주식
    stocks = []
    
    for symbol in popular_symbols:
        print(f"Processing popular stock: {symbol}")
        data = get_stock_data(symbol)
        if data:
            stocks.append({
                'symbol': symbol,
                'name': data['info'].get('longName', symbol),
                'price': data['current_price'],
                'change': data['change'],
                'change_percent': data['change_percent']
            })
            print(f"Added {symbol} to popular stocks")
        else:
            print(f"Failed to get data for {symbol}")
    
    print(f"Total popular stocks loaded: {len(stocks)}")
    return jsonify(stocks)

@app.route('/api/stock/<stock_name>')
def get_stock_api(stock_name):
    """주식 데이터 API 엔드포인트"""
    data = get_stock_data(stock_name)
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': '주식 데이터를 가져올 수 없습니다.'}), 404

@app.route('/api/chart/<stock_name>')
def get_chart_api(stock_name):
    """차트 데이터 API 엔드포인트"""
    symbol = KOREAN_STOCKS.get(stock_name)
    if symbol:
        chart_data = create_simple_chart_data(get_stock_data(symbol)['history'])
        if chart_data:
            return jsonify(chart_data)
    return jsonify({'error': '차트 데이터를 생성할 수 없습니다.'}), 404

@app.route('/api/all_stocks')
def get_all_stocks():
    """모든 주식 데이터를 가져오는 API"""
    all_data = {}
    for stock_name in KOREAN_STOCKS.keys():
        data = get_stock_data(stock_name)
        if data:
            all_data[stock_name] = data
    return jsonify(all_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 