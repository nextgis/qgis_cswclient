# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cswclientdialogbase.ui'
#
# Created: Mon Oct  4 21:46:42 2010
#      by: PyQt4 UI code generator 4.5.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_CSWClientDialog(object):
    def setupUi(self, CSWClientDialog):
        CSWClientDialog.setObjectName("CSWClientDialog")
        CSWClientDialog.resize(544, 349)
        self.gridLayout_2 = QtGui.QGridLayout(CSWClientDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtGui.QGroupBox(CSWClientDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.cmbConnections = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbConnections.sizePolicy().hasHeightForWidth())
        self.cmbConnections.setSizePolicy(sizePolicy)
        self.cmbConnections.setObjectName("cmbConnections")
        self.gridLayout.addWidget(self.cmbConnections, 0, 0, 1, 5)
        self.btnSearch = QtGui.QPushButton(self.groupBox)
        self.btnSearch.setObjectName("btnSearch")
        self.gridLayout.addWidget(self.btnSearch, 1, 0, 1, 1)
        self.btnSrvInfo = QtGui.QPushButton(self.groupBox)
        self.btnSrvInfo.setObjectName("btnSrvInfo")
        self.gridLayout.addWidget(self.btnSrvInfo, 1, 1, 1, 1)
        self.btnNew = QtGui.QPushButton(self.groupBox)
        self.btnNew.setObjectName("btnNew")
        self.gridLayout.addWidget(self.btnNew, 3, 0, 1, 1)
        self.btnSave = QtGui.QPushButton(self.groupBox)
        self.btnSave.setObjectName("btnSave")
        self.gridLayout.addWidget(self.btnSave, 3, 4, 1, 1)
        self.btnLoad = QtGui.QPushButton(self.groupBox)
        self.btnLoad.setObjectName("btnLoad")
        self.gridLayout.addWidget(self.btnLoad, 3, 3, 1, 1)
        self.btnEdit = QtGui.QPushButton(self.groupBox)
        self.btnEdit.setObjectName("btnEdit")
        self.gridLayout.addWidget(self.btnEdit, 3, 1, 1, 1)
        self.btnDelete = QtGui.QPushButton(self.groupBox)
        self.btnDelete.setObjectName("btnDelete")
        self.gridLayout.addWidget(self.btnDelete, 3, 2, 1, 1)
        self.btnDefault = QtGui.QPushButton(self.groupBox)
        self.btnDefault.setObjectName("btnDefault")
        self.gridLayout.addWidget(self.btnDefault, 1, 4, 1, 1)
        self.btnShowCapabilities = QtGui.QPushButton(self.groupBox)
        self.btnShowCapabilities.setObjectName("btnShowCapabilities")
        self.gridLayout.addWidget(self.btnShowCapabilities, 1, 2, 1, 2)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 3)
        self.textCapabilities = QtGui.QTextEdit(CSWClientDialog)
        self.textCapabilities.setObjectName("textCapabilities")
        self.gridLayout_2.addWidget(self.textCapabilities, 1, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(CSWClientDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 2, 2, 1, 1)

        self.retranslateUi(CSWClientDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), CSWClientDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), CSWClientDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CSWClientDialog)

    def retranslateUi(self, CSWClientDialog):
        CSWClientDialog.setWindowTitle(QtGui.QApplication.translate("CSWClientDialog", "CSW Client", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("CSWClientDialog", "Server connections", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSearch.setText(QtGui.QApplication.translate("CSWClientDialog", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSrvInfo.setText(QtGui.QApplication.translate("CSWClientDialog", "Server info", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNew.setText(QtGui.QApplication.translate("CSWClientDialog", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSave.setText(QtGui.QApplication.translate("CSWClientDialog", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLoad.setText(QtGui.QApplication.translate("CSWClientDialog", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.btnEdit.setText(QtGui.QApplication.translate("CSWClientDialog", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDelete.setText(QtGui.QApplication.translate("CSWClientDialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDefault.setText(QtGui.QApplication.translate("CSWClientDialog", "Add default servers", None, QtGui.QApplication.UnicodeUTF8))
        self.btnShowCapabilities.setText(QtGui.QApplication.translate("CSWClientDialog", "Show server capabilities", None, QtGui.QApplication.UnicodeUTF8))

