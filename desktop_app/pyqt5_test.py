import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

class DraggableLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("background-color: lightblue; padding: 10px; border: 1px solid black;")
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.text())
            drag.setMimeData(mime_data)
            drag.exec_(Qt.MoveAction)

class DropFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: lightgray; border: 2px dashed black;")
        self.setFixedSize(200, 200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        label = DraggableLabel(event.mimeData().text())
        self.layout.addWidget(label)
        event.acceptProposedAction()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Drag and Drop Example")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.label = DraggableLabel("드래그할 블럭")
        self.drop_frame = DropFrame()

        layout.addWidget(self.label)
        layout.addWidget(self.drop_frame)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
