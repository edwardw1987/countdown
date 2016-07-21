# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-21 15:12:55
# @Last Modified by:   vivi
# @Last Modified time: 2016-07-21 18:52:07
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
        self.frame.SetMinSize((400,300))
        # sizer = self.panel.GetSizer()
        # sizer.Fit(self.frame)
        # sizer.SetSizeHints(self.frame)
        self.frame.SetIcon(wx.Icon('rat_head.ico'))

        self.frame.Show()
    def InitMenu(self):
        self.menuBar = self.res.LoadMenuBar("MenuBar")
        self.frame.Bind(wx.EVT_MENU, self.AddCountDown, id=xrc.XRCID("AddCountDown"))
        # self.frame.Bind(wx.EVT_MENU, self.Subtract, id=xrc.XRCID("SubtractMenuItem"))
        # self.frame.Bind(wx.EVT_MENU, self.Multiply, id=xrc.XRCID("MultiplyMenuItem"))
        # self.frame.Bind(wx.EVT_MENU, self.Divide, id=xrc.XRCID("DivideMenuItem"))
        self.frame.SetMenuBar(self.menuBar)

    def AddCountDown(self, event):
        dlg = self.res.LoadDialog(self.frame, "AddCountDownDialog")
        sizer = dlg.GetSizer()

        # dlg = wx.MessageDialog(self.frame, "I can't convert this to float.",
        #                       'Conversion error', wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        # control.SetFocus()
        # control.SetSelection(-1, -1)
        # return False

def main():
    app = MyApp(0)
    app.MainLoop()
if __name__ == '__main__':
    main()