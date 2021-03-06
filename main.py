# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import sys
import os
import xml.etree.ElementTree as XET
import json
import re
from nltk.tokenize import word_tokenize, sent_tokenize

class MyWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 71, 21))
        self.label.setObjectName("label")
        
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(83, 10, 121, 41))
        self.textEdit.setObjectName("textEdit")
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(212, 10, 101, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.analyzeFolder)
        
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 70, 771, 501))
        self.textBrowser.setObjectName("textBrowser")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "KeyWord:"))
        self.pushButton.setText(_translate("MainWindow", "???????????????"))
    
    def analyzeFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self,"Open folder","./")
        key=str(self.textEdit.toPlainText())
        files= os.listdir(folder_path) #????????????????????????????????????
        #article=[]
        #index=0
        
        for file in files: #???????????????
            str1=""
            if not os.path.isdir(file): #????????????????????????,????????????????????????
                #self.textBrowser.append("File name:"+str(file))
                file_path=folder_path+"/"+file
                #self.textBrowser.append("File path:"+str(file_path))
                nm = os.path.splitext(file_path)
                #self.textBrowser.append(nm[1])
                if nm[1]==".xml" :
                    tree = XET.parse(file_path)  # ???XET????????????XML??????
                    root = tree.getroot()   # ??????XML??????
                    #for ArticleTitle in root.iter('ArticleTitle'):
                        #self.textBrowser.append(ArticleTitle.text)
                        #str1=str1+ArticleTitle.text
                        #article[index]=article[index]+ArticleTitle.text
                    for AbstractText in root.iter('AbstractText'):
                        #self.textBrowser.append(AbstractText.text)
                        str1=str1+AbstractText.text
                        #article[index]=article[index]+AbstractText.text
                elif nm[1]==".json" :
                    #self.textBrowser.append("?????????json???")
                    # ??? json ?????????????????????,???"r"??????????????????????????????utf-8?????????????????????
                    json_data = open(file_path,"r",encoding="utf-8").read()
                    # ???json????????????
                    data = json.loads(json_data)
                    # ???????????? data
                    for i in range(len(data)):
                        #self.textBrowser.append(data[i]['tweet_text'])
                        str1=str1+data[i]['tweet_text']
                        #article[index]=article[index]+data[i]['tweet_text']
                else:
                     self.textBrowser.append(file_path+"???????????????????????????????????????\n")
                     continue
                '''sentences = sent_tokenize(article[index])
                words=word_tokenize(article[index])
                characters=str(len(article[index]))
                self.textBrowser.append(file_path)
                self.textBrowser.append('Number of sentences by nltk: ' + str(len(sentences)))
                self.textBrowser.append('Number of words by nltk: ' + str(len(words)))
                self.textBrowser.append('Number of characters: ' + characters)
                for k in range(len(sentences)):
                    if key in sentences[k]:
                        self.textBrowser.append(sentences[k])
                index=index+1'''

                mark_out = re.sub(r'[^\w\s]','',str1.replace('/', ' '))

                sentences = sent_tokenize(str1)
                words=word_tokenize(mark_out)
                characters=str(len(mark_out))

                self.textBrowser.append(file_path)    
                self.textBrowser.append('Number of sentences by nltk: ' + str(len(sentences)))
                self.textBrowser.append('Number of words by nltk: ' + str(len(words)))
                self.textBrowser.append('Number of characters: ' + characters)
                
                for i in range(len(words)):
                    self.textBrowser.append(words[i]+"\n")
                for i in range(len(sentences)):
                    if key in sentences[i]:
                        self.textBrowser.append(sentences[i]+"\n")
        
       
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # ????????????QApplication?????????????????????????????????app
    MainWindow = QtWidgets.QMainWindow()    # ????????????QMainWindow????????????????????????????????????????????????
    ui = MyWindow()                         # ui???Ui_MainWindow()?????????????????????
    ui.setupUi(MainWindow)                  # ???????????????setupUi????????????????????????????????????????????????QMainWindow
    MainWindow.show()                       # ??????QMainWindow???show()?????????????????????QMainWindow
    sys.exit(app.exec_())                   # ??????exit()??????????????????????????????QApplication

