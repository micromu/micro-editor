'''
Created on Jul 8, 2013

@author: micromu
'''
#! /usr/bin/python

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from pygments import highlight 
from pygments.lexers import guess_lexer, get_lexer_by_name 
from pygments.formatters import HtmlFormatter 

class Notepad(QtWidgets.QMainWindow):
    def __init__(self):
        super(Notepad, self).__init__()
        self.initUI()
        self.highlighter = MicroHighlighter(self.text)
        
    def initUI(self):
        
        menubar = self.menuBar()
        
        #menu
        newAction = QtWidgets.QAction('New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('Create new file')
        newAction.triggered.connect(self.newFile)
        
        saveAction = QtWidgets.QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save current file')
        saveAction.triggered.connect(self.saveFile)
        
        openAction = QtWidgets.QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a file')
        openAction.triggered.connect(self.openFile)
        
        closeAction = QtWidgets.QAction('Close', self) #QAction is a widget that acts as an option in a menu
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Close Micro') #pop-ups when a user hovers the mouse over the closeAction widget
        closeAction.triggered.connect(self.close) #uses the signals-slots pattern (closeAction send a signal to the slot of the self object that will run the close action
        
        fileMenu = menubar.addMenu('&File') #the & tell the widget to add a shortcut that will be triggered with Ctrl+"first letter of the following word"
        fileMenu.addAction(newAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(closeAction)
        
        pythonAction = QtWidgets.QAction('Python', self)
        pythonAction.setShortcut('Ctrl+P')
        pythonAction.setStatusTip('Syntax highlighting for Python')
        pythonAction.setCheckable(True)
        pythonAction.setChecked(True)
        pythonAction.toggled.connect(lambda x: self.updateLanguage('python'))
        
        htmlAction = QtWidgets.QAction('html', self)
        htmlAction.setShortcut('Ctrl+H')
        htmlAction.setStatusTip('Syntax highlighting for html')
        htmlAction.setCheckable(True)
        htmlAction.toggled.connect(lambda x: self.updateLanguage('html'))
        
        languageGroup = QtWidgets.QActionGroup(self)
        languageGroup.addAction(pythonAction)
        languageGroup.addAction(htmlAction)
        
        languageMenu = menubar.addMenu('&Language')
        languageMenu.addAction(pythonAction)
        languageMenu.addAction(htmlAction)
        
        #editor
        self.text = QtWidgets.QTextEdit(self)
        self.setCentralWidget(self.text)
        
        self.setGeometry(300,300,300,300)
        self.setWindowTitle('Micro')
        self.show()
    
    def newFile(self):
        self.text.clear()
    
    def saveFile(self):
        #PyQt differs from Qt. getSaveFileName returns a tuple of strings, where the first element is the file path
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', QtCore.QDir.homePath())
        f = open(filename[0], 'w')
        filedata = self.text.toPlainText()
        f.write(filedata)
        f.close()
    
    def openFile(self):
        #PyQt differs from Qt. getOpenFileName returns a tuple of strings, where the first element is the file path
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', QtCore.QDir.homePath())
        f = open(filename[0], 'r')
        filedata = f.read()
        self.text.setText(filedata)
        f.close()
        
    def updateLanguage(self, language):
        self.highlighter.language = language
        self.highlighter.rehighlight()

class MicroHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, textEdit):
        super(MicroHighlighter, self).__init__(textEdit.document())
        self.formatter = MicroFormatter(linenos=True)
        self.text = textEdit
        self.language = 'python'
    
    def highlightBlock(self, text):
        
        currentPosition = self.currentBlock().position()
        textToHighlight = str(self.text.toPlainText()) + '\n'
        
        highlight(textToHighlight, get_lexer_by_name(self.language, stripall=True), self.formatter)
        
        for i in range(len(str(text))):
            try:
                self.setFormat(i,1,self.formatter.data[currentPosition+i])
            except IndexError:
                pass

class MicroFormatter(HtmlFormatter):
    
    def __init__(self, linenos):
        super(HtmlFormatter, self).__init__()
        self.linenos = linenos
        
        self.data = []
        self.styles = {}
        
        for token, style in self.style:
            textFormatter = QtGui.QTextCharFormat()

            if style['color']:
                textFormatter.setForeground(QtGui.QColor('#' + style['color'])) 
            if style['bgcolor']:
                textFormatter.setBackground(QtGui.QColor('#' + style['bgcolor'])) 
            if style['bold']:
                textFormatter.setFontWeight(QtGui.QFont.Bold)
            if style['italic']:
                textFormatter.setFontItalic(True)
            if style['underline']:
                textFormatter.setFontUnderline(True)
            
            self.styles[str(token)] = textFormatter
    
    def format(self, tokensource, outfile):
        global styles
        self.data = []
        
        for ttype, value in tokensource:
            l = len(value)
            t = str(ttype)                
            self.data.extend([self.styles[t],]*l)

def main():
    app = QtWidgets.QApplication(sys.argv)
    notepad = Notepad()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()