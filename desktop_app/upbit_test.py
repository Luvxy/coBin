from PySide6.QtCharts import QChart, QChartView, QCandlestickSeries, QCandlestickSet
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QPointF

class CustomChart(QChart):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.drawing = False  # 그리기 모드 활성화 여부
        self.last_point = None  # 마지막 마우스 위치
        self.pen = QPen(QColor("#FFFFFF"), 2)  # 기본 펜 설정

    def mousePressEvent(self, event):
        """마우스 클릭 이벤트 처리"""
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """마우스 이동 이벤트 처리"""
        if self.drawing and self.last_point:
            painter = QPainter(self)
            painter.setPen(self.pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            painter.end()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """마우스 버튼 해제 이벤트 처리"""
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.last_point = None
        super().mouseReleaseEvent(event)
        
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow
    
    app = QApplication(sys.argv)
    window = QMainWindow()
    chart = CustomChart()
    chart.setTitle("Custom Chart")
    chart.setAnimationOptions(QChart.SeriesAnimations)
    window.setCentralWidget(QChartView(chart))
    window.show()
    sys.exit(app.exec_())