import os, sys, subprocess, webbrowser, glob
from datetime import datetime
from PyQt5.Qt import QApplication, QClipboard, QUrl, QIcon
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QPlainTextEdit, QLabel, QGridLayout, QPushButton, QLineEdit, QTextEdit, QMessageBox, QComboBox, QTabWidget, QFormLayout, QHBoxLayout, QRadioButton, QCheckBox, QVBoxLayout, QFileDialog, QProgressBar, QCalendarWidget, QSplitter, QFrame, QTreeView, QFileSystemModel, QInputDialog, QGroupBox, QButtonGroup, QDesktopWidget
from PyQt5.QtCore import pyqtSlot, Qt

import eq_auto_seiscomp, eq_auto_hydra, eq_upload, eq_createSocMediaTemp

qt_app = QApplication(sys.argv)

class Layoutexe(QTabWidget):
    def __init__(self, parent = None):
        super(Layoutexe, self).__init__(parent)
        #self.showFullScreen()
        self.showMaximized()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget() 
        self.tab4 = QWidget() 
        self.tab5 = QWidget()      
        self.addTab(self.tab1,"EQ Auto Solution")
        self.addTab(self.tab2,"EQ Uploader")
        self.addTab(self.tab3,"EQ Update")
        self.addTab(self.tab4,"FYI Teleseismic EQ")
        self.addTab(self.tab5,"EQ Email")
        #self.tab1.setTabToolTip('This is a tooltip for the QPushButton widget')
        #self.tab2.setToolTip('This is a tooltip for the QPushButton widget')
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()
        self.tab5UI()
        self.setWindowTitle("easi 2.0.0")
        self.setWindowIcon(QIcon('wave.png'))
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: #2297c2;")
        self.setFixedSize(900, 800)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def tab1UI(self):
        vLayoutMain = QVBoxLayout()
        vLayoutMain1 = QVBoxLayout()
        vLayoutMain1.setSpacing(40)
        vLayoutMain2 = QVBoxLayout()
        hLayout = QHBoxLayout()
        hLayout1 = QHBoxLayout()
        hLayout2 = QHBoxLayout()
        hLayout3 = QHBoxLayout()
        hLayout4 = QHBoxLayout()
        hLayout5 = QHBoxLayout()
        hLayout6 = QHBoxLayout()
        hLayout7 = QHBoxLayout()

        but_clear = QPushButton("Clear", self)
        but_clear.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_clear.setStyleSheet("background-color: white; color: black")
        hLayout.addStretch()
        hLayout.addWidget(but_clear)
        vLayoutMain1.addLayout(hLayout)

        labelAutoSource = QLabel("Source:")
        labelAutoSource.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout1.addStretch()
        hLayout1.addWidget(labelAutoSource)
        
        comboAutoSource = QComboBox(self)
        comboAutoSource.addItem("")
        comboAutoSource.addItem("Seiscomp3")
        comboAutoSource.addItem("Hydra")
        comboAutoSource.setFont(QtGui.QFont("Times", 12))
        comboAutoSource.setStyleSheet("background-color: white; color: black; selection-background-color: #F38b8b")
        comboAutoSource.setMaximumWidth(300)
        hLayout1.addWidget(comboAutoSource)
        hLayout1.addStretch()
        vLayoutMain1.addLayout(hLayout1)

        labelAutoDamage = QLabel("     Expecting Damage?")
        labelAutoDamage.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout2.addWidget(labelAutoDamage)
        self.radioDamageY = QRadioButton(self)
        self.radioDamageY.setText("Yes")
        self.radioDamageY.setFont(QtGui.QFont("Times", 12))
        labelOr = QLabel("or   ")
        labelOr.setFont(QtGui.QFont("Times", 12))
        self.radioDamageN = QRadioButton(self)
        self.radioDamageN.setText("No")
        self.radioDamageN.setFont(QtGui.QFont("Times", 12))
        hLayout2.addWidget(self.radioDamageY)
        hLayout2.addWidget(labelOr)
        hLayout2.addWidget(self.radioDamageN)
        hLayout2.addStretch()
        self.groupYorNDamage = QButtonGroup()
        self.groupYorNDamage.addButton(self.radioDamageY)
        self.groupYorNDamage.addButton(self.radioDamageN)
        vLayoutMain1.addLayout(hLayout2)

        self.radioGroupDamage = QButtonGroup()
        self.radioGroupDamage.addButton(self.radioDamageY)
        self.radioGroupDamage.addButton(self.radioDamageN)

        labelInt = QLabel(" Intensity(if available)")
        labelInt.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout3.addWidget(labelInt)
        self.IntBox = QTextEdit()
        self.IntBox.setFont(QtGui.QFont("Times", 12))
        self.IntBox.setStyleSheet("background-color: white; color: black; border: 2px solid black")
        self.IntBox.setMaximumHeight(200)
        hLayout3.addWidget(self.IntBox)
        vLayoutMain1.addLayout(hLayout3)

        labelInitials = QLabel("                        Initials:")
        labelInitials.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout4.addWidget(labelInitials)
        self.tboxInitials = QLineEdit(self)
        self.tboxInitials.setFont(QtGui.QFont("Times", 12))
        self.tboxInitials.setMaximumWidth(250)
        self.tboxInitials.setPlaceholderText('PPS/PPS/PPS')
        self.tboxInitials.setStyleSheet("background-color: white; color: black; border: 2px solid black")
        hLayout4.addWidget(self.tboxInitials)
        hLayout4.addStretch()
        vLayoutMain1.addLayout(hLayout4)

        but_create = QPushButton("Create EQ Info", self)
        but_create.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_create.setStyleSheet("background-color: white; color: black")
        hLayout5.addStretch()
        hLayout5.addWidget(but_create)
        hLayout5.addStretch()
        vLayoutMain1.addLayout(hLayout5)
        vLayoutMain.addLayout(vLayoutMain1)
        vLayoutMain.addStretch()

        labelAutoInfoEv = QLabel("Automatic EQ Info:")
        labelAutoInfoEv.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout6.addStretch()
        hLayout6.addWidget(labelAutoInfoEv)
        self.AutoInfoEv = QLineEdit(self)
        self.AutoInfoEv.setFont(QtGui.QFont("Times", 12))
        self.AutoInfoEv.setMaximumWidth(300)
        self.AutoInfoEv.setPlaceholderText('2022_0101_0000_B1')
        self.AutoInfoEv.setStyleSheet("background-color: white; color: black; border: 2px solid black")
        hLayout6.addWidget(self.AutoInfoEv)
        but_search = QPushButton("Search", self)
        but_search.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_search.setStyleSheet("background-color: white; color: black")
        hLayout6.addWidget(but_search)
        hLayout6.addStretch()
        vLayoutMain2.addLayout(hLayout6)

        but_edit = QPushButton("Edit", self)
        but_edit.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_edit.setStyleSheet("background-color: white; color: black")
        hLayout7.addStretch()
        hLayout7.addWidget(but_edit)
        but_view = QPushButton("View", self)
        but_view.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_view.setStyleSheet("background-color: white; color: black")
        hLayout7.addWidget(but_view)
        hLayout7.addStretch()
        vLayoutMain2.addLayout(hLayout7)
        vLayoutMain.addLayout(vLayoutMain2)
        #vLayoutMain.addStretch()

        self.tab1.setLayout(vLayoutMain)

        def create_EqInfo():
            if comboAutoSource.currentText() == "Seiscomp3":
                print("Source: " + comboAutoSource.currentText())
                eq_auto_seiscomp.create_EQinfoSeiscomp(self)
            elif comboAutoSource.currentText() == "Hydra":
                print("Source: " + comboAutoSource.currentText())
                eq_auto_hydra.create_EQinfoHydra(self)
            else:
                QMessageBox.information(self, "Message", "Please choose a source!")
                return

        def comboAutoSource_clear():
            comboAutoSource.setCurrentIndex(0)

        def radioDamage_clear():
            self.radioGroupDamage.setExclusive(False)
            self.radioDamageY.setChecked(False)
            self.radioDamageN.setChecked(False)
            self.radioGroupDamage.setExclusive(True)

        def checkThenCreate():
            if comboAutoSource.currentText() == "":
                QMessageBox.information(self, "Message", "Please choose a source!")
                return
            elif self.tboxInitials.text() == "" :
                QMessageBox.information(self, "Message", "Please fill-up intials of watchstanders!")
                return
            else:
                create_EqInfo()

        def searchFile():
            Event_file = str(QFileDialog.getOpenFileName(self, "Select a file","","HTML files (*.html)"))
            Event_file = Event_file.split(',')[0][2:-1].split('/')[-1].split('.')[0]
            self.AutoInfoEv.setText(Event_file)

        def editFile():
            tboxEventFile = str(self.AutoInfoEv.text()) + '.html'
            try:
                yearEvent = tboxEventFile[:4]
                monthEvent = tboxEventFile[5:7]
                dayEvent = tboxEventFile[7:9]
                eventPath = 'D:\\Eq_auto\\Earthquake_Information\\' + yearEvent + '_Earthquake_Information\\' + monthEvent + '\\' + dayEvent +'\\' + tboxEventFile
                print(eventPath)
                subprocess.Popen(['subl', eventPath])
            except ValueError:
                QMessageBox.information(self, "Message", "Please choose a valid file!")
                return

        def viewFile():
            tboxEventFile = str(self.AutoInfoEv.text()) + '.html'
            try:
                yearEvent = tboxEventFile[:4]
                monthEvent = tboxEventFile[5:7]
                dayEvent = tboxEventFile[7:9]
                eventPath = 'D:\\Eq_auto\\Earthquake_Information\\' + yearEvent + '_Earthquake_Information\\' + monthEvent + '\\' + dayEvent +'\\' + tboxEventFile
                webbrowser.open('file:\\\\' + eventPath, new=2)
            except ValueError:
                QMessageBox.information(self, "Message", "Please choose a valid file!")
                return

        but_create.clicked.connect(checkThenCreate)
        but_clear.clicked.connect(radioDamage_clear)
        but_clear.clicked.connect(comboAutoSource_clear)
        but_clear.clicked.connect(self.IntBox.clear)
        but_clear.clicked.connect(self.tboxInitials.clear)
        but_clear.clicked.connect(self.AutoInfoEv.clear)
        but_search.clicked.connect(searchFile)
        but_edit.clicked.connect(editFile)
        but_view.clicked.connect(viewFile)


    def tab2UI(self):
        vLayoutMain = QVBoxLayout()
        vLayoutMain1 = QVBoxLayout()
        vLayoutMain1.setSpacing(0)
        vLayoutMain2 = QVBoxLayout()
        vLayoutMain2.setSpacing(5)
        vLayoutMain3 = QVBoxLayout()
        vLayoutMain3.setSpacing(5)
        hLayout = QHBoxLayout()
        hLayout1 = QHBoxLayout()
        hLayout1.setSpacing(10)
        hLayout2 = QHBoxLayout()
        hLayout3 = QHBoxLayout()
        hLayout3.setSpacing(15)
        hLayout4 = QHBoxLayout()
        hLayout5 = QHBoxLayout()
        hLayout6 = QHBoxLayout()
        hLayout7 = QHBoxLayout()
        hLayout8 = QHBoxLayout()
        hLayout9 = QHBoxLayout()
        hLayout10 = QHBoxLayout()
        hLayout11 = QHBoxLayout()
        hLayout12 = QHBoxLayout()
        hLayout13 = QHBoxLayout()
        hLayout13.setSpacing(15)
        hLayout14 = QHBoxLayout()

        but_clear = QPushButton("Clear", self)
        but_clear.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_clear.setStyleSheet("background-color: white; color: black")
        hLayout.addStretch()
        hLayout.addWidget(but_clear)
        vLayoutMain1.addLayout(hLayout)

        labelFOrNf = QLabel("Felt or Not Felt?")
        labelFOrNf.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout1.addWidget(labelFOrNf)
        self.comboFOrNf = QComboBox(self)
        self.comboFOrNf.addItem("")
        self.comboFOrNf.addItem("Felt")
        self.comboFOrNf.addItem("Not Felt")
        self.comboFOrNf.setFont(QtGui.QFont("Times", 12))
        self.comboFOrNf.setStyleSheet("background-color: white; color: black; selection-background-color: #F38b8b")
        self.comboFOrNf.setMaximumWidth(500)
        hLayout1.addWidget(self.comboFOrNf)
        hLayout1.addStretch()
        vLayoutMain1.addLayout(hLayout1)

        labelUpload = QLabel("UPLOAD EQ INFO")
        labelUpload.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout2.addStretch()
        hLayout2.addWidget(labelUpload)
        hLayout2.addStretch()
        vLayoutMain1.addLayout(hLayout2)

        labelInfo = QLabel("EQ Info")
        labelInfo.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout3.addStretch()
        hLayout3.addWidget(labelInfo)
        self.InfoEv = QLineEdit(self)
        self.InfoEv.setFont(QtGui.QFont("Times", 12))
        self.InfoEv.setMaximumWidth(250)
        self.InfoEv.setPlaceholderText('2022_0101_0000_B1')
        self.InfoEv.setStyleSheet("background-color: white; color: black; border: 2px solid black")
        hLayout3.addWidget(self.InfoEv)
        but_recent = QPushButton("Recent", self)
        but_recent.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_recent.setStyleSheet("background-color: white; color: black")
        hLayout3.addWidget(but_recent)
        but_search = QPushButton("Search", self)
        but_search.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_search.setStyleSheet("background-color: white; color: black")
        hLayout3.addWidget(but_search)
        hLayout3.addStretch()
        vLayoutMain1.addLayout(hLayout3)

        but_upload = QPushButton("Upload", self)
        but_upload.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_upload.setStyleSheet("background-color: white; color: black")
        hLayout4.addStretch()
        hLayout4.addWidget(but_upload)
        hLayout4.addStretch()
        vLayoutMain1.addLayout(hLayout4)

        vLayoutMain1.addStretch()
        vLayoutMain.addLayout(vLayoutMain1)
        vLayoutMain.addStretch()

        labelDisseminate = QLabel("SOCIAL MEDIA DISSEMINATION")
        labelDisseminate.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout5.addStretch()
        hLayout5.addWidget(labelDisseminate)
        hLayout5.addStretch()
        vLayoutMain2.addLayout(hLayout5)

        but_createTemp = QPushButton("Create Template", self)
        but_createTemp.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_createTemp.setStyleSheet("background-color: white; color: black")
        hLayout6.addStretch()
        hLayout6.addWidget(but_createTemp)
        hLayout6.addStretch()
        vLayoutMain2.addLayout(hLayout6)

        labelSms = QLabel("SMS")
        labelSms.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout7.addWidget(labelSms)
        hLayout7.addStretch()
        vLayoutMain2.addLayout(hLayout7)

        self.smsBox = QTextEdit(self)
        self.smsBox.setFont(QtGui.QFont("Times", 12))
        self.smsBox.setStyleSheet("background-color: white; color: black; border: 2px solid black")
        self.smsBox.setMaximumHeight(100)
        hLayout8.addWidget(self.smsBox)
        vLayoutMain2.addLayout(hLayout8)

        labelFb = QLabel("FB/Twitter/Viber")
        labelFb.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout9.addWidget(labelFb)
        hLayout9.addStretch()
        vLayoutMain2.addLayout(hLayout9)

        self.fbBox = QTextEdit()
        self.fbBox.setFont(QtGui.QFont("Times", 12))
        self.fbBox.setStyleSheet("background-color: white; color: black; border: 2px solid black")
        self.fbBox.setMaximumHeight(200)
        hLayout10.addWidget(self.fbBox)
        vLayoutMain2.addLayout(hLayout10)

        but_postTweet = QPushButton("Post & Tweet", self)
        but_postTweet.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_postTweet.setStyleSheet("background-color: white; color: black")
        hLayout11.addStretch()
        hLayout11.addWidget(but_postTweet)
        hLayout11.addStretch()
        vLayoutMain2.addLayout(hLayout11)

        vLayoutMain2.addStretch()
        vLayoutMain.addLayout(vLayoutMain2)
        vLayoutMain.addStretch()

        labelDelete = QLabel("REMOVE EQ INFO FROM WEBSITE")
        labelDelete.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout12.addStretch()
        hLayout12.addWidget(labelDelete)
        hLayout12.addStretch()
        vLayoutMain3.addLayout(hLayout12)

        labelDelInfo = QLabel("EQ Info")
        labelDelInfo.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout13.addStretch()
        hLayout13.addWidget(labelDelInfo)
        self.DelInfoEv = QLineEdit(self)
        self.DelInfoEv.setFont(QtGui.QFont("Times", 12))
        self.DelInfoEv.setMaximumWidth(250)
        self.DelInfoEv.setPlaceholderText('2022_0101_0000_B1')
        self.DelInfoEv.setStyleSheet("background-color: white; color: black; border: 2px solid black")
        hLayout13.addWidget(self.DelInfoEv)
        but_delSearch = QPushButton("Search", self)
        but_delSearch.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_delSearch.setStyleSheet("background-color: white; color: black")
        hLayout13.addWidget(but_delSearch)
        hLayout13.addStretch()
        vLayoutMain3.addLayout(hLayout13)

        but_delete = QPushButton("Delete", self)
        but_delete.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_delete.setStyleSheet("background-color: white; color: black")
        hLayout14.addStretch()
        hLayout14.addWidget(but_delete)
        hLayout14.addStretch()
        vLayoutMain3.addLayout(hLayout14)

        vLayoutMain.addLayout(vLayoutMain3)

        self.tab2.setLayout(vLayoutMain)

        def recentEqInfo():
            os.chdir('D:\\Eq_auto\\Earthquake_Information')
            dir_list = glob.glob("*")  #find and go to latest year folder
            os.chdir(dir_list[-1])
            dir_list = glob.glob("*")  #find and go to latest month folder
            os.chdir(dir_list[-1])
            dir_list = glob.glob("*")  #find and go to latest day folder
            os.chdir(dir_list[-1])
            latest_file = sorted(glob.glob("*html"))  #find the latest html file
            latest_file = ''.join(latest_file[-1])[:-5]
            self.InfoEv.setText(latest_file)

        def searchEqInfo():
            os.chdir('D:\\Eq_auto\\Earthquake_Information')
            eqInfo_file = str(QFileDialog.getOpenFileName(self, "Select a file","","HTML files (*.html)"))
            eqInfo_file = eqInfo_file.split(',')[0][2:-1].split('/')[-1][:-5]
            self.InfoEv.setText(eqInfo_file)

        def uploadEqInfo():
            #try:
            if self.InfoEv.text().strip() == "":
                QMessageBox.information(self, "Message", "Please choose an EQ Info")
                return
            else:
                eq_upload.eqUpload(self)
            #except ValueError:
            #    QMessageBox.information(self, "Message", "Please choose a valid EqInfo file!")
            #    return

        def socMediaTemp():
            try:
                if self.InfoEv.text().strip() == "":
                    QMessageBox.information(self, "Message", "Please choose an EQ Info")
                    return
                else:
                    eq_createSocMediaTemp.eqCreateTemp(self)
            except ValueError:
                QMessageBox.information(self, "Message", "Please choose a valid EqInfo file!")
                return

        but_recent.clicked.connect(recentEqInfo)
        but_search.clicked.connect(searchEqInfo)
        but_upload.clicked.connect(uploadEqInfo)
        but_createTemp.clicked.connect(socMediaTemp)

    def tab3UI(self):
        vLayoutMain = QVBoxLayout()
        vLayoutMain1 = QVBoxLayout()
        vLayoutMain1.setSpacing(20)
        vLayoutMain2 = QVBoxLayout()
        hLayout = QHBoxLayout()
        hLayout1 = QHBoxLayout()
        hLayout2 = QHBoxLayout()
        hLayout2.setSpacing(13)
        hLayout3 = QHBoxLayout()
        hLayout3.setSpacing(13)
        hLayout4 = QHBoxLayout()
        hLayout5 = QHBoxLayout()
        hLayout6 = QHBoxLayout()
        hLayout7 = QHBoxLayout()
        hLayout8 = QHBoxLayout()
        hLayout9 = QHBoxLayout()
        hLayout10 = QHBoxLayout()

        but_clear = QPushButton("Clear", self)
        but_clear.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_clear.setStyleSheet("background-color: white; color: black")
        hLayout.addStretch()
        hLayout.addWidget(but_clear)
        vLayoutMain1.addLayout(hLayout)

        labelFOrNf = QLabel("Felt or Not Felt?")
        labelFOrNf.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout1.addWidget(labelFOrNf)
        self.comboFOrNf_upt = QComboBox(self)
        self.comboFOrNf_upt.addItem("")
        self.comboFOrNf_upt.addItem("Felt")
        self.comboFOrNf_upt.addItem("Not Felt")
        self.comboFOrNf_upt.setFont(QtGui.QFont("Times", 12))
        self.comboFOrNf_upt.setStyleSheet("background-color: white; color: black; selection-background-color: #F38b8b")
        self.comboFOrNf_upt.setMaximumWidth(300)
        hLayout1.addWidget(self.comboFOrNf_upt)
        hLayout1.addStretch()
        vLayoutMain1.addLayout(hLayout1)

        labelOldInfo = QLabel("        Old EQ Info")
        labelOldInfo.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout2.addStretch()
        hLayout2.addWidget(labelOldInfo)
        self.OldInfoEv = QLineEdit(self)
        self.OldInfoEv.setFont(QtGui.QFont("Times", 12))
        self.OldInfoEv.setMaximumWidth(300)
        self.OldInfoEv.setPlaceholderText('2022_0101_0000_B1')
        self.OldInfoEv.setStyleSheet("background-color: white; color: black; border: 2px solid black")
        hLayout2.addWidget(self.OldInfoEv)
        but_SearchOld = QPushButton("Search", self)
        but_SearchOld.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_SearchOld.setStyleSheet("background-color: white; color: black")
        hLayout2.addWidget(but_SearchOld)
        hLayout2.addStretch()
        vLayoutMain1.addLayout(hLayout2)

        labelUpInfo = QLabel("Updated EQ Info")
        labelUpInfo.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout3.addStretch()
        hLayout3.addWidget(labelUpInfo)
        self.UpInfoEv = QLineEdit(self)
        self.UpInfoEv.setFont(QtGui.QFont("Times", 12))
        self.UpInfoEv.setMaximumWidth(400)
        self.UpInfoEv.setPlaceholderText('2022_0101_0000_B2')
        self.UpInfoEv.setStyleSheet("background-color: white; color: black; border: 2px solid black")
        hLayout3.addWidget(self.UpInfoEv)
        but_SearchUp = QPushButton("Search", self)
        but_SearchUp.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_SearchUp.setStyleSheet("background-color: white; color: black")
        hLayout3.addWidget(but_SearchUp)
        hLayout3.addStretch()
        vLayoutMain1.addLayout(hLayout3)

        but_Update = QPushButton("Update", self)
        but_Update.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_Update.setStyleSheet("background-color: white; color: black")
        hLayout4.addStretch()
        hLayout4.addWidget(but_Update)
        hLayout4.addStretch()
        vLayoutMain1.addLayout(hLayout4)

        vLayoutMain1.addStretch()
        vLayoutMain.addLayout(vLayoutMain1)

        but_createTemp = QPushButton("Create Template", self)
        but_createTemp.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_createTemp.setStyleSheet("background-color: white; color: black")
        hLayout5.addStretch()
        hLayout5.addWidget(but_createTemp)
        hLayout5.addStretch()
        vLayoutMain2.addLayout(hLayout5)

        labelSms = QLabel("SMS")
        labelSms.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout6.addWidget(labelSms)
        hLayout6.addStretch()
        vLayoutMain2.addLayout(hLayout6)

        self.smsBox = QTextEdit(self)
        self.smsBox.setFont(QtGui.QFont("Times", 12))
        self.smsBox.setStyleSheet("background-color: white; color: black; border: 2px solid black")
        self.smsBox.setMaximumHeight(100)
        hLayout7.addWidget(self.smsBox)
        vLayoutMain2.addLayout(hLayout7)

        labelFb = QLabel("FB/Twitter/Viber")
        labelFb.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout8.addWidget(labelFb)
        hLayout8.addStretch()
        vLayoutMain2.addLayout(hLayout8)

        self.fbBox = QTextEdit()
        self.fbBox.setFont(QtGui.QFont("Times", 12))
        self.fbBox.setStyleSheet("background-color: white; color: black; border: 2px solid black")
        self.fbBox.setMaximumHeight(200)
        hLayout9.addWidget(self.fbBox)
        vLayoutMain2.addLayout(hLayout9)

        but_postTweet = QPushButton("Post & Tweet", self)
        but_postTweet.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_postTweet.setStyleSheet("background-color: white; color: black")
        hLayout10.addStretch()
        hLayout10.addWidget(but_postTweet)
        hLayout10.addStretch()
        vLayoutMain2.addLayout(hLayout10)

        vLayoutMain2.addStretch()
        vLayoutMain.addLayout(vLayoutMain2)

        self.tab3.setLayout(vLayoutMain)

    def tab4UI(self):
        vLayoutMain = QVBoxLayout()
        vLayoutMain1 = QVBoxLayout()
        vLayoutMain1.setSpacing(70)
        vLayoutMain2 = QVBoxLayout()
        hLayout = QHBoxLayout()
        hLayout1 = QHBoxLayout()
        hLayout1.setSpacing(10)
        hLayout2 = QHBoxLayout()
        hLayout2.setSpacing(10)
        hLayout3 = QHBoxLayout()
        hLayout4 = QHBoxLayout()
        hLayout5 = QHBoxLayout()

        but_clear = QPushButton("Clear", self)
        but_clear.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_clear.setStyleSheet("background-color: white; color: black")
        hLayout.addStretch()
        hLayout.addWidget(but_clear)
        vLayoutMain1.addLayout(hLayout)

        labelAutoSource = QLabel("Source:")
        labelAutoSource.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout1.addStretch()
        hLayout1.addWidget(labelAutoSource)
        self.comboAutoSource = QComboBox(self)
        self.comboAutoSource.addItem("")
        self.comboAutoSource.addItem("Seiscomp3")
        self.comboAutoSource.addItem("USGS")
        self.comboAutoSource.addItem("Geofon")
        self.comboAutoSource.setFont(QtGui.QFont("Times", 12))
        self.comboAutoSource.setStyleSheet("background-color: white; color: black; selection-background-color: #F38b8b")
        self.comboAutoSource.setMaximumWidth(300)
        hLayout1.addWidget(self.comboAutoSource)
        hLayout1.addStretch()
        vLayoutMain1.addLayout(hLayout1)

        labelInitial = QLabel("Initial:")
        labelInitial.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout2.addStretch()
        hLayout2.addWidget(labelInitial)
        self.tboxInitial = QLineEdit(self)
        self.tboxInitial.setFont(QtGui.QFont("Times", 12))
        self.tboxInitial.setMaximumWidth(200)
        self.tboxInitial.setPlaceholderText('PPS')
        self.tboxInitial.setStyleSheet("background-color: white; color: black; border: 2px solid black")
        hLayout2.addWidget(self.tboxInitial)
        hLayout2.addStretch()
        vLayoutMain1.addLayout(hLayout2)

        but_createTemp = QPushButton("Create Template", self)
        but_createTemp.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_createTemp.setStyleSheet("background-color: white; color: black")
        hLayout3.addStretch()
        hLayout3.addWidget(but_createTemp)
        hLayout3.addStretch()
        vLayoutMain1.addLayout(hLayout3)

        vLayoutMain.addLayout(vLayoutMain1)

        labelSms = QLabel("For SMS")
        labelSms.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout4.addWidget(labelSms)
        hLayout4.addStretch()
        vLayoutMain2.addLayout(hLayout4)

        self.smsBox = QTextEdit(self)
        self.smsBox.setFont(QtGui.QFont("Times", 12))
        self.smsBox.setStyleSheet("background-color: white; color: black; border: 2px solid black")
        self.smsBox.setMaximumHeight(100)
        hLayout5.addWidget(self.smsBox)
        vLayoutMain2.addLayout(hLayout5)
        vLayoutMain2.addStretch()

        vLayoutMain.addLayout(vLayoutMain2)

        self.tab4.setLayout(vLayoutMain)

    def tab5UI(self):
        vLayoutMain = QVBoxLayout()
        vLayoutMain.setSpacing(70)
        vLayoutMain1 = QVBoxLayout()
        vLayoutMain1.setSpacing(20)
        vLayoutMain2 = QVBoxLayout()
        hLayout = QHBoxLayout()
        hLayout1 = QHBoxLayout()
        hLayout2 = QHBoxLayout()
        #hLayout2.setSpacing(13)
        hLayout3 = QHBoxLayout()
        hLayout3.setSpacing(5)
        hLayout4 = QHBoxLayout()
        hLayout4.setSpacing(5)
        hLayout5 = QHBoxLayout()
        hLayout6 = QHBoxLayout()
        hLayout7 = QHBoxLayout()
        hLayout8 = QHBoxLayout()
        hLayout9 = QHBoxLayout()
        hLayout10 = QHBoxLayout()

        but_clear = QPushButton("Clear", self)
        but_clear.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_clear.setStyleSheet("background-color: white; color: black")
        hLayout.addStretch()
        hLayout.addWidget(but_clear)
        vLayoutMain.addLayout(hLayout)
        #vLayoutMain1.addStretch()

        labelEqInfo = QLabel("EQ Info")
        labelEqInfo.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout1.addStretch()
        hLayout1.addWidget(labelEqInfo)
        self.EqInfoEv = QLineEdit(self)
        self.EqInfoEv.setFont(QtGui.QFont("Times", 12))
        self.EqInfoEv.setMaximumWidth(300)
        self.EqInfoEv.setPlaceholderText('2022_0101_0000_B1')
        self.EqInfoEv.setStyleSheet("background-color: white; color: black; border: 2px solid black")
        hLayout1.addWidget(self.EqInfoEv)
        but_SearchEq = QPushButton("Search", self)
        but_SearchEq.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_SearchEq.setStyleSheet("background-color: white; color: black")
        hLayout1.addWidget(but_SearchEq)
        hLayout1.addStretch()
        vLayoutMain1.addLayout(hLayout1)

        but_createTemp = QPushButton("Create Template", self)
        but_createTemp.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        but_createTemp.setStyleSheet("background-color: white; color: black")
        hLayout2.addStretch()
        hLayout2.addWidget(but_createTemp)
        hLayout2.addStretch()
        vLayoutMain1.addLayout(hLayout2)

        vLayoutMain.addLayout(vLayoutMain1)

        labelESubject = QLabel("Subject of Email:")
        labelESubject.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout3.addWidget(labelESubject)
        self.ESubject = QLineEdit(self)
        self.ESubject.setFont(QtGui.QFont("Times", 12))
        self.ESubject.setMaximumWidth(750)
        self.ESubject.setStyleSheet("background-color: white; color: black; border: 2px solid black")
        hLayout3.addWidget(self.ESubject)
        vLayoutMain2.addLayout(hLayout3)

        labelEBody = QLabel("Subject of Email:")
        labelEBody.setFont(QtGui.QFont("Times", 12, weight=QtGui.QFont.Bold))
        hLayout4.addWidget(labelEBody)
        self.EBody = QTextEdit()
        self.EBody.setFont(QtGui.QFont("Times", 12))
        self.EBody.setMaximumWidth(750)
        self.EBody.setMaximumHeight(400)
        self.EBody.setStyleSheet("background-color: white; color: black; border: 2px solid black")
        hLayout4.addWidget(self.EBody)
        vLayoutMain2.addLayout(hLayout4)

        vLayoutMain.addLayout(vLayoutMain2)
        #vLayoutMain.addStretch()

        self.tab5.setLayout(vLayoutMain)

    def run(self):
        # Show the form
        self.show()
        self.setCurrentIndex(1) 
        # Run the qt application
        qt_app.exec_()

# Create an instance of the application window and run it
app = Layoutexe()
app.run()
