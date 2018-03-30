from distutils.core import setup
import py2exe, sys

sys.argv.append('py2exe')

setup(
        options = {
                    'py2exe': {'bundle_files': 1,
                               'compressed': True,
                               "includes":["PySide.QtCore","PySide.QtGui", "urllib3", "requests", "queue"]
                              }
                  },
        console = [{
                    'script': "huiini.py",
                    'icon_resources': [(0, 'myicon.ico')]
                  }],
        zipfile = None,
)
