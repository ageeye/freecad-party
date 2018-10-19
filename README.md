Party
=====

# 1. Preamble

Party is an experimental workbench with more flexibel primitives. The target is to integrate the features in future to Part. The first step is to development a prototype with pure python...

Motivation: [Freecad Forum](https://forum.freecadweb.org/viewtopic.php?f=13&t=30289)

# 2. Features

Tetrahedron - Any point is editable.

Hexahedron  - Any point is editable.


# 3. Install

Currently the Party WB is not suporrted by the FreeCAD's addon manager. That's why the simplest way is to use following script to install the workbech. The script cloning the git repository to your personal FreeCAD folder. 


```
# install


class Installer():

    def __init__(self):
        self.url = \
            'https://raw.githubusercontent.com/ageeye/freecad-party/master/'
        self.files = [
            'InitGui.py', 'Party.py', 'PartyCmds.py', 'PartyEditor.py',
            'PartyTools.py', 'README.md', 'icons/Party.svg',
            'icons/Tree_Part_Hexahedron.svg', 'icons/Tree_Part_Polyhedron.svg',
            'icons/Tree_Part_Tetrahedron.svg']

    def install(self):
        import FreeCAD
        import os

        if (sys.version_info > (3, 0)):
            import urllib
            from urllib import request, error

            def requ(u):
                req = request.Request(u)
                response = request.urlopen(req)
                return response.read().decode('utf-8')

        else:
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
            if f[:6] == 'icons/':
                filename = os.path.join(ipath, f[6:])
            else:
                filename = os.path.join(ppath, f)
            fd = os.open(filename, os.O_RDWR | os.O_CREAT)
            os.write(fd, str.encode(content))
            os.close(fd)
            FreeCAD.Console.PrintMessage(filename + ' [DONE]')


i = Installer()
i.install()

```

# 4. Update

To get the updates from the git repository use this script:

```
import Party
Party.update()
```

