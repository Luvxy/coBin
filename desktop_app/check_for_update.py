import requests
import os
import zipfile
import shutil
import sys
import subprocess

# GitHub 저장소 정보
GITHUB_REPO = "luvxy/coBin"  # 변경 필요
LATEST_RELEASE_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
DOWNLOAD_PATH = "update.zip"
EXTRACT_FOLDER = "update_temp"
CURRENT_VERSION = "v1.0.0"  # 현재 버전 (매 빌드마다 업데이트 필요)

def get_latest_release():
    """GitHub에서 최신 릴리스 버전 및 다운로드 URL 가져오기"""
    response = requests.get(LATEST_RELEASE_URL)
    if response.status_code == 200:
        data = response.json()
        version = data["tag_name"]  # 최신 버전 태그
        for asset in data["assets"]:
            if asset["name"].endswith(".zip"):
                return version, asset["browser_download_url"]
    return None, None

def download_update(url):
    """업데이트 파일 다운로드"""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(DOWNLOAD_PATH, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return True
    return False

def install_update():
    """업데이트 파일 압축 해제 및 덮어쓰기"""
    if os.path.exists(EXTRACT_FOLDER):
        shutil.rmtree(EXTRACT_FOLDER)
    os.makedirs(EXTRACT_FOLDER)

    with zipfile.ZipFile(DOWNLOAD_PATH, "r") as zip_ref:
        zip_ref.extractall(EXTRACT_FOLDER)

    # 현재 실행 중인 파일을 종료 후 덮어쓰기
    exe_name = os.path.basename(sys.executable)  # 실행 파일명 가져오기
    new_exe_path = os.path.join(EXTRACT_FOLDER, exe_name)
    
    if os.path.exists(new_exe_path):
        shutil.move(new_exe_path, sys.executable)
        os.chmod(sys.executable, 0o755)

    # 정리
    shutil.rmtree(EXTRACT_FOLDER)
    os.remove(DOWNLOAD_PATH)
    
    print("업데이트 완료! 프로그램을 다시 시작합니다.")
    
    # 프로그램 자동 재실행
    subprocess.Popen([sys.executable, "launcher.py"])
    sys.exit(0)

def check_for_update():
    """현재 버전과 최신 버전을 비교하여 업데이트 수행"""
    latest_version, download_url = get_latest_release()

    if latest_version and latest_version != CURRENT_VERSION:
        print(f"새로운 업데이트 발견: {latest_version}")
        if download_update(download_url):
            install_update()
    else:
        print("최신 버전입니다.")

if __name__ == "__main__":
    check_for_update()
