# deep-translator 라이브러리에서 PapagoTranslator를 임포트합니다.
from deep_translator import PapagoTranslator

# 파일을 번역하는 함수 정의
# input_path: 원본 영어 파일 경로
# output_path: 번역된 한글 파일 경로
def translate_file(input_path, output_path):
    # PapagoTranslator 객체 생성 (영어->한국어)
    # 아래 client_id와 secret_key에 본인의 네이버 Papago API 정보를 입력하세요.
    client_id = '여기에_본인_client_id_입력'
    secret_key = '여기에_본인_secret_key_입력'
    translator = PapagoTranslator(source='en', target='ko', client_id=client_id, client_secret=secret_key)
    # 입력 파일을 읽기 모드로 엽니다.
    with open(input_path, 'r', encoding='utf-8') as infile:
        text = infile.read()  # 파일 전체 내용을 읽어옵니다.
    # 읽어온 텍스트를 영어(en)에서 한국어(ko)로 번역합니다.
    translated = translator.translate(text)
    # 번역된 텍스트를 출력 파일에 저장합니다.
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(translated)

# 사용 예시
translate_file('english_doc.txt', 'korean_doc.txt')
