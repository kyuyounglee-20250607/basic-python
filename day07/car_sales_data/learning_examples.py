"""
파이썬과 데이터베이스 학습용 예제 파일
기본 개념들을 단계별로 학습할 수 있습니다.
"""

import sqlite3
import datetime

def example_1_basic_sqlite():
    """
    예제 1: SQLite 기본 사용법
    """
    print("=" * 60)
    print("예제 1: SQLite 기본 사용법")
    print("=" * 60)
    
    # 1. 데이터베이스 연결
    print("1. 데이터베이스 연결 중...")
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # 2. 테이블 생성
    print("2. 테이블 생성 중...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade INTEGER,
            subject TEXT
        )
    ''')
    
    # 3. 데이터 삽입
    print("3. 데이터 삽입 중...")
    students_data = [
        ('김철수', 85, '수학'),
        ('이영희', 92, '영어'),
        ('박민수', 78, '과학'),
        ('정수진', 95, '국어')
    ]
    
    for student in students_data:
        cursor.execute('''
            INSERT INTO students (name, grade, subject)
            VALUES (?, ?, ?)
        ''', student)
    
    # 4. 데이터 조회
    print("4. 데이터 조회 중...")
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    
    print("\n📋 학생 목록:")
    print(f"{'ID':<5} {'이름':<10} {'점수':<5} {'과목':<10}")
    print("-" * 35)
    
    for student in students:
        id, name, grade, subject = student
        print(f"{id:<5} {name:<10} {grade:<5} {subject:<10}")
    
    # 5. 조건부 조회
    print("\n5. 조건부 조회 (90점 이상):")
    cursor.execute('SELECT * FROM students WHERE grade >= 90')
    high_scores = cursor.fetchall()
    
    for student in high_scores:
        id, name, grade, subject = student
        print(f"🎉 {name}님: {grade}점 ({subject})")
    
    # 6. 정렬
    print("\n6. 점수순 정렬:")
    cursor.execute('SELECT * FROM students ORDER BY grade DESC')
    sorted_students = cursor.fetchall()
    
    for i, student in enumerate(sorted_students, 1):
        id, name, grade, subject = student
        print(f"{i}등: {name}님 - {grade}점 ({subject})")
    
    # 7. 통계
    print("\n7. 통계 정보:")
    cursor.execute('SELECT COUNT(*) FROM students')
    total_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT AVG(grade) FROM students')
    avg_grade = cursor.fetchone()[0]
    
    cursor.execute('SELECT MAX(grade) FROM students')
    max_grade = cursor.fetchone()[0]
    
    print(f"총 학생 수: {total_count}명")
    print(f"평균 점수: {avg_grade:.1f}점")
    print(f"최고 점수: {max_grade}점")
    
    # 8. 데이터 수정
    print("\n8. 데이터 수정:")
    cursor.execute('UPDATE students SET grade = 88 WHERE name = "박민수"')
    print("박민수님의 점수를 88점으로 수정했습니다.")
    
    # 9. 수정된 데이터 확인
    cursor.execute('SELECT * FROM students WHERE name = "박민수"')
    updated_student = cursor.fetchone()
    print(f"수정된 정보: {updated_student[1]}님 - {updated_student[2]}점")
    
    # 10. 데이터 삭제
    print("\n10. 데이터 삭제:")
    cursor.execute('DELETE FROM students WHERE name = "정수진"')
    print("정수진님의 정보를 삭제했습니다.")
    
    # 11. 최종 확인
    cursor.execute('SELECT COUNT(*) FROM students')
    final_count = cursor.fetchone()[0]
    print(f"최종 학생 수: {final_count}명")
    
    # 12. 연결 종료
    conn.commit()
    conn.close()
    print("\n✅ 예제 1 완료!")

def example_2_error_handling():
    """
    예제 2: 오류 처리 방법
    """
    print("\n" + "=" * 60)
    print("예제 2: 오류 처리 방법")
    print("=" * 60)
    
    try:
        # 존재하지 않는 데이터베이스에 연결
        conn = sqlite3.connect('nonexistent.db')
        cursor = conn.cursor()
        
        # 존재하지 않는 테이블 조회
        cursor.execute('SELECT * FROM nonexistent_table')
        
    except sqlite3.OperationalError as e:
        print(f"❌ 데이터베이스 오류: {e}")
        print("💡 해결 방법: 테이블이 존재하는지 확인하세요.")
        
    except sqlite3.Error as e:
        print(f"❌ SQLite 오류: {e}")
        
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        
    finally:
        print("✅ 오류 처리가 완료되었습니다.")

def example_3_data_types():
    """
    예제 3: 데이터 타입 이해하기
    """
    print("\n" + "=" * 60)
    print("예제 3: 데이터 타입 이해하기")
    print("=" * 60)
    
    conn = sqlite3.connect('types_example.db')
    cursor = conn.cursor()
    
    # 다양한 데이터 타입을 가진 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text_field TEXT,
            integer_field INTEGER,
            real_field REAL,
            blob_field BLOB,
            null_field TEXT
        )
    ''')
    
    # 다양한 타입의 데이터 삽입
    test_data = [
        ('문자열', 42, 3.14, b'binary_data', None),
        ('한글도 가능', -10, 2.718, b'another_binary', 'NULL이 아닌 값'),
        ('', 0, 0.0, b'', '')
    ]
    
    for data in test_data:
        cursor.execute('''
            INSERT INTO data_types (text_field, integer_field, real_field, blob_field, null_field)
            VALUES (?, ?, ?, ?, ?)
        ''', data)
    
    # 데이터 조회 및 타입 확인
    cursor.execute('SELECT * FROM data_types')
    results = cursor.fetchall()
    
    print("📋 데이터 타입 예제:")
    print(f"{'ID':<5} {'TEXT':<15} {'INTEGER':<10} {'REAL':<8} {'BLOB':<15} {'NULL':<15}")
    print("-" * 70)
    
    for row in results:
        id, text_val, int_val, real_val, blob_val, null_val = row
        print(f"{id:<5} {str(text_val):<15} {int_val:<10} {real_val:<8.2f} {str(blob_val):<15} {str(null_val):<15}")
    
    conn.commit()
    conn.close()
    print("\n✅ 예제 3 완료!")

