# -*- coding: utf-8 -*-

import os, sys

class Singleton(object):
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args, **kwds):
        pass

class Settings(Singleton):
    mod_path  = os.path.dirname(__file__)

    @classmethod
    def icon(cls, ico):
        return os.path.join(cls.mod_path, 'icons', ico)

class Update(Singleton):

    def __init__(self):
        self.url = 'https://raw.githubusercontent.com/ageeye/freecad-party/master/'
        self.files = ['InitGui.py', 'Party.py', 'PartyCmds.py','PartyEditor.py', 'PartyTools.py', 'README.md', 'icons/Party.svg', 'icons/Tree_Part_Hexahedron.svg', 'icons/Tree_Part_Polyhedron.svg', 'icons/Tree_Part_Tetrahedron.svg']

    def install(self):
        import FreeCAD, os

        if (sys.version_info > (3, 0)):  #py3
            import urllib
            from urllib import request, error 
    
            def requ(u):
                req = request.Request(u)
                response = request.urlopen(req)
                return response.read().decode('utf-8')
            
        else:  #py2
            import urllib2
            from urllib2 import Request, urlopen, URLError, HTTPError
                                
            def requ(u):
                req = Request(u)
                response = urlopen(req)
                return response.read()

        # macro path
        mpath = os.path.join(FreeCAD.ConfigGet('UserAppData'), 'Mod')

        # freecad-party path
        ppath = os.path.join(mpath, 'freecad-party')
        if not os.path.exists(ppath):
            os.makedirs(ppath)

        # icons path
        ipath = os.path.join(ppath, 'icons')
        if not os.path.exists(ipath):
            os.makedirs(ipath)

        for f in self.files:
            content = requ(self.url + f)
            if f[:6]=='icons/':
                filename = os.path.join(ipath, f[6:])
            else: 
                filename = os.path.join(ppath, f)
            fd = os.open(filename, os.O_RDWR|os.O_CREAT )
            os.write(fd, str.encode(content))
            os.close(fd)
            FreeCAD.Console.PrintMessage(filename + ' [DONE]')
            
    def refresh(self):
        from imp import reload
        import Party
        reload(Party)
        import PartyEditor
        reload(PartyEditor)
        import PartyTools
        reload(PartyTools)

