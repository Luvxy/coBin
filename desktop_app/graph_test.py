import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT  # NavigationToolbar2QT 임포트

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Graph Example")

        # Matplotlib Figure 생성
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        # PyQt5 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # 그래프 그리기
        self.plot_graph()

        # Matplotlib 툴바 표시 (선택 사항)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)  # NavigationToolbar2QT 사용
        layout.addWidget(self.toolbar)

    def plot_graph(self):
        # 예시 데이터
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 1, 5, 3]

        # 그래프 추가
        self.ax.plot(x, y)

        # 그래프 업데이트
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())