def example_4_python_integration():
    """
    예제 4: 파이썬과 데이터베이스 통합
    """
    print("\n" + "=" * 60)
    print("예제 4: 파이썬과 데이터베이스 통합")
    print("=" * 60)
    
    # 파이썬 리스트를 데이터베이스에 저장
    products = [
        {'name': '노트북', 'price': 1200000, 'category': '전자제품'},
        {'name': '마우스', 'price': 25000, 'category': '전자제품'},
        {'name': '책상', 'price': 150000, 'category': '가구'},
        {'name': '의자', 'price': 80000, 'category': '가구'},
        {'name': '커피', 'price': 4500, 'category': '음료'}
    ]
    
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    # 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER,
            category TEXT,
            created_at TEXT
        )
    ''')
    
    # 파이썬 딕셔너리를 데이터베이스에 저장
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for product in products:
        cursor.execute('''
            INSERT INTO products (name, price, category, created_at)
            VALUES (?, ?, ?, ?)
        ''', (product['name'], product['price'], product['category'], current_time))
    
    # 데이터베이스에서 파이썬 딕셔너리로 변환
    cursor.execute('SELECT * FROM products')
    db_products = cursor.fetchall()
    
    # 파이썬 딕셔너리 리스트로 변환
    product_dicts = []
    for row in db_products:
        product_dict = {
            'id': row[0],
            'name': row[1],
            'price': row[2],
            'category': row[3],
            'created_at': row[4]
        }
        product_dicts.append(product_dict)
    
    # 파이썬으로 데이터 처리
    print("📦 상품 목록:")
    for product in product_dicts:
        print(f"ID: {product['id']}, 이름: {product['name']}, 가격: {product['price']:,}원, 카테고리: {product['category']}")
    
    # 파이썬 필터링
    electronics = [p for p in product_dicts if p['category'] == '전자제품']
    furniture = [p for p in product_dicts if p['category'] == '가구']
    
    print(f"\n🖥️ 전자제품 ({len(electronics)}개):")
    for item in electronics:
        print(f"  - {item['name']}: {item['price']:,}원")
    
    print(f"\n🪑 가구 ({len(furniture)}개):")
    for item in furniture:
        print(f"  - {item['name']}: {item['price']:,}원")
    
    # 파이썬 계산
    total_price = sum(p['price'] for p in product_dicts)
    avg_price = total_price / len(product_dicts)
    
    print(f"\n💰 통계:")
    print(f"총 상품 수: {len(product_dicts)}개")
    print(f"총 가격: {total_price:,}원")
    print(f"평균 가격: {avg_price:,.0f}원")
    
    conn.commit()
    conn.close()
    print("\n✅ 예제 4 완료!")

def run_all_examples():
    """
    모든 예제를 실행하는 함수
    """
    print("🎓 파이썬과 SQLite 데이터베이스 학습 예제")
    print("각 예제를 통해 기본 개념을 학습할 수 있습니다.\n")
    
    try:
        example_1_basic_sqlite()
        example_2_error_handling()
        example_3_data_types()
        example_4_python_integration()
        
        print("\n" + "=" * 60)
        print("🎉 모든 예제가 완료되었습니다!")
        print("이제 data_collector.py를 실행해보세요.")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 예제 실행 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    run_all_examples() 