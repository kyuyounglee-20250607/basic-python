"""
자동차 판매량 데이터 웹 서버
데이터베이스에서 데이터를 조회하여 웹 페이지로 제공합니다.
"""

from flask import Flask, render_template, jsonify, request
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    """데이터베이스 연결"""
    conn = sqlite3.connect('car_sales.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_brand_from_car_name(car_name):
    """차량명에서 브랜드 추출"""
    brands = ['현대', '기아', '제네시스', '쌍용', '테슬라', 'BMW', '벤츠', '아우디', 
             '폭스바겐', '볼보', '렉서스', '토요타', '혼다', '닛산', '마쓰다', '스바루',
             '미니', '랜드로버', '재규어', '포드', '쉐보레', '캐딜락', '링컨', '닷지',
             '지프', '람보르기니', '페라리', '포르쉐', '마세라티', '알파로메오', '피아트']
    
    for brand in brands:
        if brand in car_name:
            return brand
    return '기타'

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """전체 데이터 조회 API"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 모든 데이터 조회
        cursor.execute('''
            SELECT car_name, sales_count, rank_position, category, year, month, collected_at
            FROM car_sales 
            ORDER BY year DESC, month DESC, rank_position
        ''')
        
        rows = cursor.fetchall()
        
        if not rows:
            return jsonify({'error': '데이터가 없습니다.'}), 404
        
        # 데이터를 딕셔너리 리스트로 변환
        data = []
        for row in rows:
            data.append({
                'car_name': row['car_name'],
                'sales_count': row['sales_count'],
                'rank_position': row['rank_position'],
                'category': row['category'],
                'year': row['year'],
                'month': row['month'],
                'collected_at': row['collected_at']
            })
        
        # 연도별 통계 계산
        year_stats = {}
        for item in data:
            year = item['year']
            if year not in year_stats:
                year_stats[year] = {
                    'total_sales': 0,
                    'car_count': 0,
                    'months': set()
                }
            year_stats[year]['total_sales'] += item['sales_count']
            year_stats[year]['car_count'] += 1
            year_stats[year]['months'].add(item['month'])
        
        # set을 list로 변환 (JSON 직렬화를 위해)
        for year in year_stats:
            year_stats[year]['months'] = list(year_stats[year]['months'])
        
        # 브랜드별 통계 계산
        brand_stats = {}
        for item in data:
            car_name = item['car_name']
            brand = get_brand_from_car_name(car_name)
            
            if brand not in brand_stats:
                brand_stats[brand] = {
                    'total_sales': 0,
                    'car_count': 0,
                    'models': set()
                }
            brand_stats[brand]['total_sales'] += item['sales_count']
            brand_stats[brand]['car_count'] += 1
            brand_stats[brand]['models'].add(item['car_name'])
        
        # set을 list로 변환
        for brand in brand_stats:
            brand_stats[brand]['models'] = list(brand_stats[brand]['models'])
        
        # 월별 통계 계산
        monthly_stats = {}
        for item in data:
            key = f"{item['year']}-{item['month']:02d}"
            if key not in monthly_stats:
                monthly_stats[key] = {
                    'year': item['year'],
                    'month': item['month'],
                    'total_sales': 0,
                    'car_count': 0,
                    'top_car': None,
                    'top_sales': 0
                }
            monthly_stats[key]['total_sales'] += item['sales_count']
            monthly_stats[key]['car_count'] += 1
            
            if item['sales_count'] > monthly_stats[key]['top_sales']:
                monthly_stats[key]['top_sales'] = item['sales_count']
                monthly_stats[key]['top_car'] = item['car_name']
        
        # 최종 JSON 데이터 구성
        json_data = {
            'export_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'total_records': len(data),
            'data': data,
            'year_stats': year_stats,
            'brand_stats': brand_stats,
            'monthly_stats': monthly_stats
        }
        
        conn.close()
        return jsonify(json_data)
        
    except Exception as e:
        return jsonify({'error': f'데이터 조회 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/filter')
def get_filtered_data():
    """필터링된 데이터 조회 API"""
    try:
        year = request.args.get('year', '')
        brand = request.args.get('brand', '')
        model = request.args.get('model', '')
        search = request.args.get('search', '')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 기본 쿼리
        query = '''
            SELECT car_name, sales_count, rank_position, category, year, month, collected_at
            FROM car_sales 
            WHERE 1=1
        '''
        params = []
        
        # 필터 조건 추가
        if year:
            query += ' AND year = ?'
            params.append(int(year))
        
        if brand:
            # 브랜드 필터링은 애플리케이션 레벨에서 처리
            pass
        
        if model:
            query += ' AND car_name = ?'
            params.append(model)
        
        if search:
            query += ' AND car_name LIKE ?'
            params.append(f'%{search}%')
        
        query += ' ORDER BY year DESC, month DESC, rank_position'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # 데이터 변환
        data = []
        for row in rows:
            item = {
                'car_name': row['car_name'],
                'sales_count': row['sales_count'],
                'rank_position': row['rank_position'],
                'category': row['category'],
                'year': row['year'],
                'month': row['month'],
                'collected_at': row['collected_at']
            }
            
            # 브랜드 필터링 (애플리케이션 레벨)
            if brand:
                car_brand = get_brand_from_car_name(item['car_name'])
                if car_brand != brand:
                    continue
            
            data.append(item)
        
        conn.close()
        return jsonify({'data': data, 'total_records': len(data)})
        
    except Exception as e:
        return jsonify({'error': f'필터링 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/api/stats')
def get_stats():
    """통계 데이터 조회 API"""
    try:
        year = request.args.get('year', '')
        brand = request.args.get('brand', '')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 기본 쿼리
        query = 'SELECT car_name, sales_count, year, month FROM car_sales WHERE 1=1'
        params = []
        
        if year:
            query += ' AND year = ?'
            params.append(int(year))
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # 통계 계산
        total_sales = 0
        years = set()
        brands = set()
        
        for row in rows:
            total_sales += row['sales_count']
            years.add(row['year'])
            
            car_brand = get_brand_from_car_name(row['car_name'])
            if not brand or car_brand == brand:
                brands.add(car_brand)
        
        stats = {
            'total_records': len(rows),
            'total_years': len(years),
            'total_brands': len(brands),
            'total_sales': total_sales
        }
        
        conn.close()
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': f'통계 조회 중 오류가 발생했습니다: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚗 자동차 판매량 데이터 웹 서버를 시작합니다...")
    print("📊 데이터베이스에서 실시간으로 데이터를 조회합니다.")
    print("🌐 웹 브라우저에서 http://localhost:5000 으로 접속하세요.")
    app.run(debug=True, host='0.0.0.0', port=5000) 