"""
자동차 판매량 데이터 수집 프로그램
네이버 검색 결과에서 자동차 판매량 정보를 수집하여 데이터베이스에 저장합니다.
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
import re
from datetime import datetime
import time

def crawl_car_sales_data():
    """
    네이버 검색 결과에서 자동차 판매량 데이터를 수집하는 함수
    """
    print("🚗 자동차 판매량 데이터 수집을 시작합니다...")
    
    # 네이버 검색 URL (2025년 5월 자동차 판매량)
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=2025%EB%85%84+5%EC%9B%94+%EC%9E%90%EB%8F%99%EC%B0%A8+%ED%8C%90%EB%A7%A4%EB%9F%89&oquery=&tqi=ja9mldpzL8VssvFwNZwssssssdG-326752&ackey=0ykavzm0"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"📡 URL에 접속 중: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print("✅ 페이지 로드 성공")
        
    except requests.RequestException as e:
        print(f"❌ 페이지 로드 실패: {e}")
        return []
    
    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(response.content, 'html.parser')
    
    car_data = []
    
    # 방법 1: info_box 클래스를 가진 div 찾기 (제공해주신 HTML 구조)
    info_boxes = soup.find_all('div', class_='info_box')
    print(f"🔍 info_box div 찾음: {len(info_boxes)}개")
    
    for box in info_boxes:
        try:
            # 순위 추출
            rank_elem = box.find('span', class_='this_text')
            if not rank_elem:
                continue
            rank = int(rank_elem.get_text(strip=True))
            
            # 자동차 이름 추출
            title_elem = box.find('strong', class_='title')
            if not title_elem:
                continue
            car_name = title_elem.get_text(strip=True)
            
            # 판매량 추출 (첫 번째 info_txt)
            info_txts = box.find_all('span', class_='info_txt')
            if len(info_txts) < 1:
                continue
            
            sales_text = info_txts[0].get_text(strip=True)
            sales_match = re.search(r'(\d{1,3}(?:,\d{3})*)', sales_text)
            
            if not sales_match:
                continue
            sales_count = int(sales_match.group(1).replace(',', ''))
            
            # 카테고리 추출 (두 번째 info_txt)
            category = ""
            if len(info_txts) >= 2:
                category = info_txts[1].get_text(strip=True)
            
            car_data.append({
                'car_name': car_name,
                'sales_count': sales_count,
                'rank': rank,
                'category': category
            })
            
            print(f"✅ {rank}위: {car_name} - {sales_count:,}대 ({category})")
            
        except Exception as e:
            print(f"⚠️ 데이터 추출 중 오류: {e}")
            continue
    
    # 방법 2: 다른 구조로도 시도 (백업 방법)
    if not car_data:
        print("🔍 다른 방법으로 데이터 검색 중...")
        
        # horizon_box_image 클래스를 가진 div 찾기
        horizon_boxes = soup.find_all('div', class_='horizon_box_image')
        print(f"🔍 horizon_box_image div 찾음: {len(horizon_boxes)}개")
        
        for box in horizon_boxes:
            try:
                # info_area 클래스를 가진 div 찾기
                info_areas = box.find_all('div', class_='info_area')
                
                for area in info_areas:
                    # 자동차 이름 추출
                    title_elem = area.find('strong', class_='title')
                    if not title_elem:
                        continue
                    car_name = title_elem.get_text(strip=True)
                    
                    # 판매량과 카테고리 추출
                    info_txts = area.find_all('span', class_='info_txt')
                    
                    if len(info_txts) >= 1:
                        sales_text = info_txts[0].get_text(strip=True)
                        sales_match = re.search(r'(\d{1,3}(?:,\d{3})*)', sales_text)
                        
                        if sales_match:
                            sales_count = int(sales_match.group(1).replace(',', ''))
                            category = info_txts[1].get_text(strip=True) if len(info_txts) >= 2 else ""
                            
                            car_data.append({
                                'car_name': car_name,
                                'sales_count': sales_count,
                                'rank': len(car_data) + 1,
                                'category': category
                            })
                            
                            print(f"✅ 발견: {car_name} - {sales_count:,}대 ({category})")
                
            except Exception as e:
                print(f"⚠️ 데이터 추출 중 오류: {e}")
                continue
    
    # 중복 제거 및 정렬
    unique_cars = {}
    for car in car_data:
        key = car['car_name']
        if key not in unique_cars or car['sales_count'] > unique_cars[key]['sales_count']:
            unique_cars[key] = car
    
    car_data = list(unique_cars.values())
    car_data.sort(key=lambda x: x['sales_count'], reverse=True)
    
    # 순위 재정렬
    for i, car in enumerate(car_data, 1):
        car['rank'] = i
    
    print(f"\n📊 총 {len(car_data)}개의 차량 데이터를 수집했습니다.")
    
    if not car_data:
        print("❌ 수집된 데이터가 없습니다.")
        print("💡 네이버 검색 결과 페이지의 구조가 변경되었을 수 있습니다.")
        return []
    
    return car_data

def save_to_database(car_data):
    """
    수집된 데이터를 데이터베이스에 저장하는 함수
    """
    if not car_data:
        print("❌ 저장할 데이터가 없습니다.")
        return
    
    print("\n💾 데이터베이스에 저장 중...")
    
    conn = sqlite3.connect('car_sales.db')
    cursor = conn.cursor()
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_year = 2025  # URL에서 확인된 연도
    current_month = 5    # URL에서 확인된 월
    
    saved_count = 0
    
    for car in car_data:
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO car_sales 
                (car_name, sales_count, rank_position, category, year, month, collected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (car['car_name'], car['sales_count'], car['rank'], 
                  car['category'], current_year, current_month, current_time))
            
            saved_count += 1
            print(f"✅ 저장됨: {car['car_name']} - {car['sales_count']:,}대 (순위: {car['rank']})")
            
        except Exception as e:
            print(f"❌ 저장 실패 ({car['car_name']}): {e}")
            continue
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 총 {saved_count}개의 차량 데이터가 성공적으로 저장되었습니다!")

def show_collected_data():
    """
    수집된 데이터를 조회하여 표시하는 함수
    """
    print("\n📊 저장된 데이터 조회:")
    
    conn = sqlite3.connect('car_sales.db')
    cursor = conn.cursor()
    
    # 개별 차량 판매량 조회
    cursor.execute('''
        SELECT car_name, sales_count, rank_position, category, year, month
        FROM car_sales 
        ORDER BY year DESC, month DESC, rank_position
        LIMIT 20
    ''')
    
    cars = cursor.fetchall()
    
    if cars:
        print(f"\n🚗 자동차 판매량 TOP 20:")
        print(f"{'순위':<4} {'자동차명':<25} {'판매량':<8} {'카테고리':<20} {'기간'}")
        print("-" * 70)
        
        for car in cars:
            car_name, sales_count, rank, category, year, month = car
            print(f"{rank:<4} {car_name:<25} {sales_count:<8,} {category:<20} {year}년 {month}월")
    else:
        print("❌ 저장된 데이터가 없습니다.")
    
    conn.close()

def main():
    """
    메인 함수
    """
    print("🚗 자동차 판매량 데이터 수집 프로그램")
    print("=" * 50)
    
    while True:
        print("\n📋 메뉴를 선택하세요:")
        print("1. 데이터 수집 및 저장")
        print("2. 수집된 데이터 조회")
        print("3. 종료")
        
        choice = input("\n선택 (1-3): ").strip()
        
        if choice == '1':
            print("\n🔄 데이터 수집을 시작합니다...")
            car_data = crawl_car_sales_data()
            
            if car_data:
                save_choice = input("\n💾 수집된 데이터를 데이터베이스에 저장하시겠습니까? (y/n): ").strip().lower()
                if save_choice in ['y', 'yes', '예']:
                    save_to_database(car_data)
                else:
                    print("❌ 데이터 저장을 취소했습니다.")
            else:
                print("❌ 저장할 데이터가 없습니다.")
                
        elif choice == '2':
            show_collected_data()
            
        elif choice == '3':
            print("\n👋 프로그램을 종료합니다.")
            break
            
        else:
            print("❌ 잘못된 선택입니다. 1-3 중에서 선택해주세요.")

if __name__ == "__main__":
    main() 