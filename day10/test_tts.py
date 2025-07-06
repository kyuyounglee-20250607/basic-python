#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS 기능 테스트 스크립트
라이브러리가 제대로 설치되었는지 확인하고 간단한 테스트를 수행합니다.
"""

def test_imports():
    """필요한 라이브러리 import 테스트"""
    print("🔍 라이브러리 import 테스트 중...")
    
    results = {}
    
    # gTTS 테스트
    try:
        from gtts import gTTS
        results['gTTS'] = True
        print("✅ gTTS import 성공")
    except ImportError:
        results['gTTS'] = False
        print("❌ gTTS import 실패")
    
    # pyttsx3 테스트
    try:
        import pyttsx3
        results['pyttsx3'] = True
        print("✅ pyttsx3 import 성공")
    except ImportError:
        results['pyttsx3'] = False
        print("❌ pyttsx3 import 실패")
    
    # playsound 테스트
    try:
        from playsound import playsound
        results['playsound'] = True
        print("✅ playsound import 성공")
    except ImportError:
        results['playsound'] = False
        print("❌ playsound import 실패")
    
    return results

def test_google_tts():
    """Google TTS 기능 테스트"""
    print("\n🌐 Google TTS 기능 테스트 중...")
    
    try:
        from gtts import gTTS
        
        # 간단한 텍스트로 테스트
        test_text = "테스트"
        tts = gTTS(text=test_text, lang='ko', slow=False)
        
        # 파일로 저장
        test_file = "test_google.mp3"
        tts.save(test_file)
        
        print("✅ Google TTS 변환 성공")
        print(f"✅ 파일 저장 성공: {test_file}")
        
        # 파일 존재 확인
        import os
        if os.path.exists(test_file):
            print(f"✅ 파일 확인됨: {os.path.getsize(test_file)} bytes")
            return True
        else:
            print("❌ 파일이 생성되지 않았습니다.")
            return False
            
    except Exception as e:
        print(f"❌ Google TTS 테스트 실패: {e}")
        return False

def test_windows_tts():
    """Windows TTS 기능 테스트"""
    print("\n🖥️ Windows TTS 기능 테스트 중...")
    
    try:
        import pyttsx3
        
        # TTS 엔진 초기화
        engine = pyttsx3.init()
        
        # 음성 속도 설정
        engine.setProperty('rate', 150)
        
        # 간단한 테스트
        test_text = "테스트"
        engine.say(test_text)
        
        print("✅ Windows TTS 엔진 초기화 성공")
        print("✅ 음성 변환 준비 완료")
        
        # 실제 재생 여부 확인
        play_choice = input("음성을 실제로 재생하시겠습니까? (y/n): ").strip().lower()
        if play_choice == 'y':
            engine.runAndWait()
            print("✅ Windows TTS 재생 완료")
        
        return True
        
    except Exception as e:
        print(f"❌ Windows TTS 테스트 실패: {e}")
        return False

def test_playsound():
    """playsound 기능 테스트"""
    print("\n🔊 playsound 기능 테스트 중...")
    
    try:
        from playsound import playsound
        
        # Google TTS로 테스트 파일 생성
        from gtts import gTTS
        test_text = "플레이사운드 테스트"
        tts = gTTS(text=test_text, lang='ko', slow=False)
        test_file = "test_playsound.mp3"
        tts.save(test_file)
        
        print("✅ 테스트 파일 생성 완료")
        
        # 재생 여부 확인
        play_choice = input("음성을 재생하시겠습니까? (y/n): ").strip().lower()
        if play_choice == 'y':
            playsound(test_file)
            print("✅ playsound 재생 완료")
        
        return True
        
    except Exception as e:
        print(f"❌ playsound 테스트 실패: {e}")
        return False

def cleanup_test_files():
    """테스트 파일 정리"""
    import os
    
    test_files = ["test_google.mp3", "test_playsound.mp3"]
    
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"🗑️ 테스트 파일 삭제: {file}")
            except:
                print(f"⚠️ 파일 삭제 실패: {file}")

def main():
    """메인 테스트 함수"""
    print("=" * 50)
    print("🧪 TTS 프로그램 테스트")
    print("=" * 50)
    
    # 1. Import 테스트
    import_results = test_imports()
    
    # 2. 기능 테스트
    test_results = {}
    
    if import_results.get('gTTS', False):
        test_results['Google TTS'] = test_google_tts()
    
    if import_results.get('pyttsx3', False):
        test_results['Windows TTS'] = test_windows_tts()
    
    if import_results.get('playsound', False):
        test_results['playsound'] = test_playsound()
    
    # 3. 결과 요약
    print("\n" + "=" * 50)
    print("📊 테스트 결과 요약")
    print("=" * 50)
    
    for lib, result in import_results.items():
        status = "✅ 성공" if result else "❌ 실패"
        print(f"{lib}: {status}")
    
    print("\n기능 테스트:")
    for func, result in test_results.items():
        status = "✅ 성공" if result else "❌ 실패"
        print(f"{func}: {status}")
    
    # 4. 정리
    cleanup_choice = input("\n테스트 파일을 삭제하시겠습니까? (y/n): ").strip().lower()
    if cleanup_choice == 'y':
        cleanup_test_files()
    
    print("\n👋 테스트 완료!")

if __name__ == "__main__":
    main() 