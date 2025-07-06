import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 예측 분석을 위한 추가 라이브러리
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy import stats
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import scipy.stats as stats

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

class PowerAnalysisReport:
    def __init__(self, excel_file_path):
        """
        전력 발전량 분석 및 보고서 생성 클래스
        
        Args:
            excel_file_path (str): 엑셀 파일 경로
        """
        self.excel_file_path = excel_file_path
        self.raw_data = None
        self.yearly_data = None
        self.analysis_results = {}
        self.prediction_results = {}
        self.forecast_years = 3  # 예측할 년도 수
        
    def load_data(self):
        """엑셀 데이터 로드"""
        try:
            # 원본데이터 시트 로드
            self.raw_data = pd.read_excel(self.excel_file_path, sheet_name='원본데이터')
            
            # 년도별분석 시트 로드
            self.yearly_data = pd.read_excel(self.excel_file_path, sheet_name='년도별분석')
            
            print("데이터 로드 완료")
            print(f"원본데이터 행 수: {len(self.raw_data)}")
            print(f"년도별분석 행 수: {len(self.yearly_data)}")
            
        except Exception as e:
            print(f"데이터 로드 중 오류 발생: {e}")
            return False
        
        return True
    
    def analyze_data(self):
        """데이터 분석 수행"""
        # 1. 년도별 발전량 현황 분석
        self.analyze_yearly_trends()
        
        # 2. 발전원별 비중 분석
        self.analyze_power_source_ratio()
        
        # 3. 월별 발전량 패턴 분석 (원본데이터 기준)
        self.analyze_monthly_patterns()
        
        # 4. 성장률 분석
        self.analyze_growth_rates()
        
        # 5. 최근 3년 vs 이전 3년 비교
        self.compare_periods()
        
        # 6. 예측 분석 추가
        self.perform_prediction_analysis()
        
    def analyze_yearly_trends(self):
        """년도별 발전량 추세 분석"""
        yearly_totals = self.yearly_data.groupby('년도')['합계'].sum()
        
        self.analysis_results['yearly_trends'] = {
            'total_by_year': yearly_totals,
            'peak_year': yearly_totals.idxmax(),
            'peak_value': yearly_totals.max(),
            'lowest_year': yearly_totals.idxmin(),
            'lowest_value': yearly_totals.min()
        }
    
    def analyze_power_source_ratio(self):
        """발전원별 비중 분석"""
        # 최근 년도 (2024년) 기준 발전원별 비중
        latest_year = self.yearly_data['년도'].max()
        latest_data = self.yearly_data[self.yearly_data['년도'] == latest_year]
        
        if len(latest_data) > 0:
            latest_row = latest_data.iloc[0]
            power_sources = {
                '원자력': latest_row['원자력'],
                '수력': latest_row['수력'],
                '양수': latest_row['양수'],
                '신재생': latest_row['신재생']
            }
            
            total = sum(power_sources.values())
            ratios = {k: (v/total)*100 for k, v in power_sources.items()}
            
            self.analysis_results['power_source_ratio'] = {
                'ratios': ratios,
                'absolute_values': power_sources,
                'year': latest_year
            }
    
    def analyze_monthly_patterns(self):
        """월별 발전량 패턴 분석"""
        if self.raw_data is not None and '월' in self.raw_data.columns:
            monthly_avg = self.raw_data.groupby('월')['합계'].mean()
            
            self.analysis_results['monthly_patterns'] = {
                'monthly_average': monthly_avg,
                'peak_month': monthly_avg.idxmax(),
                'peak_value': monthly_avg.max(),
                'lowest_month': monthly_avg.idxmin(),
                'lowest_value': monthly_avg.min()
            }
    
    def analyze_growth_rates(self):
        """성장률 분석"""
        yearly_data_sorted = self.yearly_data.sort_values('년도')
        
        # 연간 성장률 계산
        growth_rates = {}
        for col in ['원자력', '수력', '양수', '신재생', '합계']:
            if col in yearly_data_sorted.columns:
                growth_rates[col] = yearly_data_sorted[col].pct_change() * 100
        
        self.analysis_results['growth_rates'] = growth_rates
    
    def compare_periods(self):
        """최근 3년 vs 이전 3년 비교"""
        years = sorted(self.yearly_data['년도'].unique())
        
        if len(years) >= 6:
            recent_3_years = years[-3:]
            previous_3_years = years[-6:-3]
            
            recent_avg = self.yearly_data[self.yearly_data['년도'].isin(recent_3_years)].mean()
            previous_avg = self.yearly_data[self.yearly_data['년도'].isin(previous_3_years)].mean()
            
            self.analysis_results['period_comparison'] = {
                'recent_years': recent_3_years,
                'previous_years': previous_3_years,
                'recent_average': recent_avg,
                'previous_average': previous_avg,
                'improvement': ((recent_avg - previous_avg) / previous_avg * 100)
            }
    
    def perform_prediction_analysis(self):
        """예측 분석 수행"""
        print("예측 분석을 수행합니다...")
        
        # 1. 선형 회귀 예측
        self.linear_regression_forecast()
        
        # 2. 다항식 회귀 예측
        self.polynomial_regression_forecast()
        
        # 3. 지수 평활 예측
        self.exponential_smoothing_forecast()
        
        # 4. 계절성 분해 분석
        self.seasonal_decomposition_analysis()
        
        # 5. 발전원별 성장 트렌드 분석
        self.analyze_source_trends()
    
    def linear_regression_forecast(self):
        """선형 회귀를 이용한 예측"""
        yearly_data_sorted = self.yearly_data.sort_values('년도')
        
        # 예측 결과 저장
        forecasts = {}
        model_performance = {}
        
        for column in ['원자력', '수력', '양수', '신재생', '합계']:
            if column in yearly_data_sorted.columns:
                # 데이터 준비
                X = yearly_data_sorted['년도'].values.reshape(-1, 1)
                y = yearly_data_sorted[column].values
                
                # 모델 훈련
                model = LinearRegression()
                model.fit(X, y)
                
                # 예측
                future_years = np.arange(yearly_data_sorted['년도'].max() + 1, 
                                       yearly_data_sorted['년도'].max() + 1 + self.forecast_years)
                future_X = future_years.reshape(-1, 1)
                predictions = model.predict(future_X)
                
                # 성능 평가
                y_pred = model.predict(X)
                r2 = r2_score(y, y_pred)
                mae = mean_absolute_error(y, y_pred)
                rmse = np.sqrt(mean_squared_error(y, y_pred))
                
                forecasts[column] = {
                    'years': future_years,
                    'predictions': predictions,
                    'slope': model.coef_[0],
                    'intercept': model.intercept_
                }
                
                model_performance[column] = {
                    'r2_score': r2,
                    'mae': mae,
                    'rmse': rmse
                }
        
        self.prediction_results['linear_regression'] = {
            'forecasts': forecasts,
            'performance': model_performance
        }
    
    def polynomial_regression_forecast(self):
        """다항식 회귀를 이용한 예측"""
        yearly_data_sorted = self.yearly_data.sort_values('년도')
        
        forecasts = {}
        model_performance = {}
        
        for column in ['원자력', '수력', '양수', '신재생', '합계']:
            if column in yearly_data_sorted.columns:
                # 데이터 준비
                X = yearly_data_sorted['년도'].values.reshape(-1, 1)
                y = yearly_data_sorted[column].values
                
                # 2차 다항식 특성 생성
                poly_features = PolynomialFeatures(degree=2)
                X_poly = poly_features.fit_transform(X)
                
                # 모델 훈련
                model = LinearRegression()
                model.fit(X_poly, y)
                
                # 예측
                future_years = np.arange(yearly_data_sorted['년도'].max() + 1, 
                                       yearly_data_sorted['년도'].max() + 1 + self.forecast_years)
                future_X = future_years.reshape(-1, 1)
                future_X_poly = poly_features.transform(future_X)
                predictions = model.predict(future_X_poly)
                
                # 성능 평가
                y_pred = model.predict(X_poly)
                r2 = r2_score(y, y_pred)
                mae = mean_absolute_error(y, y_pred)
                rmse = np.sqrt(mean_squared_error(y, y_pred))
                
                forecasts[column] = {
                    'years': future_years,
                    'predictions': predictions
                }
                
                model_performance[column] = {
                    'r2_score': r2,
                    'mae': mae,
                    'rmse': rmse
                }
        
        self.prediction_results['polynomial_regression'] = {
            'forecasts': forecasts,
            'performance': model_performance
        }
    
    def exponential_smoothing_forecast(self):
        """지수 평활을 이용한 예측"""
        yearly_data_sorted = self.yearly_data.sort_values('년도')
        
        forecasts = {}
        
        for column in ['원자력', '수력', '양수', '신재생', '합계']:
            if column in yearly_data_sorted.columns:
                try:
                    # 데이터 준비
                    ts_data = yearly_data_sorted.set_index('년도')[column]
                    
                    # 지수 평활 모델 (Simple Exponential Smoothing)
                    model = ExponentialSmoothing(ts_data, trend='add', seasonal=None)
                    fitted_model = model.fit()
                    
                    # 예측
                    predictions = fitted_model.forecast(steps=self.forecast_years)
                    future_years = np.arange(yearly_data_sorted['년도'].max() + 1, 
                                           yearly_data_sorted['년도'].max() + 1 + self.forecast_years)
                    
                    forecasts[column] = {
                        'years': future_years,
                        'predictions': predictions.values
                    }
                    
                except Exception as e:
                    print(f"지수 평활 예측 실패 ({column}): {e}")
        
        self.prediction_results['exponential_smoothing'] = {
            'forecasts': forecasts
        }
    
    def seasonal_decomposition_analysis(self):
        """계절성 분해 분석"""
        if self.raw_data is not None and len(self.raw_data) >= 24:  # 최소 2년 데이터 필요
            try:
                # 날짜 컬럼 생성
                self.raw_data['date'] = pd.to_datetime(self.raw_data['년도'].astype(str) + '-' + 
                                                     self.raw_data['월'].astype(str) + '-01')
                
                # 월별 데이터로 시계열 생성
                ts_data = self.raw_data.set_index('date')['합계'].sort_index()
                
                # 계절성 분해 (12개월 주기)
                decomposition = seasonal_decompose(ts_data, model='additive', period=12)
                
                self.prediction_results['seasonal_decomposition'] = {
                    'trend': decomposition.trend,
                    'seasonal': decomposition.seasonal,
                    'residual': decomposition.resid,
                    'original': ts_data
                }
                
            except Exception as e:
                print(f"계절성 분해 분석 실패: {e}")
    
    def analyze_source_trends(self):
        """발전원별 성장 트렌드 분석"""
        yearly_data_sorted = self.yearly_data.sort_values('년도')
        
        trends = {}
        
        for column in ['원자력', '수력', '양수', '신재생']:
            if column in yearly_data_sorted.columns:
                # 연평균 성장률 계산 (CAGR)
                start_value = yearly_data_sorted[column].iloc[0]
                end_value = yearly_data_sorted[column].iloc[-1]
                years = len(yearly_data_sorted) - 1
                
                if start_value > 0:
                    cagr = ((end_value / start_value) ** (1/years) - 1) * 100
                else:
                    cagr = 0
                
                # 트렌드 분석 (상승/하락/안정)
                values = yearly_data_sorted[column].values
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    range(len(values)), values)
                
                if abs(slope) < std_err:
                    trend_direction = "안정"
                elif slope > 0:
                    trend_direction = "상승"
                else:
                    trend_direction = "하락"
                
                trends[column] = {
                    'cagr': cagr,
                    'trend_direction': trend_direction,
                    'slope': slope,
                    'correlation': r_value,
                    'p_value': p_value
                }
        
        self.prediction_results['source_trends'] = trends
    
    def create_visualizations(self):
        """시각화 차트 생성"""
        # 기존 차트 + 예측 차트
        fig, axes = plt.subplots(3, 2, figsize=(18, 15))
        
        # 1. 년도별 총 발전량 추세 + 예측
        if 'yearly_trends' in self.analysis_results:
            yearly_totals = self.analysis_results['yearly_trends']['total_by_year']
            axes[0, 0].plot(yearly_totals.index, yearly_totals.values, marker='o', linewidth=2, 
                           markersize=8, label='실제값', color='blue')
            
            # 선형 회귀 예측 추가
            if 'linear_regression' in self.prediction_results:
                lr_forecast = self.prediction_results['linear_regression']['forecasts'].get('합계')
                if lr_forecast:
                    axes[0, 0].plot(lr_forecast['years'], lr_forecast['predictions'], 
                                   marker='s', linewidth=2, markersize=6, label='선형 예측', 
                                   color='red', linestyle='--')
            
            # 다항식 회귀 예측 추가
            if 'polynomial_regression' in self.prediction_results:
                poly_forecast = self.prediction_results['polynomial_regression']['forecasts'].get('합계')
                if poly_forecast:
                    axes[0, 0].plot(poly_forecast['years'], poly_forecast['predictions'], 
                                   marker='^', linewidth=2, markersize=6, label='다항식 예측', 
                                   color='green', linestyle='--')
            
            axes[0, 0].set_title('Total Power Generation: Actual vs Forecast', fontsize=14)
            axes[0, 0].set_xlabel('Year')
            axes[0, 0].set_ylabel('Total Generation (GWh)')
            axes[0, 0].legend()
            axes[0, 0].grid(True, alpha=0.3)
        
        # 2. 발전원별 비중 (파이차트)
        if 'power_source_ratio' in self.analysis_results:
            ratios = self.analysis_results['power_source_ratio']['ratios']
            axes[0, 1].pie(ratios.values(), labels=ratios.keys(), autopct='%1.1f%%', startangle=90)
            axes[0, 1].set_title(f'Power Source Ratio ({self.analysis_results["power_source_ratio"]["year"]})', fontsize=14)
        
        # 3. 발전원별 년도별 추세 + 예측
        power_columns = ['원자력', '수력', '양수', '신재생']
        colors = ['red', 'blue', 'green', 'orange']
        
        for i, (col, color) in enumerate(zip(power_columns, colors)):
            if col in self.yearly_data.columns:
                # 실제 데이터
                axes[1, 0].plot(self.yearly_data['년도'], self.yearly_data[col], 
                               marker='o', label=f'{col} (실제)', linewidth=2, color=color)
                
                # 예측 데이터
                if 'linear_regression' in self.prediction_results:
                    lr_forecast = self.prediction_results['linear_regression']['forecasts'].get(col)
                    if lr_forecast:
                        axes[1, 0].plot(lr_forecast['years'], lr_forecast['predictions'], 
                                       marker='s', label=f'{col} (예측)', linewidth=2, 
                                       color=color, linestyle='--', alpha=0.7)
        
        axes[1, 0].set_title('Power Generation by Source: Actual vs Forecast', fontsize=14)
        axes[1, 0].set_xlabel('Year')
        axes[1, 0].set_ylabel('Generation (GWh)')
        axes[1, 0].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. 월별 평균 발전량
        if 'monthly_patterns' in self.analysis_results:
            monthly_avg = self.analysis_results['monthly_patterns']['monthly_average']
            axes[1, 1].bar(monthly_avg.index, monthly_avg.values, color='skyblue', alpha=0.7)
            axes[1, 1].set_title('Average Monthly Power Generation', fontsize=14)
            axes[1, 1].set_xlabel('Month')
            axes[1, 1].set_ylabel('Average Generation (GWh)')
            axes[1, 1].grid(True, alpha=0.3)
        
        # 5. 계절성 분해 결과
        if 'seasonal_decomposition' in self.prediction_results:
            decomp = self.prediction_results['seasonal_decomposition']
            if 'trend' in decomp:
                trend_data = decomp['trend'].dropna()
                axes[2, 0].plot(trend_data.index, trend_data.values, linewidth=2, color='purple')
                axes[2, 0].set_title('Long-term Trend (Seasonal Decomposition)', fontsize=14)
                axes[2, 0].set_xlabel('Date')
                axes[2, 0].set_ylabel('Trend Component')
                axes[2, 0].grid(True, alpha=0.3)
        
        # 6. 발전원별 성장률 비교
        if 'source_trends' in self.prediction_results:
            trends = self.prediction_results['source_trends']
            sources = list(trends.keys())
            cagrs = [trends[source]['cagr'] for source in sources]
            
            bars = axes[2, 1].bar(sources, cagrs, color=['red', 'blue', 'green', 'orange'], alpha=0.7)
            axes[2, 1].set_title('Compound Annual Growth Rate (CAGR) by Source', fontsize=14)
            axes[2, 1].set_xlabel('Power Source')
            axes[2, 1].set_ylabel('CAGR (%)')
            axes[2, 1].grid(True, alpha=0.3)
            
            # 값 표시
            for bar, cagr in zip(bars, cagrs):
                axes[2, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                               f'{cagr:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('power_analysis_charts_with_forecast.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_report(self):
        """보고서 생성"""
        report = []
        report.append("="*60)
        report.append("전력 발전량 분석 보고서")
        report.append("="*60)
        report.append(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # 1. 데이터 개요
        report.append("1. 데이터 개요")
        report.append("-" * 30)
        report.append(f"분석 기간: {self.yearly_data['년도'].min()}년 ~ {self.yearly_data['년도'].max()}년")
        report.append(f"원본 데이터 건수: {len(self.raw_data) if self.raw_data is not None else 'N/A'}")
        report.append(f"년도별 데이터 건수: {len(self.yearly_data)}")
        report.append("")
        
        # 2. 년도별 발전량 현황
        if 'yearly_trends' in self.analysis_results:
            trends = self.analysis_results['yearly_trends']
            report.append("2. 년도별 발전량 현황")
            report.append("-" * 30)
            report.append(f"최대 발전량: {trends['peak_year']}년 ({trends['peak_value']:,.0f} GWh)")
            report.append(f"최소 발전량: {trends['lowest_year']}년 ({trends['lowest_value']:,.0f} GWh)")
            report.append("")
            
            # 년도별 상세 현황
            report.append("년도별 발전량 상세:")
            for year, value in trends['total_by_year'].items():
                report.append(f"  {year}년: {value:,.0f} GWh")
            report.append("")
        
        # 3. 발전원별 비중 분석
        if 'power_source_ratio' in self.analysis_results:
            ratio_data = self.analysis_results['power_source_ratio']
            report.append("3. 발전원별 비중 분석")
            report.append("-" * 30)
            report.append(f"기준 연도: {ratio_data['year']}년")
            report.append("발전원별 비중:")
            for source, ratio in ratio_data['ratios'].items():
                abs_value = ratio_data['absolute_values'][source]
                report.append(f"  {source}: {ratio:.1f}% ({abs_value:,.0f} GWh)")
            report.append("")
        
        # 4. 월별 발전량 패턴
        if 'monthly_patterns' in self.analysis_results:
            monthly = self.analysis_results['monthly_patterns']
            report.append("4. 월별 발전량 패턴")
            report.append("-" * 30)
            report.append(f"최대 발전 월: {monthly['peak_month']}월 ({monthly['peak_value']:,.0f} GWh)")
            report.append(f"최소 발전 월: {monthly['lowest_month']}월 ({monthly['lowest_value']:,.0f} GWh)")
            report.append("")
        
        # 5. 성장률 분석
        if 'growth_rates' in self.analysis_results:
            report.append("5. 전년 대비 성장률 분석")
            report.append("-" * 30)
            growth_rates = self.analysis_results['growth_rates']
            
            # 최근 년도 성장률
            latest_year_idx = self.yearly_data['년도'].idxmax()
            report.append("최근 연도 전년 대비 성장률:")
            for source, rates in growth_rates.items():
                if not rates.empty:
                    latest_growth = rates.iloc[-1]
                    if not pd.isna(latest_growth):
                        report.append(f"  {source}: {latest_growth:+.1f}%")
            report.append("")
        
        # 6. 기간별 비교 분석
        if 'period_comparison' in self.analysis_results:
            comparison = self.analysis_results['period_comparison']
            report.append("6. 기간별 비교 분석")
            report.append("-" * 30)
            recent_years_str = ", ".join(map(str, comparison['recent_years']))
            previous_years_str = ", ".join(map(str, comparison['previous_years']))
            report.append(f"최근 3년 ({recent_years_str}) vs 이전 3년 ({previous_years_str})")
            report.append("")
            
            for col in ['원자력', '수력', '양수', '신재생', '합계']:
                if col in comparison['improvement']:
                    improvement = comparison['improvement'][col]
                    if not pd.isna(improvement):
                        report.append(f"  {col}: {improvement:+.1f}% 변화")
            report.append("")
        
        # 7. 예측 분석 결과
        if self.prediction_results:
            report.append("7. 예측 분석 결과")
            report.append("-" * 30)
            
            # 7.1 선형 회귀 예측
            if 'linear_regression' in self.prediction_results:
                lr_data = self.prediction_results['linear_regression']
                report.append("7.1 선형 회귀 예측")
                report.append("   " + "-" * 25)
                
                # 모델 성능
                report.append("   모델 성능 (R² 점수):")
                for source, perf in lr_data['performance'].items():
                    report.append(f"     {source}: {perf['r2_score']:.3f}")
                report.append("")
                
                # 예측 결과
                report.append("   향후 3년 예측:")
                for source, forecast in lr_data['forecasts'].items():
                    report.append(f"     {source}:")
                    for year, pred in zip(forecast['years'], forecast['predictions']):
                        report.append(f"       {year}년: {pred:,.0f} GWh")
                    
                    # 연평균 증가율
                    if len(forecast['predictions']) > 1:
                        annual_growth = ((forecast['predictions'][-1] / forecast['predictions'][0]) ** (1/len(forecast['predictions'])) - 1) * 100
                        report.append(f"       연평균 증가율: {annual_growth:+.1f}%")
                    report.append("")
            
            # 7.2 발전원별 성장 트렌드
            if 'source_trends' in self.prediction_results:
                trends = self.prediction_results['source_trends']
                report.append("7.2 발전원별 성장 트렌드 분석")
                report.append("   " + "-" * 25)
                
                for source, trend in trends.items():
                    report.append(f"   {source}:")
                    report.append(f"     연평균 성장률(CAGR): {trend['cagr']:+.1f}%")
                    report.append(f"     트렌드 방향: {trend['trend_direction']}")
                    report.append(f"     상관계수: {trend['correlation']:.3f}")
                    report.append("")
            
            # 7.3 계절성 분석
            if 'seasonal_decomposition' in self.prediction_results:
                report.append("7.3 계절성 분석")
                report.append("   " + "-" * 25)
                decomp = self.prediction_results['seasonal_decomposition']
                
                if 'seasonal' in decomp:
                    seasonal_data = decomp['seasonal'].dropna()
                    if len(seasonal_data) > 0:
                        max_month = seasonal_data.idxmax().month
                        min_month = seasonal_data.idxmin().month
                        seasonal_variation = seasonal_data.max() - seasonal_data.min()
                        
                        report.append(f"   최대 계절성 효과: {max_month}월")
                        report.append(f"   최소 계절성 효과: {min_month}월")
                        report.append(f"   계절적 변동폭: {seasonal_variation:,.0f} GWh")
                        report.append("")
        
        # 8. 주요 인사이트 및 결론
        report.append("8. 주요 인사이트 및 결론")
        report.append("-" * 30)
        
        # 자동 인사이트 생성
        insights = []
        
        if 'yearly_trends' in self.analysis_results:
            trends = self.analysis_results['yearly_trends']
            total_growth = ((trends['total_by_year'].iloc[-1] - trends['total_by_year'].iloc[0]) / 
                          trends['total_by_year'].iloc[0] * 100)
            insights.append(f"전체 기간 동안 총 발전량은 {total_growth:+.1f}% 변화했습니다.")
        
        if 'power_source_ratio' in self.analysis_results:
            ratio_data = self.analysis_results['power_source_ratio']
            dominant_source = max(ratio_data['ratios'].items(), key=lambda x: x[1])
            insights.append(f"{dominant_source[0]}이 전체 발전량의 {dominant_source[1]:.1f}%를 차지하여 가장 큰 비중을 보입니다.")
        
        if 'monthly_patterns' in self.analysis_results:
            monthly = self.analysis_results['monthly_patterns']
            seasonal_diff = ((monthly['peak_value'] - monthly['lowest_value']) / 
                           monthly['lowest_value'] * 100)
            insights.append(f"월별 발전량 변동성은 {seasonal_diff:.1f}%로, 계절적 패턴을 보입니다.")
        
        for insight in insights:
            report.append(f"• {insight}")
        
        report.append("")
        report.append("="*60)
        
        # 보고서 파일 저장
        report_text = "\n".join(report)
        with open('power_analysis_report.txt', 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        # 콘솔 출력
        print(report_text)
        
        return report_text
    
    def run_analysis(self):
        """전체 분석 프로세스 실행"""
        print("전력 발전량 분석을 시작합니다...")
        
        # 1. 데이터 로드
        if not self.load_data():
            return False
        
        # 2. 데이터 분석
        print("데이터 분석 중...")
        self.analyze_data()
        
        # 3. 시각화 생성
        print("차트 생성 중...")
        self.create_visualizations()
        
        # 4. 보고서 생성
        print("보고서 생성 중...")
        self.generate_report()
        
        print("분석 완료!")
        print("생성된 파일:")
        print("- power_analysis_report_with_forecast.txt (예측 포함 텍스트 보고서)")
        print("- power_analysis_charts_with_forecast.png (예측 포함 차트 이미지)")
        
        return True

# 사용 예제
if __name__ == "__main__":
    # 엑셀 파일 경로 설정
    excel_file_path = "전력판매량_분석_대시보드.xlsx"  # 실제 파일 경로로 변경해주세요
    
    # 분석 객체 생성 및 실행
    analyzer = PowerAnalysisReport(excel_file_path)
    
    # 예측 기간 설정 (기본값: 3년)
    analyzer.forecast_years = 3
    
    analyzer.run_analysis()
    
    print("\n=== 추가 기능 사용법 ===")
    print("1. 예측 기간 변경: analyzer.forecast_years = 5")
    print("2. 개별 예측 결과 확인:")
    print("   - analyzer.prediction_results['linear_regression']")
    print("   - analyzer.prediction_results['source_trends']")
    print("3. 모델 성능 확인:")
    print("   - analyzer.prediction_results['linear_regression']['performance']")