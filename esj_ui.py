#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os, time

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from esj_ui_core import *

import win32api,win32con,win32gui


VERSION = "0.2.0." + str(int(time.time()))
app = QApplication(sys.argv)
RUNNING_LOCK_FILE = 'esj.lck'

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


# 检查程序是否重复运行，如果重复运行，自动退出并显示之前运行的窗口
# 该检测方式为创建文件锁的方式，如果非法关闭程序，可能导致程序无法初始化，此时需要手工删除文件夹下对应的lck文件

def running_check():
    # 先确认窗口是否存在，如果不存在，则删除LOCK文件
    esj_handle = win32gui.FindWindow('QWidget','esj_ui')
    # 如果窗口不存在，handle返回0
    if esj_handle == 0:
        try:
            os.remove(RUNNING_LOCK_FILE)
        except Exception as e:
            pass

    # 当带参数-f时，强制删除lck文件
    if len(sys.argv) > 1:
        if sys.argv[1] == '-f':
            try:
                os.remove(RUNNING_LOCK_FILE)
            except Exception as e:
                pass
    # 当LCK文件存在，默认程序正在运行，自动退出当前程序
    if os.path.exists(RUNNING_LOCK_FILE):
        

        # 如果闪动窗口，就不用提示
        # win32api.MessageBox(0, "程序正在运行".decode('UTF-8').encode('GB18030'), "提醒".decode('UTF-8').encode('GB18030'),win32con.MB_OK)
        # 获取窗口句柄并前台化窗口
        try:
            esj_handle = win32gui.FindWindow('QWidget','esj_ui')
            win32gui.ShowWindow(esj_handle,win32con.SW_SHOW)
            win32gui.ShowWindow(esj_handle,win32con.SW_NORMAL)
        except Exception as e:
            pass
        sys.exit(-1)
    # 如果不存在，则创建
    else:
        try:
            open(RUNNING_LOCK_FILE,'a').close()
        except Exception as e:
            pass



def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，
    #如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

def do_log(modname,account,log_detail,logname = 'log.log'):
    try:
        print modname + '|' + account + ':' + log_detail.decode('UTF-8',errors='ignore').encode('GB18030',errors='ignore')
    except Exception,e:
        print Exception,":",e
        print "Error in do_log"
    ospath = cur_file_dir()
    fp = open(ospath + '/' + logname,"a")
    ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    fp.write(ctime + "|"  + modname + '|' + account + ':' +log_detail + "\n")
    fp.close()



if __name__ == "__main__":
    # 检查程序是否重复运行
    running_check()

    #初始化窗体
    window = MainWindow()
    window.init_signals()
    
    #设置窗口置顶
    window.setWindowFlags(Qt.WindowStaysOnTopHint)
    #初始化处理（注意，窗体需要先初始化）
    esjcore = esj_ui_core(window)
    #消息发送，处理函数定义在Core.py
    #采集按钮 pushButton_p
    QObject.connect(window.pushButton_p,SIGNAL(_fromUtf8("clicked()")),esjcore.pushButton_p_click)
    #采集选中按钮 pushButton_s_p
    QObject.connect(window.pushButton_s_p,SIGNAL(_fromUtf8("clicked()")),esjcore.pushButton_s_p_click)
    #刷新按钮 pushButton_s_r
    QObject.connect(window.pushButton_s_r,SIGNAL(_fromUtf8("clicked()")),esjcore.pushButton_s_r_click)
    #采集并输出按钮 pushButton_op
    QObject.connect(window.pushButton_op,SIGNAL(_fromUtf8("clicked()")),esjcore.pushButton_op_click)
    #采集并输出选中按钮 pushButton_s_op
    QObject.connect(window.pushButton_s_op,SIGNAL(_fromUtf8("clicked()")),esjcore.pushButton_s_op_click)
    #输出选中按钮 pushButton_s_o
    QObject.connect(window.pushButton_s_o,SIGNAL(_fromUtf8("clicked()")),esjcore.pushButton_s_o_click)
    #搜索按钮 pushButton_s_n
    QObject.connect(window.pushButton_s_n,SIGNAL(_fromUtf8("clicked()")),esjcore.pushButton_s_n_click)
    QApplication.setQuitOnLastWindowClosed(False)
    window.show()

    
    sys.exit(app.exec_())