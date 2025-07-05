# 인덱싱 & 슬라이싱
# 임의의 2차원 데이터를 생성(3,20)
import random
import numpy as np
random.seed(42)
data = np.array(random.sample(range(100),3*24)) \
                .reshape(3,24)
print('전체',data) # 전체 출력
# 1번째  row 데이터
print('첫번째',data[0])
# 첫번재 데이터를 강남역이라고 하고 매시간마다 하차인원이라고
# 가정하면  강남역의 7시부터 10시까지의 하차인원 추출
print(type(data[0]))
print(f'강남역 7-10 : {data[0,7:11]}')
# 강남역 하차인원 50명 이상인 시간대의 데이터
print(data[0][ data[0] > 50 ])

# 강남역 하차인원 50명 이상인 시간대
indexs = np.where(data[0] > 50)
print(f'index : {indexs}')
# 해당 시간대의 하차인원
print(f'index data : {data[0][indexs]}')