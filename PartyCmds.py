# -*- coding: utf-8 -*-

import FreeCAD, FreeCADGui
from PySide import QtGui

class GuiTree():

    @classmethod 
    def current(cls):
        mw=FreeCADGui.getMainWindow()
        trees=mw.findChildren(QtGui.QTreeWidget)

        result = None
        for tree in trees:
            if tree.isVisible(): # and tree.isActiveWindow():
                result = tree
        
        return result

class cmdTreeMoveItem():
    'Prototype to move tree items up and down.'

    def GetResources(self):
        import PartyTools
        return {'Pixmap'  : PartyTools.Settings.icon('Tree_'+self.cmdType()+'.svg'),
                'MenuText': self.cmdType(),
                'ToolTip' : self.tooltip()}

    def tooltip(self):
        return ''

    def cmdType(self):
        return 'TreeMoveItem'

    def step(self):
        return 0

    def limes(self, value, items=0):
        return value > items

    def IsActive(self):
        sel = FreeCADGui.Selection.getSelection()
        if FreeCADGui.ActiveDocument and (len(sel) == 1): #and GuiTree.current():
            return True
        else:
            return False 

    def Activated(self):
        self.proceed()

    def proceed(self):
        mw=FreeCADGui.getMainWindow()
        trees=mw.findChildren(QtGui.QTreeWidget)
        tree = None
        for t in trees:
            if t.isVisible():
                tree = t

        if tree:
            top = tree.topLevelItem(0).child(0)
            item = tree.currentItem()
            row = tree.currentIndex().row()
            if self.limes(row, top.childCount()) and top.indexOfChild(item) >= 0:
                child = top.takeChild(row)
                if child is item:
                    top.insertChild(row + self.step(), item)
                    tree.setCurrentItem(item)
                else:
                    FreeCAD.Console.PrintError('take child fails..')
        else:
            FreeCAD.Console.PrintError('tree unlocated..')

class cmdTreeItemUp(cmdTreeMoveItem):

    def cmdType(self):
        return 'ItemUp'

    def step(self):
        return -1

    def tooltip(self):
        return 'Move tree item up.'

    def limes(self, value, items=0):
        return value > 0

class cmdTreeItemDown(cmdTreeMoveItem):

    def cmdType(self):
        return 'ItemDown'

    def step(self):
        return 1

    def tooltip(self):
        return 'Move tree item down.'

    def limes(self, value, items=0):
        return value < (items-1)
        
class cmdPolyhedron():
    'Prototype for polyhedron types.'

    def GetResources(self):
        import PartyTools
        return {'Pixmap'  : PartyTools.Settings.icon('Tree_Part_'+self.cmdType()+'.svg'),
                'MenuText': self.cmdType(),
                'ToolTip' : 'Create a '+self.cmdType()+'.'}

    def cmdType(self):
        return 'Polyhedron'

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        self.proceed()

    def proceed(self):
        FreeCADGui.addModule('Party')
        doc = FreeCAD.ActiveDocument
        doc.openTransaction(self.cmdType())
        FreeCADGui.doCommand('Party.make'+self.cmdType()+'()')
        doc.commitTransaction()
        doc.recompute()
        FreeCADGui.Selection.clearSelection()

class cmdSelector():
    'Create a selector.'

    def GetResources(self):
        import PartyTools
        return {'Pixmap'  : PartyTools.Settings.icon('Selector.svg'),
                'MenuText': 'Selector',
                'ToolTip' : 'Create a selector.'}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        self.proceed()

    def proceed(self):
        FreeCADGui.addModule('Party')
        doc = FreeCAD.ActiveDocument
        doc.openTransaction('Selector')
        FreeCADGui.doCommand('Party.makeSelector()')
        doc.commitTransaction()
        doc.recompute()
        FreeCADGui.Selection.clearSelection()

class cmdTetrahedron(cmdPolyhedron):
    'Create a tetrahedron.'

    def cmdType(self):
        return 'Tetrahedron'

class cmdHexahedron(cmdPolyhedron):
    'Create a hexahedron.'

    def cmdType(self):
        return 'Hexahedron'

FreeCADGui.addCommand('makeTetrahedron', cmdTetrahedron()) 
FreeCADGui.addCommand('makeHexahedron', cmdHexahedron()) 
FreeCADGui.addCommand('makeSelector', cmdSelector())
FreeCADGui.addCommand('setTreeItemUp', cmdTreeItemUp())
FreeCADGui.addCommand('setTreeItemDown', cmdTreeItemDown()) 

