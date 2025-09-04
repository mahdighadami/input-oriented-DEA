import sys, os
from PyQt5 import QtWidgets, QtGui
import start_ui


class Model_StartUp(QtWidgets.QMainWindow, start_ui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.manButton.clicked.connect(self.manualStart)
        self.detButton.clicked.connect(self.detStart)
        self.stochButton.clicked.connect(self.stochStart)
        self.contribButton.clicked.connect(self.contribStart)

        self.center_on_screen()

        
    def center_on_screen(self):
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def manualStart(self):
        from manual_page import ManualPage
        screenshots = [resource_path("manual/1.png"),
        resource_path("manual/2.png"),
        resource_path("manual/3.png"),
        resource_path("manual/4.png"),
        resource_path("manual/5.png"),
        resource_path("manual/6.png"),
        resource_path("manual/7.png")]

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

    def contribStart(self):
        from contrib_page import ContribPage
        self.contrib_page = ContribPage()
        self.contrib_page.show()
        


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(resource_path("Sbu-logo.ico")))
    MainWindow = Model_StartUp()
    MainWindow.show()
    sys.exit(app.exec_())