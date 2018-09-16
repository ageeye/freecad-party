

class PartyWB ( Workbench ):

    import PartyTools
    MenuText = 'Party'
    ToolTip  = 'Experimental advance of the Part WB'
    Icon     = PartyTools.Settings.icon('Party.svg')

    def Initialize(self):
        "This function is executed when FreeCAD starts"
        import PartyCmds
        self.list = ['makeHexahedron', 'makeTetrahedron'] # A list of command names created in the line above
        self.appendToolbar('Primitives',self.list) # creates a new toolbar with your commands

    def Activated(self):
        return

    def Deactivated(self):
        return

    def ContextMenu(self, recipient):
        return

    def GetClassName(self): 
        return 'Gui::PythonWorkbench'
       
Gui.addWorkbench(PartyWB)
