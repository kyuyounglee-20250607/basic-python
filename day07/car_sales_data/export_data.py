"""
자동차 판매량 데이터를 JSON으로 내보내는 스크립트
HTML 시각화를 위해 데이터를 JSON 형태로 변환합니다.
"""

import sqlite3
import json
from datetime import datetime

def export_car_sales_data():
    """
    데이터베이스에서 자동차 판매량 데이터를 JSON으로 내보내는 함수
    """
    print("📊 자동차 판매량 데이터를 JSON으로 내보내는 중...")
    
    conn = sqlite3.connect('car_sales.db')
    cursor = conn.cursor()
    
    # 모든 데이터 조회
    cursor.execute('''
        SELECT car_name, sales_count, rank_position, category, year, month, collected_at
        FROM car_sales 
        ORDER BY year DESC, month DESC, rank_position
    ''')
    
    rows = cursor.fetchall()
    
    if not rows:
        print("❌ 내보낼 데이터가 없습니다.")
        conn.close()
        return None
    
    # 데이터를 딕셔너리 리스트로 변환
    data = []
    for row in rows:
        car_name, sales_count, rank_position, category, year, month, collected_at = row
        data.append({
            'car_name': car_name,
            'sales_count': sales_count,
            'rank_position': rank_position,
            'category': category,
            'year': year,
            'month': month,
            'collected_at': collected_at
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
        # 차량명에서 브랜드 추출
        car_name = item['car_name']
        brand = "기타"
        
        # 주요 브랜드 목록
        brands = ['현대', '기아', '제네시스', '쌍용', '테슬라', 'BMW', '벤츠', '아우디', 
                 '폭스바겐', '볼보', '렉서스', '토요타', '혼다', '닛산', '마쓰다', '스바루',
                 '미니', '랜드로버', '재규어', '포드', '쉐보레', '캐딜락', '링컨', '닷지',
                 '지프', '람보르기니', '페라리', '포르쉐', '마세라티', '알파로메오', '피아트']
        
        for b in brands:
            if b in car_name:
                brand = b
                break
        
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
    
    # JSON 파일로 저장
    with open('car_sales_data.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    conn.close()
    
    print(f"✅ 총 {len(data)}개의 데이터를 car_sales_data.json 파일로 내보냈습니다.")
    print(f"📊 연도별 통계: {len(year_stats)}개 연도")
    print(f"🏭 브랜드별 통계: {len(brand_stats)}개 브랜드")
    print(f"📅 월별 통계: {len(monthly_stats)}개월")
    
    return json_data

if __name__ == "__main__":
    export_car_sales_data() 