import numpy as np
# 통계 함수
# 삼성전자 주식가격 최근 20일
samsung_prices = [
    63300, 63800, 60800, 60200, 59800,
    60800, 60200, 61300, 60500, 58000,
    59500, 59200, 59800, 58100, 57200,
    58300, 59500, 59900, 59200, 59800
]
samsung_prices = np.array(samsung_prices)
# 평균가격
print(samsung_prices.mean())
# 표준편차
print(samsung_prices.std())
# 최고가
print(samsung_prices.max())
# 최저가
print(samsung_prices.min())
# 주가의 일간 변화량(오늘가격 - 어제가격)
daily_returns = (samsung_prices[:-1] - samsung_prices[1:])/samsung_prices[1:]*100
print(daily_returns)