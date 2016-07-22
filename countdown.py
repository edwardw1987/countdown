# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-21 15:52:58
# @Last Modified by:   edward
# @Last Modified time: 2016-07-22 23:21:38
import wx
import ui

class App(wx.App):
    def OnInit(self):       
        fr = ui.Frame(
            None,
            title="RatHead CountDown",
            icon="rat_head.ico",
            )
        return True     

def main():
    app = App()
    app.MainLoop()
if __name__ == '__main__':
    main()