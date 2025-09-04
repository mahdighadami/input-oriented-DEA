from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QStyledItemDelegate, QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
import numpy as np
import CCRModel
import det_out


class FloatDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        # Skip first column (DMU names)
        if index.column() == 0:
            return super().createEditor(parent, option, index)

        editor = QLineEdit(parent)
        validator = QtGui.QDoubleValidator(bottom=0, top=1e100, decimals=10)
        validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        editor.setValidator(validator)
        return editor


class DetTable(QtWidgets.QMainWindow):
    backBtnSignal = pyqtSignal()
    destroySignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DEA Input Page")
        self.resize(1000, 700)
        self.center_on_screen()
        
    def center_on_screen(self):
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)


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

            /* Vertical scrollbar */
            QScrollBar:vertical {
                background: #e6faff;
                width: 12px;
                margin: 2px 0 2px 0;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #66ccff;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #33bbff;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }

            /* Horizontal scrollbar */
            QScrollBar:horizontal {
                background: #e6faff;
                height: 12px;
                margin: 0 2px 0 2px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background: #66ccff;
                min-width: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #33bbff;
            }
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: none;
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

        # Preallocation for single output
        if self.n_output == 1:
            for row in range(self.table.rowCount()):
                self.table.item(row, self.table.columnCount()-1).setText("1")

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
                    dlg.setText("You have entered data. Are you sure you want to go back? Unsaved data will be lost!")
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
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and item.text().strip() == "":
                    dlg = QtWidgets.QMessageBox(self)
                    dlg.setWindowTitle("Incomplete Data")
                    dlg.setText("Please fill in all fields before submitting.")
                    dlg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    dlg.setIcon(QtWidgets.QMessageBox.Warning)
                    dlg.exec()
                    return
                
        # Collect data from the table
        X = []
        Y = []
        for row in range(self.table.rowCount()):
            inputs = []
            outputs = []
            for col in range(1, self.n_input + 1):
                val = float(self.table.item(row, col).text())
                inputs.append(val)
            for col in range(self.n_input + 1, self.table.columnCount()):
                val = float(self.table.item(row, col).text())
                outputs.append(val)
            X.append(inputs)
            Y.append(outputs)

        X = np.array(X)  # shape: (n_dmu, n_input)
        Y = np.array(Y)  # shape: (n_dmu, n_output)
        

        # Create the model instance
        self.model = CCRModel.CCR_Model(X, Y)
        
        if self.model_type == 'weak-efficiency': 
            theta = [x.item() for x in self.model.basic_rank_dmus()]
        elif self.model_type == 'efficiency':
            theta = [x.item() for x in self.model.slack_rank_dmus()]
        else:
            theta = [x.item() for x in self.model.super_rank_dmus()]

        dmu_names = []
        for row in range(self.table.rowCount()):
            dmu_names.append(self.table.item(row, 0).text())

        # Create the output page
        self.output_page = det_out.DetOut()
        self.output_page.backBtnSignal.connect(self.show)
        self.output_page.destroySignal.connect(self.close_outer)
        self.output_page.set_data(theta, dmu_names, self.model_type)
        self.output_page.setWindowTitle("Output")
        self.output_page.show()
        self.hide()

    def close_outer(self):
        self.destroySignal.emit()
        self.close()



        

        
