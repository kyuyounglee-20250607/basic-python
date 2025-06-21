# 이메일 주소를 수집하는 간단한 파이썬 프로그램
# requests와 BeautifulSoup를 사용하여 웹사이트에서 이메일을 추출합니다.

import requests
from bs4 import BeautifulSoup
import re

# 크롤링할 웹사이트 URL
url = 'https://v.daum.net/v/20250621114326796'

# 웹페이지 요청 및 파싱
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 이메일 패턴 정규식
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# 페이지 내 모든 텍스트에서 이메일 추출
emails = re.findall(email_pattern, soup.get_text())

# 중복 제거
emails = list(set(emails))

# 결과 출력
if emails:
    print('수집된 이메일 목록:')
    for email in emails:
        print(email)
else:
    print('이메일 주소를 찾을 수 없습니다.')
