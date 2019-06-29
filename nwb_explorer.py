from PyQt5 import QtCore, QtGui, Qt
from PyQt5.QtWidgets import (QWidget, QApplication, QTreeWidget, QTreeWidgetItem,
    QMainWindow, QFileDialog, QAction, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton)

import nwbext_ecog
from pynwb import NWBHDF5IO

from console_widget import ConsoleWidget
import os
import sys

class Application(QMainWindow):
    def __init__(self, filename):
        super().__init__()

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.resize(1000, 600)
        self.setWindowTitle('NWB explorer')

        # Window layout --------------------------------------------------------
        self.tree = QTreeWidget ()
        self.tree.itemClicked.connect(self.onItemClicked)
        self.push1_0 = QPushButton('Open NWB file')
        self.push1_0.clicked.connect(self.open_file)
        self.push2_0 = QPushButton('Export NWB file')
        self.push3_0 = QPushButton('Auto-clear')
        self.push3_0.setCheckable(True)
        self.push3_0.setChecked(True)
        self.push3_0.clicked.connect(self.toggle_auto_clear)
        self.auto_clear = True

        self.grid1 = QGridLayout()
        self.grid1.addWidget(self.push1_0, 0, 0, 1, 6)
        self.grid1.addWidget(self.push2_0, 1, 0, 1, 6)
        self.grid1.addWidget(self.push3_0, 2, 0, 1, 6)
        self.vbox1 = QVBoxLayout()
        self.vbox1.addWidget(self.tree)
        self.grid1.addLayout(self.vbox1, 3, 0, 2, 6)

        self.console = ConsoleWidget(par=self)
        self.vbox2 = QVBoxLayout()
        self.vbox2.addWidget(self.console)

        self.hbox = QHBoxLayout(self.centralwidget)
        self.hbox.addLayout(self.grid1)    #add first tree
        self.hbox.addLayout(self.vbox2)    #add second tree

        # Open file ------------------------------------------------------------
        if not os.path.isfile(filename):
            self.open_file()
        else:
            self.file = filename
            self.io = NWBHDF5IO(self.file,'r+')
            self.nwb = self.io.read()      #reads NWB file
            self.fields = list(self.nwb.fields.keys())
            self.init_tree()
            self.init_console()
        self.show()

    def open_file(self):
        ''' Open NWB file '''
        filename, ftype = QFileDialog.getOpenFileName(None, 'Open file', '', "(*.nwb)")
        if ftype=='(*.nwb)':
            self.file = filename
            self.io = NWBHDF5IO(self.file,'r+')
            self.nwb = self.io.read()      #reads NWB file
            self.fields = list(self.nwb.fields.keys())
            self.init_tree()
            self.init_console()

    def toggle_auto_clear(self):
        ''' Toggle auto-clear console screen function'''
        if self.auto_clear:
            self.auto_clear = False
        else:
            self.auto_clear=True

    def init_tree(self):
        ''' Draw hierarchical tree of fields in NWB file '''
        self.tree.clear()
        for field in self.fields:  #NWB file fields
            parent = QTreeWidgetItem(self.tree)
            parent.setText(0, field)
            parent.setFlags(parent.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
            parent.setCheckState(0, QtCore.Qt.Unchecked)
            #If parent is a dictionary
            if type(self.nwb.fields[field]).__name__=='LabelledDict':
                sub_fields = list(self.nwb.fields[field].keys())
                for subf in sub_fields:
                    child = QTreeWidgetItem(parent)
                    child.setFlags(child.flags() | QtCore.Qt.ItemIsUserCheckable)
                    child.setText(0, subf)
                    child.setCheckState(0, QtCore.Qt.Unchecked)
            #if len(self.nwb.fields[field])==0:
            #    font = QtGui.QFont()
            #    font.setWeight(6)
            #    parent.setFont(0, font)


    def init_console(self):
        ''' Initialize commands on console '''
        self.console._execute("import nwbext_ecog", True)
        self.console._execute("from pynwb import NWBHDF5IO", True)
        self.console._execute("fname = '"+self.file+"'", True)
        self.console._execute("io = NWBHDF5IO(fname,'r+')", True)
        self.console._execute("nwb = io.read()", True)
        self.console.clear()
        #self.console.execute_command("")

    #@QtCore.pyqtSlot(QTreeWidgetItem, int)
    def onItemClicked(self, it, col):
        #print(it, col, it.text(col))
        if self.auto_clear:
            self.console.clear()
        if it.parent() is not None:
            field0 = it.parent().text(0)
            field1 = it.text(0)
            item = self.nwb.fields[field0][field1]
        else:
            field1 = it.text(0)
            item = self.nwb.fields[field1]
        self.console.push_vars({'item':item})
        self.console._execute("print(item)", False)


if __name__ == '__main__':
    app = QApplication(sys.argv)  #instantiate a QtGui (holder for the app)
    if len(sys.argv)==1:
        fname = ''
    else:
        fname = sys.argv[1]
    ex = Application(filename=fname)
    sys.exit(app.exec_())
