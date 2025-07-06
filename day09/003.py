import pandas as pd
import numpy as np
# csv 데이터 가져오기
url = 'https://raw.githubusercontent.com/kyuyounglee-20250607/basic-python/refs/heads/main/day09/CARD_SUBWAY_MONTH_202505.csv'
cols = pd.read_csv(url).columns.to_list()
cols.append('na')
subway = pd.read_csv(url,names=cols,header=0)
subway = subway.dropna(axis=1)
# print(subway)
# 노선명만 출력해보기
print(set(subway['노선명'].values))
# 노선명중에 '강남'이포함된 노선명만 출력
# '2호선'이 포함된 노선명만 추출
line2_name = {notion for notion in set(subway['노선명'].values) if '2호선' in notion}
print("\n'2호선'이 포함된 노선명:")
print(line2_name)
# 2호선중에 강남이 포함된 역명을 찾기
line2 = subway[subway['노선명'].str.contains('2호선')]
print([name for name in set(line2['역명'].to_numpy()) if '강남' in name])

# 강남역의 승차하 인원
print('*' * 100)
df = subway[subway['역명'] == '강남']
print(df)
# 요일별 강남역 승하차 인원에 대해 날자별 시각화
print('*' * 100)
# 날짜를 datetime 형식으로 변환
df['사용일자'] = pd.to_datetime(df['사용일자'], format='%Y%m%d')
# 요일 컬럼 추가 (0=월요일, 6=일요일)
df['요일'] = df['사용일자'].dt.day_name(locale='ko_KR')
print(df)
# 시각화
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(df['사용일자'], df['승차총승객수'], marker='o', label='승차 총승객수')
plt.plot(df['사용일자'], df['하차총승객수'], marker='s', label='하차 총승객수')
plt.show()