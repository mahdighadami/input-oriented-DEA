import os, sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal
import deterministic_ui


class DetClass(QtWidgets.QMainWindow, deterministic_ui.Ui_deterministic):
    backBtnSignal = pyqtSignal()
    destroySignal = pyqtSignal()

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.nextButton.clicked.connect(self.next_page)
        self.backButton.clicked.connect(self.back_page)
        self.center_on_screen()

    def center_on_screen(self):
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def closeEvent(self, event):
        if event.spontaneous():
            event.accept()
            self.destroySignal.emit()

    def back_page(self):
        self.backBtnSignal.emit()
        self.close()
        
    def next_page(self):
        if self.n_input.value() == 0 : 
            QtWidgets.QMessageBox.warning(self, "warning", "The number of inputs must be at least one.")
            return
        
        if self.n_output.value() == 0 : 
            QtWidgets.QMessageBox.warning(self, "warning", "The number of output must be at least one.")
            return
        
        if not (self.weak_eff_check.isChecked() or
                self.eff_check.isChecked() or
                self.sup_eff_check.isChecked()):
            QtWidgets.QMessageBox.warning(self, "warning", "Please select a model.")
            return

        data = {'n_dmu' : self.n_dmu.value(),
                'n_input' : self.n_input.value(),
                'n_output' : self.n_output.value(),
                'model' : 'efficiency' if self.eff_check.isChecked() else (
                    'super-efficiency' if self.sup_eff_check.isChecked() else 'weak-efficiency'
                )}
        
        if self.excel_import.isChecked():
            pass
        else:
            from det_table import DetModel
            self.solver_page = DetModel()
            self.solver_page.backBtnSignal.connect(self.show)
            self.solver_page.destroySignal.connect(self.close_outer)
            self.solver_page.set_data(data)
            self.solver_page.show()
            self.hide()

    def close_outer(self):
        self.destroySignal.emit()
        self.close()
        
        
        


        