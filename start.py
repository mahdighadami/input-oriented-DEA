import sys
from PyQt5 import QtWidgets
import start_ui


class Model_StartUp(QtWidgets.QMainWindow, start_ui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.manButton.clicked.connect(self.manualStart)
        self.detButton.clicked.connect(self.detStart)
        self.stochButton.clicked.connect(self.stochStart)
        self.center_on_screen()

    def center_on_screen(self):
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def manualStart(self):
        from manual_page import ManualPage
        screenshots = ["manual/1.png",
        "manual/2.png",
        "manual/3.png",
        "manual/4.png",
        "manual/5.png",
        "manual/6.png",
        "manual/7.png"]
        self.man_page = ManualPage(screenshots)
        self.man_page.show()

    def detStart(self):
        from deterministic import DetClass
        self.det_page = DetClass()
        self.det_page.backBtnSignal.connect(self.show)
        self.det_page.destroySignal.connect(self.close)
        self.det_page.show()
        MainWindow.hide()

    def stochStart(self):
        QtWidgets.QMessageBox.information(self, "information", "Comming Soon...")
        

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Model_StartUp()
    MainWindow.show()
    sys.exit(app.exec_())