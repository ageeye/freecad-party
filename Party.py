# -*- coding: utf-8 -*-

#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2018                                                    *
#*   This file is part of the FreeCAD CAx development system.              *
#*                                                                         *
#*   Authors:                                                              *
#*   Benjamin Alterauge (gift)                                             *
#*   Ulrich Brammer (ulrich1a)                                             *
#*   guess_who                                                             *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

import FreeCAD, FreeCADGui, PartyTools
from pivy import coin
import CoinNodes

def select(obj):
    sel = FreeCADGui.Selection
    sel.clearSelection()
    sel.addSelection(obj)

def makeTetrahedron():
    '''makeTetrahedron()'''
    obj=FreeCAD.ActiveDocument.addObject('Part::FeaturePython','Tetrahedron')
    Polyhedron(obj, 4)
    ViewProviderPolyhedron(obj.ViewObject)
    return obj    

def makeHexahedron():
    '''makeHexahedron()'''
    obj=FreeCAD.ActiveDocument.addObject('Part::FeaturePython','Hexahedron')
    Polyhedron(obj, 8)
    ViewProviderPolyhedron(obj.ViewObject)
    return obj

class Polyhedron:
    '''Text...'''

    forming = {
        0: 'Polyhedron',
        4: 'Tetrahedron',
        8: 'Hexahedron'
    }

    indexes = {
        0: [],
        4: [(1, 2, 3), (1, 0, 2), (3, 2, 0), (0, 1, 3)],
        8: [(0, 1, 2, 3), (5, 4, 7, 6), (6, 2, 1, 5), (3, 7, 4, 0), (7, 3, 2, 6),(5, 1, 0, 4)]
            }

    initialization = {
        0: [],
        4: [(-1., -1., -1.), (1., 1., -1.), (1., -1., 1.), (-1., 1., 1.)],
        8: [(-1., -1., -1.), (1., -1., -1.),(2., 1., -1.), (-1., 1., -1.),
            (-1., -1., 1.), (1., -1., 1.), (1., 1., 1.), (-1., 1., 1.)]
    }

    def __init__(self, obj, size=0):
        self.Object = obj
        obj.Proxy = self
        obj.addProperty('App::PropertyInteger',              'Vertex',    'Vertecies',   'Vertex number').Vertex = 1
        obj.addProperty('App::PropertyInteger',              'Count',      'Vertecies',   'Number of vertices').Count = size
        obj.addProperty('App::PropertyFloat',                'X',         'Vertecies',   'X-coord of the selected vertex').X=0.0
        obj.addProperty('App::PropertyFloat',                'Y',         'Vertecies',   'Y-coord of the selected vertex').Y=0.0
        obj.addProperty('App::PropertyFloat',                'Z',         'Vertecies',   'Z-coord of the selected vertex').Z=0.0
        obj.addProperty('App::PropertyVectorList', 'Points', 'Vertecies', 'List of all points')
        obj.setEditorMode('Count', 1) # read-only
        self.Type = self.getPolyhedronType(obj)
        self.editableXYZ = True
        if obj.Count > 0:
            self.initPolyhedron()
            self.updateXYZ()

    def getPolyhedronType(self, obj):
        return Polyhedron.forming.get(obj.Count)

    def getPolyhedronMatrix(self, obj):
        return Polyhedron.indexes[obj.Count]

    def initPolyhedron(self):
        pts = []
        for v in Polyhedron.initialization[self.Object.Count]:
            pts.append(FreeCAD.Vector(v))
        self.Object.Points = pts
        return pts

    def isPolyhedron(self):
        return True        
 
    def execute(self, obj):
        size = obj.Count
        if size > 0:
            import Part
            if size in Polyhedron.indexes:
                shellList = []
                doc = FreeCAD.ActiveDocument
                for indexes in self.getPolyhedronMatrix(obj):
                    if (size==4):
                        theWire = Part.makePolygon([obj.Points[indexes[0]], obj.Points[indexes[1]], obj.Points[indexes[2]], obj.Points[indexes[0]]])                    
                    if (size==8):
                        theWire = Part.makePolygon([obj.Points[indexes[0]], obj.Points[indexes[1]], obj.Points[indexes[2]], obj.Points[indexes[3]], obj.Points[indexes[0]]])
                    try:
                        doc.recompute()   
                        theFace = Part.Face(theWire)
                    except:
                        secWireList = theWire.Edges[:]
                        theFace = Part.makeFilledFace(Part.__sortEdges__(secWireList))
                        shellList.append(theFace)                      
                obj.Shape = Part.Solid(Part.Shell(shellList))     

    def updateXYZ(self):
        if hasattr(self, 'Object'):
            obj = self.Object
            if obj.Vertex <=0:
                self.editableXYZ = False 
            if self.editableXYZ:
                v = obj.Points[obj.Vertex-1]
                obj.X = v.x
                obj.Y = v.y
                obj.Z = v.z

    def onChanged(self, obj, prop):
        if prop == 'Vertex' and hasattr(obj, 'Count'):
            cv = obj.Count
            if obj.Vertex < 1:
                obj.Vertex = 1
            elif obj.Vertex > cv:
                 obj.Vertex = cv
            if cv > 0:
                self.updateXYZ()
        if prop == 'Points':
            self.Type  = self.getPolyhedronType(obj)
            obj.Count = len(obj.Points)
            if obj.Vertex > obj.Count:
                obj.Vertex = obj.Count
            self.updateXYZ()
        if (prop == 'X') | (prop == 'Y') | (prop == 'Z'):
            if hasattr(obj,'X') and hasattr(obj,'Y') and hasattr(obj,'Z') and hasattr(obj, 'Points'):
                if len(obj.Points) > 0:
                    pts = obj.Points
                    pts[obj.Vertex-1] = FreeCAD.Vector(obj.X, obj.Y, obj.Z)
                    self.editableXYZ = False
                    obj.Points = pts
                    self.editableXYZ = True

    def __getstate__(self):
        return self.Type

    def __setstate__(self,state):
        if state:
            self.Type = state


