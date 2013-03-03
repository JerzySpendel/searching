from PyQt4.QtCore import *
from PyQt4.QtGui import *
from main import Ui_MainWindow
from dialog import Ui_Dialog
from graph import Ui_Form
import sys
import os
import math
import getpass
import re
class Rektangiel(QRect):
    def __init__(self,x,y,width,height,text,size):
        QRect.__init__(self,x,y,width,height)
        self.text = text
        self.size = size
    def update(self,x,y):
        self.moveCenter(QPoint(x,y))
class Graph(QWidget):
    def __init__(self,path):
        QWidget.__init__(self)
        size = Func.dirSize('/home/jurek/Gity')[1]
        self.setMouseTracking(True)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.show()
        self.rects = []
        self.drag = False
        self.cursor = QCursor().pos()
        self.activeRect = None
        
        self.initiateRects(path)
    def testAddRects(self):
        for i in range(15):
            new = self.newRektangiel(width=100, height=100)
            self.rects.append(new)
    def initiateRects(self, path):
        listV = [(x[0], x[1][1]) for x in Func.dirsSizes_1(path)]
        print("listV:", listV)
        for v in listV:
            size = Func.determineSize(v[1])
            rekt = self.newRektangiel(width=size[0], height=size[1])
            rekt.text = v[0]
            rekt.size = Func.makeShorter(v[1])
            self.rects.append(rekt)
    def newRektangiel(self, **V):
        width = V['width']
        height = V['height']
        wSize = self.size()
        for x in range(wSize.width()):
            for y in range(wSize.height()):
                if not y+height>=wSize.height():
                    new = Rektangiel(x, y, width, height,None,None)
                    if not self.isThereRectangleWithWhichThatRectangleIntersects(new):
                        return Rektangiel(x, y+10, width, height,None,None)
    def isThereRectangleWithWhichThatRectangleIntersects(self, Rect):
        for rect in self.rects:
            if rect.intersects(Rect):
                return True
        return False
    def whichRect(self,point):
        for rect in self.rects:
          if rect.contains(point.x(),point.y()):
            self.activeRect = rect
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()
    def drawRectangles(self,qp):
        color = QColor(200,0,0)
        qp.setPen(QColor(0,200,0))
        qp.setBrush(color)
        for rect in self.rects:
          qp.drawRect(rect)
          x = rect.center().x()
          y = rect.center().y()
          qp.drawText(x-25,y+5,rect.size)
          qp.drawText(x-25, y-rect.height()/2, rect.text)
    def mouseMoveEvent(self,e):
        x = e.x()
        y = e.y()
        print(x,y)        
        if self.drag: 
            if self.activeRect != None:
                self.activeRect.update(x,y)
                self.update()
            print(x,y)
    def mousePressEvent(self,e):
        self.whichRect(e)
        self.drag = True
    def mouseReleaseEvent(self,e):
        self.drag = False


"""Part of program responsible for main window"""

class Func(object):
    
    """Name func is from lity which means set of utilities
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
            result.append(Func.dirSize(root))
        print(result)
    def dirsSizes_1(path):
        """ Returns list of subdirectories in path as given:
            [(dir1,(path_to_dir1,sizeOfDir1inInt))...(dirN,(path_to_dirN,sizeOfDirNinInt))]            
            """
        try:
            dirs  = os.listdir(path)
            sizes = [(x, Func.dirSize(path+'/'+x)) for x in dirs]
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
        QObject.connect(self.ui.pushButton_3,SIGNAL('clicked()'),self.visualisation)
        self.buts = []
    def testCells(self):
        self.ui.tableWidget.setRowCount(self.ui.tableWidget.rowCount()+1)
        self.ui.tableWidget.setCellWidget(0,1,QPushButton("OPEN"))
    def visualisation(self):
        
        w = Graph(self.ui.lineEdit.text())
        w.show()
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