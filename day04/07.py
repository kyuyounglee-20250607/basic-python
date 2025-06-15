def get_exchange_rate():
    """
    사용자로부터 환율 정보를 입력받는다.
    예: 1 USD = 1300 KRW 라면, 환율은 1300
    """
    try:
        rate = float(input("1 단위의 기준 통화(예: USD)는 몇 단위의 대상 통화(예: KRW)와 같습니까? (예: 1300): "))
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
    target_currency =  1368.75

    try:
        amount = float(input(f"변환할 {base_currency} 금액을 입력하세요: "))
        if amount < 0:
            raise ValueError
    except ValueError:
        print("유효한 금액을 입력해야 합니다. 프로그램을 종료합니다.")
        return

    rate = get_exchange_rate()
    converted = convert_currency(amount, rate)

    print(f"\n💹 결과: {amount:.2f} {base_currency} → {converted:.2f} {target_currency} (환율: {rate})")

if __name__ == "__main__":
    main()

