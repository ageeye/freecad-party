# -*- coding: utf-8 -*-

import FreeCAD, FreeCADGui

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

