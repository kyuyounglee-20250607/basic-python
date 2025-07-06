def get_exchange_rate(rate):
    """
    사용자로부터 환율 정보를 입력받는다.
    예: 1 USD = 1300 KRW 라면, 환율은 1300
    """
    try:        
        if rate <= 0:
            raise ValueError
        return rate
    except ValueError:
        print("유효한 양수의 숫자를 입력해주세요.")
        return get_exchange_rate()

def convert_currency(amount, rate):
    """
    주어진 금액과 환율로 변환 금액 계산
    """
    return amount * rate

def main():
    print("💱 간단한 환율 변환기")
    base_currency =  1
    target_currency =  0.00073

    try:
        amount = float(input(f"변환할 {base_currency} 금액을 입력하세요: "))
        if amount < 0:
            raise ValueError
    except ValueError:
        print("유효한 금액을 입력해야 합니다. 프로그램을 종료합니다.")
        return

    rate = get_exchange_rate( target_currency )
    converted = convert_currency(amount, rate)

    print(f"\n💹 결과: {amount:.2f} {base_currency} → {converted:.2f} {target_currency} (환율: {rate})")

if __name__ == "__main__":
    main()



# 주제 : 환율 변환기
# 필요한 기술: 환율 단위, 
# 기능 : 
# 1. 환율 변환(ex 1 usd = 1300 krw)  1000 usd = 1300000 krw
# 2. 환율(고정값)
# 3. 환전기능   : 사용자(외부)로부터   입력받는다

# RATE = 1325.0

# def check_mony(money):
#     try:
#         money = int(input("환전할 금액을 입력하세요: "))        
#         if money < 0:
#             raise ValueError("금액은 0 이상이어야 합니다.")
#         return money
#     except Exception as e:
#         print(f"입력 오류: {e}")
#         return check_mony(money)
        

# converted_money = check_mony() * RATE
# print(f"환전된 금액은 {converted_money} 원입니다.")