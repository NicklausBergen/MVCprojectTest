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
        with open('SOURCESTEST/SHOTSLIST/shotsListFile.json') as datashots_file:
            datashots_loaded = json.load(datashots_file)
        self.myShotsList = datashots_loaded['shot list']

        # Set ASSETS LIST
        with open('SOURCESTEST/ASSETSLIST/assetsListFile.json') as dataassets_file:
            dataassets_loaded = json.load(dataassets_file)
        self.myAssetsList = dataassets_loaded['asset list']

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

        self.lineeditbis = self.ui.lineEdit_8
        self.completerbis = QCompleter(self.myShotsList)
        self.completerbis.setCaseSensitivity(Qt.CaseInsensitive)
        self.completerbis.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.lineeditbis.setCompleter(self.completerbis)
        self.completerbis.popup().setStyleSheet("background:  #3a3a3a; color : #eee; alternate-background-color: #b3b3b3;")

        self.lineeditter = self.ui.lineEdit_6
        self.completerter = QCompleter(self.myShotsList)
        self.completerter.setCaseSensitivity(Qt.CaseInsensitive)
        self.completerter.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.lineeditter.setCompleter(self.completerter)
        self.completerter.popup().setStyleSheet("background:  #3a3a3a; color : #eee; alternate-background-color: #b3b3b3;")

        # get user
        self.myuser = os.getlogin()
        print (self.myuser)
        self.ui.label_18.setText(self.myuser)

        # define QtreeNames
        self.currentcastingtree = self.ui.findChild(QTreeWidget, 'treeCurrentCasting')
        self.currentcastingtree2 = self.ui.findChild(QTreeWidget, 'treeCurrentCasting_2')
        self.comparecastingtree = self.ui.findChild(QTreeWidget, 'treeCompareCasting')
        self.assetstree = self.ui.findChild(QTreeWidget, 'treeAsset')

        # refresh button
        self.ui.pushButton_7.clicked.connect(self.fillAssetsList)

        # Load Current button
        self.ui.pushButton_18.clicked.connect(self.fillCurrentCasting)
        self.ui.pushButton_17.clicked.connect(self.fillCurrentCasting)

        # Expand Trees
        self.currentcastingtree.expandAll()
        self.currentcastingtree2.expandAll()
        self.comparecastingtree.expandAll()

        # Asset Tree update Thumbnail
        self.assetstree.selectionModel().selectionChanged.connect(self.loadAssetThumbnail)

        self.ui.show()
        self.run()


    def printDragDrop(self):
        print ('DRAG DROP DONE')


    def fillAssetsList(self):

        self.assetstree.clear()
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
        self.shotname = self.ui.lineEdit_9.text()

        # path of casting folder for selected shot
        self.castingfilespath = ''
        if self.shotname:
            self.castingfilespath = ('SOURCESTEST/shots/' + self.shotname + '/casting')
        else:
            self.castingfilespath = None

        # list casting files
        self.castingfileslist=[]
        name_list = os.listdir(self.castingfilespath)
        full_list = [os.path.join(self.castingfilespath,i) for i in name_list]
        time_sorted_list = sorted(full_list, key=os.path.getmtime)
        sorted_filename_list = [ os.path.basename(i) for i in time_sorted_list]
        for eachfile in sorted_filename_list:
            if eachfile.endswith('.json'):
                self.castingfileslist.append(eachfile)
        print (self.castingfileslist)

        # add to combo box
        self.ui.comboBox_8.clear()
        for text in self.castingfileslist:
            self.ui.comboBox_8.addItem(text)


    def fillCurrentCasting(self):

        self.currentcastingtree.clear()
        self.currentcastingtree2.clear()

        self.tempFile = self.ui.comboBox_8.currentText()
        self.castingFileSelected = ('SOURCESTEST/shots/' + self.shotname + '/casting/' + self.tempFile)

        # add invisible root item
        self.rootItemCurrentCasting = self.currentcastingtree.invisibleRootItem()

        # Get Path of Casting and Comment files
        with open(self.castingFileSelected) as data_file:
            data_loaded = json.load(data_file)

        commentFilePath = data_loaded['comment']
        with open(commentFilePath, 'r') as file:
            myCommentFile = yaml.safe_load(file)

        # add splits toplevel item
        splitslist = []
        for each in data_loaded['casting']:
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
            assetsList = []
            for eachAsset in data_loaded['casting'][eachSplit]:
                self.assetItem = QTreeWidgetItem([eachAsset])
                assetsList
                QTreeWidgetItem.addChild(self.topItem, self.assetItem)

        # add assets infos
                for eachAssetInfo in data_loaded['casting'][eachSplit][eachAsset]:
                    self.assetNamespace = data_loaded['casting'][eachSplit][eachAsset]['namespace']
                    QTreeWidgetItem.setText(self.assetItem, 1,self.assetNamespace)
                    self.assetType = data_loaded['casting'][eachSplit][eachAsset]['assetType']
                    QTreeWidgetItem.setText(self.assetItem, 2,self.assetType)
                    self.actorType = data_loaded['casting'][eachSplit][eachAsset]['actorType']
                    QTreeWidgetItem.setText(self.assetItem, 3,self.actorType)
                    self.actorVersion = data_loaded['casting'][eachSplit][eachAsset]['actorVersion']
                    QTreeWidgetItem.setText(self.assetItem, 4,self.actorVersion)
                    self.modelingVariant = data_loaded['casting'][eachSplit][eachAsset]['modelingVariant']
                    QTreeWidgetItem.setText(self.assetItem, 5,self.modelingVariant)
                    self.shadingVariant = data_loaded['casting'][eachSplit][eachAsset]['shadingVariant']
                    QTreeWidgetItem.setText(self.assetItem, 6,self.shadingVariant)
                    self.loaded = str(data_loaded['casting'][eachSplit][eachAsset]['loaded'])
                    QTreeWidgetItem.setText(self.assetItem, 7,self.loaded)

        self.currentcastingtree.expandAll()
        self.currentcastingtree.sortByColumn(0, QtCore.Qt.AscendingOrder)


        # add comment
        self.ui.label_28.setText(myCommentText)
        self.ui.label_30.setText(myCommentText)

        # add to path label
        self.ui.label_26.setText(self.castingFileSelected)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Application(app)




