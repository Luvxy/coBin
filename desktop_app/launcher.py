import subprocess
import sys

if __name__ == "__main__":
    print("업데이트 확인 중...")
    
    # 업데이트 확인 및 설치
    subprocess.run([sys.executable, "check_for_update.py"])
    
    # 메인 프로그램 실행
    print("메인 프로그램 실행")
    subprocess.run([sys.executable, "main.py"])
