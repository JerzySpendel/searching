# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 21:15:46 2013

@author: jurek
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import *
from main import Ui_MainWindow
from dialog import Ui_Dialog
from graph import Ui_Form
import sys
import os
import math
class Rektangiel(QRect):
    def __init__(self,x,y,width,height,text,size):
        QRect.__init__(self,x,y,width,height)
        self.text = text
        self.size = size
    def update(self,x,y):
        self.moveCenter(QPoint(x,y))
class Graph(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        size = Functionality.dirSize('/home/jurek/Gity')[1]
        self.setMouseTracking(True)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.show()
        self.rects = []
        self.drag = False
        self.cursor = QCursor().pos()
        self.activeRect = None
    def testAddRects(self):
        for i in range(15):
            new = self.newRektangiel(width=100, height=100)
            self.rects.append(new)
    def initiateRects(self, path):
        listV = [(x[0], x[1][1]) for x in Functionality.dirsSizes_1(path)]
        print("listV:", listV)
        for v in listV:
            size = Functionality.determineSize(v[1])
            rekt = self.newRektangiel(width=size[0], height=size[1])
            rekt.text = v[0]
            rekt.size = Functionality.makeShorter(v[1])
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
        
if __name__ == '__main__':
    print("HALLLLLELLLUJA")