#! /usr/bin/python
# -*- coding: utf-8 -*-

import win32clipboard as w
import time,os,win32con,webbrowser,sys
import httplib, urllib
import socket
import time
import sys,os,ConfigParser
import json
import requests,requests.utils, pickle
import re
# 简繁转换库
from zhconv import convert
from time import sleep


# 调用数据库类
from esj import *

g_logname = "esj.log"
g_txtname = "esj.txt"

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui import *
from __builtin__ import file
from win32com.server import exception

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class esj_ui_core():
    _login_token = ""
    _domain_id = ""
    _record_id = ""
    _sub_domain = ""
    _modname = "esj_ui"
    _account = ""
    _pre_site_url = ""
    _headers = {}
    current_ip = ""
    ini_recode_id_list = []



    #初始化
    def __init__(self, window):
        #传入上层窗口
        self.window = window
        # 初始化操作
        try:
            #关联右键菜单
            self.window.setContextMenuPolicy(Qt.CustomContextMenu)
            self.window.record_list.customContextMenuRequested.connect(self.gen_novel_menu)
            #小说列表默认显示最新
            self.pushButton_s_r_click(0)
        except Exception,e:
            QMessageBox.critical(self.window, _fromUtf8("错误"), str(e) + _fromUtf8("\n\n请核对配置是否正确\n\n程序将自动退出。"), buttons=QMessageBox.Ok)
        
        
############################小说列表右键菜单初始化################################   
    def gen_novel_menu(self,pos):
        novel_menu = QMenu()
        novel_menu.addSeparator()
        urlopen_n = novel_menu.addAction(_fromUtf8("在浏览器中打开"))
        novel_menu.addSeparator()
        ##############复制的二级菜单开始##################
        copy_n = novel_menu.addMenu(_fromUtf8("复制"))
        id_copy_n = copy_n.addAction(_fromUtf8("复制小说ID"))
        url_copy_n = copy_n.addAction(_fromUtf8("复制URL"))
        name_copy_n = copy_n.addAction(_fromUtf8("复制小说名"))
        author_copy_n = copy_n.addAction(_fromUtf8("复制作者名"))
        ##############复制的二级菜单结束##################
        novel_menu.addSeparator()
        ##############导出的二级菜单开始##################
        exp_n = novel_menu.addMenu(_fromUtf8("导出"))
        exp_list_selectn = exp_n.addAction(_fromUtf8("导出选中小说"))
        ##############导出的二级菜单结束##################
        novel_menu.addSeparator()
        ##############采集的二级菜单开始##################
        collect_n = novel_menu.addMenu(_fromUtf8("采集"))
        collect_select_n = collect_n.addAction(_fromUtf8("采集选中"))
        clear_and_recollect_select_n = collect_n.addAction(_fromUtf8("清空并重采集选中"))
        collect_n.addSeparator()
        collect_all_n = collect_n.addAction(_fromUtf8("采集清单中的所有对象"))
        ##############采集的二级菜单结束##################
        novel_menu.addSeparator()
        ##############在线搜索的二级菜单开始##################
        
        action = novel_menu.exec_(self.window.record_list.mapToGlobal(pos))
        #关联方法
        if action == urlopen_n:
            self.action_urlopen_n()
            
        elif action ==  exp_n:
            self.action_exp_n()
            
        elif action == url_copy_n :
            self.action_url_copy_n()

        elif action == id_copy_n :
            self.action_id_copy_n()
            
        elif action == name_copy_n :
            self.action_name_copy_n()
            
        elif action == author_copy_n :
            self.action_author_copy_n()
            
        elif action == collect_select_n:
            self.action_collect_select_n()
            
        elif action == clear_and_recollect_select_n :
            self.action_clear_and_recollect_select_n()
            
        elif action == exp_list_selectn :
            self.action_exp_list_selectn()

        elif action == collect_all_n :
            self.action_collect_all_n()
        
        else :
            return 0

