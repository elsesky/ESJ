#! /usr/bin/python
# -*- coding: utf-8 -*-


from distutils.core import setup
import py2exe,time


from glob import glob

VERSION = "0.2.0." + str(int(time.time()))
 
data_files = [
  ('zhconv', ['zhconv/zhcdict.json']),
]
               
               
zipfile_path = "lib\shardlib.dll"

               
setup(
    options = {"py2exe": {"optimize": 2,
                            "compressed": 1,
                            "dll_excludes": ["MSVCP90.dll","crypt32.dll","mpr.dll"],
                            "bundle_files": 1,
                            "includes": ["sip","zhconv","config_core"]},
                
    },
    name = "esj_ui",
    version = VERSION,
    description = "esj_ui",
    zipfile = None,
    windows=[
              {   
                'script': 'esj_ui.py',
                "uac_info":"highestAvailable",
                "icon_resources": [(1, "./images/b1.ico"),\
                  (2, "./images/b2.ico"),\
                  (3, "./images/b3.ico"),\
                  (4, "./images/b4.ico"),\
                  (6, "./images/blame.ico"),\
                  (5, "./images/sophy.ico")
                ]
              }
             ],
    data_files = data_files
)

