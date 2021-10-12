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
        self.pushButton.setText(_translate("MainWindow", "讀取資料夾"))
    
    def analyzeFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self,"Open folder","./")
        key=str(self.textEdit.toPlainText())
        files= os.listdir(folder_path) #得到資料夾下的所有檔名稱
        #article=[]
        #index=0
        
        for file in files: #遍歷資料夾
            str1=""
            if not os.path.isdir(file): #判斷是否是資料夾,不是資料夾才打開
                #self.textBrowser.append("File name:"+str(file))
                file_path=folder_path+"/"+file
                #self.textBrowser.append("File path:"+str(file_path))
                nm = os.path.splitext(file_path)
                #self.textBrowser.append(nm[1])
                if nm[1]==".xml" :
                    tree = XET.parse(file_path)  # 以XET套件載入XML檔案
                    root = tree.getroot()   # 取得XML表格
                    for ArticleTitle in root.iter('ArticleTitle'):
                        #self.textBrowser.append(ArticleTitle.text)
                        str1=str1+ArticleTitle.text
                        #article[index]=article[index]+ArticleTitle.text
                    for AbstractText in root.iter('AbstractText'):
                        #self.textBrowser.append(AbstractText.text)
                        str1=str1+AbstractText.text
                        #article[index]=article[index]+AbstractText.text
                elif nm[1]==".json" :
                    #self.textBrowser.append("您輸入json檔")
                    # 將 json 檔案讀取成字串,以"r"讀寫模式、編碼方式為utf-8的方式開啟檔案
                    json_data = open(file_path,"r",encoding="utf-8").read()
                    # 對json資料解碼
                    data = json.loads(json_data)
                    # 直接列印 data
                    for i in range(len(data)):
                        #self.textBrowser.append(data[i]['tweet_text'])
                        str1=str1+data[i]['tweet_text']
                        #article[index]=article[index]+data[i]['tweet_text']
                else:
                     self.textBrowser.append(file_path+"檔案類型不符，此檔案不解析\n")
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

                sentences = sent_tokenize(str1)
                words=word_tokenize(str1)
                characters=str(len(str1))

                self.textBrowser.append(file_path)    
                self.textBrowser.append('Number of sentences by nltk: ' + str(len(sentences)))
                self.textBrowser.append('Number of words by nltk: ' + str(len(words)))
                self.textBrowser.append('Number of characters: ' + characters)
                for i in range(len(sentences)):
                    if key in sentences[i]:
                        self.textBrowser.append(sentences[i]+"\n")
        
       
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = QtWidgets.QMainWindow()    # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    ui = MyWindow()                         # ui是Ui_MainWindow()类的实例化对象
    ui.setupUi(MainWindow)                  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    MainWindow.show()                       # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())                   # 使用exit()或者点击关闭按钮退出QApplication

