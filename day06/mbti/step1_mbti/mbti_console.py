import pandas as pd

def load_mbti_questions(filepath='mbti.csv'):
    """
    CSV 파일에서 MBTI 질문 데이터를 불러오는 함수
    
    Args:
        filepath (str): CSV 파일 경로
        
    Returns:
        list: 질문 데이터 리스트
    """
    try:
        df = pd.read_csv(filepath)
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"[오류] 파일을 불러올 수 없습니다: {e}")
        return []

def get_opposite(letter):
    """
    MBTI 지표의 반대값을 반환하는 함수
    
    Args:
        letter (str): MBTI 지표 (E, I, S, N, T, F, J, P)
        
    Returns:
        str: 반대 지표
    """
    opposites = {
        'E': 'I', 'I': 'E',
        'S': 'N', 'N': 'S', 
        'T': 'F', 'F': 'T',
        'J': 'P', 'P': 'J'
    }
    return opposites.get(letter, letter)

def run_mbti_console():
    """
    콘솔 기반 MBTI 검사를 실행하는 메인 함수
    """
    print("=" * 50)
    print("🧠 MBTI 성격유형 검사 시작!")
    print("=" * 50)
    
    # 질문 데이터 로딩
    questions = load_mbti_questions()
    if not questions:
        print("❌ 질문 데이터를 불러올 수 없습니다. 프로그램을 종료합니다.")
        return
    
    print(f"📝 총 {len(questions)}개의 질문이 준비되었습니다.\n")
    
    # MBTI 점수 초기화
    scores = {
        'E': 0, 'I': 0,  # 외향성 vs 내향성
        'S': 0, 'N': 0,  # 감각 vs 직관
        'T': 0, 'F': 0,  # 사고 vs 감정
        'J': 0, 'P': 0   # 판단 vs 인식
    }
    
    # 질문 진행
    for idx, question in enumerate(questions, 1):
        print(f"\n[{idx}/{len(questions)}] {question['question']}")
        print("-" * 40)
        
        while True:
            try:
                answer = input("1) 동의  2) 비동의  ▶ ")
                
                if answer not in ['1', '2']:
                    print("⚠️  1 또는 2만 입력하세요.")
                    continue
                
                # 점수 계산
                if answer == '1':  # 동의
                    selected = question['direction']
                else:  # 비동의
                    selected = get_opposite(question['direction'])
                
                scores[selected] += 1
                break
                
            except KeyboardInterrupt:
                print("\n\n❌ 검사가 중단되었습니다.")
                return
            except Exception as e:
                print(f"⚠️  오류가 발생했습니다: {e}")
                continue
    
    # MBTI 결과 계산
    print("\n" + "=" * 50)
    print("🎯 검사 완료! 결과를 계산 중...")
    print("=" * 50)
    
    mbti_result = ""
    
    # E vs I
    if scores['E'] >= scores['I']:
        mbti_result += 'E'
        print(f"외향성(E): {scores['E']} vs 내향성(I): {scores['I']} → E 선택")
    else:
        mbti_result += 'I'
        print(f"외향성(E): {scores['E']} vs 내향성(I): {scores['I']} → I 선택")
    
    # S vs N
    if scores['S'] >= scores['N']:
        mbti_result += 'S'
        print(f"감각(S): {scores['S']} vs 직관(N): {scores['N']} → S 선택")
    else:
        mbti_result += 'N'
        print(f"감각(S): {scores['S']} vs 직관(N): {scores['N']} → N 선택")
    
    # T vs F
    if scores['T'] >= scores['F']:
        mbti_result += 'T'
        print(f"사고(T): {scores['T']} vs 감정(F): {scores['F']} → T 선택")
    else:
        mbti_result += 'F'
        print(f"사고(T): {scores['T']} vs 감정(F): {scores['F']} → F 선택")
    
    # J vs P
    if scores['J'] >= scores['P']:
        mbti_result += 'J'
        print(f"판단(J): {scores['J']} vs 인식(P): {scores['P']} → J 선택")
    else:
        mbti_result += 'P'
        print(f"판단(J): {scores['J']} vs 인식(P): {scores['P']} → P 선택")
    
    # 최종 결과 출력
    print("\n" + "🎉" * 20)
    print(f"🎉 당신의 MBTI는 ➤ {mbti_result} 🎉")
    print("🎉" * 20)
    
    # MBTI 유형별 설명
    mbti_descriptions = {
        'ISTJ': '청렴결백한 논리주의자',
        'ISFJ': '용감한 수호자',
        'INFJ': '통찰력 있는 선지자',
        'INTJ': '전략적인 설계자',
        'ISTP': '만능 재주꾼',
        'ISFP': '모험을 즐기는 예술가',
        'INFP': '열정적인 중재자',
        'INTP': '논리적인 사색가',
        'ESTP': '모험을 즐기는 사업가',
        'ESFP': '자유로운 영혼의 연예인',
        'ENFP': '재기발랄한 활동가',
        'ENTP': '논쟁을 즐기는 변론가',
        'ESTJ': '엄격한 관리자',
        'ESFJ': '사교적인 외교관',
        'ENFJ': '정의로운 사회운동가',
        'ENTJ': '대담한 통솔자'
    }
    
    description = mbti_descriptions.get(mbti_result, "특별한 성격유형")
    print(f"📖 {mbti_result} - {description}")
    
    print("\n" + "=" * 50)
    print("✨ MBTI 검사가 완료되었습니다! ✨")
    print("=" * 50)

def main():
    """
    프로그램 시작점
    """
    try:
        run_mbti_console()
    except KeyboardInterrupt:
        print("\n\n👋 프로그램을 종료합니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}")

if __name__ == '__main__':
    main() 