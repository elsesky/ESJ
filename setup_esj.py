#! /usr/bin/python
# -*- coding: utf-8 -*-


from distutils.core import setup
import py2exe,time


from glob import glob

VERSION = "0.2.1." + str(int(time.time()))

data_files = [
   ('', ['cacert.pem']),
   ('',['esj.ini.tpl']),
]
               
               
zipfile_path = "lib\shardlib.dll"

               
setup(
    options = {"py2exe": {"optimize": 2,
                            "compressed": 1,
                            "dll_excludes": ["MSVCP90.dll","crypt32.dll","mpr.dll"],
                            "bundle_files": 1,
                            "includes": ["sip","zhconv","config_core","win32api","win32con","win32gui"]},
                
    },
    name = "esj",
    version = VERSION,
    description = "esj",
    zipfile = None,
    console=[
              {   
                'script': 'esj.py',
                "uac_info":"highestAvailable",
                "icon_resources": [(1, "./images/b2.ico"),\
                  (2, "./images/b1.ico"),\
                  (3, "./images/b3.ico"),\
                  (4, "./images/b4.ico"),\
                  (6, "./images/blame.ico"),\
                  (5, "./images/sophy.ico")
                ]
              }
             ],
    data_files = data_files
)


