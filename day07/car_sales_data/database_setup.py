"""
자동차 판매량 데이터베이스 설정 파일
네이버 검색 결과에서 수집한 자동차 판매량 데이터를 저장하는 테이블을 생성합니다.
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
            car_name TEXT NOT NULL,           -- 자동차 이름 (예: 현대 팰리세이드 하이브리드)
            sales_count INTEGER NOT NULL,     -- 판매 대수 (예: 6426)
            rank_position INTEGER,            -- 순위 (예: 1)
            category TEXT,                    -- 카테고리 (예: 국산 대형 SUV 1위)
            year INTEGER NOT NULL,            -- 연도 (예: 2025)
            month INTEGER NOT NULL,           -- 월 (예: 5)
            collected_at TEXT NOT NULL,       -- 수집 시간
            UNIQUE(car_name, year, month)     -- 같은 차량의 같은 월 데이터 중복 방지
        )
    ''')
    
    # 변경사항 저장
    conn.commit()
    
    # 연결 종료
    conn.close()
    
    print("✅ 데이터베이스 생성 완료!")
    print("📁 car_sales.db 파일이 생성되었습니다.")
    print("📋 생성된 테이블:")
    print("   - car_sales: 자동차 판매량 데이터")

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

def show_sample_data():
    """
    저장된 데이터를 조회하여 표시하는 함수
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

# 메인 실행 부분
if __name__ == "__main__":
    print("=" * 60)
    print("🚗 자동차 판매량 데이터베이스 초기 설정")
    print("=" * 60)
    
    # 데이터베이스 생성
    create_database()
    
    # 데이터베이스 확인
    check_database()
    
    print("\n✅ 데이터베이스 설정이 완료되었습니다!")
    print("💡 이제 car_sales_crawler.py를 실행하여 실제 데이터를 수집할 수 있습니다.") 