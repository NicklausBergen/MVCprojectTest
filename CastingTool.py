import json
import os
import sys
import yaml
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtWidgets import *

class Application(object):

    def __init__(self, app):
        self.app = app
        self.ui = uic.loadUi('CastingToolV5.ui')

        # Set SHOTS LIST
        with open('SOURCESTEST/SHOTSLIST/shotsListFile.json') as dataShotsFile:
            dataShotsLoaded = json.load(dataShotsFile)
        self.myShotsList = dataShotsLoaded['shot list']

        # Set ASSETS LIST
        with open('SOURCESTEST/ASSETSLIST/assetsListFile.json') as dataAssetsFile:
            dataAssetsLoaded = json.load(dataAssetsFile)
        self.myAssetsList = dataAssetsLoaded['asset list']

        # Set Casting Path
        self.castingFilePath = ''

        # Set Completer Shot List
        self.lineedit = self.ui.lineEdit_9
        self.completer = QCompleter(self.myShotsList)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        #self.completer.setMaxVisibleItems(2)
        self.completer.activated.connect(self.fillCastingFilesList)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.lineedit.setCompleter(self.completer)
        self.completer.popup().setStyleSheet("background:  #3a3a3a; color : #eee; alternate-background-color: #b3b3b3;")

        self.lineEditBis = self.ui.lineEdit_8
        self.completerBis = QCompleter(self.myShotsList)
        self.completerBis.setCaseSensitivity(Qt.CaseInsensitive)
        self.completerBis.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.lineEditBis.setCompleter(self.completerBis)
        self.completerBis.popup().setStyleSheet("background:  #3a3a3a; color : #eee; alternate-background-color: #b3b3b3;")

        self.lineEditLer = self.ui.lineEdit_6
        self.completerTer = QCompleter(self.myShotsList)
        self.completerTer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completerTer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.lineEditLer.setCompleter(self.completerTer)
        self.completerTer.popup().setStyleSheet("background:  #3a3a3a; color : #eee; alternate-background-color: #b3b3b3;")

        # get user
        self.myUser = os.getlogin()
        print (self.myUser)
        self.ui.label_18.setText(self.myUser)

        # define QtreeNames
        self.currentCastingTree = self.ui.findChild(QTreeWidget, 'treeCurrentCasting')
        self.currentCastingTree2 = self.ui.findChild(QTreeWidget, 'treeCurrentCasting_2')
        self.compareCastingTree = self.ui.findChild(QTreeWidget, 'treeCompareCasting')
        self.assetsTree = self.ui.findChild(QTreeWidget, 'treeAsset')

        # refresh button
        self.ui.pushButton_7.clicked.connect(self.fillAssetsList)

        # Load Current button
        self.ui.pushButton_18.clicked.connect(self.fillCurrentCasting)
        self.ui.pushButton_17.clicked.connect(self.fillCurrentCasting)

        # Expand Trees
        self.currentCastingTree.expandAll()
        self.currentCastingTree2.expandAll()
        self.compareCastingTree.expandAll()

        # Asset Tree update Thumbnail
        self.assetsTree.selectionModel().selectionChanged.connect(self.loadAssetThumbnail)

        self.ui.show()
        self.run()


    def printDragDrop(self):
        print ('DRAG DROP DONE')


    def fillAssetsList(self):

        self.assetsTree.clear()
        print(self.myAssetsList)


    def run(self):
        self.app.exec_()


    def login(self):
        user = self.ui.label_18.text()
        print('User: ', user)


    def printTest(self):
        print ('THIS IS A TEST')


    def loadAssetThumbnail(self):
        print ('load thumbnail')


    def fillCastingFilesList(self):

        # get selected shot
        self.shotName = self.ui.lineEdit_9.text()

        # path of casting folder for selected shot
        self.castingFilesPath = ''
        if self.shotName:
            self.castingFilesPath = ('SOURCESTEST/shots/' + self.shotName + '/casting')
        else:
            self.castingFilesPath = None

        # list casting files
        self.castingFilesList=[]
        nameList = os.listdir(self.castingFilesPath)
        fullList = [os.path.join(self.castingFilesPath, i) for i in nameList]
        timeSortedList = sorted(fullList, key=os.path.getmtime)
        sortedFilenameList = [ os.path.basename(i) for i in timeSortedList]
        for eachFile in sortedFilenameList:
            if eachFile.endswith('.json'):
                self.castingFilesList.append(eachFile)
        print (self.castingFilesList)

        # add to combo box
        self.ui.comboBox_8.clear()
        for text in self.castingFilesList:
            self.ui.comboBox_8.addItem(text)


    def fillCurrentCasting(self):

        self.currentCastingTree.clear()
        self.currentCastingTree2.clear()

        self.tempFile = self.ui.comboBox_8.currentText()
        self.castingFileSelected = ('SOURCESTEST/shots/' + self.shotName + '/casting/' + self.tempFile)

        # add invisible root item
        self.rootItemCurrentCasting = self.currentCastingTree.invisibleRootItem()

        # Get Path of Casting and Comment files
        with open(self.castingFileSelected) as dataFile:
            dataLoaded = json.load(dataFile)

        commentFilePath = dataLoaded['comment']
        with open(commentFilePath, 'r') as file:
            myCommentFile = yaml.safe_load(file)

        # add splits toplevel item
        splitslist = []
        for each in dataLoaded['casting']:
            splitslist.append(each)
        myCommentText = myCommentFile['comment']
        print(splitslist)
        print (myCommentText)

        # add Top Level Splits
        for eachSplit in splitslist :
            if eachSplit == 'common':
                myFont = QFont("MS Shell Dlg 2", 8, QFont.Bold, 1)
                eachSplitShow = eachSplit.upper()
            else:
                myFont = QFont("MS Shell Dlg 2", 8, QFont.Bold)
                eachSplitShow = eachSplit
            self.topItem = QTreeWidgetItem(['[' + eachSplitShow + ']'])
            QTreeWidgetItem.addChild(self.rootItemCurrentCasting, self.topItem)
            self.topItem.setFont(0, myFont)

        # add Assets
            for eachAsset in dataLoaded['casting'][eachSplit]:
                self.assetItem = QTreeWidgetItem([eachAsset])
                QTreeWidgetItem.addChild(self.topItem, self.assetItem)

        # add assets infos
                for eachAssetInfo in dataLoaded['casting'][eachSplit][eachAsset]:
                    self.assetNamespace = dataLoaded['casting'][eachSplit][eachAsset]['namespace']
                    QTreeWidgetItem.setText(self.assetItem, 1,self.assetNamespace)
                    self.assetType = dataLoaded['casting'][eachSplit][eachAsset]['assetType']
                    QTreeWidgetItem.setText(self.assetItem, 2,self.assetType)
                    self.actorType = dataLoaded['casting'][eachSplit][eachAsset]['actorType']
                    QTreeWidgetItem.setText(self.assetItem, 3,self.actorType)
                    self.actorVersion = dataLoaded['casting'][eachSplit][eachAsset]['actorVersion']
                    QTreeWidgetItem.setText(self.assetItem, 4,self.actorVersion)
                    self.modelingVariant = dataLoaded['casting'][eachSplit][eachAsset]['modelingVariant']
                    QTreeWidgetItem.setText(self.assetItem, 5,self.modelingVariant)
                    self.shadingVariant = dataLoaded['casting'][eachSplit][eachAsset]['shadingVariant']
                    QTreeWidgetItem.setText(self.assetItem, 6,self.shadingVariant)
                    self.loaded = str(dataLoaded['casting'][eachSplit][eachAsset]['loaded'])
                    QTreeWidgetItem.setText(self.assetItem, 7,self.loaded)

        self.currentCastingTree.expandAll()
        self.currentCastingTree.sortByColumn(0, QtCore.Qt.AscendingOrder)

        # add comment
        self.ui.label_28.setText(myCommentText)
        self.ui.label_30.setText(myCommentText)

        # add to path label
        self.ui.label_26.setText(self.castingFileSelected)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Application(app)
