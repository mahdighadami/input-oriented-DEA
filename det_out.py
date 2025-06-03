from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy, QScrollArea
from PyQt5.QtCore import pyqtSignal, Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class DetOut(QtWidgets.QMainWindow):
    backBtnSignal = pyqtSignal()
    destroySignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.resize(1500, 950)
        self.center_on_screen()

        # Set soft cream background for whole window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #fff5e6;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel {
                color: #4a4a4a;
                font-size: 14px;
            }
            QLabel#headerLabel {
                font-weight: 700;
                font-size: 16px;
                color: #8b5e61; /* muted pink */
            }
            QPlainTextEdit {
                background-color: #fff0f2;
                border: 1.5px solid #e6b8c4; /* muted pink */
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                color: #5a3e3f;
            }
        """)

    def center_on_screen(self):
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def closeEvent(self, event):
        if event.spontaneous():
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Exit?")
            dlg.setText("Are you sure you want to exit the program?")
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
        dmu_names = [str(x) for x in dmu_names]

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # DMU Row with header label
        dmu_row = QHBoxLayout()
        dmu_row.setSpacing(15)
        dmu_header = QLabel("DMUs:")
        dmu_header.setObjectName("headerLabel")
        dmu_row.addWidget(dmu_header)
        for name in dmu_names:
            label = QLabel(name)
            label.setStyleSheet("font-weight: 600; padding: 8px 12px; color: #7b5360;")  # muted pink-ish
            label.setAlignment(Qt.AlignCenter)
            label.setMinimumWidth(60)
            label.setMaximumWidth(120)
            label.setContentsMargins(5, 5, 5, 5)
            label.setProperty('class', 'dmuLabel')
            dmu_row.addWidget(label)

        # Theta Row with header label
        theta_row = QHBoxLayout()
        theta_row.setSpacing(15)
        theta_header = QLabel("Thetas:")
        theta_header.setObjectName("headerLabel")
        theta_row.addWidget(theta_header)
        for val in thetas:
            label = QLabel(f"{val:.4f}")
            label.setStyleSheet("color: #3b5998; font-weight: 600; padding: 8px 12px;")  # subtle blue
            label.setAlignment(Qt.AlignCenter)
            label.setMinimumWidth(60)
            label.setMaximumWidth(120)
            theta_row.addWidget(label)

        # Plots layout with spacing
        plot_layout = QHBoxLayout()
        plot_layout.setSpacing(30)

        # Create efficiency plot
        fig_eff, ax_eff = plt.subplots(figsize=(6, 4))
        fig_eff.patch.set_facecolor('#fff5e6')  # match soft cream background
        ax_eff.set_facecolor('#fff9f7')  # slightly lighter cream inside plot
        ax_eff.bar(dmu_names, thetas, color='#8b5e61', width=0.5)  # muted pink bars
        ax_eff.set_title("Efficiency (Theta)", fontsize=14, color='#7b5360')
        ax_eff.set_ylabel("θ", fontsize=12)
        ax_eff.tick_params(axis='x', rotation=45, labelsize=10, labelcolor='#7b5360')
        ax_eff.tick_params(axis='y', labelsize=10, labelcolor='#7b5360')
        fig_eff.tight_layout()
        canvas_eff = FigureCanvas(fig_eff)
        canvas_eff.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas_eff.setStyleSheet("border-radius: 12px;")  # rounded corners
        plot_layout.addWidget(canvas_eff)

        # Waste plot
        waste = [1 - t for t in thetas]
        fig_waste, ax_waste = plt.subplots(figsize=(6, 4))
        fig_waste.patch.set_facecolor('#fff5e6')
        ax_waste.set_facecolor('#fff9f7')
        ax_waste.bar(dmu_names, waste, color='#c97a7b', width=0.5)  # dusty rose color
        ax_waste.set_title("Resource Waste (1 - θ)", fontsize=14, color='#7b5360')
        ax_waste.set_ylabel("Waste", fontsize=12)
        ax_waste.tick_params(axis='x', rotation=45, labelsize=10, labelcolor='#7b5360')
        ax_waste.tick_params(axis='y', labelsize=10, labelcolor='#7b5360')
        fig_waste.tight_layout()
        canvas_waste = FigureCanvas(fig_waste)
        canvas_waste.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas_waste.setStyleSheet("border-radius: 12px;")
        plot_layout.addWidget(canvas_waste)

        # Scroll area for data + plots
        scroll_content = QWidget()
        scroll_inner_layout = QVBoxLayout(scroll_content)
        scroll_inner_layout.setContentsMargins(15, 15, 15, 15)
        scroll_inner_layout.setSpacing(15)
        scroll_inner_layout.addLayout(dmu_row)
        scroll_inner_layout.addLayout(theta_row)
        scroll_inner_layout.addLayout(plot_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFixedHeight(430)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #fff5e6;
            }
            QScrollBar:horizontal {
                height: 12px;
                background: #f4dcdc;
                margin: 0px 20px 0 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background: #c97a7b;
                min-width: 30px;
                border-radius: 6px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
            }
        """)

        main_layout.addWidget(scroll_area)

        # Analysis box styling added in __init__ stylesheet
        self.analysis_box = QtWidgets.QPlainTextEdit()
        self.analysis_box.setReadOnly(True)
        self.analysis_box.setFont(QtGui.QFont("Segoe UI", 12))
        self.analysis_box.setStyleSheet("border: none; background-color: transparent;")  # scroll-style will apply to container

        analysis_scroll_area = QScrollArea()
        analysis_scroll_area.setWidgetResizable(True)
        analysis_scroll_area.setWidget(self.analysis_box)
        analysis_scroll_area.setFixedHeight(300)
        analysis_scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1.5px solid #e6b8c4;
                border-radius: 10px;
                background-color: #fff0f2;
            }
            QScrollBar:vertical {
                width: 12px;
                background: #f4dcdc;
                margin: 10px 0px 10px 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #c97a7b;
                min-height: 30px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        main_layout.addWidget(analysis_scroll_area)


        # Back button styling
        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.clicked.connect(self.back_page)
        self.back_button.setFixedSize(140, 45)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #c97a7b;
                color: white;
                font-weight: 700;
                font-size: 14px;
                border: none;
                border-radius: 15px;
                padding: 10px 20px;
                box-shadow: 0 4px 6px rgba(201, 122, 123, 0.5);
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #a55a5b;
                box-shadow: 0 6px 10px rgba(165, 90, 91, 0.7);
            }
            QPushButton:pressed {
                background-color: #7b3f40;
                box-shadow: none;
            }
        """)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.back_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setCentralWidget(main_widget)
        self.analyze_results(thetas, dmu_names, model_type)
    def analyze_results(self, thetas, dmu_names, model_type):
        avg_theta = sum(thetas) / len(thetas)
        max_theta = max(thetas)
        min_theta = min(thetas)
        best = '، '.join([dmu_names[i] for i, v in enumerate(thetas) if v == max_theta])
        worst = '، '.join([dmu_names[i] for i, v in enumerate(thetas) if v == min_theta])

        text = f"""مدل: {model_type}
میانگین θ: {avg_theta:.4f}
بیشترین کارایی: {best} (θ = {max_theta:.4f})
کمترین کارایی: {worst} (θ = {min_theta:.4f})

مقایسه واحدهای تصمیم‌گیری:
"""
        for i, dmu in enumerate(dmu_names):
            if thetas[i] == max_theta:
                comment = "بالاترین کارایی"
            elif thetas[i] == min_theta:
                comment = "پایین‌ترین کارایی"
            elif thetas[i] >= avg_theta:
                comment = "بالاتر از میانگین"
            else:
                comment = "پایین‌تر از میانگین"
            text += f"- {dmu} (θ = {thetas[i]:.4f}): {comment}\n"

        self.analysis_box.setPlainText(text)
        