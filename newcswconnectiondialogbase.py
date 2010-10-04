# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newcswconnectiondialogbase.ui'
#
# Created: Mon Oct  4 21:46:53 2010
#      by: PyQt4 UI code generator 4.5.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NewCSWConnectionDialog(object):
    def setupUi(self, NewCSWConnectionDialog):
        NewCSWConnectionDialog.setObjectName("NewCSWConnectionDialog")
        NewCSWConnectionDialog.resize(400, 138)
        self.verticalLayout = QtGui.QVBoxLayout(NewCSWConnectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(NewCSWConnectionDialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.leName = QtGui.QLineEdit(self.groupBox)
        self.leName.setObjectName("leName")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.leName)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.leURL = QtGui.QLineEdit(self.groupBox)
        self.leURL.setObjectName("leURL")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.leURL)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(NewCSWConnectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(NewCSWConnectionDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewCSWConnectionDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), NewCSWConnectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewCSWConnectionDialog)

    def retranslateUi(self, NewCSWConnectionDialog):
        NewCSWConnectionDialog.setWindowTitle(QtGui.QApplication.translate("NewCSWConnectionDialog", "Create a new CSW connection", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("NewCSWConnectionDialog", "Connection details", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewCSWConnectionDialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewCSWConnectionDialog", "URL", None, QtGui.QApplication.UnicodeUTF8))

