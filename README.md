YCDIVFX MaxPlus Packages
========================
[![Build Status](https://travis-ci.org/arturleao/YCDIVFX_MaxPlus.png?branch=master)](https://travis-ci.org/arturleao/YCDIVFX_MaxPlus)
* Add the 'packages' folder to your PYTHONPATH envirnoment variable
* maxpycharm based on Sublime3dsMax (http://cbuelter.de/?p=535)
* maxfb has a depedency on facepy (https://github.com/jgorset/facepy)
* maxplusconsole as a dependency on PySideKick (https://github.com/cloudmatrix/pysidekick/)

PyCharm usage
-------------

Create a new configuration. Fill in with the following values:
Script: C:\YCDIVFX\MaxPlus\MyExamples\run.py
Script parameters: -f C:\YCDIVFX\MaxPlus\MyExamples\pyeditor.py

Command-line usage
-------------

python.exe C:\YCDIVFX\MaxPlus\MyExamples\run.py -f C:\YCDIVFX\MaxPlus\MyExamples\pyeditor.py

(3ds Max needs to be open. You need to use full paths)