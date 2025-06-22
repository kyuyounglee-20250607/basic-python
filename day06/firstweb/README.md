# Flask 웹 애플리케이션

이 프로젝트는 Flask를 사용한 기본적인 웹 애플리케이션입니다.

## 📁 프로젝트 구조

```
firstweb/
├── app.py              # 메인 Flask 애플리케이션 파일
├── templates/          # HTML 템플릿 디렉토리
│   └── hello.html     # 동적 HTML 템플릿
└── README.md          # 프로젝트 설명서
```

## 🚀 설치 및 실행

### 1. Flask 설치
```bash
pip install flask
```

### 2. 애플리케이션 실행
```bash
python app.py
```

### 3. 브라우저에서 접속
- 메인 페이지: http://localhost:5000
- 소개 페이지: http://localhost:5000/about
- 동적 페이지: http://localhost:5000/hello/[이름]

## 📋 코드 구조 설명

### app.py - 메인 애플리케이션 파일

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return '''<h1>안녕하세요!</h1> 
    <p><h2>Flask 웹사이트입니다.</h2></p>'''

@app.route('/about')
def about():
    return "이 페이지는 소개 페이지입니다."

@app.route('/hello/<name>')
def hello_name(name):
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
```

#### 주요 구성 요소:

1. **Flask 인스턴스 생성**: `app = Flask(__name__)`
2. **라우트 정의**: `@app.route()` 데코레이터를 사용하여 URL 경로 정의
3. **뷰 함수**: 각 라우트에 대응하는 함수 정의
4. **템플릿 렌더링**: `render_template()` 함수로 HTML 템플릿 렌더링
5. **개발 서버 실행**: `app.run(debug=True)`로 디버그 모드 실행

### templates/hello.html - HTML 템플릿

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>인사</title>
</head>
<body>
     <h1>안녕하세요, {{ name }}!</h1>
</body>
</html>
```

#### 템플릿 특징:
- **Jinja2 템플릿 엔진** 사용
- **동적 변수**: `{{ name }}`으로 Python에서 전달된 변수 표시
- **HTML 구조**: 표준 HTML5 문서 구조

## 🔧 라우트 설명

### 1. 메인 페이지 (`/`)
- **함수**: `hello()`
- **기능**: 간단한 HTML 문자열 반환
- **접속**: http://localhost:5000

### 2. 소개 페이지 (`/about`)
- **함수**: `about()`
- **기능**: 텍스트 문자열 반환
- **접속**: http://localhost:5000/about

### 3. 동적 페이지 (`/hello/<name>`)
- **함수**: `hello_name(name)`
- **기능**: URL 파라미터를 받아 HTML 템플릿에 전달
- **접속**: http://localhost:5000/hello/[이름]
- **예시**: http://localhost:5000/hello/홍길동

## 🛠️ Flask 주요 개념

### 1. 라우팅 (Routing)
- `@app.route()` 데코레이터로 URL 경로 정의
- URL 파라미터는 `<변수명>` 형태로 정의

### 2. 뷰 함수 (View Functions)
- 각 라우트에 대응하는 Python 함수
- HTML 문자열, 템플릿, JSON 등 다양한 형태로 응답 가능

### 3. 템플릿 (Templates)
- `templates/` 디렉토리에 HTML 파일 저장
- Jinja2 템플릿 엔진으로 동적 콘텐츠 생성
- `{{ 변수명 }}`으로 Python 변수 표시

### 4. 디버그 모드
- `debug=True`로 설정 시 코드 변경 시 자동 재시작
- 개발 환경에서만 사용 권장

## 📝 확장 가능한 기능

1. **정적 파일**: CSS, JavaScript, 이미지 파일 추가
2. **데이터베이스**: SQLAlchemy를 사용한 데이터 저장
3. **폼 처리**: Flask-WTF를 사용한 폼 검증
4. **사용자 인증**: Flask-Login을 사용한 로그인 시스템
5. **API 개발**: JSON 응답을 위한 RESTful API

## 🔍 문제 해결

### 일반적인 오류:
1. **포트 충돌**: 다른 포트 사용 (`app.run(port=5001)`)
2. **템플릿 오류**: `templates/` 디렉토리 확인
3. **모듈 오류**: Flask 설치 확인 (`pip list | grep Flask`)

## 📚 참고 자료

- [Flask 공식 문서](https://flask.palletsprojects.com/)
- [Jinja2 템플릿 엔진](https://jinja.palletsprojects.com/)
- [Flask 튜토리얼](https://flask.palletsprojects.com/en/2.3.x/quickstart/) 