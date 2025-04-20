from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
import excel_ui 
import read_excel
import CCRModel
import det_out

class ExClass(QtWidgets.QMainWindow, excel_ui.Ui_Excel):
    hideSignal = pyqtSignal()
    destroySignal = pyqtSignal()

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.submitButton.clicked.connect(self.next_page)
        self.Browse_btn.clicked.connect(self.browse_add)
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
    
    def browse_add(self):
        self.file_location, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)")
        self.address_bar.setText(self.file_location)

    def next_page(self):
        from read_excel import read_excel
        reader = read_excel(self.file_location, self.n_input, self.n_output)
        dmu_names = reader.read_file()
        X, Y = reader.process()

        # Create the model instance
        self.model = CCRModel.CCR_Model(X, Y)
        
        if self.model_type == 'weak-efficiency': 
            theta = [x.item() for x in self.model.basic_rank_dmus()]
        elif self.model_type == 'efficiency':
            theta = [x.item() for x in self.model.slack_rank_dmus()]
        else:
            theta = [x.item() for x in self.model.super_rank_dmus()]

        # Create the output page
        self.output_page = det_out.DetOut()
        self.output_page.backBtnSignal.connect(self.show)
        self.output_page.destroySignal.connect(self.close_outer)
        self.output_page.set_data(theta, dmu_names, self.model_type)
        self.output_page.setWindowTitle("Output")
        self.output_page.show()
        self.hide()
    def back_page(self):
        pass

    def close_outer(self):
        self.destroySignal.emit()
        self.close()