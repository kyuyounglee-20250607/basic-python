def ask_question(question, option1, option2):
    while True:
        print(f"\n{question}")
        print(f"1. {option1}")
        print(f"2. {option2}")
        answer = input("번호를 입력하세요 (1 또는 2): ")
        if answer in ['1', '2']:
            return int(answer)
        else:
            print("잘못된 입력입니다. 1 또는 2를 입력해주세요.")


def get_mbti():
    print("안녕하세요! MBTI 성격유형 검사를 시작합니다.\n질문에 솔직하게 대답해주세요!")

    # 각 항목 점수
    score = {
        "E": 0, "I": 0,
        "S": 0, "N": 0,
        "T": 0, "F": 0,
        "J": 0, "P": 0
    }

    # 질문 리스트
    questions = [
        # E / I
        ("사람들과 함께 있을 때 에너지가 생기나요?", "그렇다 (E)", "혼자가 더 편하다 (I)", "E", "I"),
        ("모임이 끝난 후 기분은?", "흥겹고 에너지가 남는다 (E)", "지치고 조용히 있고 싶다 (I)", "E", "I"),

        # S / N
        ("사실적인 정보를 좋아하나요?", "네, 구체적인 것이 좋다 (S)", "아니요, 직감이나 가능성이 좋다 (N)", "S", "N"),
        ("새로운 아이디어를 생각하는 걸 좋아하나요?", "아니요, 현실적인 게 좋다 (S)", "네, 상상하는 게 즐겁다 (N)", "S", "N"),

        # T / F
        ("의사결정 시 어떤 기준을 더 중시하나요?", "논리와 객관적인 사실 (T)", "감정과 사람 관계 (F)", "T", "F"),
        ("갈등 상황에서?", "사실에 기반해 해결 (T)", "감정을 고려해 해결 (F)", "T", "F"),

        # J / P
        ("일정을 세우는 걸 좋아하나요?", "네, 계획적으로 움직인다 (J)", "아니요, 즉흥적인 편이다 (P)", "J", "P"),
        ("일이 생기면?", "계획을 세우고 실행 (J)", "유연하게 대처 (P)", "J", "P")
    ]

    # 질문 루프
    for q_text, opt1, opt2, type1, type2 in questions:
        answer = ask_question(q_text, opt1, opt2)
        if answer == 1:
            score[type1] += 1
        else:
            score[type2] += 1

    # 결과 계산
    result = ""
    result += "E" if score["E"] >= score["I"] else "I"
    result += "S" if score["S"] >= score["N"] else "N"
    result += "T" if score["T"] >= score["F"] else "F"
    result += "J" if score["J"] >= score["P"] else "P"

    print("\n🎉 검사 결과:")
    print(f"당신의 MBTI 유형은: {result} 입니다!")


# 프로그램 실행
if __name__ == "__main__":
    get_mbti()
