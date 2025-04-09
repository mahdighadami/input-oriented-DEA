from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QStyledItemDelegate, QLineEdit
)
from PyQt5.QtCore import Qt


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
        self.table.setHorizontalHeaderLabels(col_labels)  # ✔️ Set headers first

        # 🎨 Then apply your style
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #ff66b3;  /* soft pink borders */
                background-color: #cceeff;  /* light blue cells */
                selection-background-color: #99e6ff;  /* slightly darker blue for selection */
            }

            QTableWidget::item:selected {
                color: red;  /* change font color to red when selected */
            }

            QHeaderView::section {
                background-color: #99ffcc;  /* mint for headers */
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

        # Center the button
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch()

        # Add widgets to main layout
        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout)
        self.setCentralWidget(central_widget)


    

    
