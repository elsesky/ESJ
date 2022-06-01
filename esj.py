#! /usr/bin/env python
#-*-coding:UTF-8-*-

import HTMLParser
import io
import urllib,urllib2,cookielib,re,random,time,ConfigParser,os,sys,hashlib,math,platform
import win32api,win32con,win32gui
import traceback
from urllib import quote
import requests,requests.utils, pickle
import json
import MySQLdb
#from odbc import SQL_FETCH_ABSOLUTE
import re
import types
from time import sleep
from _mysql import result
from _ctypes import Array
from array import array
from __builtin__ import str
import base64
from itertools import count
# from selenium import webdriver
from time import sleep
# 简繁转换库
from zhconv import convert
# HTML处理库
from chtml import filter_tags



default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
# requests访问https协议等需要定位证书
os.environ['REQUESTS_CA_BUNDLE'] =  os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')
    
class esj:
#    数据库设置
    _DB_HOST = ''  #服务器地址
    _DB_NAME = ''   #数据库名
    _DB_USER = ''  #用户名
    _DB_PWD = ''   #密码
    _DB_PORT = 53306    #端口
    _DB_PREFIX = ''  #数据库表前缀
    _CLASS_NAME = ""
    _TIMEOUT = 15
    _modname = 'esj'
    _PROXIES = { "http": "http://10.0.0.2:7899"  ,  "https": "http://10.0.0.2:7899"}   
