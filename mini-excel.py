#!/usr/bin/env python
'''Mini Excel'''

__author__ = "Miki Tebeka <miki@mikitebeka.com>"

import wx
from wx.grid import (
    Grid, PyGridTableBase, GridTableMessage, GRIDTABLE_REQUEST_VIEW_GET_VALUES,
    EVT_GRID_CELL_LEFT_CLICK
)

from math import * # Get math functions in namespace
import re

# Make sure cell is not quoted yet
cell_re = re.compile("((?<!--\")[A-Z]\d+)") 
range_re = re.compile("([A-Z]\d+):([A-Z]\d+)")  
NUM_ROWS, NUM_COLS = 20, 10 # Arbitrary grid size 
CELLS = {} # (row, col) --> cell

def get_cell_value(row, col):
    cell = CELLS.get((row, col), None)
    if cell:
        return cell.calculate()
    else:
        return None

def name2location(cell_name):
    col, row = cell_name[0], cell_name[1:]
    col = ord(col) - ord("A")
    row = int(row)

    return row, col

def cell(cell_name):
    row, col = name2location(cell_name)
    return get_cell_value(row, col)

def cell_range(start, end):
    start_row, start_col = name2location(start)
    end_row, end_col = name2location(end)

    if start_row == end_row:
        indexes = [(start_row, col) for col in range(start_col, end_col + 1)]
    elif start_col == end_col:
        indexes = [(row, end_col) for row in range(start_row, end_row + 1)]
    else:
        raise ValueError

    return [get_cell_value(row, col) for row, col in indexes]

class TableCell:
    def __init__(self, value):
        self.value = value

    def calculate(self):
        try:
            return float(self.value)
        except ValueError:
            return self.value

class FunctionTableCell(TableCell):
    def __init__(self, value):
        TableCell.__init__(self, value)

        # Convert expression to valid Python expression
        # Replace `A4:A10` with `cell_range("A4", "A10")`
        self.py_expr = range_re.sub("cell_range(\"\\1\", \"\\2\")", value[1:])
        # Replace `A4` with `cell("A4")`
        self.py_expr = cell_re.sub("cell(\"\\1\")", self.py_expr)

    def calculate(self):
        return eval(self.py_expr)

class Table(PyGridTableBase):
    def __init__(self):
        PyGridTableBase.__init__(self)

    def GetNumberCols(self):
        return NUM_COLS

    def GetNumberRows(self):
        return NUM_ROWS

    def GetColLabelValue(self, col):
        return chr(ord("A") + col)

    def GetRowLabelValue(self, row):
        return "%d" % row

    def GetValue(self, row, col):
        try:
            value = get_cell_value(row, col)
            if value is None:
                return ""
            return str(value)
        except Exception:
            return "#ERR"

    def SetValue(self, row, col, value):
        if value.startswith("="):
            cell = FunctionTableCell(value)
        else:
            cell = TableCell(value)

        CELLS[(row, col)] = cell

        # Notify change
        msg = GridTableMessage(None, GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        self.GetView().ProcessTableMessage(msg)

class MiniExcel(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "Mini Excel")
        sizer = wx.BoxSizer(wx.VERTICAL)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(self, -1, "Value:"), 0,
                   wx.ALIGN_CENTER_VERTICAL)
        self.cell_value = wx.TextCtrl(self, -1)
        hsizer.Add(self.cell_value, 1, wx.EXPAND)
        b = wx.Button(self, -1, "&Set")
        self.Bind(wx.EVT_BUTTON, self.OnSetCell, b)
        hsizer.Add(b)
        sizer.Add(hsizer, 0, wx.EXPAND)

        grid = Grid(self)
        grid.SetTable(Table())
        grid.ForceRefresh()
        self.grid = grid

        self.Bind(EVT_GRID_CELL_LEFT_CLICK, self.OnCellClick, grid)
        self.current_cell = (0, 0)

        sizer.Add(grid, 1, wx.EXPAND)
        self.SetSizer(sizer)
        sizer.Fit(self)
        grid.SetFocus()

        self.CenterOnScreen()

    def OnSetCell(self, evt):
        value = self.cell_value.GetValue().strip()
        table = self.grid.GetTable()

        table.SetValue(self.current_cell[0], self.current_cell[1], value)

    def OnCellClick(self, evt):
        row = evt.GetRow()
        col = evt.GetCol()

        self.current_cell = (row, col)

        cell = CELLS.get((row, col), None)
        if cell:
            self.cell_value.SetValue(str(cell.value))
        else:
            self.cell_value.SetValue("")
            evt.Skip() # Let the grid process the event as well

if __name__ == "__main__":
    app = wx.PySimpleApp()
    dlg = MiniExcel()
    dlg.ShowModal()
