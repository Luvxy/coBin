from PySide6.QtWidgets import *
from PySide6.QtCharts import QCandlestickSeries, QChart, QChartView, QDateTimeAxis, QValueAxis, QCandlestickSet
from PySide6.QtGui import QPainter, QPen, QColor, QCursor
from PySide6 import QtGui
from PySide6.QtCore import Qt, QDateTime, QThread, Signal, QTimer
import pyupbit
import time
from pandas import Series
import sys
import requests  # 1) requests 라이브러리 추가


class Worker(QThread):
    price = Signal(float)

    def __init__(self, coin="KRW-BTC"):
        super().__init__()
        self.coin = coin
        self.running = True

    def run(self):
        while self.running:
            cur_price = pyupbit.get_current_price(self.coin)
            if cur_price:
                self.price.emit(cur_price)
            time.sleep(1)

    def change_coin(self, coin):
        self.coin = coin

    def stop(self):
        """쓰레드 안전 종료"""
        self.running = False
        self.wait()  # 👉 기존 쓰레드가 안전하게 종료될 때까지 대기


class ChartWidget(QWidget):
    def __init__(self, parent=None, coin="KRW-BTC", interval='minute30', count=80):
        super().__init__(parent)
        self.coin = coin
        self.interval = interval
        self.count = count
        self.axis_y = QValueAxis()
        self.ticks = {}
        self.tooltip_timer = QTimer(self)  # 툴팁 갱신용 타이머
        self.tooltip_timer.setInterval(100)  # 500ms마다 갱신
        self.tooltip_timer.timeout.connect(self.update_tooltip)
        self.current_tooltip_text = ""  # 현재 툴팁 텍스트
        self.current_tooltip_pos = None  # 현재 툴팁 위치
        self.init_ui()

    def init_ui(self):
        self.worker = Worker(self.coin)
        self.worker.price.connect(self.get_price)
        self.worker.start()

        self.series = QCandlestickSeries()
        self.series.setIncreasingColor("#FF0000")  # 상승 캔들 색상 (빨간색)
        self.series.setDecreasingColor("#00FFFF")  # 하락 캔들 색상 (파랑색)

        # ✅ 캔들 외곽선 설정
        self.series.setBodyOutlineVisible(True)  # 외곽선 표시
        self.series.setPen(QtGui.QPen(QtGui.QColor("#000000"), 1))  # 외곽선 색상: 하얀색, 두께: 1px

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.series)

        # ✅ 차트 스타일 설정
        self.chart.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("#1C1F26")))  # 더 어두운 배경색
        self.chart.setPlotAreaBackgroundBrush(QtGui.QBrush(QtGui.QColor("#2B303B")))  # 플롯 영역 배경색
        self.chart.setPlotAreaBackgroundVisible(True)
        
        # X축 설정
        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("hh:mm:ss")
        self.axis_x.setLabelsBrush(QtGui.QBrush(QtGui.QColor("#D8DEE9")))  # X축 라벨 색상
        self.axis_x.setLinePen(QtGui.QPen(QtGui.QColor("#4C566A")))  # X축 선 색상
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        # Y축 설정
        self.axis_y.setLabelFormat("%i")
        self.axis_y.setLabelsBrush(QtGui.QBrush(QtGui.QColor("#D8DEE9")))  # Y축 라벨 색상
        self.axis_y.setLinePen(QtGui.QPen(QtGui.QColor("#4C566A")))  # Y축 선 색상
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)
        
        # ✅ 격자 제거
        self.chart.setPlotAreaBackgroundVisible(False)
        
        self.load_data(self.interval, self.count)
        
        self.series.hovered.connect(self.show_tooltip)  # hovered 신호 연결
        
        QApplication.instance().setStyleSheet("""
            QToolTip {
                background-color: #2E3440;  /* 툴팁 배경색 */
                color: #D8DEE9;  /* 툴팁 글자 색상 */
                border: 1px solid #4C566A;  /* 툴팁 테두리 색상 */
                border-radius: 5px;  /* 모서리 둥글게 */
                padding: 5px;  /* 내부 여백 */
                font-size: 12px;  /* 글자 크기 */
            }
        """)

        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        layout = QVBoxLayout()
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

    def load_data(self, interval='minute30', count=80):
        """코인 차트 데이터를 로드"""
        df = pyupbit.get_ohlcv(self.coin, interval=interval, count=count)
        if df is None:
            print(f"코인 데이터 로드 실패: {self.coin}")
            return

        self.series.clear()
        for index in df.index:
            open_price = df.loc[index, 'open']
            high = df.loc[index, 'high']
            low = df.loc[index, 'low']
            close = df.loc[index, 'close']

            format = "%Y-%m-%d %H:%M:%S"
            str_time = index.strftime(format)
            dt = QDateTime.fromString(str_time, "yyyy-MM-dd hh:mm:ss")
            ts = dt.toMSecsSinceEpoch()

            elem = QCandlestickSet(open_price, high, low, close, ts)
            self.series.append(elem)
        
        self.update_axis_y(df['low'].min(), df['high'].max())
        self.update_axis_x()
    
    def update_axis_x(self):
        """X축 범위를 interval과 count에 맞게 조정"""
        if not self.series.sets():
            print("차트 데이터가 없어 X축을 설정할 수 없습니다.")
            return
        
        first_time = int(self.series.sets()[0].timestamp())
        last_time = int(self.series.sets()[-1].timestamp())
        
        self.axis_x.setRange(QDateTime.fromMSecsSinceEpoch(first_time), QDateTime.fromMSecsSinceEpoch(last_time))
    
    def update_axis_y(self, min_val, max_val):
        """Y축 범위를 설정"""
        margin = max((max_val - min_val) * 0.05, 1)  # 최소 마진 설정
        self.axis_y.setRange(min_val - margin, max_val + margin)

    def get_price(self, cur_price):
        """실시간 가격 업데이트"""
        dt = QDateTime.currentDateTime()
        self.ticks[dt] = cur_price

        ts = dt.toMSecsSinceEpoch()
        sets = self.series.sets()
        last_set = sets[-1] if sets else None

        if last_set:
            open_price = last_set.open()
            high = max(last_set.high(), cur_price)
            low = min(last_set.low(), cur_price)
            new_set = QCandlestickSet(open_price, high, low, cur_price, last_set.timestamp())
            self.series.remove(last_set)
            self.series.append(new_set)
            
    def change_coin(self, new_coin, interval='minute30', count=80):
        """코인을 변경하고 새로운 차트를 로드"""        
        print(f"코인 변경: {self.coin} → {new_coin}")

        self.worker.stop()

        self.coin = new_coin
        self.interval = interval
        self.count = count
        self.series.clear()
        self.load_data(interval, count)

        self.worker = Worker(new_coin)
        self.worker.price.connect(self.get_price)
        self.worker.start()
        
    def show_tooltip(self, state: bool, candlestick_set: QCandlestickSet):
        """캔들 위에 마우스를 올릴 때 툴팁 표시"""
        if state:  # 마우스가 캔들 위에 있을 때
            if not isinstance(candlestick_set, QCandlestickSet):
                return  # candlestick_set이 QCandlestickSet이 아니면 무시

            open_price = candlestick_set.open()
            close_price = candlestick_set.close()
            low_price = candlestick_set.low()
            high_price = candlestick_set.high()
            change_rate = ((close_price - open_price) / open_price) * 100

            # 상승률 색상 설정
            change_rate_color = "#FF4C4C" if change_rate > 0 else "#4C9FFF"

            # 툴팁 텍스트 생성
            tooltip_text = (
                f"시가: {open_price:.2f}<br>"
                f"종가: {close_price:.2f}<br>"
                f"최저가: {low_price:.2f}<br>"
                f"최고가: {high_price:.2f}<br>"
                f"<span style='color: {change_rate_color};'>"
                f"변동률: {change_rate:.2f}%</span>"
            )

            # 툴팁 표시
            self.current_tooltip_text = tooltip_text
            self.current_tooltip_pos = QCursor.pos()
            QToolTip.showText(self.current_tooltip_pos, tooltip_text, self.chart_view)

            # 타이머 시작
            self.tooltip_timer.start()
        else:  # 마우스가 캔들에서 벗어날 때
            QToolTip.hideText()
            self.tooltip_timer.stop()

    def update_tooltip(self):
        """툴팁을 갱신하여 사라지지 않도록 유지"""
        if self.current_tooltip_text and self.current_tooltip_pos:
            QToolTip.showText(self.current_tooltip_pos, self.current_tooltip_text, self.chart_view)
    
