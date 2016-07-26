#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-21 15:52:58
# @Last Modified by:   edward
# @Last Modified time: 2016-07-26 12:16:53
import wx
import ui
from resource import rat_head_original
import test_version

class App(wx.App):
    def __init__(self, *args, **kw):
        self.test_version = kw.pop('test_version', None)
        super(App, self).__init__(*args, **kw)

    def OnInit(self): 
        fr = ui.Frame(
            None,
            title="RatHead CountDown",
            icon=rat_head_original.getIcon(),
            # icon="rat_head16.ico",
            size=(640,480),
            minsize=(400,300),
            )

        if self.test_version:
            fr.SetTitle(fr.GetTitle() + '(test_version)')
            signal = test_version.expired(2016,8,15)
            if signal:
                wx.MessageBox('expired!' if signal == True else 'network error')
                fr.Destroy()
        self.SetTopWindow(fr)
        return True




def main():
    app = App(test_version=True)
    app.MainLoop()
if __name__ == '__main__':
    main()
