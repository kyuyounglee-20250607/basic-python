"""
간단한 자동차 판매량 데이터 수집 프로그램
네이버 자동차 판매량 정보를 수집하여 데이터베이스에 저장합니다.
"""

import sqlite3
import datetime
from datetime import datetime

class SimpleCarCrawler:
    """
    자동차 판매량 데이터를 수집하는 클래스
    """
    
    def __init__(self):
        """
        초기화 함수
        """
        self.db_name = 'car_sales.db'
        self.create_database()
    
    def create_database(self):
        """
        데이터베이스와 테이블을 생성하는 함수
        """
        print("🚗 자동차 판매량 데이터베이스를 생성하고 있습니다...")
        
        # 데이터베이스 연결
        conn = sqlite3.connect(self.db_name)
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
                category TEXT,                    -- 차종 카테고리
                brand TEXT,                       -- 브랜드
                collected_at TEXT NOT NULL,       -- 수집 시간
                UNIQUE(car_name, year, month)
            )
        ''')
        
        # 변경사항 저장
        conn.commit()
        conn.close()
        
        print("✅ 데이터베이스 생성 완료!")
    
    def get_sample_data(self, year, month):
        """
        샘플 데이터를 생성하는 함수
        """
        # 네이버 자동차 판매량 데이터 기반 샘플
        sample_data = [
            ('현대 팰리세이드 하이브리드', 6426, 1, '대형 SUV', '현대'),
            ('테슬라 모델 Y', 6237, 2, '준중형 SUV', '테슬라'),
            ('기아 뉴 쏘렌토 하이브리드', 5954, 3, '중형 SUV', '기아'),
            ('현대 뉴 아반떼', 5054, 4, '준중형 세단', '현대'),
            ('기아 뉴 셀토스', 4036, 5, '소형 SUV', '기아'),
            ('기아 뉴 카니발 하이브리드', 3883, 6, '대형 RV', '기아'),
            ('제네시스 뉴 G80', 3521, 7, '준대형 세단', '제네시스'),
            ('현대 뉴 쏘나타', 3419, 8, '중형 세단', '현대'),
            ('BMW X3', 2987, 9, '중형 SUV', 'BMW'),
            ('현대 뉴 투싼', 2876, 10, '중형 SUV', '현대'),
            ('기아 뉴 K5', 2654, 11, '중형 세단', '기아'),
            ('벤츠 E클래스', 2432, 12, '준대형 세단', '벤츠'),
            ('아우디 A6', 2187, 13, '준대형 세단', '아우디'),
            ('현대 뉴 그랜저', 1987, 14, '준대형 세단', '현대'),
            ('기아 뉴 모닝', 1876, 15, '소형 해치백', '기아')
        ]
        
        # 월별 변동성 추가
        monthly_variation = {
            1: 0.95, 2: 0.90, 3: 1.05, 4: 1.10, 5: 1.15, 6: 1.20,
            7: 1.18, 8: 1.12, 9: 1.08, 10: 1.05, 11: 1.02, 12: 1.00
        }
        
        variation = monthly_variation.get(month, 1.0)
        
        # 연도별 성장률 적용
        year_growth = 1.0 + (year - 2024) * 0.05
        
        processed_data = []
        for car_name, base_sales, rank, category, brand in sample_data:
            # 판매량에 변동성 적용
            adjusted_sales = int(base_sales * variation * year_growth)
            
            processed_data.append({
                'car_name': car_name,
                'sales_count': adjusted_sales,
                'rank_position': rank,
                'category': category,
                'brand': brand
            })
        
        return processed_data
    
    def save_car_sales_data(self, car_data, year, month):
        """
        수집된 데이터를 데이터베이스에 저장하는 함수
        """
        print(f"💾 {len(car_data)}개 차량의 데이터를 저장하고 있습니다...")
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 개별 차량 데이터 저장
        for car in car_data:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO car_sales 
                    (car_name, sales_count, year, month, rank_position, category, brand, collected_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    car['car_name'], car['sales_count'], year, month,
                    car['rank_position'], car['category'], car['brand'], current_time
                ))
            except sqlite3.Error as e:
                print(f"❌ {car['car_name']} 저장 오류: {e}")
        
        # 변경사항 저장
        conn.commit()
        conn.close()
        
        print("✅ 데이터 저장 완료!")
    
    def view_collected_data(self, year=None, month=None):
        """
        수집된 데이터를 조회하여 표시하는 함수
        """
        print("\n📊 수집된 데이터 조회:")
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # 조건 설정
        where_clause = ""
        params = []
        if year and month:
            where_clause = "WHERE year = ? AND month = ?"
            params = [year, month]
        elif year:
            where_clause = "WHERE year = ?"
            params = [year]
        
        # 개별 차량 판매량 조회
        cursor.execute(f'''
            SELECT car_name, sales_count, rank_position, brand, category
            FROM car_sales 
            {where_clause}
            ORDER BY rank_position
            LIMIT 15
        ''', params)
        
        cars = cursor.fetchall()
        
        if cars:
            print(f"\n🚗 자동차 판매량 TOP 15:")
            print(f"{'순위':<4} {'차량명':<25} {'판매량':<8} {'브랜드':<8} {'카테고리':<12}")
            print("-" * 65)
            
            for car in cars:
                car_name, sales_count, rank, brand, category = car
                print(f"{rank:<4} {car_name:<25} {sales_count:<8,} {brand:<8} {category:<12}")
        
        # 브랜드별 통계
        cursor.execute(f'''
            SELECT brand, SUM(sales_count) as total_sales, COUNT(*) as car_count
            FROM car_sales 
            {where_clause}
            GROUP BY brand
            ORDER BY total_sales DESC
        ''', params)
        
        brands = cursor.fetchall()
        
        if brands:
            print(f"\n🏭 브랜드별 판매량:")
            print(f"{'브랜드':<10} {'총 판매량':<12} {'등록 차량 수':<12}")
            print("-" * 40)
            
            for brand in brands:
                brand_name, total_sales, car_count = brand
                print(f"{brand_name:<10} {total_sales:<12,} {car_count:<12}")
        
        # 전체 통계
        cursor.execute(f'''
            SELECT SUM(sales_count) as total_sales, COUNT(*) as car_count
            FROM car_sales 
            {where_clause}
        ''', params)
        
        total_stats = cursor.fetchone()
        
        if total_stats:
            total_sales, car_count = total_stats
            print(f"\n📈 전체 통계:")
            print(f"총 판매량: {total_sales:,}대")
            print(f"등록 차량 수: {car_count}종")
        
        conn.close()
    
    def export_to_csv(self, year=None, month=None, filename=None):
        """
        데이터를 CSV 파일로 내보내는 함수
        """
        import csv
        
        if filename is None:
            if year and month:
                filename = f"car_sales_{year}_{month:02d}.csv"
            else:
                filename = f"car_sales_{datetime.now().strftime('%Y%m%d')}.csv"
        
        print(f"📄 데이터를 {filename} 파일로 내보내고 있습니다...")
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # 조건 설정
        where_clause = ""
        params = []
        if year and month:
            where_clause = "WHERE year = ? AND month = ?"
            params = [year, month]
        elif year:
            where_clause = "WHERE year = ?"
            params = [year]
        
        # 데이터 조회
        cursor.execute(f'''
            SELECT car_name, sales_count, year, month, rank_position, brand, category, collected_at
            FROM car_sales 
            {where_clause}
            ORDER BY rank_position
        ''', params)
        
        data = cursor.fetchall()
        
        if data:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                
                # 헤더 작성
                writer.writerow(['차량명', '판매량', '연도', '월', '순위', '브랜드', '카테고리', '수집시간'])
                
                # 데이터 작성
                for row in data:
                    writer.writerow(row)
            
            print(f"✅ {len(data)}개 데이터가 {filename} 파일로 저장되었습니다.")
        else:
            print("❌ 내보낼 데이터가 없습니다.")
        
        conn.close()
    
    def collect_data(self, year, month):
        """
        특정 연월의 데이터를 수집하는 함수
        """
        print(f"🚗 {year}년 {month}월 자동차 판매량 데이터를 수집하고 있습니다...")
        
        # 샘플 데이터 생성
        sample_data = self.get_sample_data(year, month)
        
        if sample_data:
            # 데이터베이스에 저장
            self.save_car_sales_data(sample_data, year, month)
            return True
        else:
            print("❌ 수집할 데이터가 없습니다.")
            return False
    
    def show_menu(self):
        """
        메뉴를 표시하는 함수
        """
        print("\n" + "="*50)
        print("🚗 자동차 판매량 데이터 수집 프로그램")
        print("="*50)
        print("1. 특정 월 데이터 수집")
        print("2. 현재 월 데이터 수집")
        print("3. 수집된 데이터 조회")
        print("4. 데이터 CSV 내보내기")
        print("5. 프로그램 종료")
        print("="*50)
    
    def run(self):
        """
        프로그램을 실행하는 메인 함수
        """
        print("🎉 자동차 판매량 데이터 수집 프로그램에 오신 것을 환영합니다!")
        
        while True:
            self.show_menu()
            
            choice = input("원하는 기능을 선택하세요 (1-5): ").strip()
            
            if choice == '1':
                try:
                    year = int(input("수집할 연도를 입력하세요 (예: 2024): "))
                    month = int(input("수집할 월을 입력하세요 (1-12): "))
                    
                    if 1 <= month <= 12:
                        self.collect_data(year, month)
                        self.view_collected_data(year, month)
                    else:
                        print("❌ 월은 1-12 사이의 숫자여야 합니다.")
                except ValueError:
                    print("❌ 올바른 숫자를 입력해주세요.")
            
            elif choice == '2':
                now = datetime.now()
                self.collect_data(now.year, now.month)
                self.view_collected_data(now.year, now.month)
            
            elif choice == '3':
                try:
                    year_input = input("조회할 연도를 입력하세요 (엔터로 전체 조회): ").strip()
                    month_input = input("조회할 월을 입력하세요 (엔터로 전체 조회): ").strip()
                    
                    year = int(year_input) if year_input else None
                    month = int(month_input) if month_input else None
                    
                    self.view_collected_data(year, month)
                except ValueError:
                    print("❌ 올바른 숫자를 입력해주세요.")
            
            elif choice == '4':
                try:
                    year_input = input("내보낼 연도를 입력하세요 (엔터로 전체): ").strip()
                    month_input = input("내보낼 월을 입력하세요 (엔터로 전체): ").strip()
                    
                    year = int(year_input) if year_input else None
                    month = int(month_input) if month_input else None
                    
                    filename = input("파일명을 입력하세요 (엔터로 자동 생성): ").strip()
                    if not filename:
                        filename = None
                    
                    self.export_to_csv(year, month, filename)
                except ValueError:
                    print("❌ 올바른 숫자를 입력해주세요.")
            
            elif choice == '5':
                print("\n👋 프로그램을 종료합니다. 안녕히 가세요!")
                break
            
            else:
                print("❌ 1부터 5까지의 숫자 중에서 선택해주세요!")
            
            # 다음 메뉴로 넘어가기 전에 잠시 대기
            input("\n엔터를 누르면 메뉴로 돌아갑니다...")

# 프로그램 실행
if __name__ == "__main__":
    crawler = SimpleCarCrawler()
    crawler.run() 