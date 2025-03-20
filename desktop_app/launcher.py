import os
import sys
import requests
import shutil
import subprocess
import json
import time
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.ui_loading import loading

# GitHub 저장소 정보
GITHUB_REPO = "luvxy/coBin"  # GitHub 저장소 이름
LATEST_RELEASE_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
TOKEN = "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"  # GitHub Personal Access Token
DOWNLOAD_PATH = os.path.join(os.path.dirname(__file__), "cobin.exe")  # 다운로드 파일 경로
VERSION_FILE = "version.json"  # 버전 정보 파일

def set_current_version(version):
    """업데이트 후 version.json에 새로운 버전 저장"""
    with open(VERSION_FILE, "w") as file:
        json.dump({"current_version": version}, file, indent=4)
    print(f"[DEBUG] 새로운 버전 저장: {version}")

def get_current_version():
    """현재 버전을 version.json에서 읽어오기"""
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as file:
            data = json.load(file)
            return data.get("current_version", "v0.0.0")
    return "v0.0.0"  # 기본값

CURRENT_VERSION = get_current_version()  # version.json에서 현재 버전 읽기

def get_latest_release():
    """GitHub에서 최신 릴리스 태그와 파일 API URL 가져오기"""
    headers = {
        "Authorization": f"token {TOKEN}"  # 인증 토큰 추가
    }
    response = requests.get(LATEST_RELEASE_URL, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        version = data["tag_name"].strip()
        print(f"[DEBUG] 최신 버전: {version}")  # 디버깅 로그 추가

        for asset in data["assets"]:
            print(f"[DEBUG] Asset Name: {asset['name']}")  # 릴리스 파일 목록 출력
            print(f"[DEBUG] Asset API URL: {asset['url']}")  # GitHub API 다운로드 URL

            if asset["name"].endswith(".exe"):  # .exe 파일만 처리
                version
                return version, asset["url"]  # GitHub API URL 반환
    
    else:
        print(f"API 요청 실패: {response.status_code}, 메시지: {response.text}")
    
    return None, None

def launch_main_application():
    """메인 애플리케이션 실행"""
    exe_path = "cobin.exe"  # 메인 실행 파일 경로
    if os.path.exists(exe_path):
        print("[DEBUG] 메인 애플리케이션 실행 중...")
        subprocess.Popen([exe_path])  # cobin.exe 실행
        sys.exit(0)
    else:
        print("[ERROR] cobin.exe 파일을 찾을 수 없습니다. 설치를 진행합니다.")
        QMessageBox.warning(None, "설치 필요", "cobin.exe 파일이 없습니다. 설치를 진행합니다.")
        latest_version, download_url = get_latest_release()
        if latest_version and download_url:
            if download_update(download_url):
                install_update(latest_version)
            else:
                QMessageBox.critical(None, "설치 실패", "cobin.exe 파일을 다운로드할 수 없습니다.")
                sys.exit(1)
        else:
            QMessageBox.critical(None, "설치 실패", "릴리스 정보를 가져올 수 없습니다.")
            sys.exit(1)

def download_update(api_url):
    """GitHub API를 사용하여 업데이트 파일 다운로드"""
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/octet-stream",  # GitHub에서 직접 다운로드 가능하도록 설정
        "User-Agent": "Mozilla/5.0"
    }

    print(f"[DEBUG] 다운로드 API URL: {api_url}")  # 디버깅 로그 추가

    response = requests.get(api_url, stream=True, headers=headers)
    print(f"[DEBUG] 다운로드 상태: {response.status_code}")  # 상태 코드 확인

    if response.status_code == 200:
        with open(DOWNLOAD_PATH, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print("[DEBUG] 다운로드 완료 ✅")
        return True

    print(f"[ERROR] 다운로드 실패 ❌ 상태 코드: {response.status_code}, 메시지: {response.text}")
    return False

def install_update(update_versions):
    """업데이트 파일을 덮어쓰기"""
    exe_path = "cobin.exe"  # 업데이트 대상 파일 경로
    new_exe_path = exe_path + ".old"  # 백업 파일 경로

    if os.path.exists(DOWNLOAD_PATH):
        print("업데이트 적용 중...")

        # 기존 백업 파일이 있으면 삭제
        if os.path.exists(new_exe_path):
            os.remove(new_exe_path)

        # 기존 실행 파일을 백업
        os.rename(exe_path, new_exe_path)

        # 새 파일을 실행 파일로 이동
        shutil.move(DOWNLOAD_PATH, exe_path)

        print("업데이트 완료! 프로그램을 다시 시작합니다.")
        set_current_version(update_versions)  # 새로운 버전 저장
        subprocess.Popen([exe_path])
        sys.exit(0)

class LoadingScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = loading()
        self.ui.setupUi(self)
        
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # ProgressBar 초기화
        self.ui.progressBar.setValue(0)  # 초기값 0%

        self.show()
        QTimer.singleShot(500, self.check_for_update)

    def set_status_text(self, text):
        """로딩 창의 상태 메시지 업데이트"""
        self.ui.label_3.setText(text)
        QApplication.processEvents()  # UI 업데이트 강제 실행

    def update_progress_bar(self, value):
        """ProgressBar 업데이트"""
        self.ui.progressBar.setValue(value)
        QApplication.processEvents()  # UI 업데이트 강제 실행

    def check_for_update(self):
        """업데이트 확인 및 실행"""
        self.set_status_text("<strong>업데이트 확인 중...</strong>")
        exe_path = "cobin.exe"
    
        # cobin.exe가 없는 경우 설치 진행
        if not os.path.exists(exe_path):
            self.set_status_text("<strong>cobin.exe 파일이 없습니다. 설치를 진행합니다...</strong>")
            for i in range(0, 33):
                self.ui.progressBar.setValue(i)
                time.sleep(0.05)
            latest_version, download_url = get_latest_release()
            if latest_version and download_url:
                if download_update(download_url):
                    self.set_status_text("<strong>설치 완료</strong> 설치 중...")
                    for i in range(33, 53):
                        self.ui.progressBar.setValue(i)
                        time.sleep(0.05)
                    install_update(latest_version)
                    for i in range(53, 100):
                        self.ui.progressBar.setValue(i)
                        time.sleep(0.05)
                    self.set_status_text("<strong>설치 완료! 프로그램을 재시작합니다.</strong>")
                else:
                    QMessageBox.critical(self, "설치 실패", "cobin.exe 파일을 다운로드할 수 없습니다.")
                    sys.exit(1)
            else:
                QMessageBox.critical(self, "설치 실패", "릴리스 정보를 가져올 수 없습니다.")
                sys.exit(1)
            return
    
        # cobin.exe가 있는 경우 업데이트 확인
        latest_version, download_url = get_latest_release()
        if latest_version and download_url:
            if latest_version != CURRENT_VERSION:
                self.set_status_text(f"<strong>업데이트 발견: {latest_version}</strong> 다운로드 중...")
                print(f"[DEBUG] 다운로드 URL: {download_url}")  # 디버깅 로그 추가
                for i in range(0, 33):
                    self.ui.progressBar.setValue(i)
                    time.sleep(0.05)
                if download_update(download_url):
                    self.set_status_text("<strong>업데이트 완료</strong> 설치 중...")
                    for i in range(33, 53):
                        self.ui.progressBar.setValue(i)
                        time.sleep(0.05)
                    install_update(latest_version)
                    set_current_version(latest_version)  # 새로운 버전 저장
                    for i in range(53, 100):
                        self.ui.progressBar.setValue(i)
                        time.sleep(0.05)
                    self.set_status_text("<strong>업데이트 완료! 프로그램을 재시작합니다.</strong>")
                else:
                    QMessageBox.critical(self, "업데이트 실패", "업데이트 파일 다운로드에 실패했습니다.")
                    self.set_status_text("<strong>업데이트 실패</strong>")
                    QTimer.singleShot(2000, sys.exit)
                    return
            else:
                self.set_status_text("<strong>최신 버전입니다.</strong>")
                self.ui.progressBar.setValue(100)  # ProgressBar 100%로 설정
        else:
            QMessageBox.warning(self, "업데이트 확인 실패", "릴리스 정보를 가져올 수 없습니다.")
            self.set_status_text("<strong>업데이트 확인 실패</strong>")
            QTimer.singleShot(2000, sys.exit)
    
        QTimer.singleShot(1000, launch_main_application)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoadingScreen()
    window.show()
    sys.exit(app.exec())