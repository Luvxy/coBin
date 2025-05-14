import sys
import sqlite3
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox
)

class SQLiteBrowser(QWidget):
    def __init__(self, db_path="C:/Users/user/Desktop/coding/coBin/coBin/cobin/db.sqlite3"):
        super().__init__()
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.init_ui()
        self.load_tables()
    
    def init_ui(self):
        self.setWindowTitle("SQLite3 관리자")
        self.resize(800, 600)
        layout = QVBoxLayout(self)
        
        control_layout = QHBoxLayout()
        # DB 파일 선택 버튼
        self.open_btn = QPushButton("열기")
        self.open_btn.clicked.connect(self.open_db)
        control_layout.addWidget(self.open_btn)
        self.table_combo = QComboBox()
        self.table_combo.currentTextChanged.connect(self.load_data)
        control_layout.addWidget(self.table_combo)
        
        self.add_btn = QPushButton("추가")
        self.add_btn.clicked.connect(self.add_row)
        control_layout.addWidget(self.add_btn)
        
        self.delete_btn = QPushButton("삭제")
        self.delete_btn.clicked.connect(self.delete_row)
        control_layout.addWidget(self.delete_btn)
        
        self.save_btn = QPushButton("저장")
        self.save_btn.clicked.connect(self.save_changes)
        control_layout.addWidget(self.save_btn)
        
        layout.addLayout(control_layout)
        
        self.table_widget = QTableWidget()
        self.table_widget.setEditTriggers(QTableWidget.AllEditTriggers)
        layout.addWidget(self.table_widget)
    
    def open_db(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "DB 파일 선택", "", "SQLite DB Files (*.sqlite3 *.db);;All Files (*)"
        )
        if file_path:
            # 기존 연결 종료 후 새 DB 연결
            self.conn.close()
            self.conn = sqlite3.connect(file_path)
            self.conn.row_factory = sqlite3.Row
            self.db_path = file_path
            self.load_tables()
            self.table_widget.clear()
        
    def load_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row["name"] for row in cursor.fetchall()]
        self.table_combo.clear()
        self.table_combo.addItems(tables)
    
    def load_data(self, table_name):
        if not table_name:
            return
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [col["name"] for col in cursor.fetchall()]
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        
        self.table_widget.clear()
        self.table_widget.setColumnCount(len(columns))
        self.table_widget.setHorizontalHeaderLabels(columns)
        self.table_widget.setRowCount(len(rows))
        
        for i, row in enumerate(rows):
            for j, col in enumerate(columns):
                item = QTableWidgetItem(str(row[col]))
                self.table_widget.setItem(i, j, item)
    
    def add_row(self):
        row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(row_count)
    
    def delete_row(self):
        selected = self.table_widget.selectionModel().selectedRows()
        for idx in sorted(selected, reverse=True):
            self.table_widget.removeRow(idx.row())
    
    def save_changes(self):
        table_name = self.table_combo.currentText()
        if not table_name:
            return
        cursor = self.conn.cursor()
        columns = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]
        try:
            cursor.execute("BEGIN")
            cursor.execute(f"DELETE FROM {table_name}")
            for i in range(self.table_widget.rowCount()):
                values = [
                    self.table_widget.item(i, j).text() if self.table_widget.item(i, j) else None
                    for j in range(self.table_widget.columnCount())
                ]
                placeholders = ",".join(["?"] * len(values))
                cursor.execute(
                    f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})",
                    values
                )
            self.conn.commit()
            QMessageBox.information(self, "성공", "변경사항이 저장되었습니다.")
        except Exception as e:
            self.conn.rollback()
            QMessageBox.critical(self, "오류", f"저장 실패: {e}")
    
    def closeEvent(self, event):
        self.conn.close()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SQLiteBrowser("db.sqlite3")
    window.show()
    sys.exit(app.exec())