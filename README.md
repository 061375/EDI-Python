# EDI-Python
Some experiments extracting EDI using Python

Based off of this code: http://code.activestate.com/recipes/299485-parsing-out-edi-messages/

However, I modified it a bit to work with Python3 -> The version to look at that I worked with is hippaa.edi.3.py
Also I fixed some bugs:
* CMD argument for user defined files
* Fixed a bug where the program would run forever if the EDI didn't have a closing envelope.

