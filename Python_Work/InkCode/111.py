from PyQt4.QtGui import *
from PyQt4.QtCore import *
from misc.myframe import inkwmapdisplayframe
import re
from shared.scripts.filltable import FillTable
from cp.scripts.extractcpresult import *


class InkWmapDisplayDialog(QDialog, inkwmapdisplayframe.Ui_Dialog):

    def __init__(self, ids, lines):
        super(InkWmapDisplayDialog, self).__init__()
        self.setupUi(self)
        self.id = ids[0]
        self.lines = lines
        self.pushButtonResetTable.clicked.connect(self.showwamp)
        self.pushButtonAddBinInk.clicked.connect(self.addinkfromcpbin)
        self.pushButtonAddFcInk.clicked.connect(self.addinkfromcpfc)
        self.pushButtonAddIddInk.clicked.connect(self.addinkfromcpidd)
        self.pushButtonExportWmap.clicked.connect(self.exportwmap)
        self.pushButtonSetColor.clicked.connect(self.setupcolor)

        self.sortink = {}
        self.fcLimit = {}
        self.dclowLimit = {}
        self.dcupLimit = {}
        self.color = QColor('Blue')
        self.pushButtonSetColor.setStyleSheet("background-color:" + self.color.name() + ";")
        self.initLimit()
        self.setcombotestnames()
        self.showwamp()
        self.exec_()

    def setupinfolabel(self):
        totalCount = 0
        failCount = 0
        inkCount = 0
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                itemText = str(self.tableWidget.item(i, j).text())
                if itemText == '':
                    continue
                else:
                    totalCount += 1
                    if int(itemText) > 15:
                        failCount += 1
                        if int(itemText) == 99:
                            inkCount += 1
        infoText = "Total Duts: %4d  ----  Total Fail Duts: %4d  ----  Total Inked Duts: %4d   " % (
            totalCount, failCount, inkCount)
        self.labelInfo.setText(infoText)

    def setupcolor(self):
        color = QColorDialog.getColor(Qt.blue)
        if color.isValid():
            self.color =  QColorDialog.getColor(Qt.blue)
        self.pushButtonSetColor.setStyleSheet("background-color:" + self.color.name() + ";")

    def initLimit(self):
        import cx_Oracle
        conn = cx_Oracle.connect('wangbin/Wangbin@172.21.12.241/ora11')
        cursor = conn.cursor()
        oracle_cmd = "SELECT TESTSTAGE, FNLOC FROM CPFILE WHERE CPID=%d" % self.id
        cursor.execute(oracle_cmd)
        stage, self.notch = cursor.fetchone()
        cursor.close()
        conn.close()
        import csv
        if stage == '1':
            with open('fc_ht.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.fcLimit[row['testname']] =  float(row['limit'])
            with open('dc_ht.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.dclowLimit[row['testname']] =  float(row['lowlimit'])
                    self.dcupLimit[row['testname']] =  float(row['uplimit'])
        else:
            with open('fc_lt.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.fcLimit[row['testname']] =  float(row['limit'])
            with open('dc_lt.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.dclowLimit[row['testname']] =  float(row['lowlimit'])
                    self.dcupLimit[row['testname']] =  float(row['uplimit'])

    def setcombotestnames(self):
        self.comboBoxFcNames.addItems(['All'] + sorted(self.fcLimit.keys()))
        self.comboBoxIddNames.addItems(['All'] + sorted(self.dcupLimit.keys()))

    def showwamp(self):
        '''
        put the selected lot and wafer wmap to the table
        :return:
        '''
        import cx_Oracle
        conn = cx_Oracle.connect('wangbin/Wangbin@172.21.12.241/ora11')
        cursor = conn.cursor()
        oracle_cmd = "SELECT LOTID, WAFER FROM CPFILE WHERE CPID=%d" % self.id
        cursor.execute(oracle_cmd)
        cpfilerow = cursor.fetchone()
        self.lotId = cpfilerow[0]
        self.waferNum = cpfilerow[1]
        self.waferLineIndex = 0
        self.COLCNT = 0
        self.ROWCNT = 0
        curLineNum = 0
        MAPflag = False
        for line in self.lines:
            if line.startswith('MAPID1'):
                tmpArr = line[7:].split('.')
                if self.lotId.startswith(tmpArr[0]) and tmpArr[1] == "%02d" % self.waferNum:
                    MAPflag = True
            elif line.startswith('COLCNT'):
                self.COLCNT = int(line[-2:])
            elif line.startswith('ROWCNT'):
                self.ROWCNT = int(line[-2:])
            elif MAPflag and line.startswith('MAP'):
                self.waferLineIndex = curLineNum
                break

            curLineNum += 1
        self.infosIndex = []
        self.contentsIndex = range(1, self.COLCNT+1)
        self.contentsIndex = [str(_tmp) for _tmp in self.contentsIndex]
        if self.notch == 0:
            self.contentsIndex.reverse()
        self.rowInfos2D = []
        self.contents2D = []
        self.verIndexs = range(1,self.ROWCNT+1)
        if self.notch == 180:
            self.verIndexs.reverse()
        for line in self.lines[self.waferLineIndex:]:
            if not line.startswith('MAP'):
                continue
            self.contents2D.append([_tmp.replace('00','') for _tmp in re.findall(r'..', line[7:])])

            if line.startswith('MAP%03d' % self.ROWCNT):
                break

        FillTable(self.tableWidget, self.infosIndex, self.contentsIndex,
                  self.rowInfos2D, self.contents2D, self.verIndexs)
        self.setupinfolabel()
        font = QFont()
        font.setPixelSize(8)
        self.tableWidget.horizontalHeader().setFont(font)
        for i in range(len(self.contentsIndex)):
            self.tableWidget.setColumnWidth(i, 18)
            self.tableWidget.setFont(font)
        for i in range(len(self.verIndexs)):
            self.tableWidget.setRowHeight(i, 14)
        for i in range(len(self.verIndexs)):
            for j in range(len(self.contentsIndex)):
                itemText = str(self.tableWidget.item(i, j).text())
                if itemText != '' and int(itemText) > 15:
                    self.tableWidget.item(i, j).setBackgroundColor(QColor('Red'))


    def addinkfromcpbin(self):
        import cx_Oracle
        conn = cx_Oracle.connect('wangbin/Wangbin@172.21.12.241/ora11')
        cursor = conn.cursor()
        oracle_cmd = "SELECT X,Y,SORT FROM CPCHIPINFO WHERE CPID=%d" % self.id
        cursor.execute(oracle_cmd)
        dutinfos = cursor.fetchall()
        cursor.close()
        conn.close()
        passdutinfosHash = {}
        faildutinfosHash = {}
        for dutinfo in dutinfos:
            if dutinfo[2] > 15:
                try:
                    faildutinfosHash[dutinfo[0]][dutinfo[1]] = 2
                except KeyError:
                    faildutinfosHash[dutinfo[0]] = {}
                    faildutinfosHash[dutinfo[0]][dutinfo[1]] = 2
            else:
                try:
                    passdutinfosHash[dutinfo[0]][dutinfo[1]] = 0
                except KeyError:
                    passdutinfosHash[dutinfo[0]] = {}
                    passdutinfosHash[dutinfo[0]][dutinfo[1]] = 0
        self.sortink = self.findring(faildutinfosHash, passdutinfosHash)
        self.mapink2table(self.sortink)
        self.setupinfolabel()

    def insertfailtohash(self, passdutinfosHash, faildutinfosHash, X, Y):
        '''
        insert fail information to the faildutinfosHash
        remove this information from passdutinfosHash if exists
        :param passdutinfosHash:
        :param faildutinfosHash:
        :param X: X Coord
        :param Y: Y Coord
        :return: None
        '''
        try:
            del passdutinfosHash[X][Y]
        except KeyError:
            pass
        try:
            faildutinfosHash[X][Y] = 2
        except KeyError:
            faildutinfosHash[X] = {}
            faildutinfosHash[X][Y] = 2

    def insertpasstohash(self, passdutinfosHash, faildutinfosHash, X, Y):
        '''
        add the pass information to the passdutinfosHash in place if this dut
        not in the faildutinfosHash
        :param passdutinfosHash:
        :param faildutinfosHash:
        :param X:
        :param Y:
        :return: None
        '''
        try:
            faildutinfosHash[X][Y]
        except KeyError:
            try:
                passdutinfosHash[X][Y] = 0
            except KeyError:
                passdutinfosHash[X] = {}
                passdutinfosHash[X][Y] = 0

    def addinkfromcpfc(self):
        '''
        the callback of the button pushButtonAddFcInk, add the ink dut to the table
        :return: None
        '''

        # self.pushButtonAddFcInk.setStyleSheet("background-color:" + color.name() + ";")
        if str(self.comboBoxFcNames.currentText()) == 'All':
            testNames = self.fcLimit.keys()
        else:
            testNames = [str(self.comboBoxFcNames.currentText())]
        resultAll =  extractresultbynamesofwafer(self.id, testNames, 'FC', True)
        passdutinfosHash = {}
        faildutinfosHash = {}
        for testName in resultAll.keys():
            uplimit = self.fcLimit[testName]
            for X in resultAll[testName].keys():
                for Y in resultAll[testName][X].keys():
                    if len(resultAll[testName][X][Y]) == 9:
                        self.insertfailtohash(passdutinfosHash, faildutinfosHash, X, Y)
                    elif resultAll[testName][X][Y] == '':
                        self.insertpasstohash(passdutinfosHash, faildutinfosHash, X, Y)
                    else:
                        if int(resultAll[testName][X][Y]) > uplimit:
                            self.insertfailtohash(passdutinfosHash, faildutinfosHash, X, Y)
                        else:
                            self.insertpasstohash(passdutinfosHash, faildutinfosHash, X, Y)
        self.mapfail2table(faildutinfosHash)
        self.setupinfolabel()

    def addinkfromcpidd(self):
        '''
        the callback of the button pushButtonAddIddInk, add the ink dut to the table
        :return: None
        '''

        # self.pushButtonAddIddInk.setStyleSheet("background-color:" + color.name() + ";")
        if str(self.comboBoxIddNames.currentText()) == 'All':
            testNames = self.dclowLimit.keys()
        else:
            testNames = [str(self.comboBoxIddNames.currentText())]
        resultAll = extractresultbynamesofwafer(self.id, testNames, 'DC', True)
        passdutinfosHash = {}
        faildutinfosHash = {}
        for testName in resultAll.keys():
            uplimit = self.dcupLimit[testName]
            lowlimit = self.dclowLimit[testName]
            for X in resultAll[testName].keys():
                for Y in resultAll[testName][X].keys():
                    if resultAll[testName][X][Y].startswith('N') or resultAll[testName][X][Y].startswith('O'):
                        self.insertfailtohash(passdutinfosHash, faildutinfosHash, X, Y)
                    else:
                        if float(resultAll[testName][X][Y]) > uplimit or float(resultAll[testName][X][Y]) < lowlimit:
                            self.insertfailtohash(passdutinfosHash, faildutinfosHash, X, Y)
                        else:
                            self.insertpasstohash(passdutinfosHash, faildutinfosHash, X, Y)
        self.mapfail2table(faildutinfosHash)
        self.setupinfolabel()

    def findring(self, faildutinfosHash, passdutinfosHash):
        '''
        find the ink duts based on the faildutinfosHash ,passdutinfosHash and ring number
        :param faildutinfosHash:
        :param passdutinfosHash:
        :return: the inked dut position
        '''
        ringHash = {}
        ringNums = int(str(self.comboBoxRingNum.currentText()))
        for _i in range(ringNums):
            ringHash[_i] = {}
        for X in faildutinfosHash.keys():
            for Y in faildutinfosHash[X].keys():
                for xoffset, yoffset in zip([1,0,-1,0], [0,-1,0,1]):
                    try:
                        if faildutinfosHash[X + xoffset][Y + yoffset]:
                            faildutinfosHash[X][Y] += 1
                    except KeyError:
                        pass

        for X in faildutinfosHash.keys():
            for Y in faildutinfosHash[X].keys():
                for xoffset, yoffset in zip([1,0,-1,0], [0,-1,0,1]):
                    try:
                        if faildutinfosHash[X + xoffset][Y + yoffset] > 4:
                            faildutinfosHash[X][Y] = 5
                    except KeyError:
                        pass

        for X in passdutinfosHash.keys():
            for Y in passdutinfosHash[X].keys():
                for xoffset  in [-1, 0, 1]:
                    for yoffset in [-1, 0, 1]:
                        if xoffset == 0 and yoffset == 0:
                            continue
                        try:
                            if faildutinfosHash[X + xoffset][Y + yoffset] > 4:
                                passdutinfosHash[X][Y] = 1
                                try:
                                    ringHash[0][X][Y] = 1
                                except KeyError:
                                    ringHash[0][X] = {}
                                    ringHash[0][X][Y] = 1
                        except KeyError:
                            pass

        for ringNum in range(1, ringNums):
            for X in passdutinfosHash.keys():
                for Y in passdutinfosHash[X].keys():
                    for xoffset in [-1, 0, 1]:
                        for yoffset in [-1, 0, 1]:
                            if xoffset == 0 and yoffset == 0:
                                continue
                            try:
                                if ringHash[ringNum - 1][X - 1][Y] == 1:
                                    try:
                                        ringHash[ringNum][X][Y] = 1
                                    except KeyError:
                                        ringHash[ringNum][X] = {}
                                        ringHash[ringNum][X][Y] = 1
                            except KeyError:
                                pass

        return ringHash

    def mapfail2table(self, failhash):
        for X in failhash.keys():
            for Y in failhash[X].keys():
                if self.notch == 180:
                    tableRow = self.ROWCNT-Y
                    tableCol = X-1
                else:
                    tableRow = Y-1
                    tableCol = self.COLCNT-X
                if int(str(self.tableWidget.item(tableRow, tableCol).text())) <16:
                    self.tableWidget.item(tableRow, tableCol).setText('99')
                    self.tableWidget.item(tableRow, tableCol).setBackgroundColor(self.color)

    def mapink2table(self, ringHash):
        ringNums = int(str(self.comboBoxRingNum.currentText()))
        for _i in range(ringNums):
            self.mapfail2table(ringHash[_i])

    def exportwmap(self):
        self.table2stringlist()
        self.outLines = [_tmp1[:8] + _tmp2 for _tmp1, _tmp2 in \
                         zip(self.lines[self.waferLineIndex:self.waferLineIndex+self.ROWCNT], self.outLines)]
        alloutlines = self.lines[:self.waferLineIndex] + self.outLines + self.lines[self.waferLineIndex+self.ROWCNT:]
        alloutlines = [_tmp1+'\n' for _tmp1 in alloutlines]

        path = QFileDialog.getSaveFileName(self, "Save File", '.', '*')
        with open(path, 'w') as FHOUT:
            FHOUT.writelines(alloutlines)

    def table2stringlist(self):
        self.outLines = []
        for i in range(self.ROWCNT):
            line = ''
            for j in range(self.COLCNT):
                if self.tableWidget.item(i,j).text() == '':
                    line += '00'
                else:
                    line += str(self.tableWidget.item(i,j).text())
            self.outLines.append(line)
