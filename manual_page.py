from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QFrame
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QRect
import sys


class ManualPage(QWidget):
    def __init__(self, screenshots):
        super().__init__()
        self.screenshots = screenshots
        self.current_index = 0

        # Window setup
        self.resize(900, 650)
        self.center_on_screen()
        self.setWindowTitle("User Manual")
        self.setStyleSheet("QWidget { background-color: #fff2e6; }")  # pastel background

        # Main frame styled like first page
        self.frame = QFrame(self)
        self.frame.setStyleSheet("""
            QFrame {
                background-color: #ff8080;
                border: 2px solid #aaa;
                border-radius: 10px;
            }
        """)
        layout = QVBoxLayout(self.frame)

        # Title
        title = QLabel("User Manual", self)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        title.setStyleSheet("""
        QLabel {
            background-color: #fff2e6;
            color: #333;
            border: 2px solid #555;
            border-radius: 6px;
            padding: 8px;
        }
    """)

        # Image display
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label, stretch=1)
        self.update_image()

        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("◀ Previous")
        self.next_button = QPushButton("Next ▶")
        for btn in (self.prev_button, self.next_button):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #b5e7a0;
                    border: 2px solid #333;
                    border-radius: 6px;
                    padding: 6px 12px;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: #a2d891;
                    border-color: #222;
                }
                QPushButton:pressed {
                    background-color: #8fcf82;
                    border-color: #111;
                }
            """)
        self.prev_button.clicked.connect(self.show_prev)
        self.next_button.clicked.connect(self.show_next)

        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        layout.addLayout(nav_layout)

        # Progress indicator
        self.progress_label = QLabel("", self)
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(self.progress_label)
        self.update_progress()

        # Set main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.frame)

    def center_on_screen(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def update_image(self):
        pixmap = QPixmap(self.screenshots[self.current_index])
        scaled = pixmap.scaled(1200, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled)

    def update_progress(self):
        self.progress_label.setText(f"Slide {self.current_index + 1} of {len(self.screenshots)}")

    def show_prev(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_image()
            self.update_progress()

    def show_next(self):
        if self.current_index < len(self.screenshots) - 1:
            self.current_index += 1
            self.update_image()
            self.update_progress()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screenshots = ["manual/1.png",
        "manual/2.png",
        "manual/3.png",
        "manual/4.png",
        "manual/5.png",
        "manual/6.png",
        "manual/7.png"]  # put your screenshots here
    window = ManualPage(screenshots)
    window.show()
    sys.exit(app.exec_())
