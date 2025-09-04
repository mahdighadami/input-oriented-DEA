from PyQt5 import QtWidgets, QtCore, QtGui


class ContribPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contributors")
        self.resize(600, 400)
        self.center_on_screen()

        # Apply background
        self.setStyleSheet("background-color: #fff2e6;")

        # Central widget
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Title
        title = QtWidgets.QLabel("Contributors")
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("color: #ff8080;")
        layout.addWidget(title)

        layout.addSpacing(30)

        # Contributors info
        contributors = [
            ("Mahdi Ghadami", "mahdighadami2@gmail.com"),
            ("Ali Assadbeiki", "Assadbeikiali@gmail.com"),
        ]

        for name, email in contributors:
            label = QtWidgets.QLabel(
                f"<b>{name}</b><br>"
                f"<a href='mailto:{email}' style='color:#fff2e6; text-decoration: underline;'>{email}</a>"
            )
            label.setAlignment(QtCore.Qt.AlignCenter)

            # 🔑 Make links clickable
            label.setTextFormat(QtCore.Qt.RichText)
            label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)  # enables clicking/selection
            label.setOpenExternalLinks(True)  # open mailto: in default mail app

            label.setFont(QtGui.QFont("Arial", 12))
            label.setStyleSheet("""
                QLabel {
                    background-color: #ff8080;
                    color: #fff2e6;
                    border-radius: 10px;
                    padding: 12px;
                    margin: 10px;
                }
            """)
            layout.addWidget(label)

        layout.addStretch()

        # Back button
        self.back_button = QtWidgets.QPushButton("Back")
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
        layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignCenter)
        self.back_button.clicked.connect(self.close)
        

        self.setCentralWidget(central_widget)

    def center_on_screen(self):
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
