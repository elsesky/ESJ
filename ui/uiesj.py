# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiesj.ui'
#
# Created: Thu Apr 29 15:17:48 2021
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_uiesj(object):
    def setupUi(self, uiesj):
        uiesj.setObjectName(_fromUtf8("uiesj"))
        uiesj.resize(750, 520)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(uiesj.sizePolicy().hasHeightForWidth())
        uiesj.setSizePolicy(sizePolicy)
        uiesj.setMinimumSize(QtCore.QSize(750, 520))
        uiesj.setMaximumSize(QtCore.QSize(750, 520))
        self.record_list = QtGui.QTableWidget(uiesj)
        self.record_list.setGeometry(QtCore.QRect(10, 60, 731, 381))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.record_list.sizePolicy().hasHeightForWidth())
        self.record_list.setSizePolicy(sizePolicy)
        self.record_list.setObjectName(_fromUtf8("record_list"))
        self.record_list.setColumnCount(6)
        self.record_list.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Adobe Devanagari"))
        item.setFont(font)
        self.record_list.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.record_list.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.record_list.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.record_list.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.record_list.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.record_list.setHorizontalHeaderItem(5, item)
        self.pushButton_p = QtGui.QPushButton(uiesj)
        self.pushButton_p.setGeometry(QtCore.QRect(640, 10, 91, 23))
        self.pushButton_p.setObjectName(_fromUtf8("pushButton_p"))
        self.txt_t__id = QtGui.QLineEdit(uiesj)
        self.txt_t__id.setGeometry(QtCore.QRect(100, 20, 521, 20))
        self.txt_t__id.setObjectName(_fromUtf8("txt_t__id"))
        self.label = QtGui.QLabel(uiesj)
        self.label.setGeometry(QtCore.QRect(10, 20, 91, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.layoutWidget = QtGui.QWidget(uiesj)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 450, 701, 25))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_s_r = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_s_r.setObjectName(_fromUtf8("pushButton_s_r"))
        self.horizontalLayout.addWidget(self.pushButton_s_r)
        self.pushButton_s_p = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_s_p.setObjectName(_fromUtf8("pushButton_s_p"))
        self.horizontalLayout.addWidget(self.pushButton_s_p)
        self.pushButton_s_op = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_s_op.setObjectName(_fromUtf8("pushButton_s_op"))
        self.horizontalLayout.addWidget(self.pushButton_s_op)
        self.pushButton_s_o = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_s_o.setObjectName(_fromUtf8("pushButton_s_o"))
        self.horizontalLayout.addWidget(self.pushButton_s_o)
        self.pushButton_op = QtGui.QPushButton(uiesj)
        self.pushButton_op.setGeometry(QtCore.QRect(640, 33, 91, 23))
        self.pushButton_op.setObjectName(_fromUtf8("pushButton_op"))
        self.layoutWidget1 = QtGui.QWidget(uiesj)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 490, 711, 25))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.n_name = QtGui.QLineEdit(self.layoutWidget1)
        self.n_name.setObjectName(_fromUtf8("n_name"))
        self.gridLayout.addWidget(self.n_name, 0, 1, 1, 1)
        self.pushButton_s_n = QtGui.QPushButton(self.layoutWidget1)
        self.pushButton_s_n.setObjectName(_fromUtf8("pushButton_s_n"))
        self.gridLayout.addWidget(self.pushButton_s_n, 0, 2, 1, 1)

        self.retranslateUi(uiesj)
        QtCore.QMetaObject.connectSlotsByName(uiesj)

    def retranslateUi(self, uiesj):
        uiesj.setWindowTitle(_translate("uiesj", "esj_ui", None))
        item = self.record_list.horizontalHeaderItem(0)
        item.setText(_translate("uiesj", "小说ID", None))
        item = self.record_list.horizontalHeaderItem(1)
        item.setText(_translate("uiesj", "小说名称", None))
        item = self.record_list.horizontalHeaderItem(2)
        item.setText(_translate("uiesj", "作者", None))
        item = self.record_list.horizontalHeaderItem(3)
        item.setText(_translate("uiesj", "最后更新", None))
        item = self.record_list.horizontalHeaderItem(4)
        item.setText(_translate("uiesj", "URL", None))
        item = self.record_list.horizontalHeaderItem(5)
        item.setText(_translate("uiesj", "阅览次数", None))
        self.pushButton_p.setText(_translate("uiesj", "采集", None))
        self.label.setText(_translate("uiesj", "输入小说ID", None))
        self.pushButton_s_r.setText(_translate("uiesj", "刷新", None))
        self.pushButton_s_p.setText(_translate("uiesj", "采集选中", None))
        self.pushButton_s_op.setText(_translate("uiesj", "采集并输出选中", None))
        self.pushButton_s_o.setText(_translate("uiesj", "输出", None))
        self.pushButton_op.setText(_translate("uiesj", "采集并输出", None))
        self.label_2.setText(_translate("uiesj", "输入小说名称", None))
        self.pushButton_s_n.setText(_translate("uiesj", "搜索", None))

