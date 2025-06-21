# 엑셀 파일을 읽어 각 이메일로 자동 발송하는 파이썬 코드
# 필요한 패키지: openpyxl, smtplib, email
# pip install openpyxl

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import openpyxl

# 엑셀 파일 경로
excel_path = 'customer.xlsx'  # 엑셀 파일명을 실제 파일명으로 변경하세요

# 구글 계정 정보
sender_email = '구글계정'
app_password = '구글앱비번'  # 구글의 2단계 인증을 사용하고 앱 비밀번호를 생성해야 합니다.

# 메일 제목과 내용
subject = '안녕하세요! 자동 발송 메일입니다.'
body = '이 메일은 파이썬 자동화로 발송되었습니다.'

# 엑셀 파일 읽기
data = []
wb = openpyxl.load_workbook(excel_path)
ws = wb.active
for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0] and row[1]:
        data.append((row[0], row[1]))  # (이메일, 이름)
print(data)
# SMTP 서버 연결 및 메일 발송
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender_email, app_password)
    for email, name in data:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        # 이름을 포함한 본문
        content = f"{name}님,\n\n{body}"
        msg.attach(MIMEText(content, 'plain'))
        smtp.send_message(msg)
        print(f"{email} ({name})에게 메일 발송 완료")
