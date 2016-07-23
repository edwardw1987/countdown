# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-22 14:35:41
# @Last Modified by:   edward
# @Last Modified time: 2016-07-23 22:24:17
import wx
from util import After, create_menubar, create_menu
from validator import NotEmptyValidator
import db
from tinydb.database import Element
from collections import OrderedDict


class Label(After, wx.StaticText):
    pass


class ListCtrl(After, wx.ListCtrl):
    def DoAfterInit(self):
        self._itemStates = {}
        self._eids = []
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onLeftDClick)

    def ToggleItemState(self, index):
        eid = self.GetEid(index)
        self._itemStates[eid] = not self._itemStates.get(eid, 0)

    def GetItemState(self, index):
        return self._itemStates.get(self.GetEid(index), 0)

    def OnRightClick(self, e):
        raise NotImplementedError()

    def SetEids(self, eids):
        self._eids = eids

    def GetEid(self, pos):
        eid = self._eids[-(pos + 1)]
        return eid

    def AddEids(self, eid):
        self._eids.append(eid)

    def DelEidsByPos(self, pos):
        print pos, -(pos + 1)
        eid = self._eids.pop(-(pos + 1))
        db.delete([eid])

    def AdaptWidth(self, headings_num, proportions):
        num = sum(proportions)
        for i in range(headings_num):
            w = self.GetParent().GetClientSize()[0] / float(num)
            w *= proportions[i]
            self.SetColumnWidth(i, w)

    def onLeftDClick(self, e):
        print 'onLeftDClick'

        self._pos = e.GetIndex()
        if self._pos < 0:
            return
        self.OnToggleStatus(e)

    def onRightClick(self, e):
        print 'onRightClick'
        self._pos = e.GetIndex()
        if self._pos < 0:
            return
        data = {
            'rightClick': [
                (u'停止', 'stop', 0, self.OnToggleStatus) if self.GetItemState(self._pos) else (
                    u'启动', 'start', 0, self.OnToggleStatus),
                (u'删除', 'del', 0, self.OnDel),
                (u'修改', 'mod', 0, self.OnMod),
            ]
        }
        for m, title in create_menu(self.GetParent(), data):
            self.PopupMenu(m)
            break

    def OnDel(self, e):
        self.DeleteItem(self._pos)
        self.DelEidsByPos(self._pos)

    def OnMod(self, e):
        print 'OnMod'

    def OnToggleStatus(self, e):
        self.ToggleItemState(self._pos)
        self.SetStringItem(
            self._pos, 5, u'已启动' if self.GetItemState(self._pos) else u'已停止')


class Dialog(After, wx.Dialog):
    def OnAdd(self):
        print 'OnAdd'
        data = {
            'boss': self.ctrls[1].GetValue(),
            'refresh': self.ctrls[3].GetValue(),
            'countdown': self.ctrls[5].GetValue(),
        }
        ele = Element(data)
        ele.eid = db.insert(ele)
        self.GetParent().AddRows([ele])
        self.GetParent().LC.AddEids(ele.eid)

    def DoAfterInit(self):
        # self.panel = wx.Panel(self)
        sizer = wx.FlexGridSizer(5, 2)
        fgcolor_val = '#485C80'
        ctrls = [
            Label(self, label=u'BOSS名称', fgcolor=fgcolor_val),
            wx.TextCtrl(self, style=wx.TE_CENTER, name='boss',
                        validator=NotEmptyValidator(
                            message=u"BOSS名称不能为空!",
                            from_window_callback=self.OnAdd,
                        ),
                        ),
            Label(self, label=u'刷新时间', fgcolor=fgcolor_val),
            wx.SpinCtrl(self, style=wx.TE_CENTER, name='refresh'),
            Label(self, label=u'倒计时', fgcolor=fgcolor_val),
            wx.SpinCtrl(self, style=wx.TE_CENTER, name='countdown'),
            wx.Button(self, wx.ID_CANCEL),
            wx.Button(self, wx.ID_OK),

        ]
        self.ctrls = ctrls
        ctrls[6].SetDefault()
        # ==========
        # layout
        # ==========
        border_val = 5
        sizer.Add(ctrls[0], flag=wx.ALIGN_RIGHT | wx.TOP, border=border_val)
        sizer.Add(ctrls[1], flag=wx.EXPAND | (
            wx.ALL ^ wx.BOTTOM), border=border_val)
        sizer.Add(ctrls[2], flag=wx.ALIGN_RIGHT | wx.TOP, border=border_val)
        sizer.Add(ctrls[3], flag=wx.EXPAND | (
            wx.ALL ^ wx.BOTTOM), border=border_val)
        sizer.Add(ctrls[4], flag=wx.ALIGN_RIGHT | wx.TOP, border=border_val)
        sizer.Add(ctrls[5], flag=wx.EXPAND | (
            wx.ALL ^ wx.BOTTOM), border=border_val)
        sizer.Add(wx.StaticLine(self), flag=(
            wx.TOP | wx.BOTTOM) | wx.EXPAND, border=border_val * 3)
        sizer.Add(wx.StaticLine(self), flag=(
            wx.TOP | wx.BOTTOM) | wx.EXPAND, border=border_val * 3)
        # sizer.AddStretchSpacer()
        sizer.Add(ctrls[6], flag=wx.ALIGN_RIGHT, border=border_val)
        sizer.Add(ctrls[7], flag=wx.ALIGN_RIGHT | wx.RIGHT, border=border_val)
        proportion = 5
        sizer.AddGrowableCol(0, proportion)  # idx, proportion
        sizer.AddGrowableCol(1, 10 - proportion)

        self.SetSizer(sizer)


