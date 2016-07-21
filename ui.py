# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-20 23:37:49
# @Last Modified by:   edward
# @Last Modified time: 2016-07-21 09:20:51
import wx

class Frame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Frame, self).__init__(*args, **kwargs)
        self.SetMenuBar(self.menubar)

    @property
    def menubar(self):
        mb = wx.MenuBar()
        mb.Append(wx.Menu(), 'file\tf')
        return mb
