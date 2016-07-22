# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-22 14:35:41
# @Last Modified by:   edward
# @Last Modified time: 2016-07-22 17:00:38
import wx
from util import After, create_menubar


class Frame(After, wx.Frame):
    def DoAfterInit(self):
        self.panel = wx.Panel(self)
        self.initAll()
        self.Show()
        self.Center()

    def initAll(self):
        self._initMenuBar()

    def _initMenuBar(self):
        _data = {
            u'操作(&O)': [
                (u'添加倒计时\tCtrl+N', 'add', 0, self.OnAdd),
                (None, '', 3, None),
                (u'退出\tCtrl+Q', 'quit', 0, self.OnQuit),
              ],
            }

        mb, mi_hash = create_menubar(self, _data)
        # create item(normal, check, raido)
        # create sparartor
        # create submenu

        # final
        self.SetMenuBar(mb)
    # ==========
    def OnAdd(self, e):
        print 'add'
    def OnQuit(self, e):
        print 'quit'
