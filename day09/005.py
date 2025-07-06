# 리스트 컴프리 핸션
result = []
for i in range(5):
    result.append(i * 2)
print(result)  # [0, 2, 4, 6, 8]

result = [i * 2 for i in range(5)]
print(result)
print('*' * 100)
import random
print(random.randint(1,100))
print([random.randint(1,100) for _ in range(10)])

print([i*2 for i in [1,5,9]])

# 1과 100중에 3의 배수만 출력
print([i for i in range(1,101) if i%3==0   ])

# 1과 100중에 3의 배수면 값을 표시하고 그렇지 않으면 0으로 채운다
print([i if i%3==0 else 'none'    for i in range(1,101)])

# 두 개의 리스트 [1, 2, 3]과 [10, 20, 30]의 
# 곱셈 결과 리스트 만들기 (1*10, 2*20, 3*30)
print([a*b for a,b in zip( [1,2,3],[10,20,30] )])  # [10, 40, 90]
print(list(zip( [1,2,3],[10,20,30] )))  #[(1, 10), (2, 20), (3, 30)]