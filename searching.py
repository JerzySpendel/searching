from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import *
from main import Ui_MainWindow
from dialog import Ui_Dialog
from graph import Ui_Form
import sys
import os
import math
from graphing import Graph
from whoosh import 
class Functionality(object):
    def initSearchEngine():
        """ Do all necessary things to perform searching in future """
        pass
    def indexFilesIn(path):
        """ Indexes all files in path """
        for root,dirs,files in os.walk(path):
            for file in files:
                if not os.path.islink(root+'/'+file):
                    
    def dirSize(path):
        size = 0
        for root,dirs,files in os.walk(path):
            for file in files:
                if not os.path.islink(root+'/'+file):
                    size+=os.path.getsize(root+'/'+file)
        return path,size
    def dirsSizes(path):
        result = []
        for root,dirs,files in os.walk(path):
            result.append(Functionality.dirSize(root))
        print(result)
    def dirsSizes_1(path):
        """ Returns list of subdirectories in path as given:
            [(dir1,(path_to_dir1,sizeOfDir1inInt))...(dirN,(path_to_dirN,sizeOfDirNinInt))]            
            """
        dirs  = os.listdir(path)
        sizes = [(x, Functionality.dirSize(path+'/'+x)) for x in dirs]
        return sizes
    def makeShorter(size):
        """ Changes size given as Integer to string like: 10MB,10KB or 10GB """
        if size>=10**9:
          size = size//1000000000
          return str(size)+'GB'
        elif size>=10**6:
          size = size//1000000
          return str(size)+'MB'
        elif size>=10**3:
          size = size//1000
          return str(size)+'KB'
        else:
          return str(size)
    def determineSize(size):
        if size>10**10:
            return 200,200
        elif size>10**9:
            return 100, 100
        elif size>10**8:
            return  100, 50
        elif size>10**6:
            return 100, 20
        else:
            return 10, 10

class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        QObject.connect(self.ui.pushButton,SIGNAL('clicked()'),self.setB)
        QObject.connect(self.ui.pushButton_2,SIGNAL('clicked()'),self.search)
        
        self.testCells()
    def testCells(self):
        self.ui.tableWidget.setRowCount(self.ui.tableWidget.rowCount()+1)
        self.ui.tableWidget.setCellWidget(0,0,QPushButton("OPEN"))
    def setB(self):
        self.ui.lineEdit.setText(QFileDialog.getExistingDirectory())
    def searchF(self,startpoint,ext):
        dirs = os.listdir(startpoint)
        c_dirs = [dirr for dirr in dirs if os.path.isdir(os.path.join(startpoint,dirr))]
        filess = []
        for root,dirs,files in os.walk(startpoint):
            for file in files:
                if file.endswith(ext):
                    filess.append(file)
        return(filess)
    def search(self):
        if self.ui.lineEdit_2.text() == '':
            dialog = QDialog()
            Ui_Dialog().setupUi(dialog)
            dialog.exec_()
        else:
            found = self.searchF(self.ui.lineEdit.text(),self.ui.lineEdit_2.text())
            found = [[os.path.splitext(found)] for found in found]
            print(found)
            counter = 0
            for li in found:
                self.ui.tableWidget.setRowCount(self.ui.tableWidget.rowCount()+1)
                self.ui.tableWidget.setItem(counter,0,QTableWidgetItem(li[0][1]))
                self.ui.tableWidget.setItem(counter,1,QTableWidgetItem(li[0][0]))
                self.ui.tableWidget.setCellWidget(counter,2,QPushButton("Open"))
                counter+=1
app = QApplication(sys.argv)
print('DirsSizes_1', Functionality.dirsSizes_1('/home/jurek/Gity'))
main=Main()
main.show()
sys.exit(app.exec_())