#    采集相关设置
    _N_HOST = "https://www.esjzone.net/"
    _N_XZ_DETAIL = "https://www.esjzone.net/detail/"
    _N_XZ_CONTENT = "https://www.esjzone.net/forum/"
    _DB = None
    _S = None
    window = None
    _USERMAIL = ''
    _USERPWD = ''
    
    
    
    _headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.35',\
        'origin':'https://www.esjzone.net',\
        'Referer':'https://www.esjzone.net',\
        # 'authorization':'76dd133df3N5_RKm4T56Uezr-aHjPTf3LMjUuKBrEA_qQ4Aazas-fLP8FHshz9Gm3Q_mCZCbdI00mqhUahs_cNmKH5f3o9wwk9pOE',\
        # 'cookie' : 'hidden=value; hidden=value; _ga=GA1.2.1022070352.1653370996; ws_wt=0; ws_last=d7d7f86422BEJdQwHYifIql2-qqFrBu1JU0vba6K3OMeLoYBSmUg; msg_alert=10; _gid=GA1.2.2007424314.1653974365; ws_last_visit_post=d698013b291PldQAiHXhq0nLGiEPubfbplxneq2OrIDnOeHvOdJOU; ws_rr=067165654d287NW4gCmdWR4xgpSy9u6M7HJw_5wCntHT0WZZYb9N3Y9IoQ-pUmS8Sxz_leRHuJr07rAEaCj38l7JHnNTS7Tc_IR8VBysmD4wJsylD5Eu8; ws_last_visit_code=96bd6c4a0d6xX0eaGCij6ZbCDZjgsYXbFSzjMpdsy2jtvTn1MHUXaYC8bTGNdknwUKnkf8ZCO9; __cf_bm=vnd.JdRk6vcpnlFrji.W6MUlWRcBmPT6_XaJocjW5mI-1653975276-0-AVgnCJMs74UNEKaO4WYWWqasP177m/43d52nulEAadRWEacnYk+wGY6WmCiMrAORPz+Sw6laU1+sKaEeBJBs8ewjL8N+MJY29/pQkmORoKcbhyfkcyCe3OB5oOopiIGkdw==; ws_key=fa13f5adb8Dficp8uoGdplzkMIz6wWLkoUB6B303etYQH0aRiOgG8NpYx6hta6DPixKK8; ws_token=32b50d2e3aOwBmorLBSVtoYJ5HpQEQiXzVLGUxTJUOp0iNpQCg4psv6ysMDh-fPEMqVIarRk1PeMhkoRHG5TlnKUOW71632j_I9UQ'
    } 

    def __init__(self,login=True):
        self.set_user_login_from_ini()
        self._DB = MySQLdb.connect(self._DB_HOST,self._DB_USER,self._DB_PWD,self._DB_NAME,charset='utf8',port=self._DB_PORT)
        s = requests.Session()
        # 先登录，如果登录失败，则退出
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',\
            'origin':'https://www.esjzone.net',\
            'cache-control': 'no-cache',\
        } 
        # 由于该类会被esj_ui调用，而esj_ui里面某些操作只会查询数据库，不会连接esj网站，这种情况下不需要触发登录。
        if login:
            s = self.user_login(s)
        self._S = s

    # 从ini文件读取配置
    def set_user_login_from_ini(self):
        #根据配置文件读取配置
        from config_core import config_c
        cfg_esj = config_c(self)
        # 数据库部分,注意，没有做合规性检查
        self._DB_HOST = cfg_esj.get_conf_val("MYSQLDB","_DB_HOST")
        self._DB_NAME = cfg_esj.get_conf_val("MYSQLDB","_DB_NAME")
        self._DB_USER = cfg_esj.get_conf_val("MYSQLDB","_DB_USER")
        self._DB_PWD = cfg_esj.get_conf_val("MYSQLDB","_DB_PWD")
        _DB_PORT = int(cfg_esj.get_conf_val("MYSQLDB","_DB_PORT"))
        try:
            if int(_DB_PORT) > 65534 or int(_DB_PORT) < 1:
                _DB_PORT = 3306
        except Exception as e:
            _DB_PORT = 15
        self._DB_PORT = _DB_PORT
        self._DB_PREFIX = cfg_esj.get_conf_val("MYSQLDB","_DB_PREFIX")
        # 链接超时时间
        timeout = cfg_esj.get_conf_val("SITE","_TIMEOUT")
        try:
            if int(timeout) < 15:
                timeout = 15
        except Exception as e:
            timeout = 15
        self._TIMEOUT = float(timeout)
        # 用户部分，注意，没有做合规性检查
        self._USERMAIL = cfg_esj.get_conf_val("USER","email")
        self._USERPWD = cfg_esj.get_conf_val("USER","pwd")

    # 用户登录
    def user_login(self,s):
        try:
            # 获取token
            post_data = {'plxf':'getAuthToken'}
            r = s.post('https://www.esjzone.net/my/login',timeout=10,data=post_data)
            # 提交登录
            post_data = {
                'email':self._USERMAIL,\
                'pwd':self._USERPWD,\
                'remember_me':'on',\
            }
            r = s.post('https://www.esjzone.net/inc/mem_login.php',timeout=10,data=post_data)
            time.sleep(1)
            # 验证用户是否登录
            r = s.get('https://www.esjzone.net/my/profile',timeout=10)
            if len(r.text.split('elsesky')) > 1:
                do_log('esj','elsesky','[OK]||User login success!')
            else:
                do_log('esj','elsesky','[FAILED]||User login failed')
        except Exception,e:
            do_log('esj','elsesky','[FAILED]||User login failed')
            do_errlog('esj','elsesky')

        return s

    #论坛水帖
    def shui(self):
        s = self._S
        try:
            # 获取token
            post_data = {'plxf':'getAuthToken'}
            r = s.post('https://www.esjzone.net/forum/1585405223/80242.html',headers=self._headers,timeout=10,data=post_data)
            # 提交登录
            post_data = {
                'content':'每日的水1则',\
                'data':'forum',\
                'forum_id':'80242',\
            }
            r = s.post('https://www.esjzone.net/inc/forum_reply.php',timeout=10,headers=self._headers,data=post_data)
            time.sleep(1)
            do_log('esj','elsesky','[OK]||Daly checkin done!')

        except Exception,e:
            do_log('esj','elsesky','[FAILED]||User login failed')
            do_errlog('esj','elsesky')


    def getpicbyidq(self,t__id,outputtxt = False):
        time.sleep(1)
        # -------------------开始处理内容--------------------
        nl_content = self.open_by_id(t__id)
        # print(nl_content.encode('UTF-8'))
        # exit()
        if type(nl_content) is types.NoneType:
            do_log(self._modname ,'root' ,"ERR:小说id:" + t__id + " 获取失败!")
            return -1
        try:
            lu = self.get_luq(nl_content)
            # print lu
            author = self.addslashes(self.get_authorq(nl_content))
            # print author
            name = self.addslashes(self.get_nameq(nl_content))
            # print name
            ImageUrl = self.addslashes(self.get_ImageUrlq(nl_content))
            # print ImageUrl
            ViewCount = str(self.get_ViewCountq(nl_content))
            # print ViewCount       
            rcount = 0
            rcount = str(self.get_RCountq(nl_content))
        except Exception,e:
            do_errlog(self._modname,'root')
            return -1
        
        if ViewCount=='还没有':
            ViewCount = str(0)
        Introduction = self.addslashes(HTMLParser.HTMLParser().unescape(self.get_Introductionq(nl_content))).replace("<p>", "").replace("</p>", "")
        #检查是否存在
        id_count = self.get_id_count(t__id)
        if id_count<1:
            #不存在，插入
            do_log(self._modname ,'root' ,"新增小说:" + name + " ")
            self.do_taginsert(t__id, lu, name, 0, ViewCount, rcount, Introduction, author, ImageUrl)
        else:
            #存在，更新最后更新时间
            cursor = self._DB.cursor()
            sql = "UPDATE " + self._DB_PREFIX + self._CLASS_NAME + "novels SET lastupdate=" + str(lu) + ",ViewCount=" + ViewCount + ",rcount=" + rcount + " WHERE id = " + t__id
            try:
                do_log(self._modname ,'root' ,"更新小说:" + name + " ")
                cursor.execute(sql)
                self._DB.commit()
            except Exception,e:
                print e
                self._DB.rollback()
                do_log(self._modname ,'root' ,'Unknown ERR!')

        result = self.get_id_count(t__id, 'nid', 'chapters')
        #---------------- 插入小说记录完毕 --------------------------
        # ----------------获取章节ID列表-------------------------
        # 注意，有可能整个小说内容都是空的情况，直接跳过
        try:
            cptext = nl_content.split('<div id="chapterList">')[1].split("</div>")[0]
        except Exception,e:
            do_log(self._modname ,'root' ,'该小说内容为空，很可能是ESJ把内容清空了，请直接访问网站确认。')
            return -1

        tids =  re.findall(r'<a(.*)/(.*)\.html\" target=',cptext)
        # 如果返回的章节数为0，则可能是调用其他网站的连接，需要提示。
        if len(tids) < 1:
            do_log(self._modname ,'root' ,"该小说的内容为外部连接，无法采集，请直接访问网站查看。")
            return -1
            pass
        order_num = 1
        for tds in tids:
            # 以下三行是用来跳前面采集的内容，调试用
            # if order_num < 275:
            #     order_num = order_num + 1
            #     continue
            tid = tds[1]
            # ----------------进章节采集-----------------------------
            turl = self._N_XZ_CONTENT + t__id + "/" + tid + ".html"
            tl_content = self.open(turl)
            ######################## 处理正文内容 ##############################
            # 注意，有的情况下，连接的内容可能被删除了，需要跳过
            try:
                t_title = tl_content.split("<h2>")[1].split('</h2>')[0]
                # 繁转简
                t_title = convert(t_title, 'zh-hans')
            except Exception,e:
                do_log(self._modname ,'root' ,'该小节内容为空，跳过。')
                do_log(self._modname ,'root' ,'访问URL为：' + turl)
                continue
                pass
            t_text = tl_content.split('<div class="forum-content mt-3" id="">')[1]             \
            .split('</div>')[0]\
            .replace("&nbsp;" , "")\
            .replace("<p>" , "")\
            .replace("<br>" , "")\
            .replace("</p>" , "")
            # 繁转简
            t_text = convert(t_text, 'zh-hans')
            #去掉HTML剩余标记
            t_text = filter_tags(t_text)
            # 带HTML转义字符的文本串（自动加了每小节标题，带5位顺序号，方便转EPUB）
            t_all_text_html = self.addslashes("\n\n" + str(order_num).zfill(5) + " - " + t_title + "\n\n" + t_text)
            #------------调试用，检查简繁转换是否正常---------------
            # print base64.b64encode(t_all_text_html)
            # exit()
            #------------调试用，检查简繁转换是否正常---------------

            # 去掉HTML转义字符的文本串(如果这个后续入库报错，就用前面那个)
            t_text = HTMLParser.HTMLParser().unescape(t_text)
            # 带HTML转义字符的文本串（自动加了每小节标题，带5位顺序号，方便转EPUB）
            t_all_text_org = self.addslashes("\n\n" + str(order_num).zfill(5) + " - " + t_title + "\n\n" + t_text)
            t_title_print = t_title.replace('・','')
            # ---------------------入库---------------------------------
            #跳过已经有的（通过数据库检查）
            tid_count = self.get_tid_count(tid)
            if tid_count > 0:
                # do_log(self._modname ,'root' ,"|跳过章节:" + t_title + "|")
                # 如果存在，跳过，但是要更新排序号（因为可能由于插入中间章节，导致序号会变）
                cursor = self._DB.cursor()
                sql = "UPDATE " + self._DB_PREFIX + self._CLASS_NAME + "chapters SET order_num=" + str(order_num) + " WHERE id=" + tid
                try:
                    do_log(self._modname ,'root' ,"更新章节|" + t_title_print + "|排序为：" + str(order_num))
                    cursor.execute(sql)
                    self._DB.commit()
                    # 由于这里会跳过，记得让序号自增
                    order_num = order_num + 1
                except Exception,e:
                    print e
                    self._DB.rollback()
                    do_log(self._modname ,'root' ,'Unknown ERR!')
                continue
            do_log(self._modname ,'root' ,"|新增章节:" + t_title_print + "|")
            # t_id：小说ID，tid：章节ID，t_title：章节名称，t_all_text_html：带HTML转义字符的文本串，t_all_text_org:去掉HTML转义字符的文本串
            try:
                result = self.do_photoinsert(t__id, tid, self.addslashes(t_title), t_all_text_html, t_all_text_org,str(order_num))
            except Exception,e:
                print Exception,":",e
            order_num = order_num + 1
            #判断是否插入失败或者有重复
            # if not result:
            #     return False
        # ---------------------如果设置了输出标识，则输出内容-------------------
        # 注意这里的fp是在函数一开始就定义了的
        if outputtxt :
            # -------------------直接重新写文件--------------------
            ospath = cur_file_dir()
            fp = open(ospath + '/' + str(t__id) + ".txt","w")
            # 从数据库中查出内容
            cursor = self._DB.cursor()
            sql = "SELECT " + self._DB_PREFIX + self._CLASS_NAME + "chapter_name , content " + " FROM " + self._DB_PREFIX  + self._CLASS_NAME + "chapters where nid=" + t__id + " order by order_num asc"
            txt_array = []
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                for i in results:
                    do_log(self._modname ,'root' ,"|正在输出章节:[" + i[0].replace('・','') + "]的内容|")
                    fp.write(base64.b64decode(i[1]))
            except Exception,e:
                print Exception,":",e
                self._DB.rollback()
                do_log(self._modname ,'root' ,'Unknown ERR!')
            fp.close()
        return True

    
    def outputbyidq(self,t__id):
        # -------------------直接重新写文件--------------------
        ospath = cur_file_dir()
        fp = open(ospath + '/' + str(t__id) + ".txt","w")
        # 从数据库中查出内容
        cursor = self._DB.cursor()
        sql = "SELECT " + self._DB_PREFIX + self._CLASS_NAME + "chapter_name , content " + " FROM " + self._DB_PREFIX  + self._CLASS_NAME + "chapters where nid=" + t__id + " order by order_num asc"
        txt_array = []
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for i in results:
                do_log(self._modname ,'root' ,"|正在输出章节:[" + i[0].replace('・','') + "]的内容|")
                fp.write(base64.b64decode(i[1]))
        except Exception,e:
            print Exception,":",e
            self._DB.rollback()
            do_log(self._modname ,'root' ,'Unknown ERR!')
        fp.close()
        return True

    def get_n_list(self):
        cursor = self._DB.cursor()
        sql = "SELECT * FROM  novels order by lastupdate desc"
        txt_array = []
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception,e:
            print Exception,":",e
            self._DB.rollback()
            do_log(self._modname ,'root' ,'Unknown ERR!')
            return txt_array
    
    def outputbyidq_with_path(self,t__id,full_path):
        # -------------------直接重新写文件--------------------
        fp = open(full_path ,"w")
        # 从数据库中查出内容
        cursor = self._DB.cursor()
        sql = 'SELECT chapter_name,content,order_num FROM chapters where nid=' + t__id + ' order by order_num asc'
        txt_array = []

        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for i in results:
                try:
                    do_log(self._modname ,'root' ,"|[OK]正在输出章节:[" + i[0].replace('・','') + "]的内容|")
                    # 输出章节标题（强制繁简转换）
                    cn = convert(i[0].replace('・',''), 'zh-hans')
                    # 在采集的时候已经加了，没必要在输出的时候再加一次
                    # fp.write(str(i[2]).zfill(5) + " - " + cn + "\n")
                    # 输出章节内容（强制繁简转换）
                    fp.write(convert(base64.b64decode(i[1]),'zh-hans'))
                    fp.write("\n\n")

                except Exception,e:
                    do_log(self._modname ,'root' ,"|[FAILED]|章节:[" + i[0].replace('・','') + "]输出失败|")
                    print Exception,":",e
        except Exception,e:
            print Exception,":",e
            self._DB.rollback()
            do_log(self._modname ,'root' ,'Unknown ERR!')
        fp.close()
        return True

    # 小说名模糊查询
    def get_sn_list(self,n_name):
        # 将传入的关键字均做一次简转繁和繁转简，然后组合成三关键词的模糊查询，通用识别输入内容为简体或者繁体的情况。
        n1 = convert(n_name, 'zh-hans')
        n2 = convert(n_name, 'zh-hant')
        cursor = self._DB.cursor()
        sql = "SELECT * FROM  novels where name LIKE \"%" + n_name + "%\"" + " OR name LIKE \"%" + n1 + "%\"" +  " OR name LIKE \"%" + n2 + "%\"" + " order by lastupdate desc"
        # 避免空提交
        if len(n_name.strip()) < 1:
            sql = "SELECT * FROM  novels order by lastupdate desc"
        txt_array = []
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception,e:
            print Exception,":",e
            self._DB.rollback()
            do_log(self._modname ,'root' ,'Unknown ERR!')
            return txt_array


    def do_taginsert(self, t__id, lu, name, count, scount, rcount, Introduction, author, ImageUrl):
        cursor = self._DB.cursor()
        sql = "INSERT INTO " + self._DB_PREFIX + self._CLASS_NAME + "novels(id , name, Author, ImageUrl, Introduction,lastupdate,count,ViewCount,rcount)  \
        VALUES ('" + t__id + "','" + name + "','" + author + "','" + ImageUrl + "','" + Introduction + "','" + str(lu) + "','" + str(count) + "','" + scount + "','" + str(rcount) + "')"
        try:
            cursor.execute(sql)
            self._DB.commit()
        except Exception,e:
            print Exception,":",e
            self._DB.rollback()
            do_log(self._modname ,'root' ,'Unknown ERR!')
    
    def do_photoinsert(self,t__id, nid, chapter_name, orgcontent, content,order="0"):
        orgcontent = base64.b64encode(orgcontent)
        content = base64.b64encode(content)
        cursor = self._DB.cursor()
        sql = "INSERT INTO " + self._DB_PREFIX + self._CLASS_NAME + "chapters(`nid` , `id`, `chapter_name`, `orgcontent`, `content`,`order_num`) \
        VALUES ('" + t__id + "','" + nid + "','" + chapter_name + "','" + orgcontent + "','" + content + "','" + order + "')"
        try:
            cursor.execute(sql)
            self._DB.commit()
        except Exception,e:
            print Exception,":",e
            self._DB.rollback()
            do_log(self._modname ,'root' ,'Unknown ERR!')
            return False
        return True
    
    def get_id_count(self,t__id,idname='id',tablename = 'novels'):
        cursor = self._DB.cursor()
        sql = "SELECT count(*) FROM " + self._DB_PREFIX + self._CLASS_NAME + tablename + " where " + idname +"=" + t__id
        cursor.execute(sql)
        results = cursor.fetchall()
        return results[0][0]
    
    def get_tid_count(self,t__id,idname='id',tablename = 'chapters'):
        cursor = self._DB.cursor()
        sql = "SELECT count(*) FROM " + self._DB_PREFIX + self._CLASS_NAME + tablename + " where " + idname +"=" + t__id
        cursor.execute(sql)
        results = cursor.fetchall()
        return results[0][0]
        
    def get_lu(self,content):
        try:
            lu = content.encode('UTF-8').split('更新日期:</strong> ')[1].split('</li>')[0]
        except Exception,e:
            print e
            return -1
        lu = time.mktime(time.strptime(lu,'%Y-%m-%d'))
        return int(lu)

    def get_luq(self,content):
        try:
            lu = content.encode('UTF-8').split('更新日期:</strong> ')[1].split('</li>')[0]
        except Exception,e:
            print e
            return -1
        lu = time.mktime(time.strptime(lu,'%Y-%m-%d'))
        return int(lu)
        
    def get_author(self,content) :
        author = content.encode('UTF-8').split('作者：')[1].split('</span>')[0]
        return author

    def get_authorq(self,content) :
        try:
            author = content.encode('UTF-8').split('作者:</strong> ')[1].split('</a>')[0].split('">')[1]
        except Exception,e:
            # 可能存在有的没有描述的情况，会出现异常。
            do_log(self._modname ,'root' ,'[INFO]|该小说无作者')
            author = "佚名"
        return author
    
    def get_name(self,content) :
        name = content.encode('UTF-8').split('"><h1>')[1].split('</h1></a></li>')[0]
        return name

    def get_nameq(self,content) :
        try:
            name = content.encode('UTF-8').split('p-t-10 text-normal">')[1].split('</h2>')[0]
        except Exception,e:
            # 可能存在有的没有描述的情况，会出现异常。
            do_log(self._modname ,'root' ,'[INFO]|该小说无书名')
            name = "无名"
        return name

    def get_ImageUrl(self,content) :
        ImageUrl = content.encode('UTF-8').split('"><img src="')[1].split('" alt="')[0]
        return ImageUrl

    def get_ImageUrlq(self,content) :
        try:
            ImageUrl = content.encode('UTF-8').split('product-gallery text-center mb-3')[1].split('" alt="')[0].split('<img src="')[1]
        except Exception,e:
            ImageUrl = '#'
            pass
        return ImageUrl

    def get_ViewCount(self,content) :
        ViewCount = content.encode('UTF-8').split('class="fontorange12">')[1].split('人</span>')[0]
        return ViewCount

    def get_ViewCountq(self,content) :
        ViewCount = content.encode('UTF-8').split('<span id="vtimes">')[1].split('</span>')[0]
        return ViewCount
        # return 0
    
    def get_RCountq(self,content) :
        RCount = content.encode('UTF-8').split('<span id="favorite">')[1].split('</span>')[0]
        return RCount
        # return 0
    
    def get_Introduction(self,content) :
        Introduction = content.encode('UTF-8').split('id="full_intro">')[1].split('</div>')[0]
        return Introduction

    def get_Introductionq(self,content) :
        try:
            Introduction = content.encode('UTF-8').split('<div class="description">')[1].split('</div>')[0]
        except Exception,e:
            # 可能存在有的没有描述的情况，会出现异常。
            do_log(self._modname ,'root' ,'[INFO]|该小说无描述')
            Introduction = "无描述"
        return Introduction

    def get_totalpage(self,content):
        total_pages = content.encode('UTF-8').split('下一頁')[0].split('<a class=onpage>1</a>')[1].split('</a>')
        tl = len(total_pages)
        total_pages[tl-2].split('>')
        return total_pages[1]
        
    def open_by_id(self,t__id):
        ospath = cur_file_dir()
        # 注意，必须先访问一次该站的引用页以获取cookie，然后才能开始访问实际需要访问的站
        s = self._S
        # s.get('https://www.esjzone.net/')
        url = self.mk_n_url(self._N_XZ_DETAIL, t__id)
        try:
            r = s.get(url,headers=self._headers,timeout=self._TIMEOUT)
            # r = s.get(url)
            # content = s.page_source
            # print 1
            # time.sleep(10)
            # print content.encode('UTF-8')
            # print 2
            # return content
            return r.text
        except Exception,e:
            do_errlog('esj','elsesky')
    
    def open(self,url):
        time.sleep(1)
        s = self._S
        
        #print self._headers
        try:
            r = s.get(url,headers=self._headers,timeout=self._TIMEOUT)
            return r.text
        except Exception,e:
            print e
            do_log(self._modname ,'root' ,'err in open')

        # r = s.get(url)
        # time.sleep(10)
        # content = s.page_source
        # return content

        
    
    def mk_n_url(self,host,t__id):
        # https://www.esjzone.net/detail/1580565850.html
        # print(str(host) + str(t__id) + ".html")
        return str(host) + str(t__id) + ".html"
        
   
    def mk_utf8txtdl_url(self,host, t__id, cid):
        return host + t__id + "/" + cid + "/" + cid + ".txt";
    
    def mk_gbktxtdl_url(self,host, t__id, cid):
        return host + t__id + "/" + cid + "/" + cid + "_GBK.txt";
        
    def addslashes(self,s):
        d = {'"':'\\"', "'":"\\'", "\0":"\\\0", "\\":"\\\\"}
        return ''.join(d.get(c, c) for c in s)
        
    def clear_tag_by_id(self,t__id):
        try:
            cursor = self._DB.cursor()
            sql = "UPDATE " + self._DB_PREFIX + self._CLASS_NAME + "novels SET `count`=0 where id=" + t__id
            cursor.execute(sql)
            sql = "DELETE FROM " + self._DB_PREFIX + self._CLASS_NAME + "chapters WHERE nid=" + t__id;
            cursor.execute(sql)
            self._DB.commit()
        except Exception,e:
            print Exception,":",e
            do_log(self._modname ,'root' ,'Unknown ERR!')

    def clear_tag_by_idq(self,t__id):
        try:
            cursor = self._DB.cursor()
            sql = "UPDATE " + self._DB_PREFIX + self._CLASS_NAME + "novels SET `count`=0,`ViewCount`=0,`rcount`=0 where id=" + t__id
            cursor.execute(sql)
            sql = "DELETE FROM " + self._DB_PREFIX + self._CLASS_NAME + "chapters WHERE nid=" + t__id;
            cursor.execute(sql)
            self._DB.commit()
            return True
        except Exception,e:
            do_errlog(self._modname ,'root')
            return False

        
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

