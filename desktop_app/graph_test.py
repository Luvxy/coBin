from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, QPoint

class FramelessWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # ✅ 프레임 없는 창
        self.setStyleSheet("background-color: #2E2E2E; border-radius: 10px;")

        # 드래그 이동 관련 변수
        self.old_pos = None  

        # 상단 바 (버튼 영역)
        self.top_bar = QWidget()
        self.top_bar.setFixedHeight(40)
        self.top_bar.setStyleSheet("background-color: #444; border-top-left-radius: 10px; border-top-right-radius: 10px;")

        # 버튼 (닫기, 최소화, 최대화)
        self.close_btn = QPushButton("✕")
        self.minimize_btn = QPushButton("━")
        self.maximize_btn = QPushButton("▢")

        self.close_btn.setFixedSize(30, 30)
        self.minimize_btn.setFixedSize(30, 30)
        self.maximize_btn.setFixedSize(30, 30)

        # 버튼 스타일
        for btn in [self.close_btn, self.minimize_btn, self.maximize_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    border: none; color: white; font-size: 14px;
                    background-color: #444; border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #666;
                }
            """)

        # 버튼 이벤트 연결
        self.close_btn.clicked.connect(self.close)
        self.minimize_btn.clicked.connect(self.showMinimized)
        self.maximize_btn.clicked.connect(self.toggle_maximize_restore)

        # 레이아웃 설정
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.minimize_btn)
        button_layout.addWidget(self.maximize_btn)
        button_layout.addWidget(self.close_btn)

        top_layout = QHBoxLayout(self.top_bar)
        top_layout.addLayout(button_layout)

        # 전체 레이아웃
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.top_bar)
        
        self.setLayout(main_layout)

    def toggle_maximize_restore(self):
        """최대화 / 원래 크기 토글"""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event):
        """창 이동 시작"""
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        """창 이동"""
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        """이동 끝"""
        self.old_pos = None

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = FramelessWindow()
    window.show()
    sys.exit(app.exec_())