class OrderBookWidget(QWidget):
    def __init__(self, coin_symbol="KRW-BTC"):
        super().__init__()
        self.coin_symbol = coin_symbol
        self.setWindowTitle(f"OrderBook - {self.coin_symbol}")

        layout = QVBoxLayout(self)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(20)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)

        # ✅ 테이블 스타일 설정
        self.tableWidget.setStyleSheet("""
            QTableWidget {
                background-color: #2E3440;  /* 테이블 배경색 */
                border: 2px solid #4C566A;  /* 테두리 색상 */
                gridline-color: #4C566A;  /* 셀 간격선 색상 */
                border-radius: 8px;  /* 모서리 둥글게 */
            }
            QTableWidget::item {
                color: #D8DEE9;  /* 글자 색상 */
                padding: 5px;  /* 셀 내부 여백 */
            }
            QTableWidget::item:selected {
                background-color: #81A1C1;  /* 선택된 셀 배경색 */
                color: #2E3440;  /* 선택된 셀 글자 색상 */
            }
        """)

        # ✅ 크기 자동 조정 설정
        self.tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # ✅ 스크롤 제거
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        # ✅ 타이머 설정 (2초마다 업데이트)
        self.timer = QTimer(self)
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self.update_orderbook)
        self.timer.start()

        self.update_orderbook()

    def change_coin(self, coin_symbol):
        """코인 변경 후 즉시 업데이트"""
        self.coin_symbol = coin_symbol
        self.setWindowTitle(f"OrderBook - {self.coin_symbol}")
        self.update_orderbook()

    def resizeEvent(self, event):
        """부모 위젯 크기에 맞게 자동 조정"""
        table_width = self.width()
        self.tableWidget.setColumnWidth(0, int(table_width * 0.38))
        self.tableWidget.setColumnWidth(1, int(table_width * 0.2))
        self.tableWidget.setColumnWidth(2, int(table_width * 0.38))
        super().resizeEvent(event)

    def update_orderbook(self):
        """Upbit API에서 호가 데이터를 가져와 업데이트"""
        url = f"https://api.upbit.com/v1/orderbook?markets={self.coin_symbol}"
        response = requests.get(url)
        if response.status_code != 200:
            return

        data = response.json()
        if not data:
            return

        orderbook_units = data[0]['orderbook_units']

        # 테이블 초기화
        for r in range(20):
            for c in range(3):
                self.tableWidget.setItem(r, c, QTableWidgetItem(""))
                self.tableWidget.setCellWidget(r, c, None)

        max_size = max([unit['ask_size'] for unit in orderbook_units] + [unit['bid_size'] for unit in orderbook_units])

        # 상위 10개 매도(asks)와 하위 10개 매수(bids) 데이터 가져오기
        asks = orderbook_units[:10][::-1]  # 매도는 역순으로 표시
        bids = orderbook_units[:10]

        # 매도(asks)
        for i, ask in enumerate(asks):
            price = ask['ask_price']
            size = ask['ask_size']

            item = QTableWidgetItem(format(int(price), ","))
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableWidget.setItem(i, 1, item)

            self.set_progress_bar(i, 0, size, max_size, "#ff6666", True)  # 빨간색 ProgressBar

        # 매수(bids)
        for i, bid in enumerate(bids, start=10):
            price = bid['bid_price']
            size = bid['bid_size']

            item = QTableWidgetItem(format(int(price), ","))
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableWidget.setItem(i, 1, item)

            self.set_progress_bar(i, 2, size, max_size, "#66b3ff", False)  # 파란색 ProgressBar

    def set_progress_bar(self, row, col, size, max_size, color, inverted):
        """호가 수량을 시각적으로 나타내는 ProgressBar 설정"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        pbar = QProgressBar()
        pbar.setFixedHeight(20)
        pbar.setInvertedAppearance(inverted)
        pbar.setAlignment(Qt.AlignRight | Qt.AlignVCenter if inverted else Qt.AlignLeft | Qt.AlignVCenter)
        pbar.setRange(0, int(max_size))
        pbar.setFormat(f"{size:.2f}")  # 소수점 2자리까지 표시
        pbar.setValue(int(size))
        pbar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #3B4252;  /* ProgressBar 배경색 */
                border: 1px solid #4C566A;  /* ProgressBar 테두리 */
                border-radius: 5px;  /* 모서리 둥글게 */
                text-align: center;  /* 텍스트 중앙 정렬 */
                padding: 0px 5px;  /* 좌우 여백 5px */
            }}
            QProgressBar::chunk {{
                background-color: {color};  /* ProgressBar 색상 */
                border-radius: 5px;  /* 모서리 둥글게 */
            }}
        """)
        layout.addWidget(pbar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignVCenter)
        widget.setLayout(layout)
        self.tableWidget.setCellWidget(row, col, widget)
