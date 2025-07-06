"""
자동차 판매량 데이터 수집 프로그램
사용자가 연도와 기간을 설정하면 해당 기간의 월별 판매량을 자동으로 수집하여 데이터베이스에 저장합니다.
Selenium을 사용하여 JavaScript 기반 페이지네이션을 처리합니다.
"""

import sqlite3
import re
from datetime import datetime, date
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def setup_driver():
    """
    Chrome WebDriver를 설정하는 함수
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 헤드리스 모드
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def crawl_car_sales_data(year, month):
    """
    네이버 검색 결과에서 자동차 판매량 데이터를 수집하는 함수 (연도, 월 지정)
    Selenium을 사용하여 JavaScript 기반 페이지네이션을 처리합니다.
    """
    print(f"🚗 {year}년 {month}월 자동차 판매량 데이터 수집을 시작합니다...")
    
    driver = None
    try:
        driver = setup_driver()
        all_car_data = []
        page = 1
        
        # 네이버 검색 URL
        url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={year}%EB%85%84%20{month}%EC%9B%94%20%EC%9E%90%EB%8F%99%EC%B0%A8%20%ED%8C%90%EB%A7%A4%EB%9F%89"
        
        print(f"📡 URL에 접속 중: {url}")
        driver.get(url)
        
        # 페이지 로드 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("✅ 페이지 로드 성공")
        
        while True:
            print(f"\n📄 페이지 {page} 수집 중...")
            
            # 현재 페이지의 HTML 파싱
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            page_car_data = []
            
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
            
            # 다음 페이지 버튼 찾기 및 클릭
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'a.pg_next:not([aria-disabled="true"])')
                if next_button and next_button.is_enabled():
                    print("➡️ 다음 페이지로 이동...")
                    next_button.click()
                    
                    # 페이지 로드 대기
                    time.sleep(2)
                    page += 1
                else:
                    print("🏁 마지막 페이지에 도달했습니다.")
                    break
            except Exception as e:
                print(f"🏁 다음 페이지 버튼을 찾을 수 없습니다: {e}")
                break
        
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
        
    except Exception as e:
        print(f"❌ 크롤링 중 오류 발생: {e}")
        return []
    finally:
        if driver:
            driver.quit()
            print("🔒 브라우저 종료")

def save_to_database(car_data, year, month):
    """
    수집된 데이터를 SQLite 데이터베이스에 저장하는 함수
    """
    if not car_data:
        print("❌ 저장할 데이터가 없습니다.")
        return
    
    conn = sqlite3.connect('car_sales.db')
    cursor = conn.cursor()
    
    try:
        # 테이블이 없으면 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS car_sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_name TEXT NOT NULL,
                sales_count INTEGER NOT NULL,
                rank_position INTEGER NOT NULL,
                category TEXT,
                year INTEGER NOT NULL,
                month INTEGER NOT NULL,
                collected_at TEXT NOT NULL
            )
        ''')
        
        # 기존 데이터 삭제 (같은 연도/월)
        cursor.execute('DELETE FROM car_sales WHERE year = ? AND month = ?', (year, month))
        
        # 새 데이터 삽입
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for car in car_data:
            cursor.execute('''
                INSERT INTO car_sales (car_name, sales_count, rank_position, category, year, month, collected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (car['car_name'], car['sales_count'], car['rank'], car['category'], year, month, current_time))
        
        conn.commit()
        print(f"✅ {year}년 {month}월 데이터 {len(car_data)}개를 데이터베이스에 저장했습니다.")
        
    except sqlite3.Error as e:
        print(f"❌ 데이터베이스 저장 중 오류: {e}")
    finally:
        conn.close()

def collect_period_sales():
    """
    사용자로부터 연도 범위를 입력받아 해당 기간의 월별 데이터를 수집하는 메인 함수
    """
    print("🚗 자동차 판매량 데이터 수집 프로그램")
    print("=" * 50)
    
    # 시작 연도 입력
    while True:
        try:
            start_year = int(input("시작 연도를 입력하세요 (예: 2022): "))
            if 2000 <= start_year <= 2030:
                break
            else:
                print("❌ 2000년~2030년 사이의 연도를 입력해주세요.")
        except ValueError:
            print("❌ 올바른 숫자를 입력해주세요.")
    
    # 끝 연도 입력
    while True:
        try:
            end_year = int(input("끝 연도를 입력하세요 (예: 2025): "))
            if start_year <= end_year <= 2030:
                break
            else:
                print(f"❌ 시작 연도({start_year})보다 크거나 같고 2030년 이하의 연도를 입력해주세요.")
        except ValueError:
            print("❌ 올바른 숫자를 입력해주세요.")
    
    # 현재 연도 확인
    current_year = date.today().year
    if end_year > current_year:
        print(f"⚠️ 경고: {end_year}년은 현재 연도({current_year}년)보다 큽니다.")
        confirm = input("계속 진행하시겠습니까? (y/n): ").lower()
        if confirm != 'y':
            print("❌ 프로그램을 종료합니다.")
            return
    
    # 수집할 총 개월 수 계산
    total_months = (end_year - start_year + 1) * 12
    print(f"\n📅 {start_year}년 1월 ~ {end_year}년 12월 데이터 수집을 시작합니다...")
    print(f"📊 총 {total_months}개월의 데이터를 수집합니다.")
    print("=" * 60)
    
    collected_count = 0
    
    for year in range(start_year, end_year + 1):
        print(f"\n🏁 {year}년 데이터 수집 시작 (1월 ~ 12월)")
        print("-" * 50)
        
        for month in range(1, 13):
            # 현재 연도이고 현재 월을 넘어가면 중단
            if year == current_year and month > date.today().month:
                print(f"⏭️ {year}년 {month}월은 아직 데이터가 없습니다. 수집을 중단합니다.")
                break
            
            collected_count += 1
            print(f"\n===== {year}년 {month}월 데이터 수집 시작 ({collected_count}/{total_months}) =====")
            
            # 데이터 수집
            car_data = crawl_car_sales_data(year, month)
            
            if car_data:
                # 데이터베이스에 저장
                save_to_database(car_data, year, month)
            else:
                print(f"⚠️ {year}년 {month}월 데이터 수집에 실패했습니다.")
            
            # 월별 수집 간 대기 (서버 부하 방지)
            if month < 12 and not (year == current_year and month >= date.today().month):
                print("⏳ 다음 월 수집을 위해 잠시 대기 중...")
                time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print("🎉 모든 데이터 수집이 완료되었습니다!")
    print(f"📊 총 {collected_count}개월의 데이터를 처리했습니다.")
    
    # 수집된 데이터 조회 여부 확인
    show_data = input("\n수집된 데이터를 조회하시겠습니까? (y/n): ").lower()
    if show_data == 'y':
        show_collected_data()

def show_collected_data():
    """
    데이터베이스에서 수집된 데이터를 조회하여 표시하는 함수
    """
    conn = sqlite3.connect('car_sales.db')
    cursor = conn.cursor()
    
    try:
        # 전체 데이터 조회
        cursor.execute('''
            SELECT year, month, car_name, sales_count, rank_position, category, collected_at
            FROM car_sales
            ORDER BY year DESC, month DESC, rank_position ASC
        ''')
        
        rows = cursor.fetchall()
        
        if not rows:
            print("❌ 데이터베이스에 저장된 데이터가 없습니다.")
            return
        
        print(f"\n📊 데이터베이스에 저장된 총 {len(rows)}개의 레코드:")
        print("=" * 80)
        
        current_year_month = None
        for row in rows:
            year, month, car_name, sales_count, rank, category, collected_at = row
            
            # 연도/월이 바뀌면 구분선 출력
            if current_year_month != (year, month):
                if current_year_month:
                    print("-" * 80)
                print(f"\n📅 {year}년 {month}월 데이터 (수집: {collected_at})")
                print("-" * 80)
                current_year_month = (year, month)
            
            print(f"{rank:2d}위: {car_name:<30} - {sales_count:>6,}대 ({category})")
        
        print("\n" + "=" * 80)
        
    except sqlite3.Error as e:
        print(f"❌ 데이터 조회 중 오류: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    collect_period_sales() 