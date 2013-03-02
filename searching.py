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
import getpass
import re
class Func(object):
    
    """Name func is from Functionality which means set of utilities
    used from various places of program"""
    reg = None
    def compileRegex(pattern):
        translated = ''
        for letter in pattern:
            if letter == '?':
                translated = translated+'.'
            elif letter == '.':
                translated = translated+r'\.'
            elif letter == '*':
                translated = translated+r'.*'
            else:
                translated = translated+letter
        Func.reg = re.compile(translated)
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
        try:
            dirs  = os.listdir(path)
            sizes = [(x, Functionality.dirSize(path+'/'+x)) for x in dirs]
            return sizes
        except FileNotFoundError:
            print("Theres not such file or directory")
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
        """Returns various list <width,height> for generating rectangles"""
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
class MyButton(QPushButton):
    def __init__(self,name,path):
        QPushButton.__init__(self,name)
        self.path = path
    def openMe(self):
        os.system('xdg-open "%s"' % self.path)
class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        QObject.connect(self.ui.pushButton,SIGNAL('clicked()'),self.setB)
        QObject.connect(self.ui.pushButton_2,SIGNAL('clicked()'),self.search)
        self.buts = []
    def testCells(self):
        self.ui.tableWidget.setRowCount(self.ui.tableWidget.rowCount()+1)
        self.ui.tableWidget.setCellWidget(0,1,QPushButton("OPEN"))
    def setB(self):
        self.ui.lineEdit.setText(QFileDialog.getExistingDirectory())
    def search(self):
        Func.compileRegex(self.ui.lineEdit_2.text())
        for root,dirs,files in os.walk(self.ui.lineEdit.text()):
            for file in files:
                if Func.reg.match(file):
                    counter = self.ui.tableWidget.rowCount()-1
                    text = os.path.splitext(root+'/'+file)
                    name = text[0].split('/')
                    name = name[len(name)-1]
                    ext = text[1]
                    print(text)
                    self.ui.tableWidget.setRowCount(self.ui.tableWidget.rowCount()+1)
                    self.ui.tableWidget.setItem(counter,0,QTableWidgetItem(ext))
                    self.ui.tableWidget.setItem(counter,1,QTableWidgetItem(name))
                    baton = MyButton("Open",text[0]+text[1])
                    self.buts.append(baton)
                    which = len(self.buts)-1
                    QObject.connect(self.buts[which],SIGNAL('clicked()'),self.buts[which].openMe)
                    
                    self.ui.tableWidget.setCellWidget(counter,2,self.buts[which])
if __name__ == '__main__':
    app = QApplication(sys.argv)
    print('DirsSizes_1', Func.dirsSizes_1('/home/jurek/Gity'))
    main=Main()
    main.show()
    sys.exit(app.exec_())