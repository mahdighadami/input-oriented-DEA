from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QStyledItemDelegate, QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

class FloatDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        # Skip first column (DMU names)
        if index.column() == 0:
            return super().createEditor(parent, option, index)

        editor = QLineEdit(parent)
        validator = QtGui.QDoubleValidator(bottom=-1e100, top=1e100, decimals=10)
        validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        editor.setValidator(validator)
        return editor


class DetModel(QtWidgets.QMainWindow):
    backBtnSignal = pyqtSignal()
    destroySignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DEA Input Page")
        self.resize(800, 600)
        self.center_on_screen()
        
    def center_on_screen(self):
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def closeEvent(self, event):
        if event.spontaneous():
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Exit?")
            dlg.setText("Are you sure to Exit the program?")
            dlg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            dlg.setIcon(QtWidgets.QMessageBox.Question)
            button = dlg.exec()
            if button == QtWidgets.QMessageBox.Yes:
                event.accept()
                self.destroySignal.emit()
            else:
                event.ignore()

    def back_page(self):
        for row in range(self.table.rowCount()):
            for col in range(1, self.table.columnCount()):
                item = self.table.item(row, col)
                if item and item.text().strip() != "":
                    dlg = QtWidgets.QMessageBox(self)
                    dlg.setWindowTitle("Unsaved Data")
                    dlg.setText("You have entered data. Are you sure you want to go back? Unsaved data will be lost.")
                    dlg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    dlg.setIcon(QtWidgets.QMessageBox.Question)
                    button = dlg.exec()
                    if button == QtWidgets.QMessageBox.Yes:
                        self.backBtnSignal.emit()
                        self.close()
                        return
                    else:
                        return
                    
        self.backBtnSignal.emit()
        self.close()


    def submit_page(self):
        pass

    def set_data(self, data):
        self.n_dmu = data['n_dmu']
        self.n_input = data['n_input']
        self.n_output = data['n_output']
        self.model_type = data['model']

        self.init_table()

    def init_table(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Create and configure the table
        col_labels = (
            ["DMU"] +
            [f"Input {i+1}" for i in range(self.n_input)] +
            [f"Output {i+1}" for i in range(self.n_output)]
        )
        total_columns = len(col_labels)

        self.table = QTableWidget(self.n_dmu, total_columns)
        self.table.setHorizontalHeaderLabels(col_labels)  

        # apply style
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #ff66b3;
                background-color: #cceeff;
                selection-background-color: #99e6ff;
            }
            QTableWidget::item:selected {
                color: red;
            }
            QHeaderView::section {
                background-color: #99ffcc;
                padding: 4px;
                border: 1px solid #ff66b3;
                font-weight: bold;
            }
            QTableWidget::item {
                border: 1px solid #ff66b3;
                background-color: #cceeff;
            }
        """)

        # Apply the float-only delegate
        delegate = FloatDelegate()
        self.table.setItemDelegate(delegate)

        for row in range(self.n_dmu):
            for col in range(total_columns):
                item = QTableWidgetItem()
                if col == 0:
                    item.setText(f"DMU {row+1}")
                else:
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

        # Create the submit button
        self.submit_button = QtWidgets.QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_page)
        self.submit_button.setFixedSize(120, 40)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #e6f7ff;
                color: #003366;
                font-weight: bold;
                border: 2px solid #b3d9ff;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #cceeff;
                border: 2px solid #3399ff;
            }
        """)

        # Create the back button
        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.clicked.connect(self.back_page)
        self.back_button.setFixedSize(120, 40)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #ffe6e6;
                color: #660000;
                font-weight: bold;
                border: 2px solid #ff9999;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #ffcccc;
                border: 2px solid #ff6666;
            }
        """)

        # Center both buttons in the layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.back_button)
        button_layout.addSpacing(20)  # space between buttons
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch()

        # Add widgets to main layout
        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout)
        self.setCentralWidget(central_widget)


        

        
