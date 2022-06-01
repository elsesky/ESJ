#! /usr/bin/python
# -*- coding: utf-8 -*-

#######################################################################################
#                                                                                     #
#    File: config_core.py                                                             #
#    Part of esj                                                                     #
#    用途：esj配置文件处理类                                                                                                                                                            #
#                                                                                     #
#    Copyright (c) 2010-2022 <elsesky@elsesky.bid>                                    #
#                                                                                     #
#    Permission is hereby granted, free of charge, to any person obtaining a copy     #
#    of this software and associated documentation files (the "Software"), to deal    #
#    in the Software without restriction, including without limitation the rights     #
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell        #
#    copies of the Software, and to permit persons to whom the Software is            #
#    furnished to do so, subject to the following conditions:                         #
#                                                                                     #
#    The above copyright notice and this permission notice shall be included in       #
#    all copies or substantial portions of the Software.                              #
#                                                                                     #
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR       #
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,         #
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE      #
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER           #
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,    #
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN        #
#    THE SOFTWARE.                                                                    #
#                                                                                     #
#######################################################################################
from __future__ import with_statement
import sys,os,ConfigParser
from PyQt4 import QtCore, QtGui
from winerror import RPC_E_SERVERCALL_RETRYLATER
from afxres import AFX_IDC_PROPNAME
import win32api,win32con,win32gui


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，
    #如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


class config_c():
    conf_name = "esj.ini"
    config = ConfigParser.ConfigParser()
    conf_path = ""
    confs = None
    cfgfile = None
    
    def __init__(self,window):
        self.conf_path = cur_file_dir() + '\\' + self.conf_name
        if not(os.path.exists(self.conf_path)):
            win32api.MessageBox(0, "配置文件丢失，请检查！".decode('UTF-8').encode('GB18030'), "错误".decode('UTF-8').encode('GB18030'),win32con.MB_OK)
            sys.exit(-1)
        try:
            with open(self.conf_path,'r+') as cfgfile:
                self.config.readfp(cfgfile)
            self.confs = self.config
        except Exception,e:
            print e
            return
        return
    

                
    def get_conf_val(self,pname,valname):
        try:
            return self.confs.get(pname,valname)
        except Exception,e:
            print str(e)
            return False 
    
    def set_conf_val(self,pname,valname,val):
        try:
            self.confs.set(pname,valname,val)
            cfgfile = open(self.conf_path,'r+')
            self.confs.write(cfgfile)
            cfgfile.close()
        except Exception,e:
            print str(e)
            return False 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    