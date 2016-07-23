# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-21 15:52:58
# @Last Modified by:   edward
# @Last Modified time: 2016-07-23 18:46:18
import wx
import ui

class App(wx.App):
    def OnInit(self):       
        fr = ui.Frame(
            None,
            title="RatHead CountDown",
            icon="rat_head.ico",
            size=(640,480),
            minsize=(400,300),
            )
        self.SetTopWindow(fr)
        return True     

def main():
    app = App()
    app.MainLoop()
if __name__ == '__main__':
    main()