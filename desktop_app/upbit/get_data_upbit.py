from PySide6.QtWidgets import *
from PySide6.QtCharts import QCandlestickSeries, QChart, QChartView, QDateTimeAxis, QValueAxis, QCandlestickSet
from PySide6.QtGui import QPainter
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
        self.init_ui()

    def init_ui(self):
        self.worker = Worker(self.coin)
        self.worker.price.connect(self.get_price)
        self.worker.start()

        self.series = QCandlestickSeries()
        self.series.setIncreasingColor(Qt.red)
        self.series.setDecreasingColor(Qt.blue)

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.series)

        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("hh:mm:ss")
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        self.axis_y.setLabelFormat("%i")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)
        
        self.load_data(self.interval, self.count)

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
    
    def load_data(self, interval='minute30', count=80):
        """코인 차트 데이터를 로드"""
        df = pyupbit.get_ohlcv(self.coin, interval=interval, count=count)
        if df is None or df.empty:
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
        
        first_time = max(first_time, -9223372036854775808)  # 최소값 제한
        last_time = min(last_time, 9223372036854775807)  # 최대값 제한
        
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
        if self.coin == new_coin:
            return
        
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

        # ✅ 크기 자동 조정 설정
        self.tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # ✅ 스크롤 제거
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        # ✅ 타이머 설정 (2초마다 업데이트)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
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
        self.tableWidget.setColumnWidth(0, int(table_width * 0.4))
        self.tableWidget.setColumnWidth(1, int(table_width * 0.2))
        self.tableWidget.setColumnWidth(2, int(table_width * 0.4))
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

            self.set_progress_bar(i, 0, size, max_size, "blue", True)

        # 매수(bids)
        for i, bid in enumerate(bids, start=10):
            price = bid['bid_price']
            size = bid['bid_size']

            item = QTableWidgetItem(format(int(price), ","))
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableWidget.setItem(i, 1, item)

            self.set_progress_bar(i, 2, size, max_size, "red", False)

    def set_progress_bar(self, row, col, size, max_size, color, inverted):
        """호가 수량을 시각적으로 나타내는 ProgressBar 설정"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        pbar = QProgressBar()
        pbar.setFixedHeight(20)
        pbar.setInvertedAppearance(inverted)
        pbar.setAlignment(Qt.AlignRight | Qt.AlignVCenter if inverted else Qt.AlignLeft | Qt.AlignVCenter)
        pbar.setRange(0, int(max_size))
        pbar.setFormat(str(size))
        pbar.setValue(int(size))
        pbar.setStyleSheet(f"""
            QProgressBar {{background-color : rgba(0, 0, 0, 0%); border: 1}}
            QProgressBar::Chunk {{background-color : rgba({'0, 0, 255' if color == 'blue' else '255, 0, 0'}, 20%); border: 1}}
        """)
        layout.addWidget(pbar)
        layout.setContentsMargins(0,0,0,0)
        layout.setAlignment(Qt.AlignVCenter)
        widget.setLayout(layout)
        self.tableWidget.setCellWidget(row, col, widget)
