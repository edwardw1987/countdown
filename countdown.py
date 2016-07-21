# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-21 15:12:55
# @Last Modified by:   edward
# @Last Modified time: 2016-07-21 15:37:51
import wx
from wx import xrc
class MyApp(wx.App):
    def OnInit(self):
        self.res = xrc.XmlResource('countdown.xrc')
        self.init()
        self.InitMenu()
        return True

    def init(self):
        self.frame = self.res.LoadFrame(None, "MainFrame")
        self.panel = xrc.XRCCTRL(self.frame, "MainPanel")

        sizer = self.panel.GetSizer()
        sizer.Fit(self.frame)
        sizer.SetSizeHints(self.frame)
        self.frame.Show()
    def InitMenu(self):
        self.menuBar = self.res.LoadMenuBar("MenuBar")
        # self.frame.Bind(wx.EVT_MENU, self.Add, id=xrc.XRCID("AddMenuItem"))
        # self.frame.Bind(wx.EVT_MENU, self.Subtract, id=xrc.XRCID("SubtractMenuItem"))
        # self.frame.Bind(wx.EVT_MENU, self.Multiply, id=xrc.XRCID("MultiplyMenuItem"))
        # self.frame.Bind(wx.EVT_MENU, self.Divide, id=xrc.XRCID("DivideMenuItem"))
        self.frame.SetMenuBar(self.menuBar)

def main():
    app = MyApp(0)
    app.MainLoop()
if __name__ == '__main__':
    main()