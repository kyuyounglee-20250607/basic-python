#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
간단한 TTS 패키지 테스트
"""

from tts_simple import SimpleTTS, Language, quick_speak, speak_korean, speak_english, speak_chinese, speak_japanese

def test_import():
    """import 테스트"""
    print("🔍 Import 테스트 중...")
    
    try:
        from tts_simple import SimpleTTS, Language
        print("✅ Import 성공!")
        return True
    except Exception as e:
        print(f"❌ Import 실패: {e}")
        return False

def test_tts_creation():
    """TTS 객체 생성 테스트"""
    print("\n🔍 TTS 객체 생성 테스트 중...")
    
    try:
        tts = SimpleTTS()
        print("✅ TTS 객체 생성 성공!")
        return tts
    except Exception as e:
        print(f"❌ TTS 객체 생성 실패: {e}")
        return None

def test_korean_voice(tts):
    """한국어 음성 테스트"""
    print("\n🇰🇷 한국어 음성 테스트:")
    
    test_texts = [
        "안녕하세요! 이것은 한국어 음성 테스트입니다.",
        "오늘 날씨가 정말 좋네요.",
        "파이썬으로 만든 TTS 프로그램입니다."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{i}. {text}")
        success = tts.speak(text, language=Language.KOREAN)
        print(f"   결과: {'✅ 성공' if success else '❌ 실패'}")

def test_english_voice(tts):
    """영어 음성 테스트"""
    print("\n🇺🇸 영어 음성 테스트:")
    
    test_texts = [
        "Hello! This is an English voice test.",
        "The weather is really nice today.",
        "This is a TTS program made with Python."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{i}. {text}")
        success = tts.speak(text, language=Language.ENGLISH)
        print(f"   결과: {'✅ 성공' if success else '❌ 실패'}")

def test_chinese_voice(tts):
    """중국어 음성 테스트"""
    print("\n🇨🇳 중국어 음성 테스트:")
    
    test_texts = [
        "你好！这是中文语音测试。",
        "今天天气真好。",
        "这是用Python制作的TTS程序。"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{i}. {text}")
        success = tts.speak(text, language=Language.CHINESE)
        print(f"   결과: {'✅ 성공' if success else '❌ 실패'}")

def test_japanese_voice(tts):
    """일본어 음성 테스트"""
    print("\n🇯🇵 일본어 음성 테스트:")
    
    test_texts = [
        "こんにちは！これは日本語の音声テストです。",
        "今日は天気がとても良いです。",
        "これはPythonで作られたTTSプログラムです。"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{i}. {text}")
        success = tts.speak(text, language=Language.JAPANESE)
        print(f"   결과: {'✅ 성공' if success else '❌ 실패'}")

def test_file_saving(tts):
    """파일 저장 테스트"""
    print("\n💾 파일 저장 테스트:")
    
    test_text = "이 음성은 파일로 저장됩니다."
    filename = "test_saved_voice.mp3"
    
    print(f"저장할 텍스트: {test_text}")
    success = tts.speak(
        text=test_text,
        language=Language.KOREAN,
        save_to_file=True,
        filename=filename,
        play_audio=True
    )
    
    if success:
        print(f"✅ 파일 저장 성공: {filename}")
    else:
        print("❌ 파일 저장 실패")

def test_batch_processing(tts):
    """일괄 처리 테스트"""
    print("\n🔄 일괄 처리 테스트:")
    
    texts = [
        "첫 번째 문장입니다.",
        "두 번째 문장입니다.",
        "세 번째 문장입니다."
    ]
    
    print("연속으로 3개 문장을 처리합니다...")
    success = tts.batch_speak(texts, language=Language.KOREAN, delay_between=1.5)
    
    if success:
        print("✅ 일괄 처리 성공!")
    else:
        print("❌ 일괄 처리 실패")

def test_convenience_functions():
    """편의 함수 테스트"""
    print("\n⚡ 편의 함수 테스트:")
    
    # 한국어
    print("1. 한국어 편의 함수:")
    success = speak_korean("안녕하세요! 편의 함수 테스트입니다.")
    print(f"   결과: {'✅ 성공' if success else '❌ 실패'}")
    
    # 영어
    print("\n2. 영어 편의 함수:")
    success = speak_english("Hello! This is a convenience function test.")
    print(f"   결과: {'✅ 성공' if success else '❌ 실패'}")
    
    # 중국어
    print("\n3. 중국어 편의 함수:")
    success = speak_chinese("你好！这是便利函数测试。")
    print(f"   결과: {'✅ 성공' if success else '❌ 실패'}")
    
    # 일본어
    print("\n4. 일본어 편의 함수:")
    success = speak_japanese("こんにちは！これは便利関数のテストです。")
    print(f"   결과: {'✅ 성공' if success else '❌ 실패'}")

def test_quick_speak():
    """빠른 음성 변환 테스트"""
    print("\n🚀 빠른 음성 변환 테스트:")
    
    # 한국어
    print("1. 한국어 빠른 변환:")
    success = quick_speak("안녕하세요! 빠른 변환 테스트입니다.", Language.KOREAN)
    print(f"   결과: {'✅ 성공' if success else '❌ 실패'}")
    
    # 영어
    print("\n2. 영어 빠른 변환:")
    success = quick_speak("Hello! This is a quick conversion test.", Language.ENGLISH)
    print(f"   결과: {'✅ 성공' if success else '❌ 실패'}")

def test_supported_languages(tts):
    """지원 언어 목록 테스트"""
    print("\n📋 지원 언어 목록:")
    
    languages = tts.get_supported_languages()
    for name, code in languages.items():
        print(f"  {name}: {code}")

def interactive_test():
    """대화형 테스트"""
    print("\n🎮 대화형 테스트:")
    
    tts = SimpleTTS()
    languages = tts.get_supported_languages()
    
    while True:
        print("\n" + "-" * 40)
        print("옵션 선택:")
        print("1. 한국어 음성 변환")
        print("2. 영어 음성 변환")
        print("3. 중국어 음성 변환")
        print("4. 일본어 음성 변환")
        print("5. 파일로 저장")
        print("6. 종료")
        print("-" * 40)
        
        choice = input("선택하세요 (1-6): ").strip()
        
        if choice == "1":
            text = input("한국어 텍스트를 입력하세요: ").strip()
            if text:
                tts.speak(text, language=Language.KOREAN)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "2":
            text = input("영어 텍스트를 입력하세요: ").strip()
            if text:
                tts.speak(text, language=Language.ENGLISH)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "3":
            text = input("중국어 텍스트를 입력하세요: ").strip()
            if text:
                tts.speak(text, language=Language.CHINESE)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "4":
            text = input("일본어 텍스트를 입력하세요: ").strip()
            if text:
                tts.speak(text, language=Language.JAPANESE)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "5":
            text = input("저장할 텍스트를 입력하세요: ").strip()
            if text:
                language = input("언어를 선택하세요 (ko/en/zh/ja): ").strip()
                if language not in ['ko', 'en', 'zh', 'ja']:
                    language = Language.KOREAN
                
                filename = input("파일명을 입력하세요 (기본: output.mp3): ").strip()
                if not filename:
                    filename = "output.mp3"
                if not filename.endswith('.mp3'):
                    filename += '.mp3'
                
                tts.speak(text, language=language, save_to_file=True, filename=filename)
            else:
                print("❌ 텍스트를 입력해주세요.")
        
        elif choice == "6":
            print("👋 대화형 테스트를 종료합니다!")
            break
        
        else:
            print("❌ 잘못된 선택입니다.")

def main():
    """메인 테스트 함수"""
    print("🧪 간단한 TTS 패키지 테스트")
    print("=" * 50)
    
    # 1. Import 테스트
    if not test_import():
        print("\n❌ Import 문제가 있습니다. 라이브러리 설치를 확인하세요.")
        return
    
    # 2. TTS 객체 생성 테스트
    tts = test_tts_creation()
    if not tts:
        print("\n❌ TTS 객체 생성 문제가 있습니다.")
        return
    
    # 3. 지원 언어 목록 확인
    test_supported_languages(tts)
    
    # 4. 각 언어별 테스트
    test_korean_voice(tts)
    test_english_voice(tts)
    test_chinese_voice(tts)
    test_japanese_voice(tts)
    
    # 5. 파일 저장 테스트
    test_file_saving(tts)
    
    # 6. 일괄 처리 테스트
    test_batch_processing(tts)
    
    # 7. 편의 함수 테스트
    test_convenience_functions()
    
    # 8. 빠른 변환 테스트
    test_quick_speak()
    
    # 9. 대화형 테스트
    demo_choice = input("\n대화형 테스트를 실행하시겠습니까? (y/n): ").strip().lower()
    if demo_choice == 'y':
        interactive_test()
    
    print("\n🎉 모든 테스트 완료!")

if __name__ == "__main__":
    main() 