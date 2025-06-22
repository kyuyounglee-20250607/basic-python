from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

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

def calculate_mbti(scores):
    """
    점수를 바탕으로 MBTI 결과를 계산하는 함수
    
    Args:
        scores (dict): 각 MBTI 지표별 점수
        
    Returns:
        str: MBTI 결과 (예: 'INTJ')
    """
    result = ""
    
    # E vs I
    result += 'E' if scores['E'] >= scores['I'] else 'I'
    
    # S vs N
    result += 'S' if scores['S'] >= scores['N'] else 'N'
    
    # T vs F
    result += 'T' if scores['T'] >= scores['F'] else 'F'
    
    # J vs P
    result += 'J' if scores['J'] >= scores['P'] else 'P'
    
    return result

def get_mbti_description(mbti_type):
    """
    MBTI 유형에 따른 설명을 반환하는 함수
    
    Args:
        mbti_type (str): MBTI 유형
        
    Returns:
        str: MBTI 설명
    """
    descriptions = {
        'ISTJ': '청렴결백한 논리주의자 - 책임감이 강하고 체계적인 성격',
        'ISFJ': '용감한 수호자 - 따뜻하고 헌신적인 성격',
        'INFJ': '통찰력 있는 선지자 - 이상주의적이고 창의적인 성격',
        'INTJ': '전략적인 설계자 - 독창적이고 전략적인 사고를 가진 성격',
        'ISTP': '만능 재주꾼 - 실용적이고 유연한 성격',
        'ISFP': '모험을 즐기는 예술가 - 예술적이고 자유로운 성격',
        'INFP': '열정적인 중재자 - 이상주의적이고 공감능력이 뛰어난 성격',
        'INTP': '논리적인 사색가 - 분석적이고 창의적인 성격',
        'ESTP': '모험을 즐기는 사업가 - 활동적이고 실용적인 성격',
        'ESFP': '자유로운 영혼의 연예인 - 사교적이고 낙관적인 성격',
        'ENFP': '재기발랄한 활동가 - 열정적이고 창의적인 성격',
        'ENTP': '논쟁을 즐기는 변론가 - 독창적이고 분석적인 성격',
        'ESTJ': '엄격한 관리자 - 체계적이고 책임감이 강한 성격',
        'ESFJ': '사교적인 외교관 - 따뜻하고 협력적인 성격',
        'ENFJ': '정의로운 사회운동가 - 카리스마 있고 이타적인 성격',
        'ENTJ': '대담한 통솔자 - 리더십이 강하고 전략적인 성격'
    }
    return descriptions.get(mbti_type, "특별한 성격유형입니다.")

# 질문 데이터 로딩
questions = load_mbti_questions()

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    메인 페이지 - MBTI 검사 폼
    """
    if request.method == 'POST':
        # 폼 데이터 처리
        scores = {
            'E': 0, 'I': 0,
            'S': 0, 'N': 0,
            'T': 0, 'F': 0,
            'J': 0, 'P': 0
        }
        
        # 각 질문에 대한 답변 처리
        for idx, question in enumerate(questions):
            answer = request.form.get(f'q{idx}')
            if answer:
                if answer == 'agree':
                    selected = question['direction']
                else:  # disagree
                    selected = get_opposite(question['direction'])
                scores[selected] += 1
        
        # MBTI 결과 계산
        mbti_result = calculate_mbti(scores)
        description = get_mbti_description(mbti_result)
        
        # 결과 페이지로 리다이렉트
        return render_template('result.html', 
                             mbti=mbti_result, 
                             description=description,
                             scores=scores)
    
    # GET 요청 시 검사 페이지 표시
    return render_template('index.html', questions=questions)

@app.route('/result')
def result():
    """
    결과 페이지 (직접 접근 시 메인으로 리다이렉트)
    """
    return redirect(url_for('index'))

@app.route('/about')
def about():
    """
    MBTI에 대한 정보 페이지
    """
    return render_template('about.html')

@app.errorhandler(404)
def not_found(error):
    """
    404 에러 처리
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """
    500 에러 처리
    """
    return render_template('500.html'), 500

if __name__ == '__main__':
    # 개발 서버 실행
    print("🚀 Flask MBTI 검사 애플리케이션을 시작합니다...")
    print("📝 총 질문 수:", len(questions))
    print("🌐 웹 브라우저에서 http://localhost:5000 으로 접속하세요!")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 