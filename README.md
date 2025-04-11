# coBin: 자동 코인 트레이딩 시스템

## 📌 소개
**coBin**은 사용자 맞춤형 전략을 기반으로 자동 매매를 수행할 수 있는 데스크탑 애플리케이션입니다.  
GUI를 통해 매매 전략을 자유롭게 설계하고, 실시간 데이터를 반영하여 자동 매수/매도를 실행할 수 있습니다.

## 🛠️ 주요 기능
- **블록 기반 전략 구성**: 조건과 액션을 조합하여 매매 전략 구성
- **실시간 Upbit API 연동**: 현재가, 잔고, 수익률 등 정보 실시간 조회
- **전략 저장 및 불러오기**: JSON 기반으로 전략 저장 및 로드 가능
- **시장가 매수/매도**: 직접 입력 또는 % 입력으로 거래 실행
- **백테스트 기능**: 과거 데이터 기반으로 전략 수익률 확인
- **Django 서버 연동**: 로그인/유저 포인트/실시간 데이터 연동 (WebSocket 포함)
- **작은 창 모드 지원**: 최소화된 상태에서도 전략 실행 가능
- **도움말 및 패치노트 보기**: PDF 뷰어 내장

## 📁 프로젝트 구조
```
project/
├── main.py                  # 메인 프로그램
├── ui/                      # PySide6 UI 파일 모음
├── upbit/                   # 업비트 관련 API 및 설정
├── resources/               # GIF, PDF 등 리소스 파일
├── static/error_docs.md     # 에러 코드 문서
├── templates/error.html     # 에러 뷰어 HTML
├── base_exceptions.py       # 에러 코드 및 예외 정의
├── README.md                # 프로젝트 설명 파일
```

## ✅ 실행 방법
```bash
pip install -r requirements.txt
python main.py
```

※ 실행 시 이미 켜져 있는 경우 중복 실행 방지됨.

## 🔐 로그인 계정 (테스트용)
- ID: `brunch`
- PW: `qaz4455!`

## 💬 기술 스택
- Python (PySide6, requests, asyncio)
- Upbit API
- Django + DRF + WebSocket
- pyqtgraph
- Firebase (로그 기록용)

## 📦 설치 패키지
`requirements.txt` 참고

## 📜 라이선스
본 프로젝트는 비상업적 목적으로만 사용 가능합니다.
