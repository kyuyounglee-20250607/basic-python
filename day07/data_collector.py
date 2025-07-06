"""
데이터 수집 프로그램
사용자로부터 데이터를 입력받아 데이터베이스에 저장하고 관리합니다.
"""

import sqlite3
import datetime
from database_setup import create_database

class DataCollector:
    """
    데이터 수집을 담당하는 클래스
    """
    
    def __init__(self):
        """
        초기화 함수 - 데이터베이스 연결을 설정합니다
        """
        # 데이터베이스가 없으면 생성
        create_database()
        self.db_name = 'data.db'
    
    def get_connection(self):
        """
        데이터베이스 연결을 반환하는 함수
        """
        return sqlite3.connect(self.db_name)
    
    def add_user(self):
        """
        새로운 사용자 정보를 입력받아 데이터베이스에 저장하는 함수
        """
        print("\n" + "="*40)
        print("새로운 사용자 정보 입력")
        print("="*40)
        
        # 사용자로부터 정보 입력받기
        name = input("이름을 입력하세요: ").strip()
        
        # 이름이 비어있으면 다시 입력받기
        while not name:
            print("❌ 이름은 필수 입력 항목입니다!")
            name = input("이름을 입력하세요: ").strip()
        
        # 나이 입력받기 (선택사항)
        age_input = input("나이를 입력하세요 (선택사항, 엔터로 건너뛰기): ").strip()
        age = None
        if age_input:
            try:
                age = int(age_input)
            except ValueError:
                print("⚠️ 나이는 숫자로 입력해주세요. 건너뛰겠습니다.")
        
        # 이메일 입력받기 (선택사항)
        email = input("이메일을 입력하세요 (선택사항, 엔터로 건너뛰기): ").strip()
        if not email:
            email = None
        
        # 현재 시간 가져오기
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # 데이터베이스에 저장
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # INSERT INTO: 데이터를 테이블에 추가하는 SQL 명령어
            cursor.execute('''
                INSERT INTO users (name, age, email, created_at)
                VALUES (?, ?, ?, ?)
            ''', (name, age, email, current_time))
            
            # 변경사항 저장
            conn.commit()
            conn.close()
            
            print("✅ 사용자 정보가 성공적으로 저장되었습니다!")
            
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {e}")
    
    def view_all_users(self):
        """
        모든 사용자 정보를 조회하는 함수
        """
        print("\n" + "="*60)
        print("전체 사용자 목록")
        print("="*60)
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # SELECT: 데이터를 조회하는 SQL 명령어
            cursor.execute('SELECT * FROM users ORDER BY id')
            users = cursor.fetchall()
            
            if not users:
                print("📭 저장된 사용자가 없습니다.")
            else:
                print(f"{'ID':<5} {'이름':<10} {'나이':<5} {'이메일':<20} {'생성시간':<20}")
                print("-" * 60)
                
                for user in users:
                    id, name, age, email, created_at = user
                    # None 값 처리
                    age_str = str(age) if age else "N/A"
                    email_str = email if email else "N/A"
                    
                    print(f"{id:<5} {name:<10} {age_str:<5} {email_str:<20} {created_at:<20}")
                
                print(f"\n총 {len(users)}명의 사용자가 등록되어 있습니다.")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {e}")
    
    def search_user(self):
        """
        사용자를 검색하는 함수
        """
        print("\n" + "="*40)
        print("사용자 검색")
        print("="*40)
        
        search_term = input("검색할 이름을 입력하세요: ").strip()
        
        if not search_term:
            print("❌ 검색어를 입력해주세요!")
            return
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # LIKE: 부분 일치 검색을 위한 SQL 연산자
            cursor.execute('''
                SELECT * FROM users 
                WHERE name LIKE ? 
                ORDER BY id
            ''', (f'%{search_term}%',))
            
            users = cursor.fetchall()
            
            if not users:
                print(f"🔍 '{search_term}'과 일치하는 사용자를 찾을 수 없습니다.")
            else:
                print(f"\n'{search_term}' 검색 결과:")
                print(f"{'ID':<5} {'이름':<10} {'나이':<5} {'이메일':<20} {'생성시간':<20}")
                print("-" * 60)
                
                for user in users:
                    id, name, age, email, created_at = user
                    age_str = str(age) if age else "N/A"
                    email_str = email if email else "N/A"
                    
                    print(f"{id:<5} {name:<10} {age_str:<5} {email_str:<20} {created_at:<20}")
                
                print(f"\n총 {len(users)}명의 사용자가 검색되었습니다.")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {e}")
    
    def delete_user(self):
        """
        사용자를 삭제하는 함수
        """
        print("\n" + "="*40)
        print("사용자 삭제")
        print("="*40)
        
        # 먼저 모든 사용자 목록을 보여줌
        self.view_all_users()
        
        try:
            user_id = input("\n삭제할 사용자의 ID를 입력하세요: ").strip()
            
            if not user_id:
                print("❌ ID를 입력해주세요!")
                return
            
            user_id = int(user_id)
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 삭제할 사용자가 존재하는지 확인
            cursor.execute('SELECT name FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            
            if not user:
                print(f"❌ ID {user_id}인 사용자를 찾을 수 없습니다.")
                conn.close()
                return
            
            # 삭제 확인
            confirm = input(f"'{user[0]}' 사용자를 정말 삭제하시겠습니까? (y/N): ").strip().lower()
            
            if confirm == 'y':
                # DELETE: 데이터를 삭제하는 SQL 명령어
                cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
                conn.commit()
                print(f"✅ '{user[0]}' 사용자가 삭제되었습니다.")
            else:
                print("❌ 삭제가 취소되었습니다.")
            
            conn.close()
            
        except ValueError:
            print("❌ ID는 숫자로 입력해주세요!")
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {e}")
    
    def show_menu(self):
        """
        메뉴를 표시하는 함수
        """
        print("\n" + "="*50)
        print("📊 데이터 수집 프로그램")
        print("="*50)
        print("1. 새로운 사용자 추가")
        print("2. 전체 사용자 조회")
        print("3. 사용자 검색")
        print("4. 사용자 삭제")
        print("5. 프로그램 종료")
        print("="*50)
    
    def run(self):
        """
        프로그램을 실행하는 메인 함수
        """
        print("🎉 데이터 수집 프로그램에 오신 것을 환영합니다!")
        
        while True:
            self.show_menu()
            
            choice = input("원하는 기능을 선택하세요 (1-5): ").strip()
            
            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.view_all_users()
            elif choice == '3':
                self.search_user()
            elif choice == '4':
                self.delete_user()
            elif choice == '5':
                print("\n👋 프로그램을 종료합니다. 안녕히 가세요!")
                break
            else:
                print("❌ 1부터 5까지의 숫자 중에서 선택해주세요!")
            
            # 다음 메뉴로 넘어가기 전에 잠시 대기
            input("\n엔터를 누르면 메뉴로 돌아갑니다...")

# 프로그램 실행
if __name__ == "__main__":
    collector = DataCollector()
    collector.run() 