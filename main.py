# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-20 23:37:23
# @Last Modified by:   edward
# @Last Modified time: 2016-07-20 23:45:14
import wx
import ui

class MainApp(wx.App):
    def OnInit(self):
        fr = ui.Frame(None)
        fr.Center()
        fr.Show()
        return True
def main():
    app = MainApp()
    app.MainLoop()
if __name__ == '__main__':
    main()