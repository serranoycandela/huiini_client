# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe


setup(
       windows=['huiini.py'],
       options={
               "py2exe":{
                       "unbuffered": True,
                       "optimize": 2,
                       "excludes": ["email"],
                       "includes":["PySide.QtCore","PySide.QtGui"]
               }
       }
) 