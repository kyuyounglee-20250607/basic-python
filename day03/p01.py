import random

secret_number = random.randint(1, 100)
attempts = 0

print("숫자 맞추기 게임을 시작합니다!")
print("게임을 종료하려면 'q' 또는 'quit'을 입력하세요.")

while True:
    try:
        user_input = input("1부터 100 사이의 숫자를 입력하세요: ").strip().lower()

        if user_input in ['q', 'quit']:
            print("게임을 종료합니다.")
            break

        guess = int(user_input)
        attempts += 1
        diff = guess - secret_number

        if diff == 0:
            print(f"정답입니다! {attempts}번 만에 맞췄어요.")
            break
        elif diff < -19:
            print("너무 작다.")
        elif diff < 0:
            print("작다.")
        elif diff > 19:
            print("너무 크다.")
        else:
            print("크다.")
    except ValueError:
        print("숫자를 입력하거나 종료하려면 'q'를 입력하세요.")
