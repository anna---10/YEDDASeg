# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'anno.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(".") if isfile(join(".", f))]
onlyfiles = [f for f in onlyfiles if f.endswith(".txt")]
onlyfiles.sort()
path = "./"

class Ui_Dialog(object):
    
    def get_txt(self):
        
        if isfile(path+onlyfiles[self.list_index]+".ann"):
            file_path = path+onlyfiles[self.list_index]+".ann"
            self.label_2.setText(onlyfiles[self.list_index]+".ann")
        else:
            file_path = path+onlyfiles[self.list_index]
            self.label_2.setText(onlyfiles[self.list_index])
        
        
        with open(file_path, "r") as file:
            txt = file.read()
        
        self.textEdit.setText(txt)
        
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1005, 704)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 2, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        
        #save
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.sve)
        self.verticalLayout_3.addWidget(self.pushButton_2)
        
        #next
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.nxt)
        self.verticalLayout_3.addWidget(self.pushButton_3)
        
        #back
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.bck)
        self.verticalLayout_3.addWidget(self.pushButton_4)
        
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_20 = QtWidgets.QLabel(Dialog)
        self.label_20.setObjectName("label_20")
        self.verticalLayout_2.addWidget(self.label_20)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_2.addWidget(self.label_14)
        self.label_15 = QtWidgets.QLabel(Dialog)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_2.addWidget(self.label_15)
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_2.addWidget(self.label_12)
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_2.addWidget(self.label_11)
        self.label_13 = QtWidgets.QLabel(Dialog)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_2.addWidget(self.label_13)
        self.label_10 = QtWidgets.QLabel(Dialog)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_2.addWidget(self.label_10)
        self.label_16 = QtWidgets.QLabel(Dialog)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_2.addWidget(self.label_16)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 2, 2, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 484, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        #added loading
        self.list_index = 0
        
        self.get_txt()
#         with open(path+onlyfiles[self.list_index], "r") as file:
#             txt = file.read()
        
#         self.textEdit.setText(txt)
        
        
        #added
        self.shortcut1 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+1"), self.textEdit)
        self.shortcut1.activated.connect(self.on_one)
        
        self.shortcut2 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+2"), self.textEdit)
        self.shortcut2.activated.connect(self.on_two)
        
        self.shortcut3 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+3"), self.textEdit)
        self.shortcut3.activated.connect(self.on_three)
        
        self.shortcut4 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+4"), self.textEdit)
        self.shortcut4.activated.connect(self.on_four)
        
        self.shortcut5 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+5"), self.textEdit)
        self.shortcut5.activated.connect(self.on_five)
        
        self.shortcut6 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+6"), self.textEdit)
        self.shortcut6.activated.connect(self.on_six)
        
        self.shortcut7 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+7"), self.textEdit)
        self.shortcut7.activated.connect(self.on_seven)
        
        self.shortcut8 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+8"), self.textEdit)
        self.shortcut8.activated.connect(self.on_eight)
        
        self.shortcut9 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+9"), self.textEdit)
        self.shortcut9.activated.connect(self.on_nine)
        
        self.shortcut10 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Space"), self.textEdit)
        self.shortcut10.activated.connect(self.on_concl)
        
        self.shortcut11 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+h"), self.textEdit)
        self.shortcut11.activated.connect(self.on_high)
        
        self.shortcut12 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+l"), self.textEdit)
        self.shortcut12.activated.connect(self.on_low)
        
        self.shortcut13 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+m"), self.textEdit)
        self.shortcut13.activated.connect(self.on_medium)
        
        self.shortcut14 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+o"), self.textEdit)
        self.shortcut14.activated.connect(self.on_out)
        
        
        #next
    
        
        
        
    def on_one(self):

        self.textEdit.insertPlainText("\n<<<aspect1>>>\n")
        
    def on_two(self):
        self.textEdit.insertPlainText("\n<<<aspect2>>>\n")
        
    def on_three(self):
        self.textEdit.insertPlainText("\n<<<aspect3>>>\n")
        
    def on_four(self):
        self.textEdit.insertPlainText("\n<<<aspect4>>>\n")
        
    def on_five(self):
        self.textEdit.insertPlainText("\n<<<aspect5>>>\n")
        
    def on_six(self):
        self.textEdit.insertPlainText("\n<<<aspect6>>>\n")
        
    def on_seven(self):
        self.textEdit.insertPlainText("\n<<<aspect7>>>\n")
    
    def on_eight(self):
        self.textEdit.insertPlainText("\n<<<aspect8>>>\n")
        
    def on_nine(self):
        self.textEdit.insertPlainText("\n<<<aspect9>>>\n")
        
    def on_concl(self):
        self.textEdit.insertPlainText("\n<<<conclusion>>>\n")
        
    def on_high(self):
        self.textEdit.insertPlainText("<<<high quality>>>\n")
        
    def on_low(self):
        self.textEdit.insertPlainText("<<<low quality>>>\n")
        
    def on_medium(self):
        self.textEdit.insertPlainText("<<<medium quality>>>\n")
        
    def on_out(self):
        self.textEdit.insertPlainText("\n<<<outside of argumentation>>>\n")
                            
    def nxt(self):
        self.list_index += 1
        self.get_txt()
    
    def bck(self):
        self.list_index -= 1
        self.get_txt()
        
    def sve(self):
        text = self.textEdit.toPlainText()
        with open(path+onlyfiles[self.list_index]+".ann", "w") as file:
            file.write(text)
    
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "TextLabel"))
        self.pushButton_2.setText(_translate("Dialog", "Save"))
        self.pushButton_3.setText(_translate("Dialog", "Next"))
        self.pushButton_4.setText(_translate("Dialog", "Back"))
        self.label_20.setText(_translate("Dialog", "Ctrl + :"))
        self.label_3.setText(_translate("Dialog", "1: aspect1"))
        self.label_4.setText(_translate("Dialog", "2: aspect2"))
        self.label_5.setText(_translate("Dialog", "3: aspect3"))
        self.label_6.setText(_translate("Dialog", "4: aspect4"))
        self.label_7.setText(_translate("Dialog", "5: aspect5"))
        self.label_8.setText(_translate("Dialog", "6: aspect6"))
        self.label_14.setText(_translate("Dialog", "7: aspect7"))
        self.label_15.setText(_translate("Dialog", "8: aspect8"))
        self.label_9.setText(_translate("Dialog", "9: aspect9"))
        self.label_12.setText(_translate("Dialog", "space: conclusion"))
        self.label_11.setText(_translate("Dialog", "h: high quality"))
        self.label_13.setText(_translate("Dialog", "l: low quality"))
        self.label_10.setText(_translate("Dialog", "m: medium quality"))
        self.label_16.setText(_translate("Dialog", "o: outside of argumentation"))
        self.pushButton.setText(_translate("Dialog", "save and exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

