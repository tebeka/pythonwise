#!/usr/bin/env python

# So that 8/3 will be 2.6666 and not 2
from __future__ import division

__author__ = 'Miki Tebeka <miki@mikitebeka.com>'
__version__ = '0.0.2'

# Calculator GUI:

# ___________v
# [7][8][9][/]
# [4][5][6][*]
# [1][2][3][-]
# [0][.][C][+]
# [    =     ]

import wx
# So we can evaluate 'sqrt(8)'
from math import *

class Calculator(wx.Dialog):
   '''Main calculator dialog'''
   def __init__(self):
       title = 'Calculator version %s' % __version__
       wx.Dialog.__init__(self, None, -1, title)
       sizer = wx.BoxSizer(wx.VERTICAL) # Main vertical sizer

       # ____________v
       self.display = wx.ComboBox(self, -1) # Current calculation
       sizer.Add(self.display, 0, wx.EXPAND) # Add to main sizer

       # [7][8][9][/]
       # [4][5][6][*]
       # [1][2][3][-]
       # [0][.][C][+]
       gsizer = wx.GridSizer(4, 4)
       for row in (('7', '8', '9', '/'),
                   ('4', '5', '6', '*'),
                   ('1', '2', '3', '-'),
                   ('0', '.', 'C', '+')):
           for label in row:
               b = wx.Button(self, -1, label)
               gsizer.Add(b)
               self.Bind(wx.EVT_BUTTON, self.OnButton, b)
       sizer.Add(gsizer, 1, wx.EXPAND)

       # [    =     ]
       b = wx.Button(self, -1, '=')
       self.Bind(wx.EVT_BUTTON, self.OnButton, b)
       sizer.Add(b, 0, wx.EXPAND)
       self.equal = b

       # Set sizer and center
       self.SetSizer(sizer)
       sizer.Fit(self)
       self.CenterOnScreen()

   def OnButton(self, evt):
       '''Handle button click event'''
       # Get title of clicked button
       label = evt.GetEventObject().GetLabel()

       if label == '=': # Calculate
           try:
               compute = self.display.GetValue()
               # Ignore empty calculation
               if not compute.strip():
                   return

               # Calculate result
               result = eval(compute)

               # Add to history
               self.display.Insert(compute, 0)

               # Show result
               self.display.SetValue(str(result))
           except Exception as err:
               wx.LogError(str(err))
               return

       elif label == 'C': # Clear
           self.display.SetValue('')

       else: # Just add button text to current calculation
           self.display.SetValue(self.display.GetValue() + label)
           self.equal.SetFocus() # Set the [=] button in focus

if __name__ == '__main__':
   # Run the application
   app = wx.PySimpleApp()
   dlg = Calculator()
   dlg.ShowModal()
   dlg.Destroy()
