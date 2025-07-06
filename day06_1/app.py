from flask import Flask, render_template, request, jsonify
import requests
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 백엔드 설정
import io
import base64
from datetime import datetime
import json

app = Flask(__name__)

class CryptoPriceService:
    """암호화폐 가격 데이터를 조회하는 서비스 클래스"""
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        # API 요청 헤더 설정
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_price_data(self, crypto_id, currency, days, interval='daily'):
        """
        CoinGecko에서 가격 데이터를 조회
        
        Args:
            crypto_id (str): 코인 ID (예: 'bitcoin')
            currency (str): 통화 (예: 'krw', 'usd')
            days (str): 조회 기간 (예: '7', '30', 'max')
            interval (str): 데이터 간격 ('daily' 또는 'hourly')
            
        Returns:
            tuple: (날짜/시간 리스트, 가격 리스트) 또는 (None, None) if error
        """
        url = f"{self.base_url}/coins/{crypto_id}/market_chart"
        params = {
            'vs_currency': currency,
            'days': days
        }
        
        if interval == 'hourly':
            params['interval'] = 'hourly'
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            prices = data.get("prices", [])
            
            if not prices:
                return None, None
            
            time_list = []
            price_list = []
            
            for timestamp, price in prices:
                dt = datetime.fromtimestamp(timestamp / 1000)
                if interval == 'daily':
                    # 일 단위로 중복 제거
                    date_str = dt.strftime('%Y-%m-%d')
                    if not time_list or time_list[-1] != date_str:
                        time_list.append(date_str)
                        price_list.append(price)
                else:
                    time_list.append(dt.strftime('%Y-%m-%d %H:%M'))
                    price_list.append(price)
            
            return time_list, price_list
            
        except requests.RequestException as e:
            print(f"API 요청 오류: {e}")
            return None, None
        except Exception as e:
            print(f"데이터 처리 오류: {e}")
            return None, None
    
    def get_current_price(self, crypto_id, currency):
        """현재 가격 조회"""
        url = f"{self.base_url}/simple/price"
        params = {
            'ids': crypto_id,
            'vs_currencies': currency
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get(crypto_id, {}).get(currency)
        except requests.RequestException as e:
            print(f"현재 가격 조회 오류: {e}")
            return None

class ChartGenerator:
    """차트 생성 클래스"""
    
    @staticmethod
    def create_price_chart(times, prices, crypto_id, currency, interval='daily'):
        """가격 차트 생성 및 base64 인코딩된 이미지 반환"""
        try:
            # 한글 폰트 설정
            plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial Unicode MS', 'Malgun Gothic']
            
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(times, prices, marker='o' if interval == 'daily' else None, 
                   linestyle='-', color='#1f77b4', linewidth=2)
            
            title = f"{crypto_id.capitalize()} 가격 변화 ({currency.upper()})"
            if interval == 'hourly':
                title += " (시간별)"
            else:
                title += " (일별)"
            
            ax.set_title(title, fontsize=14, fontweight='bold')
            ax.set_xlabel("날짜", fontsize=12)
            ax.set_ylabel(f"가격 ({currency.upper()})", fontsize=12)
            ax.grid(True, alpha=0.3)
            
            # x축 레이블 회전
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            plt.tight_layout()
            
            # 이미지를 base64로 인코딩
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            img_buffer.seek(0)
            img_str = base64.b64encode(img_buffer.getvalue()).decode()
            plt.close()
            
            return img_str
            
        except Exception as e:
            print(f"차트 생성 오류: {e}")
            return None

# 서비스 인스턴스 생성
crypto_service = CryptoPriceService()
chart_generator = ChartGenerator()

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/price', methods=['POST'])
def get_price_data():
    """가격 데이터 API 엔드포인트"""
    try:
        data = request.get_json()
        crypto_id = data.get('crypto_id', 'bitcoin').lower()
        currency = data.get('currency', 'krw').lower()
        days = data.get('days', '7')
        interval = data.get('interval', 'daily')
        
        # 입력 검증
        if not crypto_id or not currency or not days:
            return jsonify({'error': '필수 파라미터가 누락되었습니다.'}), 400
        
        # 현재 가격 조회
        current_price = crypto_service.get_current_price(crypto_id, currency)
        
        # 히스토리 데이터 조회
        times, prices = crypto_service.get_price_data(crypto_id, currency, days, interval)
        
        if times is None or prices is None:
            return jsonify({'error': '데이터를 가져오지 못했습니다.'}), 500
        
        # 차트 생성
        chart_image = chart_generator.create_price_chart(times, prices, crypto_id, currency, interval)
        
        return jsonify({
            'success': True,
            'current_price': current_price,
            'times': times,
            'prices': prices,
            'chart_image': chart_image,
            'crypto_id': crypto_id,
            'currency': currency,
            'interval': interval
        })
        
    except Exception as e:
        return jsonify({'error': f'서버 오류: {str(e)}'}), 500

@app.route('/api/current-price/<crypto_id>/<currency>')
def get_current_price(crypto_id, currency):
    """현재 가격만 조회하는 API"""
    try:
        price = crypto_service.get_current_price(crypto_id.lower(), currency.lower())
        if price is None:
            return jsonify({'error': '가격을 가져오지 못했습니다.'}), 500
        
        return jsonify({
            'crypto_id': crypto_id,
            'currency': currency,
            'price': price
        })
        
    except Exception as e:
        return jsonify({'error': f'서버 오류: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 