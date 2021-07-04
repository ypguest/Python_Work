# !/usr/bin/python
# -*- coding: utf-8 -*-
# @FileName:PandasTableModel.py
# @Time:2020/11/24 17:56
# @Author:Jason_Yin

import pandas as pd
from PyQt5 import QtCore, QtWidgets


class PandasTableModel(QtCore.QAbstractTableModel):

    def __init__(self,  parent=None, *args):
        super(PandasTableModel,  self).__init__(parent,  *args)
        self._filters = {}
        self._sortBy = []
        self._sortDirection = []
        self._dfSource = pd.DataFrame()
        self._dfDisplay = pd.DataFrame()

    def rowCount(self,  parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return self._dfDisplay.shape[0]

    def columnCount(self,  parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return self._dfDisplay.shape[1]

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self._dfDisplay.values[index.row()][index.column()])
        return QtCore.QVariant()

    def headerData(self, col, orientation=QtCore.Qt.Horizontal, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(str(self._dfDisplay.columns[col]))
        return QtCore.QVariant()

    def setupModel(self, header, data):
        self._dfSource = pd.DataFrame(data, columns=header)
        self._sortBy = []
        self._sortDirection = []
        self.setFilters({})

    def setFilters(self, filters):
        self.modelAboutToBeReset.emit()
        self._filters = filters
        self.updateDisplay()
        self.modelReset.emit()

    def sort(self, col, order=QtCore.Qt.AscendingOrder):
        #self.layoutAboutToBeChanged.emit()
        column = self._dfDisplay.columns[col]
        ascending = (order == QtCore.Qt.AscendingOrder)
        if column in self._sortBy:
            i = self._sortBy.index(column)
            self._sortBy.pop(i)
            self._sortDirection.pop(i)
        self._sortBy.insert(0, column)
        self._sortDirection.insert(0, ascending)
        self.updateDisplay()
        #self.layoutChanged.emit()
        self.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())

    def updateDisplay(self):

        dfDisplay = self._dfSource.copy()

        # Filtering
        cond = pd.Series(True, index = dfDisplay.index)
        for column, value in self._filters.items():
            cond = cond & \
                (dfDisplay[column].str.lower().str.find(str(value).lower()) >= 0)
        dfDisplay = dfDisplay[cond]

        # Sorting
        if len(self._sortBy) != 0:
            dfDisplay.sort_values(by=self._sortBy,
                                ascending=self._sortDirection,
                                inplace=True)

        # Updating
        self._dfDisplay = dfDisplay

