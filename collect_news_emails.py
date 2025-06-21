# Selenium을 사용하여 동적으로 렌더링된 다음 메인페이지에서 기사 목록의 뉴스 링크를 수집하고, 각 뉴스에서 이메일을 추출하는 프로그램
# 필요한 패키지: selenium, beautifulsoup4, re
# 크롬 드라이버(chromedriver.exe)가 필요하며, 파이썬 파일과 같은 폴더에 두세요.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time

# 크롬 드라이버 옵션 설정 (브라우저 창을 띄우지 않으려면 headless 사용)
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# 크롬 드라이버 실행
browser = webdriver.Chrome(options=chrome_options)

# 메인페이지 접속
main_url = 'https://www.daum.net/?t__nil_top=refresh'
browser.get(main_url)
time.sleep(2)  # 페이지 로딩 대기

# 렌더링된 페이지 소스 가져오기
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

# 기사 목록(이미지 옆 기사목록)에서 뉴스 링크 추출
news_links = []
news_list = soup.find('ul', class_='list_txt')
if news_list:
    for a in news_list.find_all('a', class_='link_item', href=True):
        link = a['href']
        if link.startswith('http'):
            news_links.append(link)
else:
    print('기사 목록을 찾을 수 없습니다.')

# 이메일 패턴 정규식
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# 각 뉴스에서 이메일 추출
all_emails = set()
for url in news_links:
    try:
        browser.get(url)
        time.sleep(1)  # 뉴스 페이지 로딩 대기
        news_html = browser.page_source
        news_soup = BeautifulSoup(news_html, 'html.parser')
        emails = re.findall(email_pattern, news_soup.get_text())
        all_emails.update(emails)
    except Exception as e:
        print(f'뉴스 페이지 접근 오류: {url} - {e}')

browser.quit()

# 결과 출력
if all_emails:
    print('수집된 이메일 목록:')
    for email in all_emails:
        print(email)
else:
    print('이메일 주소를 찾을 수 없습니다.')
