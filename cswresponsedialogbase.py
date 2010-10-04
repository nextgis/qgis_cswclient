# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cswresponsedialogbase.ui'
#
# Created by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_CSWResponseDialog(object):
    def setupUi(self, CSWResponseDialog):
        CSWResponseDialog.setObjectName("CSWResponseDialog")
        CSWResponseDialog.resize(467, 363)
        self.verticalLayout = QtGui.QVBoxLayout(CSWResponseDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textXML = QtGui.QTextEdit(CSWResponseDialog)
        self.textXML.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textXML.setObjectName("textXML")
        self.verticalLayout.addWidget(self.textXML)
        self.buttonBox = QtGui.QDialogButtonBox(CSWResponseDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CSWResponseDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), CSWResponseDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), CSWResponseDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CSWResponseDialog)

    def retranslateUi(self, CSWResponseDialog):
        CSWResponseDialog.setWindowTitle(QtGui.QApplication.translate("CSWResponseDialog", "Server response", None, QtGui.QApplication.UnicodeUTF8))

