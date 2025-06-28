"""
자동차 판매량 데이터베이스 설정 파일
차량명, 판매 대수, 해당 월, 수집 시간을 저장하는 테이블을 생성합니다.
"""

import sqlite3
import os
from datetime import datetime

def create_database():
    """
    자동차 판매량 데이터베이스와 테이블을 생성하는 함수
    """
    print("🚗 자동차 판매량 데이터베이스를 생성하고 있습니다...")
    
    # 데이터베이스 연결 (파일이 없으면 새로 생성됨)
    conn = sqlite3.connect('car_sales.db')
    
    # 커서 생성 (데이터베이스에 명령을 내리는 도구)
    cursor = conn.cursor()
    
    # 자동차 판매량 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS car_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_name TEXT NOT NULL,           -- 차량명
            sales_count INTEGER NOT NULL,     -- 판매 대수
            year INTEGER NOT NULL,            -- 연도
            month INTEGER NOT NULL,           -- 월
            rank_position INTEGER,            -- 순위
            category TEXT,                    -- 차종 카테고리 (SUV, 세단 등)
            brand TEXT,                       -- 브랜드 (현대, 기아 등)
            collected_at TEXT NOT NULL,       -- 수집 시간
            UNIQUE(car_name, year, month)     -- 같은 차량의 같은 월 데이터 중복 방지
        )
    ''')
    
    # 브랜드별 통계 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS brand_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,              -- 브랜드명
            year INTEGER NOT NULL,            -- 연도
            month INTEGER NOT NULL,           -- 월
            total_sales INTEGER NOT NULL,     -- 총 판매량
            car_count INTEGER NOT NULL,       -- 등록된 차량 수
            collected_at TEXT NOT NULL,       -- 수집 시간
            UNIQUE(brand, year, month)
        )
    ''')
    
    # 월별 전체 통계 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monthly_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,            -- 연도
            month INTEGER NOT NULL,           -- 월
            total_sales INTEGER NOT NULL,     -- 전체 판매량
            car_count INTEGER NOT NULL,       -- 등록된 차량 수
            top_brand TEXT,                   -- 1위 브랜드
            top_car TEXT,                     -- 1위 차량
            collected_at TEXT NOT NULL,       -- 수집 시간
            UNIQUE(year, month)
        )
    ''')
    
    # 변경사항 저장
    conn.commit()
    
    # 연결 종료
    conn.close()
    
    print("✅ 데이터베이스 생성 완료!")
    print("📁 car_sales.db 파일이 생성되었습니다.")
    print("📋 생성된 테이블:")
    print("   - car_sales: 개별 차량 판매량")
    print("   - brand_stats: 브랜드별 통계")
    print("   - monthly_stats: 월별 전체 통계")

def check_database():
    """
    데이터베이스가 제대로 생성되었는지 확인하는 함수
    """
    if os.path.exists('car_sales.db'):
        print("\n✅ 데이터베이스 파일이 존재합니다.")
        
        # 데이터베이스 연결
        conn = sqlite3.connect('car_sales.db')
        cursor = conn.cursor()
        
        # 테이블 목록 확인
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"📋 생성된 테이블: {[table[0] for table in tables]}")
        
        # 테이블 구조 확인
        for table in tables:
            table_name = table[0]
            print(f"\n📊 {table_name} 테이블 구조:")
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                print(f"   - {col_name}: {col_type} {'(필수)' if not_null else '(선택)'}")
        
        conn.close()
    else:
        print("❌ 데이터베이스 파일이 없습니다.")

def insert_sample_data():
    """
    샘플 데이터를 삽입하는 함수 (테스트용)
    """
    print("\n📝 샘플 데이터를 삽입하고 있습니다...")
    
    conn = sqlite3.connect('car_sales.db')
    cursor = conn.cursor()
    
    # 샘플 데이터 (2024년 5월 기준)
    sample_data = [
        ('현대 팰리세이드 하이브리드', 6426, 2024, 5, 1, '대형 SUV', '현대'),
        ('테슬라 모델 Y', 6237, 2024, 5, 2, '준중형 SUV', '테슬라'),
        ('기아 뉴 쏘렌토 하이브리드', 5954, 2024, 5, 3, '중형 SUV', '기아'),
        ('현대 뉴 아반떼', 5054, 2024, 5, 4, '준중형 세단', '현대'),
        ('기아 뉴 셀토스', 4036, 2024, 5, 5, '소형 SUV', '기아'),
        ('기아 뉴 카니발 하이브리드', 3883, 2024, 5, 6, '대형 RV', '기아'),
        ('제네시스 뉴 G80', 3521, 2024, 5, 7, '준대형 세단', '제네시스'),
        ('현대 뉴 쏘나타', 3419, 2024, 5, 8, '중형 세단', '현대')
    ]
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for data in sample_data:
        car_name, sales_count, year, month, rank, category, brand = data
        try:
            cursor.execute('''
                INSERT INTO car_sales (car_name, sales_count, year, month, rank_position, category, brand, collected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (car_name, sales_count, year, month, rank, category, brand, current_time))
        except sqlite3.IntegrityError:
            print(f"⚠️ {car_name} 데이터가 이미 존재합니다.")
    
    # 브랜드별 통계 계산 및 삽입
    cursor.execute('''
        SELECT brand, SUM(sales_count) as total_sales, COUNT(*) as car_count
        FROM car_sales 
        WHERE year = 2024 AND month = 5
        GROUP BY brand
        ORDER BY total_sales DESC
    ''')
    
    brand_stats = cursor.fetchall()
    
    for brand, total_sales, car_count in brand_stats:
        try:
            cursor.execute('''
                INSERT INTO brand_stats (brand, year, month, total_sales, car_count, collected_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (brand, 2024, 5, total_sales, car_count, current_time))
        except sqlite3.IntegrityError:
            print(f"⚠️ {brand} 브랜드 통계가 이미 존재합니다.")
    
    # 월별 전체 통계 계산 및 삽입
    cursor.execute('''
        SELECT SUM(sales_count) as total_sales, COUNT(*) as car_count,
               (SELECT brand FROM car_sales WHERE year = 2024 AND month = 5 ORDER BY sales_count DESC LIMIT 1) as top_brand,
               (SELECT car_name FROM car_sales WHERE year = 2024 AND month = 5 ORDER BY sales_count DESC LIMIT 1) as top_car
        FROM car_sales 
        WHERE year = 2024 AND month = 5
    ''')
    
    monthly_stats = cursor.fetchone()
    if monthly_stats:
        total_sales, car_count, top_brand, top_car = monthly_stats
        try:
            cursor.execute('''
                INSERT INTO monthly_stats (year, month, total_sales, car_count, top_brand, top_car, collected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (2024, 5, total_sales, car_count, top_brand, top_car, current_time))
        except sqlite3.IntegrityError:
            print("⚠️ 월별 통계가 이미 존재합니다.")
    
    # 변경사항 저장
    conn.commit()
    conn.close()
    
    print("✅ 샘플 데이터 삽입 완료!")

def show_sample_data():
    """
    샘플 데이터를 조회하여 표시하는 함수
    """
    print("\n📊 샘플 데이터 조회:")
    
    conn = sqlite3.connect('car_sales.db')
    cursor = conn.cursor()
    
    # 개별 차량 판매량 조회
    cursor.execute('''
        SELECT car_name, sales_count, rank_position, brand, category
        FROM car_sales 
        WHERE year = 2024 AND month = 5
        ORDER BY rank_position
        LIMIT 10
    ''')
    
    cars = cursor.fetchall()
    
    if cars:
        print("\n🚗 2024년 5월 자동차 판매량 TOP 10:")
        print(f"{'순위':<4} {'차량명':<25} {'판매량':<8} {'브랜드':<8} {'카테고리':<12}")
        print("-" * 65)
        
        for car in cars:
            car_name, sales_count, rank, brand, category = car
            print(f"{rank:<4} {car_name:<25} {sales_count:<8,} {brand:<8} {category:<12}")
    
    # 브랜드별 통계 조회
    cursor.execute('''
        SELECT brand, total_sales, car_count
        FROM brand_stats 
        WHERE year = 2024 AND month = 5
        ORDER BY total_sales DESC
    ''')
    
    brands = cursor.fetchall()
    
    if brands:
        print(f"\n🏭 브랜드별 판매량 (2024년 5월):")
        print(f"{'브랜드':<10} {'총 판매량':<12} {'등록 차량 수':<12}")
        print("-" * 40)
        
        for brand in brands:
            brand_name, total_sales, car_count = brand
            print(f"{brand_name:<10} {total_sales:<12,} {car_count:<12}")
    
    # 월별 전체 통계 조회
    cursor.execute('''
        SELECT total_sales, car_count, top_brand, top_car
        FROM monthly_stats 
        WHERE year = 2024 AND month = 5
    ''')
    
    monthly = cursor.fetchone()
    
    if monthly:
        total_sales, car_count, top_brand, top_car = monthly
        print(f"\n📈 2024년 5월 전체 통계:")
        print(f"총 판매량: {total_sales:,}대")
        print(f"등록 차량 수: {car_count}종")
        print(f"1위 브랜드: {top_brand}")
        print(f"1위 차량: {top_car}")
    
    conn.close()

if __name__ == "__main__":
    # 이 파일을 직접 실행했을 때만 실행되는 코드
    print("=" * 60)
    print("🚗 자동차 판매량 데이터베이스 초기 설정")
    print("=" * 60)
    
    create_database()
    check_database()
    insert_sample_data()
    show_sample_data()
    
    print("\n" + "=" * 60)
    print("🎉 설정이 완료되었습니다!")
    print("이제 car_sales_crawler.py를 실행하여 실제 데이터를 수집할 수 있습니다.")
    print("=" * 60) 