# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-22 14:35:41
# @Last Modified by:   edward
# @Last Modified time: 2016-07-22 23:58:34
import wx
from util import After, create_menubar
class Label(After, wx.StaticText):
    pass

class Dialog(After, wx.Dialog):
    def DoAfterInit(self):
        self.panel = wx.Panel(self)
        sizer = wx.FlexGridSizer(5, 2)
        fgcolor_val = '#485C80'
        ctrls = [
            Label(self.panel, label=u'BOSS名称', fgcolor=fgcolor_val),
            wx.TextCtrl(self.panel, style=wx.TE_CENTER, name='boss'),
            Label(self.panel, label=u'刷新时间', fgcolor=fgcolor_val),
            wx.SpinCtrl(self.panel, style=wx.TE_CENTER, name='refresh'),
            Label(self.panel, label=u'倒计时', fgcolor=fgcolor_val),
            wx.SpinCtrl(self.panel, style=wx.TE_CENTER, name='countdown'),
            wx.Button(self.panel, label=u"添加", name="addBtn"),
            
        ]
        border_val = 5
        sizer.Add(ctrls[0], flag=wx.ALIGN_RIGHT|wx.TOP, border=border_val)
        sizer.Add(ctrls[1], flag=wx.EXPAND|(wx.ALL^wx.BOTTOM), border=border_val)
        sizer.Add(ctrls[2], flag=wx.ALIGN_RIGHT|wx.TOP, border=border_val)
        sizer.Add(ctrls[3], flag=wx.EXPAND|(wx.ALL^wx.BOTTOM), border=border_val)
        sizer.Add(ctrls[4], flag=wx.ALIGN_RIGHT|wx.TOP, border=border_val)
        sizer.Add(ctrls[5], flag=wx.EXPAND|(wx.ALL^wx.BOTTOM), border=border_val)
        sizer.Add(wx.StaticLine(self.panel), flag=(wx.TOP|wx.BOTTOM)|wx.EXPAND, border=border_val*3)
        sizer.Add(wx.StaticLine(self.panel), flag=(wx.TOP|wx.BOTTOM)|wx.EXPAND, border=border_val*3)
        sizer.AddStretchSpacer()
        sizer.Add(ctrls[6], flag=wx.ALIGN_RIGHT|wx.RIGHT, border=border_val)
        proportion = 5
        sizer.AddGrowableCol(0, proportion) # idx, proportion
        sizer.AddGrowableCol(1, 10 - proportion)

        self.panel.SetSizer(sizer)

        


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
                (None, '', -1, None),
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
        dlg = Dialog(self, title=u"添加倒计时", size=(240, 180))
        dlg.ShowModal()
    def OnQuit(self, e):
        self.Destroy()