class ViewProviderPolyhedron:

    def __init__(self, vobj):
        vobj.Proxy = self
        self.Object = vobj.Object
        self.Restore = None

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

    def getIcon(self):
        if hasattr(self, 'Object'):
            return PartyTools.Settings.icon('Tree_Part_'+self.Object.Proxy.Type+'.svg')

    def setupContextMenu(self,vobj, menu):
        action = menu.addAction('Edit..')
        action.triggered.connect(self.edit_nwb)

    def edit_nwb(self):
        self.Restore = self.Object.ViewObject.DisplayMode
        self.Object.ViewObject.DisplayMode = u'Editor'
        import PartyEditor
        PartyEditor.create(self)

    def setEdit(self,vobj,mode=0):
        if mode == 0:
            self.edit_nwb()
            return True
        return False

    def unsetEdit(self,vobj,mode=0):
        return False

    def getDisplayModes(self,obj):
        return ['Editor']

    def attach(self, obj):
        self.Object = obj.Object
        self.scale = coin.SoScale()
        self.ptncolor = coin.SoBaseColor()
        self.lncolor = coin.SoBaseColor()
        self.data=coin.SoCoordinate3()
        self.face=coin.SoIndexedLineSet()   
        self.editor = coin.SoGroup()
        self.editor.addChild(self.scale)
        self.editor.addChild(self.lncolor)
        self.editor.addChild(self.data)
        self.editor.addChild(self.face)
        style=coin.SoDrawStyle()
        style.style = coin.SoDrawStyle.POINTS
        style.pointSize = 3.0
        self.pointset = coin.SoType.fromName('SoBrepPointSet').createInstance()
        self.editor.addChild(self.ptncolor)
        self.editor.addChild(style)
        self.editor.addChild(self.pointset)
        self.activePoint = CoinNodes.markerSetNode((1,1,0),coin.SoMarkerSet.CIRCLE_LINE_9_9)
        self.activePoint.markers.startIndex = 0
        self.activePoint.markers.numPoints = 1
        self.editor.addChild(self.activePoint)
        obj.addDisplayMode(self.editor, 'Editor')

    def updateData(self, fp, prop):  
        self.ptncolor.rgb.setValue(255, 255, 0)
        self.lncolor.rgb.setValue(0, 0, 0)
        if prop == 'Shape':
            self.pointset.numPoints.setValue(len(fp.Points))
            for i, v in enumerate(fp.Points):
                self.data.point.set1Value(i, v.x, v.y, v.z)
            self.activePoint.markers.startIndex = fp.Vertex - 1
            cnt=0
            for mtx in fp.Proxy.getPolyhedronMatrix(fp):
                for v in mtx:
                    self.face.coordIndex.set1Value(cnt, v)
                    cnt+=1 
                self.face.coordIndex.set1Value(cnt, -1)
                cnt+=1


