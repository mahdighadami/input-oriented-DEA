from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import pyqtSignal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class DetOut(QtWidgets.QMainWindow):
    backBtnSignal = pyqtSignal()
    destroySignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.resize(1500, 950)
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
        self.backBtnSignal.emit()
        self.close()


    def set_data(self, thetas, dmu_names, model_type):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Labels for DMU names
        dmu_row = QHBoxLayout()
        dmu_row.addWidget(QLabel("DMUs:"))
        for name in dmu_names:
            label = QLabel(name)
            label.setStyleSheet("font-weight: bold; padding: 10px;")
            dmu_row.addWidget(label)
        layout.addLayout(dmu_row)

        # Labels for Theta values
        theta_row = QHBoxLayout()
        theta_row.addWidget(QLabel("Thetas:"))
        for val in thetas:
            label = QLabel(f"{val:.4f}")
            label.setStyleSheet("color: blue; padding: 10px;")
            theta_row.addWidget(label)
        layout.addLayout(theta_row)

        # Bar Plot of Thetas
        fig, ax = plt.subplots()
        ax.bar(dmu_names, thetas, color='skyblue')
        ax.set_title("Efficiency Scores (Theta)")
        ax.set_ylabel("Theta")
        ax.set_xticks(range(len(dmu_names)))
        ax.set_xticklabels(dmu_names, rotation=45)

        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(canvas)

        # Analysis Section
        self.analysis_box = QtWidgets.QPlainTextEdit()
        self.analysis_box.setReadOnly(True)
        self.analysis_box.setPlaceholderText("the results...")
        self.analysis_box.setFont(QtGui.QFont("Arial", 10))
        self.analysis_box.setFixedHeight(300) 
        self.analysis_box.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        self.analysis_box.setStyleSheet("""
            QPlainTextEdit {
                font-size: 16px;
                padding: 10px;
                border: 2px solid #cccccc;
                border-radius: 10px;
                background-color: #ffffff;
                color: #2c3e50;
            }
            
            QScrollBar:vertical {
                border: none;
                background: #f2f2f2;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background: #a0aab5;
                min-height: 20px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical:hover {
                background: #8795a1;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        self.analysis_box.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.analysis_box.setMinimumHeight(200)
        layout.addWidget(self.analysis_box)

        # Back Button
        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.clicked.connect(self.back_page)
        layout.addWidget(self.back_button)
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

        # Center the button
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.back_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)


        # Set the central widget and layout
        self.setCentralWidget(central_widget)
        # Start analysis
        self.analyze_results(thetas, dmu_names, model_type)



    def analyze_results(self, thetas, dmu_names, model_type):
        average_theta = sum(thetas) / len(thetas)
        max_theta = max(thetas)
        min_theta = min(thetas)
        best_indices = [i for i, val in enumerate(thetas) if val == max_theta]
        worst_indices = [i for i, val in enumerate(thetas) if val == min_theta]

        best_dmus = ', '.join([dmu_names[i] for i in best_indices])
        worst_dmus = ', '.join([dmu_names[i] for i in worst_indices])

        analysis = f"""Model Type: {model_type}
        Average Efficiency (θ): {average_theta:.4f}

        Most Efficient DMU(s): {best_dmus} (θ = {max_theta:.4f})
        Least Efficient DMU(s): {worst_dmus} (θ = {min_theta:.4f})

        Comparison:
        """

        # Compare each DMU to the others
        for i, dmu in enumerate(dmu_names):
            if thetas[i] == max_theta:
                comment = "is among the most efficient."
            elif thetas[i] == min_theta:
                comment = "is among the least efficient."
            elif thetas[i] >= average_theta:
                comment = "is above average in efficiency."
            else:
                comment = "is below average in efficiency."
            
            analysis += f"- {dmu} ({thetas[i]:.4f}) {comment}\n"

        analysis += "\nInterpretation:\n"
        analysis += "- A theta (θ) closer to 1 means higher efficiency.\n"
        analysis += "- Lower values indicate potential for improvement in input-output ratio.\n"

        self.analysis_box.setPlainText(analysis)

