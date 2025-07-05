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
line2 = {notion for notion in set(subway['노선명'].values) if '2호선' in notion}
print("\n'2호선'이 포함된 노선명:")
print(line2)
# # 강남노션에 대한 역명들을 출력
# # '강남'이 포함된 노선명에 해당하는 역명만 출력
# filtered_stations = subway[subway['노선명'].str.contains('강남')]['역명']
# print(subway[subway['노선명'].str.contains('강남')])