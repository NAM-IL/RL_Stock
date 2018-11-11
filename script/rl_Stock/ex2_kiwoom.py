import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(200, 300, 600, 400)
        
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        
        
#         self.kiwoom.dynamicCall("CommConnect()")
        
#         self.text_edit = QTextEdit(self)
#         self.text_edit.setGeometry(150, 70, 200, 80)
#         self.text_edit.setEnabled(False)
        
#         self.kiwoom.OnEventConnect.connect(self.event_connect)
   
        
        btn1 = QPushButton("Login", self)
        btn1.move(20, 20)
        btn1.clicked.connect(self.btn1_clicked)
        
        btn2 = QPushButton("Check state", self)
        btn2.move(20, 70)
        btn2.clicked.connect(self.btn2_clicked)
        
        btn3 = QPushButton("종목코드 얻기", self)
        btn3.move(20, 110)
        btn3.clicked.connect(self.btn3_clicked)
        
        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(20, 150, 250,230)
        
    def event_connect(self, error_code):
        if error_code == 0:
            self.text_edit.append("로그인 성공")
        
    def btn1_clicked(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")
        print('ret: {}'.format(ret))
         
    def btn2_clicked(self):
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            self.statusBar().showMessage("Not Connected")
        else:
            self.statusBar().showMessage("Connected")
    
    def btn3_clicked(self):
        if self.kiwoom.dynamicCall("GetConnectState()") == 1:
            ret = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", ["0"])
            kospi_code_list = ret.split(';')
            kospi_code_name_list = []
            
            for x in kospi_code_list:
                name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", [x])
                kospi_code_name_list.append(x + " : " + name)
                
            self.listWidget.addItems(kospi_code_name_list)
        
        else:
            self.statusBar().showMessage("Not Connected")
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
    