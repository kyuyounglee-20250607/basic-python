"""
데이터베이스 초기 설정 파일
이 파일은 데이터베이스와 테이블을 생성합니다.
"""

import sqlite3
import os

def create_database():
    """
    데이터베이스와 테이블을 생성하는 함수
    """
    print("데이터베이스를 생성하고 있습니다...")
    
    # 데이터베이스 연결 (파일이 없으면 새로 생성됨)
    conn = sqlite3.connect('data.db')
    
    # 커서 생성 (데이터베이스에 명령을 내리는 도구)
    cursor = conn.cursor()
    
    # 테이블 생성
    # CREATE TABLE: 새로운 테이블을 만드는 SQL 명령어
    # users: 테이블 이름
    # id: 고유 번호 (자동 증가)
    # name: 이름 (텍스트, 필수 입력)
    # age: 나이 (숫자)
    # email: 이메일 (텍스트)
    # created_at: 생성 시간 (텍스트)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT,
            created_at TEXT
        )
    ''')
    
    # 변경사항 저장
    conn.commit()
    
    # 연결 종료
    conn.close()
    
    print("✅ 데이터베이스 생성 완료!")
    print("📁 data.db 파일이 생성되었습니다.")

def check_database():
    """
    데이터베이스가 제대로 생성되었는지 확인하는 함수
    """
    if os.path.exists('data.db'):
        print("✅ 데이터베이스 파일이 존재합니다.")
        
        # 데이터베이스 연결
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        # 테이블 목록 확인
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"📋 생성된 테이블: {[table[0] for table in tables]}")
        
        conn.close()
    else:
        print("❌ 데이터베이스 파일이 없습니다.")

if __name__ == "__main__":
    # 이 파일을 직접 실행했을 때만 실행되는 코드
    print("=" * 50)
    print("데이터베이스 초기 설정")
    print("=" * 50)
    
    create_database()
    check_database()
    
    print("\n🎉 설정이 완료되었습니다!")
    print("이제 data_collector.py를 실행하여 데이터를 수집할 수 있습니다.") 