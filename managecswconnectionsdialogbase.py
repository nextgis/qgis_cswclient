# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'managecswconnectionsdialogbase.ui'
#
# Created: Mon Oct  4 21:46:56 2010
#      by: PyQt4 UI code generator 4.5.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ManageCSWConnectionsDialog(object):
    def setupUi(self, ManageCSWConnectionsDialog):
        ManageCSWConnectionsDialog.setObjectName("ManageCSWConnectionsDialog")
        ManageCSWConnectionsDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(ManageCSWConnectionsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(ManageCSWConnectionsDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.leFileName = QtGui.QLineEdit(ManageCSWConnectionsDialog)
        self.leFileName.setObjectName("leFileName")
        self.horizontalLayout.addWidget(self.leFileName)
        self.btnBrowse = QtGui.QPushButton(ManageCSWConnectionsDialog)
        self.btnBrowse.setObjectName("btnBrowse")
        self.horizontalLayout.addWidget(self.btnBrowse)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listConnections = QtGui.QListWidget(ManageCSWConnectionsDialog)
        self.listConnections.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listConnections.setAlternatingRowColors(True)
        self.listConnections.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listConnections.setObjectName("listConnections")
        self.verticalLayout.addWidget(self.listConnections)
        self.buttonBox = QtGui.QDialogButtonBox(ManageCSWConnectionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ManageCSWConnectionsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ManageCSWConnectionsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ManageCSWConnectionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ManageCSWConnectionsDialog)

    def retranslateUi(self, ManageCSWConnectionsDialog):
        ManageCSWConnectionsDialog.setWindowTitle(QtGui.QApplication.translate("ManageCSWConnectionsDialog", "Manage connections", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ManageCSWConnectionsDialog", "Save to file", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowse.setText(QtGui.QApplication.translate("ManageCSWConnectionsDialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))