############################小说列表右键菜处理函数################################  
    #点通过浏览器打开
    def action_urlopen_n(self):
        url_str = self.qstr_2_pystr(self.window.record_list.item(self.window.record_list.currentRow(),4).text())
        sys.path.append("libs")
        webbrowser.open(url_str)
        return 0

    #导出小说内容
    def action_exp_n(self,tid=0):
        esjt = esj(False)
        #弹出选择保存目录
        try:
            # tid为0的时候，默认采集选中的tid，如果为外部传参，则采集传参的tid
            if tid==0:
                t__id = self.qstr_2_pystr(self.window.record_list.item(self.window.record_list.currentRow(),0).text()).strip()
                pass
            else:
                t__id = tid
            file_path =  self.qstr_2_pystr(QFileDialog.getSaveFileName(self.window,_fromUtf8("导出该小说"),
                                                     _fromUtf8(str(t__id) + "_" + self.window.record_list.item(self.window.record_list.currentRow(),1).text()) ,
                                                     _fromUtf8("文本文件 (*.txt);;全部 (*.*)")))
            if file_path != "":
                #判断文件夹是否存在
                dir_path = os.path.split(file_path)[0]
                if os.path.exists(dir_path):
                    #判断文件夹是否可写
                    if os.access(dir_path, os.W_OK):
                        #写入(记得把id转成字符串，鬼知道直接取出来的是啥)
                        esjt.outputbyidq_with_path(str(_fromUtf8(t__id)),file_path)

                        reply = QtGui.QMessageBox.question(self.window, _fromUtf8("保存完毕"), \
                                           _fromUtf8("保存完毕，是否打开清单所在文件夹?"),\
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                        if reply == QtGui.QMessageBox.Yes:
                            cmd = dir_path.replace('/',"\\")
                            os.startfile(cmd)
                            return
                        else:
                            return
        except Exception,e:
            do_log(esjt._modname ,"root" ,str(e))
            QMessageBox.critical(self.window, _fromUtf8("保存失败"),  str(e), buttons=QMessageBox.Ok)
        return 0

    # 复制URL
    def action_url_copy_n(self):
        url_str = self.qstr_2_pystr(self.window.record_list.item(self.window.record_list.currentRow(),4).text())
        w.OpenClipboard()
        w.EmptyClipboard()
        #注意，复制的是UTF8字符串，得用CF_UNICODETEXT标识
        w.SetClipboardData(win32con.CF_UNICODETEXT, url_str)
        w.CloseClipboard()
        # QMessageBox.information(self.window, _fromUtf8("Done"),  _fromUtf8("此功能暂不支持"), buttons=QMessageBox.Ok)
        return 0

    # 复制小说名
    def action_name_copy_n(self):
        name_str = self.qstr_2_pystr(self.window.record_list.item(self.window.record_list.currentRow(),1).text())
        w.OpenClipboard()
        w.EmptyClipboard()
        #注意，复制的是UTF8字符串，得用CF_UNICODETEXT标识
        w.SetClipboardData(win32con.CF_UNICODETEXT, name_str)
        w.CloseClipboard()
        return 0

    # 复制作者名
    def action_author_copy_n(self):
        author_str = self.qstr_2_pystr(self.window.record_list.item(self.window.record_list.currentRow(),2).text())
        w.OpenClipboard()
        w.EmptyClipboard()
        #注意，复制的是UTF8字符串，得用CF_UNICODETEXT标识
        w.SetClipboardData(win32con.CF_UNICODETEXT, author_str)
        w.CloseClipboard()
        return 0

    # 复制ID
    def action_id_copy_n(self):
        id_str = self.qstr_2_pystr(self.window.record_list.item(self.window.record_list.currentRow(),0).text())
        w.OpenClipboard()
        w.EmptyClipboard()
        #注意，复制的是UTF8字符串，得用CF_UNICODETEXT标识
        w.SetClipboardData(win32con.CF_UNICODETEXT, id_str)
        w.CloseClipboard()
        return 0

    

    # 点采集选中
    def action_collect_select_n(self):
        # 直接填入ID并触发采集的点击
        id_str = self.qstr_2_pystr(self.window.record_list.item(self.window.record_list.currentRow(),0).text()).strip()
        # 填入ID
        self.window.txt_t__id.setText(id_str)
        # 点采集按钮
        self.pushButton_p_click(0)
        #QMessageBox.information(self.window, _fromUtf8("Done"),  _fromUtf8("采集完成"), buttons=QMessageBox.Ok)
        return 0

    # 清空并采集
    def action_clear_and_recollect_select_n(self):
        id_str = self.qstr_2_pystr(self.window.record_list.item(self.window.record_list.currentRow(),0).text()).strip()
        try:
            result = os.system('start "" esj.exe -cp ' + id_str)
            # 进程返回错误（返回值基本为-1）
            if result < 0:
                QMessageBox.critical(self.window, _fromUtf8("注意"), _fromUtf8("采集结束，但有错误。请核对日志信息。"), buttons=QMessageBox.Ok)
                pass
            self.list_n()
        except Exception,e:
            print e
            pass
        # QMessageBox.information(self.window, _fromUtf8("Done"),  _fromUtf8("此功能暂不支持"), buttons=QMessageBox.Ok)
        return 0

    # 按列表采集
    def action_collect_all_n(self):
        # 取总行数
        for i in range(self.window.record_list.rowCount()):
            # 直接填入ID并触发采集的点击
            id_str = self.qstr_2_pystr(self.window.record_list.item(i,0).text()).strip()
            # 填入ID
            self.window.txt_t__id.setText(id_str)
            # 点采集按钮
            try:
                print "ID: " + id_str + "  START!" 
                self.pushButton_p_click_s(0)
            except Exception,e:
                print e
                # QMessageBox.information(self.window, _fromUtf8("ERROR"), _fromUtf8("该ID采集失败：") + id_str, buttons=QMessageBox.Ok)
                return 0
        #QMessageBox.information(self.window, _fromUtf8("Done"),  _fromUtf8("采集完成"), buttons=QMessageBox.Ok)
        
    # 导出
    def action_exp_list_selectn(self):
        self.action_exp_n()
        return 0
        
#############################事件关联处理函数#############################
    #点击采集按钮
    def  pushButton_p_click(self,current=0):
        # 添加兼容处理直接输入URL的情况（使用正则匹配，注意非法情况）
        try:
            t__id =  re.findall('\d+',self.qstr_2_pystr(self.window.txt_t__id.text()).strip())
        except Exception,e:
            print e
            QMessageBox.information(self.window, _fromUtf8("ERROR"), _fromUtf8("输入数据不合法。"), buttons=QMessageBox.Ok)
            return 0
            pass
        t__id = t__id[0]
        # 这个是处理直接输入ID的情况(已弃用)
        # t__id = self.qstr_2_pystr(self.window.txt_t__id.text()).strip()
        # QMessageBox.information(self.window, _fromUtf8("Done"), t__id, buttons=QMessageBox.Ok)
        try:
            result = os.system('start "" esj.exe -p ' + t__id)
            # 进程返回错误（返回值基本为-1）
            if result < 0:
                QMessageBox.critical(self.window, _fromUtf8("注意"), _fromUtf8("采集结束，但有错误。请核对日志信息。"), buttons=QMessageBox.Ok)
                pass
            self.list_n()
        except Exception,e:
            print e
            pass
        return 0

    #点击采集按钮(但不抛错)
    def  pushButton_p_click_s(self,current=0):
        # 添加兼容处理直接输入URL的情况（使用正则匹配，注意非法情况）
        try:
            t__id =  re.findall('\d+',self.qstr_2_pystr(self.window.txt_t__id.text()).strip())
        except Exception,e:
            print e
            # QMessageBox.information(self.window, _fromUtf8("ERROR"), _fromUtf8("输入数据不合法。"), buttons=QMessageBox.Ok)
            return 0
            pass
        t__id = t__id[0]
        # 这个是处理直接输入ID的情况(已弃用)
        # t__id = self.qstr_2_pystr(self.window.txt_t__id.text()).strip()
        # QMessageBox.information(self.window, _fromUtf8("Done"), t__id, buttons=QMessageBox.Ok)
        try:
            result = os.system('esj.exe -p ' + t__id)
            # 进程返回错误（返回值基本为-1）
            if result < 0:
                # QMessageBox.critical(self.window, _fromUtf8("注意"), _fromUtf8("采集结束，但有错误。请核对日志信息。"), buttons=QMessageBox.Ok)
                pass
            self.list_n()
        except Exception,e:
            print e
            pass
        return 0

    # 点击采集选中按钮
    def pushButton_s_p_click(self,current=0):
        items = self.window.record_list.selectedIndexes()    #取选中行
        # items[0].row()第一行选中行的行号
        t__id = str(self.window.record_list.item(items[0].row(), 0).text())
        try:
            result = os.system('esj.exe -p ' + t__id)
            # 进程返回错误（返回值基本为-1）
            if result < 0:
                QMessageBox.critical(self.window, _fromUtf8("注意"), _fromUtf8("采集结束，但有错误。请核对日志信息。"), buttons=QMessageBox.Ok)
                pass
            self.list_n()
        except Exception,e:
            print e
            pass
        return 0

    # 点击采集并输出按钮
    def pushButton_op_click(self,current=0):
        # 采集
        self.pushButton_p_click()
        # 输出
        try:
            t__id =  re.findall('\d+',self.qstr_2_pystr(self.window.txt_t__id.text()).strip())[0]
        except Exception,e:
            print e
            QMessageBox.information(self.window, _fromUtf8("ERROR"), _fromUtf8("输入数据不合法。"), buttons=QMessageBox.Ok)
            return 0
            pass
        esjt = esj(False)
        #弹出选择保存目录
        try:
            file_path =  self.qstr_2_pystr(QFileDialog.getSaveFileName(self.window,_fromUtf8("导出该小说"),
                                                     _fromUtf8(str(t__id)) ,
                                                     _fromUtf8("文本文件 (*.txt);;全部 (*.*)")))
            if file_path != "":
                #判断文件夹是否存在
                dir_path = os.path.split(file_path)[0]
                if os.path.exists(dir_path):
                    #判断文件夹是否可写
                    if os.access(dir_path, os.W_OK):
                        #写入(记得把id转成字符串，鬼知道直接取出来的是啥)
                        esjt.outputbyidq_with_path(str(_fromUtf8(t__id)),file_path)

                        reply = QtGui.QMessageBox.question(self.window, _fromUtf8("保存完毕"), \
                                           _fromUtf8("保存完毕，是否打开清单所在文件夹?"),\
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                        if reply == QtGui.QMessageBox.Yes:
                            cmd = dir_path.replace('/',"\\")
                            os.startfile(cmd)
                            return
                        else:
                            return
        except Exception,e:
            do_log(esjt._modname ,"root" ,str(e))
            QMessageBox.critical(self.window, _fromUtf8("保存失败"),  str(e), buttons=QMessageBox.Ok)
        return 0

    # 点击采集并输出选中按钮
    def pushButton_s_op_click(self,current=0):
        # 采集
        # self.action_collect_select_n()
        # 直接填入ID并触发采集的点击
        id_str = self.qstr_2_pystr(self.window.record_list.item(self.window.record_list.currentRow(),0).text()).strip()
        # 填入ID
        self.window.txt_t__id.setText(id_str)
        try:
            result = os.system('esj.exe -p ' + id_str)
        except Exception,e:
            print e
            pass
        # 输出
        self.action_exp_n()
        self.list_n()
        return 0

    # 点击输出选中按钮
    def pushButton_s_o_click(self,current=0):
        self.action_exp_n()

    # 点击刷新按钮
    def pushButton_s_r_click(self,current=0):
        self.list_n()
        return 0

    # 点击搜索按钮
    def pushButton_s_n_click(self,current=0):
        try:
            n_name = self.qstr_2_pystr(self.window.n_name.text()).strip()
        except Exception,e:
            print e
            QMessageBox.information(self.window, _fromUtf8("ERROR"), _fromUtf8("输入数据不合法。"), buttons=QMessageBox.Ok)
            return 0
            pass
        self.search_n(n_name)

#############################通用函数#############################
    #从数据库中获取记录清单
    def list_n(self):
        # 先清空
        self.window.record_list.setRowCount(0)
        self.window.record_list.clearContents()

        esjt = esj(False)
        n_list = esjt.get_n_list()
        for j in n_list:
            # 转换时间格式
            timeStamp = j[5]
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
            # 拼接URL
            URL = esjt.mk_n_url(esj._N_XZ_DETAIL,str(j[0]))


            self.add_recode( \
                str(j[0]), \
                str(j[1]), \
                str(j[2]), \
                otherStyleTime,\
                URL, \
                str(j[5]), \
            )
        return True

    # 搜索小说名并记录
    def search_n(self,n_name):
        # 先清空
        self.window.record_list.setRowCount(0)
        self.window.record_list.clearContents()

        esjt = esj(False)
        n_list = esjt.get_sn_list(n_name)
        for j in n_list:
            # 转换时间格式
            timeStamp = j[5]
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
            # 拼接URL
            URL = esjt.mk_n_url(esj._N_XZ_DETAIL,str(j[0]))


            self.add_recode( \
                str(j[0]), \
                str(j[1]), \
                str(j[2]), \
                otherStyleTime,\
                URL, \
                str(j[5]), \
            )
        return True
  
#################################辅助函数#################################
    #在记录清单中添加一行
    def  add_recode(self,domain_name,domain_id,recode_name,recode_id,recode_type,token):
        q_domain_name = QTableWidgetItem(_fromUtf8(domain_name))
        q_domain_id = QTableWidgetItem(_fromUtf8(domain_id))
        q_recode_name = QTableWidgetItem(_fromUtf8(recode_name))
        q_recode_id = QTableWidgetItem(_fromUtf8(recode_id))
        q_recode_type = QTableWidgetItem(_fromUtf8(recode_type))
        q_token = QTableWidgetItem(_fromUtf8(token))
        

        last_row = self.window.record_list.rowCount()
        self.window.record_list.insertRow(last_row)
        self.window.record_list.setItem(last_row, 0, q_domain_name)
        self.window.record_list.setItem(last_row, 1, q_domain_id)
        self.window.record_list.setItem(last_row, 2, q_recode_name)
        self.window.record_list.setItem(last_row, 3, q_recode_id)
        self.window.record_list.setItem(last_row, 4, q_recode_type)
        self.window.record_list.setItem(last_row, 5, q_token)
        #由于可能显示不全，添加提示
        self.window.record_list.item(last_row, 0).setToolTip(_fromUtf8(domain_name))
        self.window.record_list.item(last_row, 2).setToolTip(_fromUtf8(recode_name))
        self.window.record_list.item(last_row, 5).setToolTip(_fromUtf8(token))
        self.window.record_list.resizeColumnsToContents()
        #每次刷新重新定义列宽
        self.window.record_list.setColumnWidth(0,100)
        self.window.record_list.setColumnWidth(1,180)
        self.window.record_list.setColumnWidth(2,100)
        self.window.record_list.setColumnWidth(3,100)
        self.window.record_list.setColumnWidth(4,240)
        
        
    #qstring转标准str
    def qstr_2_pystr(self, qStr):
    # # QString，如果内容是中文，则直接使用会有问题，要转换成 python string
        return unicode(qStr.toUtf8(), 'utf-8', 'ignore')


def do_errlog(modname,account,logname = g_logname):
    err_msg = traceback.format_exc()
    do_log(modname ,account ,
        "\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-B=-E=-G=-I=-N=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n\n" \
        +  err_msg \
        + "\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-E=-N=-D=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",\
        logname
    )

        
def do_log(modname,account,log_detail,logname = g_logname):
    print modname + '|' + account + ':' + log_detail
    ospath = cur_file_dir()
    fp = open(ospath + '/' + logname,"a")
    ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    fp.write(ctime + "|"  + modname + '|' + account + ':' +log_detail + "\n")
    fp.close()


def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，
    #如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)
