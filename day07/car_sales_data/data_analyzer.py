"""
자동차 판매량 데이터 분석 도구
수집된 데이터를 분석하고 통계를 제공합니다.
"""

import sqlite3
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# seaborn을 선택적으로 import
try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    print("⚠️ seaborn이 설치되지 않았습니다. 기본 matplotlib 스타일을 사용합니다.")

class CarSalesAnalyzer:
    """
    자동차 판매량 데이터를 분석하는 클래스
    """
    
    def __init__(self):
        """
        초기화 함수
        """
        self.db_name = 'car_sales.db'
        
        # 한글 폰트 설정 (matplotlib)
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] = False
        
        # seaborn이 있으면 스타일 설정
        if SEABORN_AVAILABLE:
            sns.set_style("whitegrid")
            sns.set_palette("husl")
    
    def get_connection(self):
        """
        데이터베이스 연결을 반환하는 함수
        """
        return sqlite3.connect(self.db_name)
    
    def get_car_sales_data(self, year=None, month=None):
        """
        자동차 판매량 데이터를 pandas DataFrame으로 가져오는 함수
        """
        conn = self.get_connection()
        
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
        query = f'''
            SELECT car_name, sales_count, year, month, rank_position, brand, category, collected_at
            FROM car_sales 
            {where_clause}
            ORDER BY rank_position
        '''
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return df
    
    def get_brand_stats_data(self, year=None, month=None):
        """
        브랜드별 통계 데이터를 pandas DataFrame으로 가져오는 함수
        """
        conn = self.get_connection()
        
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
        query = f'''
            SELECT brand, total_sales, car_count, year, month
            FROM brand_stats 
            {where_clause}
            ORDER BY total_sales DESC
        '''
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return df
    
    def get_monthly_stats_data(self, year=None):
        """
        월별 통계 데이터를 pandas DataFrame으로 가져오는 함수
        """
        conn = self.get_connection()
        
        # 조건 설정
        where_clause = ""
        params = []
        if year:
            where_clause = "WHERE year = ?"
            params = [year]
        
        # 데이터 조회
        query = f'''
            SELECT year, month, total_sales, car_count, top_brand, top_car
            FROM monthly_stats 
            {where_clause}
            ORDER BY year, month
        '''
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return df
    
    def show_basic_statistics(self, year=None, month=None):
        """
        기본 통계 정보를 표시하는 함수
        """
        print("📊 기본 통계 정보")
        print("=" * 50)
        
        df = self.get_car_sales_data(year, month)
        
        if df.empty:
            print("❌ 분석할 데이터가 없습니다.")
            return
        
        print(f"📅 분석 기간: {year if year else '전체'}년 {month if month else '전체'}월")
        print(f"🚗 총 차량 수: {len(df)}종")
        print(f"🏭 총 브랜드 수: {df['brand'].nunique()}개")
        print(f"📈 총 판매량: {df['sales_count'].sum():,}대")
        print(f"📊 평균 판매량: {df['sales_count'].mean():.0f}대")
        print(f"📉 최소 판매량: {df['sales_count'].min():,}대")
        print(f"📈 최대 판매량: {df['sales_count'].max():,}대")
        
        # 1위 차량 정보
        top_car = df.loc[df['rank_position'] == 1]
        if not top_car.empty:
            car_name = top_car.iloc[0]['car_name']
            sales_count = top_car.iloc[0]['sales_count']
            brand = top_car.iloc[0]['brand']
            print(f"🥇 1위 차량: {car_name} ({brand}) - {sales_count:,}대")
        
        # 브랜드별 통계
        brand_stats = df.groupby('brand')['sales_count'].agg(['sum', 'count']).sort_values('sum', ascending=False)
        print(f"\n🏭 브랜드별 판매량 TOP 5:")
        for i, (brand, stats) in enumerate(brand_stats.head().iterrows(), 1):
            print(f"{i}. {brand}: {stats['sum']:,}대 ({stats['count']}종)")
    
    def show_category_analysis(self, year=None, month=None):
        """
        차종 카테고리별 분석을 표시하는 함수
        """
        print("\n🚙 차종 카테고리별 분석")
        print("=" * 50)
        
        df = self.get_car_sales_data(year, month)
        
        if df.empty:
            print("❌ 분석할 데이터가 없습니다.")
            return
        
        # 카테고리별 통계
        category_stats = df.groupby('category').agg({
            'sales_count': ['sum', 'mean', 'count'],
            'car_name': 'count'
        }).round(0)
        
        category_stats.columns = ['총 판매량', '평균 판매량', '차량 수']
        category_stats = category_stats.sort_values('총 판매량', ascending=False)
        
        print("📊 카테고리별 판매량:")
        print(f"{'카테고리':<15} {'총 판매량':<12} {'평균 판매량':<12} {'차량 수':<8}")
        print("-" * 50)
        
        for category, stats in category_stats.iterrows():
            print(f"{category:<15} {stats['총 판매량']:<12,} {stats['평균 판매량']:<12.0f} {stats['차량 수']:<8}")
        
        # 가장 인기 있는 카테고리
        top_category = category_stats.index[0]
        top_category_sales = category_stats.iloc[0]['총 판매량']
        print(f"\n🔥 가장 인기 있는 카테고리: {top_category} ({top_category_sales:,}대)")
    
    def show_brand_analysis(self, year=None, month=None):
        """
        브랜드별 상세 분석을 표시하는 함수
        """
        print("\n🏭 브랜드별 상세 분석")
        print("=" * 50)
        
        df = self.get_car_sales_data(year, month)
        
        if df.empty:
            print("❌ 분석할 데이터가 없습니다.")
            return
        
        # 브랜드별 통계
        brand_stats = df.groupby('brand').agg({
            'sales_count': ['sum', 'mean', 'count'],
            'rank_position': 'min'
        }).round(0)
        
        brand_stats.columns = ['총 판매량', '평균 판매량', '차량 수', '최고 순위']
        brand_stats = brand_stats.sort_values('총 판매량', ascending=False)
        
        print("📊 브랜드별 상세 통계:")
        print(f"{'브랜드':<12} {'총 판매량':<12} {'평균 판매량':<12} {'차량 수':<8} {'최고 순위':<8}")
        print("-" * 60)
        
        for brand, stats in brand_stats.iterrows():
            print(f"{brand:<12} {stats['총 판매량']:<12,} {stats['평균 판매량']:<12.0f} {stats['차량 수']:<8} {stats['최고 순위']:<8}")
        
        # 시장 점유율 계산
        total_sales = brand_stats['총 판매량'].sum()
        brand_stats['시장 점유율'] = (brand_stats['총 판매량'] / total_sales * 100).round(1)
        
        print(f"\n📈 시장 점유율 TOP 5:")
        for i, (brand, stats) in enumerate(brand_stats.head().iterrows(), 1):
            market_share = stats['시장 점유율']
            print(f"{i}. {brand}: {market_share}% ({stats['총 판매량']:,}대)")
    
    def show_trend_analysis(self, year=None):
        """
        월별 트렌드 분석을 표시하는 함수
        """
        print("\n📈 월별 트렌드 분석")
        print("=" * 50)
        
        df = self.get_monthly_stats_data(year)
        
        if df.empty:
            print("❌ 분석할 데이터가 없습니다.")
            return
        
        print("📊 월별 판매량 추이:")
        print(f"{'연도':<6} {'월':<4} {'총 판매량':<12} {'차량 수':<8} {'1위 브랜드':<12} {'1위 차량':<25}")
        print("-" * 80)
        
        for _, row in df.iterrows():
            print(f"{row['year']:<6} {row['month']:<4} {row['total_sales']:<12,} {row['car_count']:<8} {row['top_brand']:<12} {row['top_car']:<25}")
        
        # 성장률 계산
        if len(df) > 1:
            df_sorted = df.sort_values(['year', 'month'])
            df_sorted['전월 대비'] = df_sorted['total_sales'].pct_change() * 100
            
            print(f"\n📊 월별 성장률:")
            for _, row in df_sorted.iterrows():
                if pd.notna(row['전월 대비']):
                    growth = row['전월 대비']
                    trend = "📈" if growth > 0 else "📉" if growth < 0 else "➡️"
                    print(f"{row['year']}년 {row['month']}월: {trend} {growth:+.1f}%")
    
    def create_sales_chart(self, year=None, month=None, save_path=None):
        """
        판매량 차트를 생성하는 함수
        """
        try:
            df = self.get_car_sales_data(year, month)
            
            if df.empty:
                print("❌ 차트를 생성할 데이터가 없습니다.")
                return
            
            # 상위 10개 차량만 선택
            top_10 = df.head(10)
            
            # 차트 생성
            plt.figure(figsize=(12, 8))
            
            # 막대 차트
            bars = plt.barh(range(len(top_10)), top_10['sales_count'])
            
            # 차트 꾸미기
            plt.yticks(range(len(top_10)), top_10['car_name'])
            plt.xlabel('판매량 (대)')
            plt.title(f'자동차 판매량 TOP 10 ({year if year else "전체"}년 {month if month else "전체"}월)')
            
            # 판매량 표시
            for i, (bar, sales) in enumerate(zip(bars, top_10['sales_count'])):
                plt.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2, 
                        f'{sales:,}대', ha='left', va='center')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"📊 차트가 {save_path}에 저장되었습니다.")
            else:
                plt.show()
            
            plt.close()
            
        except Exception as e:
            print(f"❌ 차트 생성 오류: {e}")
    
    def create_brand_chart(self, year=None, month=None, save_path=None):
        """
        브랜드별 판매량 차트를 생성하는 함수
        """
        try:
            df = self.get_brand_stats_data(year, month)
            
            if df.empty:
                print("❌ 차트를 생성할 데이터가 없습니다.")
                return
            
            # 상위 8개 브랜드만 선택
            top_8 = df.head(8)
            
            # 파이 차트 생성
            plt.figure(figsize=(10, 8))
            
            colors = plt.cm.Set3(range(len(top_8)))
            wedges, texts, autotexts = plt.pie(top_8['total_sales'], 
                                              labels=top_8['brand'],
                                              autopct='%1.1f%%',
                                              colors=colors,
                                              startangle=90)
            
            plt.title(f'브랜드별 판매량 비율 ({year if year else "전체"}년 {month if month else "전체"}월)')
            
            # 범례 추가
            plt.legend(wedges, [f'{brand} ({sales:,}대)' for brand, sales in zip(top_8['brand'], top_8['total_sales'])],
                      title="브랜드별 판매량",
                      loc="center left",
                      bbox_to_anchor=(1, 0, 0.5, 1))
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"📊 브랜드 차트가 {save_path}에 저장되었습니다.")
            else:
                plt.show()
            
            plt.close()
            
        except Exception as e:
            print(f"❌ 브랜드 차트 생성 오류: {e}")
    
    def export_analysis_report(self, year=None, month=None, filename=None):
        """
        분석 결과를 텍스트 파일로 내보내는 함수
        """
        if filename is None:
            if year and month:
                filename = f"car_sales_analysis_{year}_{month:02d}.txt"
            else:
                filename = f"car_sales_analysis_{datetime.now().strftime('%Y%m%d')}.txt"
        
        print(f"📄 분석 결과를 {filename} 파일로 내보내고 있습니다...")
        
        # 분석 데이터 가져오기
        df = self.get_car_sales_data(year, month)
        brand_df = self.get_brand_stats_data(year, month)
        
        if df.empty:
            print("❌ 내보낼 데이터가 없습니다.")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("🚗 자동차 판매량 분석 보고서\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"📅 분석 기간: {year if year else '전체'}년 {month if month else '전체'}월\n")
            f.write(f"📊 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 기본 통계
            f.write("📈 기본 통계\n")
            f.write("-" * 30 + "\n")
            f.write(f"총 차량 수: {len(df)}종\n")
            f.write(f"총 브랜드 수: {df['brand'].nunique()}개\n")
            f.write(f"총 판매량: {df['sales_count'].sum():,}대\n")
            f.write(f"평균 판매량: {df['sales_count'].mean():.0f}대\n\n")
            
            # TOP 10 차량
            f.write("🥇 판매량 TOP 10\n")
            f.write("-" * 30 + "\n")
            for i, (_, row) in enumerate(df.head(10).iterrows(), 1):
                f.write(f"{i:2d}. {row['car_name']:<25} {row['sales_count']:>8,}대 ({row['brand']})\n")
            f.write("\n")
            
            # 브랜드별 통계
            f.write("🏭 브랜드별 판매량\n")
            f.write("-" * 30 + "\n")
            for i, (_, row) in enumerate(brand_df.iterrows(), 1):
                f.write(f"{i:2d}. {row['brand']:<12} {row['total_sales']:>10,}대 ({row['car_count']}종)\n")
            f.write("\n")
            
            # 카테고리별 통계
            category_stats = df.groupby('category')['sales_count'].sum().sort_values(ascending=False)
            f.write("🚙 카테고리별 판매량\n")
            f.write("-" * 30 + "\n")
            for category, sales in category_stats.items():
                f.write(f"• {category:<15} {sales:>10,}대\n")
        
        print(f"✅ 분석 보고서가 {filename} 파일로 저장되었습니다.")
    
    def show_menu(self):
        """
        메뉴를 표시하는 함수
        """
        print("\n" + "="*60)
        print("📊 자동차 판매량 데이터 분석 도구")
        print("="*60)
        print("1. 기본 통계 정보")
        print("2. 차종 카테고리별 분석")
        print("3. 브랜드별 상세 분석")
        print("4. 월별 트렌드 분석")
        print("5. 판매량 차트 생성")
        print("6. 브랜드별 차트 생성")
        print("7. 분석 보고서 내보내기")
        print("8. 프로그램 종료")
        print("="*60)
    
    def run(self):
        """
        프로그램을 실행하는 메인 함수
        """
        print("🎉 자동차 판매량 데이터 분석 도구에 오신 것을 환영합니다!")
        
        while True:
            self.show_menu()
            
            choice = input("원하는 기능을 선택하세요 (1-8): ").strip()
            
            if choice == '1':
                try:
                    year_input = input("분석할 연도를 입력하세요 (엔터로 전체): ").strip()
                    month_input = input("분석할 월을 입력하세요 (엔터로 전체): ").strip()
                    
                    year = int(year_input) if year_input else None
                    month = int(month_input) if month_input else None
                    
                    self.show_basic_statistics(year, month)
                except ValueError:
                    print("❌ 올바른 숫자를 입력해주세요.")
            
            elif choice == '2':
                try:
                    year_input = input("분석할 연도를 입력하세요 (엔터로 전체): ").strip()
                    month_input = input("분석할 월을 입력하세요 (엔터로 전체): ").strip()
                    
                    year = int(year_input) if year_input else None
                    month = int(month_input) if month_input else None
                    
                    self.show_category_analysis(year, month)
                except ValueError:
                    print("❌ 올바른 숫자를 입력해주세요.")
            
            elif choice == '3':
                try:
                    year_input = input("분석할 연도를 입력하세요 (엔터로 전체): ").strip()
                    month_input = input("분석할 월을 입력하세요 (엔터로 전체): ").strip()
                    
                    year = int(year_input) if year_input else None
                    month = int(month_input) if month_input else None
                    
                    self.show_brand_analysis(year, month)
                except ValueError:
                    print("❌ 올바른 숫자를 입력해주세요.")
            
            elif choice == '4':
                try:
                    year_input = input("분석할 연도를 입력하세요 (엔터로 전체): ").strip()
                    year = int(year_input) if year_input else None
                    
                    self.show_trend_analysis(year)
                except ValueError:
                    print("❌ 올바른 숫자를 입력해주세요.")
            
            elif choice == '5':
                try:
                    year_input = input("차트 연도를 입력하세요 (엔터로 전체): ").strip()
                    month_input = input("차트 월을 입력하세요 (엔터로 전체): ").strip()
                    
                    year = int(year_input) if year_input else None
                    month = int(month_input) if month_input else None
                    
                    save_path = input("저장할 파일명을 입력하세요 (엔터로 화면 표시): ").strip()
                    if not save_path:
                        save_path = None
                    
                    self.create_sales_chart(year, month, save_path)
                except ValueError:
                    print("❌ 올바른 숫자를 입력해주세요.")
            
            elif choice == '6':
                try:
                    year_input = input("차트 연도를 입력하세요 (엔터로 전체): ").strip()
                    month_input = input("차트 월을 입력하세요 (엔터로 전체): ").strip()
                    
                    year = int(year_input) if year_input else None
                    month = int(month_input) if month_input else None
                    
                    save_path = input("저장할 파일명을 입력하세요 (엔터로 화면 표시): ").strip()
                    if not save_path:
                        save_path = None
                    
                    self.create_brand_chart(year, month, save_path)
                except ValueError:
                    print("❌ 올바른 숫자를 입력해주세요.")
            
            elif choice == '7':
                try:
                    year_input = input("보고서 연도를 입력하세요 (엔터로 전체): ").strip()
                    month_input = input("보고서 월을 입력하세요 (엔터로 전체): ").strip()
                    
                    year = int(year_input) if year_input else None
                    month = int(month_input) if month_input else None
                    
                    filename = input("파일명을 입력하세요 (엔터로 자동 생성): ").strip()
                    if not filename:
                        filename = None
                    
                    self.export_analysis_report(year, month, filename)
                except ValueError:
                    print("❌ 올바른 숫자를 입력해주세요.")
            
            elif choice == '8':
                print("\n👋 프로그램을 종료합니다. 안녕히 가세요!")
                break
            
            else:
                print("❌ 1부터 8까지의 숫자 중에서 선택해주세요!")
            
            # 다음 메뉴로 넘어가기 전에 잠시 대기
            input("\n엔터를 누르면 메뉴로 돌아갑니다...")

# 프로그램 실행
if __name__ == "__main__":
    analyzer = CarSalesAnalyzer()
    analyzer.run() 