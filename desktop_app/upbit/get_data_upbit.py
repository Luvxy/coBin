from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QCandlestickSeries, QChart, QChartView, QDateTimeAxis, QValueAxis, QCandlestickSet
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QDateTime, QThread, Signal
import pyupbit
import time
from pandas import Series


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
    def __init__(self, parent=None, coin="KRW-BTC"):
        super().__init__(parent)
        self.coin = coin
        self.init_ui()

    def init_ui(self):
        self.worker = Worker(self.coin)
        self.worker.price.connect(self.get_price)
        self.worker.start()

        self.ticks = Series(dtype='float64')

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

        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%i")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        layout = QVBoxLayout()
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

        self.load_data()

    def load_data(self):
        """코인 차트 데이터를 로드"""
        df = pyupbit.get_ohlcv(self.coin, interval='minute1', count=80)
        if df is None:
            return

        self.series.clear()  # 👉 기존 차트 데이터 삭제
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

    def change_coin(self, new_coin):
        """코인을 변경하고 새로운 차트를 로드"""
        if self.coin == new_coin:
            return  # 👉 같은 코인 선택 시 무시

        print(f"코인 변경: {self.coin} → {new_coin}")

        # ✅ 기존 쓰레드 안전 종료
        self.worker.stop()

        # ✅ 새로운 코인으로 차트 업데이트
        self.coin = new_coin
        self.series.clear()  # 👉 기존 차트 데이터 삭제
        self.load_data()  # 👉 새 코인 데이터 로드

        # ✅ 새 워커 쓰레드 시작
        self.worker = Worker(new_coin)
        self.worker.price.connect(self.get_price)
        self.worker.start()