def do_errlog(modname,account,logname = 'log.log'):
    err_msg = traceback.format_exc()
    do_log(modname ,account ,
        "\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-B=-E=-G=-I=-N=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n\n" \
        +  err_msg \
        + "\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-E=-N=-D=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",\
        logname
    )

def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，
    #如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

def str_deal(in_str):
    in_str = in_str.replace("ㆁ","")\
        .replace("ω","")\
        .replace("ლ","")\
        .replace("ڡ","")
    return in_str

def show_usage():
    print 'Usage: python main.py [OPTION]'
    print 'By id:'
    print '    -p idnumbers such as 2013'


    
if __name__ == '__main__':
    if len(sys.argv)<2:
        show_usage()
        sys.exit(-1)
    dmzjt = esj()
    #检测输入参数
    if sys.argv[1] == '-p':
        if len(sys.argv)<3:
            print 'You must input the novel id!'
            show_usage()
            sys.exit(-1)
        if int(sys.argv[2]) > 0:
            i_d = sys.argv[2]
            result = dmzjt.getpicbyidq(i_d)
            if not result:
                do_log('esj' ,'root' ,"插入失败，可能为中间插入章节导致，将清空该小说后重新采集。")
                # dmzjt.clear_tag_by_id(i_d)
                dmzjt.getpicbyidq(i_d)
            do_log('esj' ,'root' ,"采集结束。")
            sys.exit(result)
        else:
            print 'You must input the novel id!'
            show_usage()
    elif sys.argv[1].lower() == '-op':
        if len(sys.argv)<3:
            print 'You must input the novel id!'
            show_usage()
        if int(sys.argv[2]) > 0:
            i_d = sys.argv[2]
            result = dmzjt.getpicbyidq(i_d,True)
            if not result:
                do_log('esj' ,'root' ,"插入失败，可能为中间插入章节导致，将清空该小说后重新采集。")
                # dmzjt.clear_tag_by_id(i_d)
                dmzjt.getpicbyid(i_d,True)
            do_log('esj' ,'root' ,"采集结束。")
            sys.exit(result)
    # 清空并重新采集指定小说内容
    elif sys.argv[1].lower() == '-cp':
        if len(sys.argv)<3:
            print 'You must input the novel id!'
            show_usage()
        if int(sys.argv[2]) > 0:
            i_d = sys.argv[2]
            result = dmzjt.clear_tag_by_idq(i_d)
            if not result:
                # 清空出错时终止后续重采集
                do_log('esj' ,'root' ,"清空过程中出现错误，请检查代码。")
            else:
                # 清空正常后，重新采集
                do_log('esj' ,'root' ,"开始重采集。")
                result = dmzjt.getpicbyidq(i_d)
                do_log('esj' ,'root' ,"清空并重采集完毕。")
            sys.exit(result)
    # 水帖
    elif sys.argv[1].lower() == '-shui':
            result = dmzjt.shui()
            sys.exit(0)
    elif sys.argv[1].lower() == '-o':
        if len(sys.argv)<3:
            print 'You must input the novel id!'
            show_usage()
            exit()
        if int(sys.argv[2]) > 0:
            i_d = sys.argv[2]
            result = dmzjt.outputbyidq(i_d)
            if not result:
                do_log('esj' ,'root' ,"输出失败，请检查ID是否存在")
            else :
                do_log('esj' ,'root' ,"输出完成")
    elif sys.argv[1].lower() == '-oth':
        if len(sys.argv)<4:
            print 'You must input the novel id and path!'
            show_usage()
        if int(sys.argv[2]) > 0:
            i_d = sys.argv[2]
            path = sys.argv[3]
            result = dmzjt.outputbyidq_with_path(i_d,path)
            if not result:
                do_log('esj' ,'root' ,"输出失败，请检查ID是否存在")
            else :
                do_log('esj' ,'root' ,"输出完成")
        
    else:
        show_usage()
        sys.exit(-1)


    dmzjt._DB.close()
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
