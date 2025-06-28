"""
자동차 판매량 데이터 수집 프로그램
사용자가 연도와 기간을 설정하면 해당 기간의 월별 판매량을 자동으로 수집하여 데이터베이스에 저장합니다.
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
import re
from datetime import datetime, date
import time

def crawl_car_sales_data(year, month):
    """
    네이버 검색 결과에서 자동차 판매량 데이터를 수집하는 함수 (연도, 월 지정)
    모든 페이지의 데이터를 수집합니다.
    """
    print(f"🚗 {year}년 {month}월 자동차 판매량 데이터 수집을 시작합니다...")
    
    all_car_data = []
    page = 1
    total_pages = 1
    
    while True:
        print(f"\n📄 페이지 {page} 수집 중...")
        
        # 네이버 검색 URL 동적 생성 (페이지 파라미터 추가)
        if page == 1:
            url = f"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query={year}%EB%85%84%20{month}%EC%9B%94%20%EC%9E%90%EB%8F%99%EC%B0%A8%20%ED%8C%90%EB%A7%A4%EB%9F%89"
        else:
            url = f"https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&qvt=0&query={year}%EB%85%84%20{month}%EC%9B%94%20%EC%9E%90%EB%8F%99%EC%B0%A8%20%ED%8C%90%EB%A7%A4%EB%9F%89&start={((page-1)*10)+1}"
        
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
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        page_car_data = []
        
        # 첫 번째 페이지에서 전체 페이지 수 확인
        if page == 1:
            total_pages = get_total_pages(soup)
            print(f"📊 전체 페이지 수: {total_pages}")
        
        # 방법 1: info_box 클래스를 가진 div 찾기
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
                
                page_car_data.append({
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
        if not page_car_data:
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
                                
                                page_car_data.append({
                                    'car_name': car_name,
                                    'sales_count': sales_count,
                                    'rank': len(page_car_data) + 1,
                                    'category': category
                                })
                                
                                print(f"✅ 발견: {car_name} - {sales_count:,}대 ({category})")
                    
                except Exception as e:
                    print(f"⚠️ 데이터 추출 중 오류: {e}")
                    continue
        
        # 현재 페이지 데이터를 전체 데이터에 추가
        all_car_data.extend(page_car_data)
        print(f"📄 페이지 {page}에서 {len(page_car_data)}개 데이터 수집 완료")
        
        # 다음 페이지로 이동
        page += 1
        
        # 전체 페이지 수에 도달하거나 데이터가 없으면 종료
        if page > total_pages or not page_car_data:
            print(f"🏁 페이지 수집 완료 (총 {page-1}페이지)")
            break
        
        # 정적 크롤링이므로 최소한의 딜레이만 적용 (서버 부하 방지)
        time.sleep(0.1)
    
    # 중복 제거 및 정렬
    unique_cars = {}
    for car in all_car_data:
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

def get_total_pages(soup):
    """
    페이지네이션에서 전체 페이지 수를 추출하는 함수
    """
    try:
        # 페이지네이션 영역 찾기
        pgs_div = soup.find('div', class_='pgs')
        if not pgs_div:
            return 1
        
        # 전체 페이지 수 추출
        total_span = pgs_div.find('span', class_='_total')
        if total_span:
            total_pages = int(total_span.get_text(strip=True))
            return total_pages
        
        # 다른 방법으로 페이지 수 확인
        npgs_span = pgs_div.find('span', class_='npgs')
        if npgs_span:
            # "1 / 13" 형태의 텍스트에서 추출
            text = npgs_span.get_text(strip=True)
            match = re.search(r'(\d+)\s*/\s*(\d+)', text)
            if match:
                return int(match.group(2))
        
        return 1
        
    except Exception as e:
        print(f"⚠️ 페이지 수 추출 중 오류: {e}")
        return 1

def save_to_database(car_data, year, month):
    """
    수집된 데이터를 데이터베이스에 저장하는 함수 (연도, 월 지정)
    """
    if not car_data:
        print("❌ 저장할 데이터가 없습니다.")
        return
    
    print("\n💾 데이터베이스에 저장 중...")
    
    conn = sqlite3.connect('car_sales.db')
    cursor = conn.cursor()
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    saved_count = 0
    
    for car in car_data:
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO car_sales 
                (car_name, sales_count, rank_position, category, year, month, collected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (car['car_name'], car['sales_count'], car['rank'], 
                  car['category'], year, month, current_time))
            
            saved_count += 1
            print(f"✅ 저장됨: {car['car_name']} - {car['sales_count']:,}대 (순위: {car['rank']})")
            
        except Exception as e:
            print(f"❌ 저장 실패 ({car['car_name']}): {e}")
            continue
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 총 {saved_count}개의 차량 데이터가 성공적으로 저장되었습니다!")

def collect_period_sales():
    """
    사용자가 시작 연도와 끝 연도를 설정하면 해당 연도 범위의 모든 월별 판매량을 수집/저장
    """
    print("🚗 자동차 판매량 데이터 수집 프로그램")
    print("=" * 50)
    
    # 시작 연도 입력
    while True:
        try:
            start_year = int(input("시작 연도를 입력하세요 (예: 2022): ").strip())
            if start_year < 2000 or start_year > 2030:
                print("❌ 2000년~2030년 사이의 연도를 입력하세요.")
                continue
            break
        except ValueError:
            print("❌ 올바른 연도를 입력하세요.")
    
    # 끝 연도 입력
    while True:
        try:
            end_year = int(input("끝 연도를 입력하세요 (예: 2025): ").strip())
            if end_year < 2000 or end_year > 2030:
                print("❌ 2000년~2030년 사이의 연도를 입력하세요.")
                continue
            if end_year < start_year:
                print("❌ 끝 연도는 시작 연도보다 크거나 같아야 합니다.")
                continue
            break
        except ValueError:
            print("❌ 올바른 연도를 입력하세요.")
    
    # 현재 날짜 확인 (미래 데이터 방지)
    now = date.today()
    if end_year > now.year:
        print(f"⚠️ {end_year}년은 아직 데이터가 없을 수 있습니다.")
        continue_choice = input("계속 진행하시겠습니까? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes', '예']:
            print("❌ 프로그램을 종료합니다.")
            return
    
    # 수집할 총 월 수 계산
    total_months = (end_year - start_year + 1) * 12
    if end_year == now.year:
        # 현재 연도인 경우 현재 월까지만 수집
        total_months = (end_year - start_year) * 12 + now.month
    
    print(f"\n📅 {start_year}년 1월 ~ {end_year}년 12월 데이터 수집을 시작합니다...")
    print(f"📊 총 {total_months}개월의 데이터를 수집합니다.")
    print("=" * 60)
    
    total_collected = 0
    month_count = 0
    
    # 지정된 연도 범위의 모든 월별 데이터 수집
    for year in range(start_year, end_year + 1):
        # 각 연도의 월 범위 결정
        if year == start_year:
            start_month = 1
        else:
            start_month = 1
            
        if year == end_year:
            if year == now.year:
                end_month = now.month  # 현재 연도인 경우 현재 월까지만
            else:
                end_month = 12
        else:
            end_month = 12
        
        print(f"\n🏁 {year}년 데이터 수집 시작 ({start_month}월 ~ {end_month}월)")
        print("-" * 50)
        
        for month in range(start_month, end_month + 1):
            month_count += 1
            print(f"\n===== {year}년 {month}월 데이터 수집 시작 ({month_count}/{total_months}) =====")
            
            car_data = crawl_car_sales_data(year, month)
            
            if car_data:
                save_to_database(car_data, year, month)
                total_collected += len(car_data)
                print(f"✅ {year}년 {month}월: {len(car_data)}개 차량 데이터 수집 완료")
            else:
                print(f"⚠️ {year}년 {month}월 데이터가 없습니다.")
            
            # 네이버 서버 부하 방지를 위한 대기
            if month_count < total_months:
                print("⏳ 다음 월 수집을 위해 0.5초 대기 중...")
                time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print(f"✅ {start_year}년 ~ {end_year}년 데이터 수집이 완료되었습니다!")
    print(f"📊 총 {month_count}개월, {total_collected}개의 차량 데이터가 수집되었습니다.")
    print("=" * 60)

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

# 메인 실행
if __name__ == "__main__":
    collect_period_sales()
    
    # 수집 완료 후 데이터 조회 여부 확인
    while True:
        show_choice = input("\n📊 수집된 데이터를 조회하시겠습니까? (y/n): ").strip().lower()
        if show_choice in ['y', 'yes', '예']:
            show_collected_data()
            break
        elif show_choice in ['n', 'no', '아니오']:
            print("👋 프로그램을 종료합니다.")
            break
        else:
            print("❌ y 또는 n을 입력하세요.") 