class Frame(After, wx.Frame):
    def DoAfterInit(self):
        # self.panel = wx.Panel(self)
        self.initAll()
        self.Show()
        self.Center()

    def initAll(self):
        self._initMenuBar()
        self._initListCtrl()
        self._initOthers()

    def _initOthers(self):
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def AddRows(self, data_list):
        for row in data_list:
            pos = self.LC.InsertStringItem(0, str(row.eid))
            # add values in the other columns on the same row
            self.LC.SetStringItem(pos, 1, row['boss'])
            self.LC.SetStringItem(pos, 4, str(row['refresh']))
            self.LC.SetStringItem(pos, 5, u'已停止')

    def _initListCtrl(self):
        self.LC = ListCtrl(self,
                           style=wx.LC_REPORT,
                           headings=['ID', u'BOSS名称',
                                     u'死亡时间', u'倒计时', '刷新时间', '状态'],
                           columnFormat=wx.LIST_FORMAT_CENTER,
                           fgcolor='#f40',

                           )
        # ===============
        self.LC.AdaptWidth(6, proportions=[0.5, 3, 2, 1, 2, 1.5])
        # ===============
        rows = db.all()
        self.AddRows(rows)
        self.LC.SetEids([i.eid for i in rows])
        # 0 will insert at the start of the list

    def _initMenuBar(self):
        _OD = OrderedDict()

        _OD[u'操作(&O)'] = [
            (u'添加倒计时\tCtrl+N', 'add', 0, self.OnAdd),
            (None, '', -1, None),
            (u'退出\tCtrl+Q', 'quit', 0, self.OnQuit),
        ]
        _OD[u'查看(&V)'] = [
            (u'窗口置顶', 'top', 1, self.OnSwitchTop),
        ]

        mb = create_menubar(self, _OD)
        # create item(normal, check, raido)
        # create sparartor
        # create submenu

        # final
        self.SetMenuBar(mb)
    # ==========

    def OnAdd(self, e):
        dlg = Dialog(self, title=u"添加倒计时", size=(240, 180))
        dlg.ShowModal()

    def OnSwitchTop(self, e):
        if e.IsChecked():
            self.SetWindowStyle(self.GetWindowStyle() | wx.STAY_ON_TOP)
        else:
            self.SetWindowStyle(self.GetWindowStyle() ^ wx.STAY_ON_TOP)

    def OnQuit(self, e):
        self.Destroy()

    def OnResize(self, e):
        self.LC.AdaptWidth(6, proportions=[0.5, 3, 2, 1, 2, 1.5, ])
        self.LC.SetClientSize(self.GetClientSize())
