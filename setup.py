# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe, sys

sys.argv.append('py2exe')

setup(
    windows=[
            {
                "script": "huiini.py",
                "icon_resources": [(1, "myicon.ico")]
            }
        ],
    

    options={
               "py2exe":{
                       "unbuffered": True,
                       "optimize": 2,
                       "includes":["PySide.QtCore","PySide.QtGui", "urllib3", "requests", "queue"]
               }
       },
       
) 