'''
        ########################################################
        # TEST Insert ComboBox
        self.eachELMNT = ('[TEST]')
        self.testELMNT = QTreeWidgetItem([self.eachELMNT])
        self.currentcastingtree.addTopLevelItem(self.testELMNT)

        item = QTreeWidgetItem()
        QTreeWidgetItem.addChild(self.testELMNT,item)
        widget = QComboBox()
        widget.setMaximumHeight(17)
        widget.addItem('v001')
        widget.addItem('v002')
        widget.addItem('v003')
        widget.addItem('v004')
        widget.addItem('v005')
        widget.setCurrentIndex(3)
        self.currentcastingtree.setItemWidget(item, 4, widget)

        item2 = QTreeWidgetItem()
        widget2 = QComboBox()
        widget2.setMaximumHeight(17)
        widget2.addItem('regular')
        widget2.addItem('used')
        widget2.addItem('destroyed')
        widget2.setCurrentIndex(0)
        self.currentcastingtree.setItemWidget(item, 5, widget2)

        item3 = QTreeWidgetItem()
        widget3 = QComboBox()
        widget3.setMaximumHeight(17)
        widget3.addItem('regular')
        widget3.addItem('green')
        widget3.addItem('red')
        widget3.addItem('blue')
        widget3.setCurrentIndex(2)
        self.currentcastingtree.setItemWidget(item, 6, widget3)

        item4 = QTreeWidgetItem()
        widget4 = QComboBox()
        widget4.setMaximumHeight(17)
        widget4.addItem('actor_anim')
        widget4.addItem('actor_lo')
        widget4.addItem('actor_layout')
        widget4.addItem('actor_shading')
        widget4.setCurrentIndex(0)
        self.currentcastingtree.setItemWidget(item, 3, widget4)

        QTreeWidgetItem.setText(item, 0, 'AssetNameTest')
        QTreeWidgetItem.setText(item, 1, 'NamespaceTest')
        QTreeWidgetItem.setText(item, 2, 'AssetTypeTest')
        QTreeWidgetItem.setText(item, 7, 'LoadedInTest')

        ########################################################

'''