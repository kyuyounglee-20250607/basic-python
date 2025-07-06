# 🧠 MBTI 성격유형 검사 프로그램

이 프로젝트는 MBTI 성격유형 검사를 단계별로 구현한 프로그램입니다. 1단계에서는 콘솔 기반으로 시작하여, 2단계에서는 Flask 웹 애플리케이션으로 확장됩니다.

## 📋 목차

- [프로젝트 개요](#프로젝트-개요)
- [1단계: 콘솔 기반 MBTI 검사](#1단계-콘솔-기반-mbti-검사)
- [2단계: Flask 웹 애플리케이션](#2단계-flask-웹-애플리케이션)
- [설치 및 실행](#설치-및-실행)
- [기술 스택](#기술-스택)
- [프로젝트 구조](#프로젝트-구조)

## 🎯 프로젝트 개요

이 프로젝트는 MBTI 성격유형 검사를 단계적으로 구현한 프로그램입니다:

- **1단계**: 콘솔 기반의 간단한 MBTI 검사 프로그램
- **2단계**: Flask를 사용한 웹 기반 MBTI 검사 애플리케이션

각 단계는 동일한 MBTI 계산 로직을 공유하지만, 사용자 인터페이스와 상호작용 방식이 다릅니다.

## ✅ 1단계: 콘솔 기반 MBTI 검사

### 📁 파일 구성
```
step1_mbti/
├── mbti.csv          # MBTI 질문 데이터
└── mbti_console.py   # 콘솔 기반 메인 프로그램
```

### 🔧 주요 기능

- **질문 로딩**: CSV 파일에서 MBTI 질문 데이터를 불러옴
- **대화형 검사**: 사용자와 1:1 대화형으로 질문 진행
- **점수 계산**: 각 MBTI 지표별 점수 집계
- **결과 출력**: 최종 MBTI 유형 표시

### 💻 핵심 코드

```python
def run_mbti_console():
    questions = load_mbti_questions()
    scores = {'E':0, 'I':0, 'S':0, 'N':0, 'T':0, 'F':0, 'J':0, 'P':0}
    
    for idx, q in enumerate(questions):
        print(f"{idx + 1}. {q['question']}")
        answer = input("1) 동의  2) 비동의  ▶ ")
        # 점수 계산 로직...
    
    mbti = (
        'E' if scores['E'] >= scores['I'] else 'I' +
        'S' if scores['S'] >= scores['N'] else 'N' +
        'T' if scores['T'] >= scores['F'] else 'F' +
        'J' if scores['J'] >= scores['P'] else 'P'
    )
```

### 🚀 실행 방법

```bash
cd step1_mbti
python mbti_console.py
```

## ✅ 2단계: Flask 웹 애플리케이션

### 📁 파일 구성
```
step2_flask_mbti/
├── mbti.csv              # MBTI 질문 데이터
├── app.py                # Flask 메인 애플리케이션
└── templates/
    ├── index.html        # 검사 페이지
    └── result.html       # 결과 페이지
```

### 🔧 주요 기능

- **웹 인터페이스**: 브라우저를 통한 직관적인 UI
- **폼 기반 검사**: 라디오 버튼을 통한 쉬운 답변 선택
- **실시간 결과**: 검사 완료 후 즉시 결과 표시
- **재검사 기능**: 결과 페이지에서 다시 검사 가능

### 💻 핵심 코드

```python
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        scores = {k: 0 for k in 'EISNTFJP'}
        for idx, q in enumerate(questions):
            answer = request.form.get(f'q{idx}')
            selected = q['direction'] if answer == 'agree' else get_opposite(q['direction'])
            scores[selected] += 1
        
        result = ''
        result += 'E' if scores['E'] >= scores['I'] else 'I'
        result += 'S' if scores['S'] >= scores['N'] else 'N'
        result += 'T' if scores['T'] >= scores['F'] else 'F'
        result += 'J' if scores['J'] >= scores['P'] else 'P'
        
        return render_template("result.html", mbti=result)
    return render_template("index.html", questions=questions)
```

### 🚀 실행 방법

```bash
cd step2_flask_mbti
pip install flask pandas
python app.py
```

웹 브라우저에서 `http://localhost:5000` 접속

## 📦 설치 및 실행

### 필수 요구사항

- Python 3.6 이상
- pandas (데이터 처리용)
- Flask (2단계 웹 애플리케이션용)

### 설치 방법

```bash
# 1단계 실행을 위한 설치
pip install pandas

# 2단계 실행을 위한 설치
pip install flask pandas
```

### 실행 순서

1. **1단계 실행**
   ```bash
   cd step1_mbti
   python mbti_console.py
   ```

2. **2단계 실행**
   ```bash
   cd step2_flask_mbti
   python app.py
   # 브라우저에서 http://localhost:5000 접속
   ```

## 🛠 기술 스택

### 1단계
- **Python**: 메인 프로그래밍 언어
- **pandas**: CSV 데이터 처리
- **표준 라이브러리**: 파일 I/O, 사용자 입력 처리

### 2단계
- **Python**: 메인 프로그래밍 언어
- **Flask**: 웹 프레임워크
- **pandas**: CSV 데이터 처리
- **HTML**: 웹 페이지 템플릿
- **Jinja2**: 템플릿 엔진

## 📂 프로젝트 구조

```
mbti/
├── README.md
├── step1_mbti/
│   ├── mbti.csv
│   └── mbti_console.py
└── step2_flask_mbti/
    ├── mbti.csv
    ├── app.py
    └── templates/
        ├── index.html
        └── result.html
```

## 🔄 공통 기능

두 단계 모두에서 공유되는 핵심 기능들:

- **`load_mbti_questions()`**: CSV 파일에서 질문 데이터 로딩
- **`get_opposite()`**: MBTI 지표의 반대값 반환
- **MBTI 계산 로직**: E/I, S/N, T/F, J/P 지표별 점수 비교

## 🎨 특징

- **단계적 구현**: 콘솔 → 웹으로의 자연스러운 확장
- **코드 재사용**: 핵심 로직의 효율적인 공유
- **사용자 친화적**: 직관적인 인터페이스 제공
- **확장 가능**: 추가 기능 구현이 용이한 구조

## 📝 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

---

**개발자**: MBTI 검사 프로그램 개발팀  
**버전**: 1.0  
**최종 업데이트**: 2024년 