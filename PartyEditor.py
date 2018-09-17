# -*- coding: utf-8 -*-

from PySide import QtGui, QtCore

from PySide.QtCore import *
from PySide.QtGui import *
 
import FreeCAD, FreeCADGui, Part, Draft

def create(proxy):
    editor = PartyEditor()
    editor.setProxy(proxy)
    editor.show()
    editor.updateEditor()
    editor.backup = proxy.Object.Points 
    return editor

class PartyEditor(QtGui.QWidget):

    def __init__(self):
        super(PartyEditor, self).__init__()      
        self.initUI()
        self.setRestore()
        self.setProxy()

    def initUI(self): 

        # create info label

        self.lbInfo = QtGui.QLabel('Vertex: ', self)
        self.lbInfo.move(10, 20)
        self.lbInfo.setFixedWidth(350)

        # create buttons

        btns = [
            ['<<', lambda:self.btn_start(), 10, 50],
            ['<', lambda:self.btn_backward(), 110, 50],
            ['>', lambda:self.btn_forward(), 210, 50],
            ['>>', lambda:self.btn_end(), 310, 50],
            ['Restore', lambda:self.edt_restore(), 300, 170]
        ]      

        for dat in btns:
            t, f, x, y = dat      
            btn = QtGui.QPushButton(t, self)
            btn.clicked.connect(f)
            btn.resize(btn.minimumSizeHint())
            btn.move(x, y)

        # create inputs fields  

        self.editableXYZ = True
        self.edit = []

        edts = [
            ['X', lambda:self.edt_xyz('X'), 15, 90],
            ['Y', lambda:self.edt_xyz('Y'), 15, 130], 
            ['Z', lambda:self.edt_xyz('Z'), 15, 170],
        ]

        for dat in edts:
            t, f, x, y = dat
            lab = QtGui.QLabel(t, self)
            lab.move(x, y+5)
            edt = QtGui.QLineEdit(self)
            edt.move(x+20, y)
            edt.textChanged.connect(f)
            self.edit.append(edt)
          
        
        self.setGeometry(300, 350, 410, 210)
        self.setWindowTitle('Editor')  

    def setRestore(self, restore=None):
        self.Restore = restore

    def setProxy(self, proxy=None):
        self.Proxy = proxy
        if hasattr(proxy, 'Restore'):
            self.setRestore(proxy.Restore)

    def closeEvent(self, event):
        if self.Restore:
            self.Proxy.Object.ViewObject.DisplayMode = self.Restore
            self.Proxy.Restore = None
            self.Restore = None
        FreeCADGui.ActiveDocument.resetEdit()

    def btn_start(self):
        self.Proxy.Object.Vertex = 1
        FreeCAD.activeDocument().recompute()
        self.updateEditor()

    def btn_forward(self):
        self.Proxy.Object.Vertex += 1
        FreeCAD.activeDocument().recompute()
        self.updateEditor()

    def btn_backward(self):
        self.Proxy.Object.Vertex -= 1
        FreeCAD.activeDocument().recompute()
        self.updateEditor()

    def btn_end(self):
        self.Proxy.Object.Vertex = len(self.Proxy.Object.Points)
        FreeCAD.activeDocument().recompute()
        self.updateEditor()

    def edt_xyz(self, axis):
        self.editableXYZ = False
        obj = self.Proxy.Object
        if axis=='X':
            obj.X = float(self.edit[0].text().replace(',','.'))
        elif  axis=='Y':
            obj.Y = float(self.edit[1].text().replace(',','.'))
        elif  axis=='Z':
            obj.Z = float(self.edit[2].text().replace(',','.'))
        FreeCAD.activeDocument().recompute()
        self.editableXYZ = True

    def edt_restore(self):
        self.Proxy.Object.Points = self.backup
        FreeCAD.activeDocument().recompute()
        self.updateEditor()

    def updateEditor(self):
        if self.editableXYZ == True:
            obj = self.Proxy.Object
            self.lbInfo.setText('Vertex: ' + str(obj.Vertex))
            self.edit[0].setText(str(obj.X))
            self.edit[1].setText(str(obj.Y))
            self.edit[2].setText(str(obj.Z))



