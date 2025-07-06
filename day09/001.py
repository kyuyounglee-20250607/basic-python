import numpy as np
import matplotlib.pylab as plt
np.random.seed(42)
plt.style.use('seaborn-v0_8')

data = np.array([
    [1,1],
    [12,' '],
    [1,2]
]
)
# 배열정보
print(f'데이터 모양 : {data.shape}')
print(f'데이터 타입 : {data.dtype}')
print(f'데이터 개수 : {data.size}')