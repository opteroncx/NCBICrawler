import xlrd
import utils
import sys
from PyQt5 import QtCore, uic, QtWidgets ,QtGui
import os

def runByXls():
    xlsfile = r'dataindex.xlsx'   
    book = xlrd.open_workbook(xlsfile) 
    sheet=book.sheet_by_index(0)
    genes = sheet.col_values(0)
    genes=genes[1::]
    species=sheet.col_values(2)
    species=species[1::]
    #print(len(genes))
    #print(len(species))

    for i in range(len(genes)):
        keywords=genes[i]+'+'+species[i]
        utils.run(keywords)
        
def runByKeywords(keywords):
    utils.run(keywords)

#GUI
qtCreatorFile = "main.ui" 
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QtWidgets .QMainWindow, Ui_MainWindow):
    prog=0
    def __init__(self):
        QtWidgets .QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.start.clicked.connect(self.crawlGui)
        self.timer =QtCore.QBasicTimer()  
        self.step = 0  

    def getItems(self, keywords):
        allItems=utils.get_ID(keywords)
        allItemsNum=len(allItems)
        self.tb.setText('文献数量'+str(allItemsNum))
        return allItemsNum

    def setpBar(self,v): 
        self.prog=v
        #print(v)

    def timerEvent(self, event):
        self.prog=self.sb.prog
        self.pbar.setValue(self.prog)
        
    
    def crawlGui(self):
        keywords=self.keywordsInput.toPlainText()
        self.timer.start(100,self)
        num=self.getItems(keywords)
        self.doCrawl=WorkThread()
        self.doCrawl.keywords=keywords
        self.doCrawl.start()
        self.sb=BarThread()
        self.sb.num=num
        self.sb.start()
        
 


#多线程，防止UI卡死
class WorkThread(QtCore.QThread):
    keywords=''
    def __init__(self, parent=None):
        super(WorkThread, self).__init__(parent)

    #重写 run() 函数
    def run(self):
        runByKeywords(self.keywords)

class BarThread(QtCore.QThread):
    num=1
    vSignal = QtCore.pyqtSignal(int)
    prog=0
    def __init__(self, parent=None):
        super(BarThread, self).__init__(parent)

    def getV(self):
        v=0
        dir='./archive'
        while v<=100:
            files=os.listdir(dir)
            v1=100*len(files)
            v2=self.num
            v=v1/v2
            #print('v1/v2='+str(v1/v2))
            v=int(v)
            self.prog=v
            #print(v)
            #print(len(files))
            #print(self.num)

    def run(self):
        self.getV()

if __name__ == "__main__":
    app = QtWidgets .QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

