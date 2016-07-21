#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-21 12:43:36
# @Last Modified by:   edward
# @Last Modified time: 2016-07-21 15:01:40
"""
Simple calculator that uses XRC.
"""
import wx
from wx import xrc
class MyApp(wx.App):
    def OnInit(self):
        self.res = xrc.XmlResource("calc.xrc")
        self.InitFrame()
        self.InitMenu()
        self.InitEverythingElse()
        return True
    def InitFrame(self):
        self.frame = self.res.LoadFrame(None, "MainFrame")
        self.panel = xrc.XRCCTRL(self.frame, "MainPanel")
        self.first_arg = xrc.XRCCTRL(self.panel, "FirstArg")
        self.second_arg = xrc.XRCCTRL(self.panel, "SecondArg")
        self.result = xrc.XRCCTRL(self.panel, "Result")
        self.first_arg.SetValue("Hi")
        self.second_arg.SetValue("You")
        self.result.SetValue("man")
    def InitMenu(self):
        self.menuBar = self.res.LoadMenuBar("MenuBar")
        self.frame.Bind(wx.EVT_MENU, self.Add, id=xrc.XRCID("AddMenuItem"))
        self.frame.Bind(wx.EVT_MENU, self.Subtract, id=xrc.XRCID("SubtractMenuItem"))
        self.frame.Bind(wx.EVT_MENU, self.Multiply, id=xrc.XRCID("MultiplyMenuItem"))
        self.frame.Bind(wx.EVT_MENU, self.Divide, id=xrc.XRCID("DivideMenuItem"))
        self.frame.SetMenuBar(self.menuBar)
    def InitEverythingElse(self):
        sizer = self.panel.GetSizer()
        sizer.Fit(self.frame)
        sizer.SetSizeHints(self.frame)
        self.frame.Show()
    def InitArgs(self):
        try:
            self.first = float(self.first_arg.GetValue())
        except ValueError:
            return self.BadFloatValue(self.first_arg)
        try:
            self.second = float(self.second_arg.GetValue())
        except ValueError:
            return self.BadFloatValue(self.second_arg)
        return True
    def BadFloatValue(self, control):
        dlg = wx.MessageDialog(self.frame, "I can't convert this to float.",
                              'Conversion error', wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        control.SetFocus()
        control.SetSelection(-1, -1)
        return False
    def Add(self, evt):
        if self.InitArgs():
            self.result.SetValue(str(self.first + self.second))
    def Subtract(self, evt):
        if self.InitArgs():
            self.result.SetValue(str(self.first - self.second))
    def Multiply(self, evt):
        if self.InitArgs():
            self.result.SetValue(str(self.first * self.second))
    def Divide(self, evt):
        if self.InitArgs():
            if self.second != 0:
                self.result.SetValue(str(self.first / self.second))
            else:
                self.result.SetValue("#ERROR")
def main():
    app = MyApp(0)
    app.MainLoop()
if __name__ == '__main__':
    main()