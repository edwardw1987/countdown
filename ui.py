# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-22 14:35:41
# @Last Modified by:   edward
# @Last Modified time: 2016-07-24 15:08:47
import wx
from util import After, create_menubar, create_menu
from validator import NotEmptyValidator
import db
from tinydb.database import Element
from collections import OrderedDict
import glob
from datetime import datetime, timedelta
import threading
import time
from event import CountEvent, EVT_COUNT, CountingThread


class Label(After, wx.StaticText):
    pass


class ListCtrl(After, wx.ListCtrl):
    def DoAfterInit(self):
        self._itemStates = {}
        self._threadPool = {}
        self._eids = []
        self._refs = []
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onLeftDClick)
        self.Bind(EVT_COUNT, self.OnCount)

    def getThread(self, pos):
        eid = self.GetEid(pos)
        return self._threadPool.get(eid)
    def setThread(self, pos, thread):
        eid = self.GetEid(pos)
        self._threadPool[eid] = thread

    def OnCount(self, evt):
        pos, s = evt.GetValue()
        self.SetStringItem(pos, 3, '%d s' % s)
        if s == 0: # finish thread task
            self.toggleState(pos)
   
    def AddRows(self, data_list):
        for row in data_list:
            pos = self.InsertStringItem(self.GetItemCount(), str(row.eid))
            # add values in the other columns on the same row
            self.SetStringItem(pos, 1, row['boss'], imageId=0)
            self.SetStringItem(pos, 2, '0000-00-00 00:00:00')
            self.SetStringItem(pos, 3, '0 s')
            self.SetStringItem(pos, 4, str(row['refresh']) + ' min')
            self.SetStringItem(pos, 5, u'已停止')
        self.addCache(data_list)

    initRows = AddRows

    def addCache(self, rows):
        self._refs.extend(i['refresh'] for i in rows)
        self._eids.extend(i.eid for i in rows)

    def GetRefresh(self, pos):
        return self._refs[pos]

    @property
    def IsStartAll(self):
        return all(self._itemStates.values() or [0])

    @property
    def IsStopAll(self):
        return not any(self._itemStates.values())

    def ToggleItemState(self, index, state=None):
        eid = self.GetEid(index)
        if state is None:
            self._itemStates[eid] = not self._itemStates.get(eid, 0)
        elif state in {0, 1}:
            self._itemStates[eid] = state
        return self._itemStates[eid]

    def GetItemState(self, index):
        return self._itemStates.get(self.GetEid(index), 0)

    def OnRightClick(self, e):
        raise NotImplementedError()

    def GetEid(self, pos):
        eid = self._eids[pos]
        return eid

    def AddEids(self, eid):
        self._eids.append(eid)
        print self._eids


    def DelEidsByPos(self, pos):
        print pos
        print self._eids
        eid = self._eids.pop(pos)

        print eid
        print self._eids
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
        self.OnToggleState(e)

    def onRightClick(self, e):
        print 'onRightClick'
        self._pos = e.GetIndex()
        if self._pos < 0:
            return
        data = {
            'rightClick': [
                (u'停止', 'stop', 0, self.OnToggleState) if self.GetItemState(self._pos) else (
                    u'启动', 'start', 0, self.OnToggleState),
                (u'全部启动', 'startall', 0, self.OnStartAll) if not self.IsStartAll else (
                    None, None, None, None),
                (u'全部停止', 'stopall', 0, self.OnStopAll) if not self.IsStopAll else (
                    None, None, None, None),
                (None, None, -1, None),
                (u'删除', 'del', 0, self.OnDel),
                (u'修改', 'mod', 0, self.OnMod),
            ]
        }
        for m, title in create_menu(self.GetParent(), data):
            self.PopupMenu(m)
            break

    def DeleteItem(self, pos):
        super(ListCtrl, self).DeleteItem(pos)
        self.DelEidsByPos(pos)

    def OnDel(self, e):
        self.DeleteItem(self._pos)

    def OnMod(self, e):
        print 'OnMod'

    def toggleThread(self, pos, state):
        if state == 1:
            ref = self.GetRefresh(pos)
            worker = CountingThread(self, (ref, pos))
            worker.start()
            self.setThread(pos, worker)
            print 'start'
        elif state == 0:
            thread = self.getThread(pos)
            if thread is not None and not thread.stopped():
                thread.stop()
                self.SetStringItem(pos, 3, '0 s')
                print 'stop'

    def toggleState(self, pos):
        state = self.ToggleItemState(pos)
        self.SetStringItem(
            pos, 5, u'已启动' if state else u'已停止')
        self.SetStringItem(
            pos, 2, datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S') if state else u'0000-00-00 00:00:00')
        ref = self.GetRefresh(pos)
        self.SetStringItem(
            pos, 4, datetime.strftime(datetime.now() + timedelta(seconds=60 * ref), '%Y-%m-%d %H:%M:%S') if state else '%d min' % ref)
        return state

    def OnToggleState(self, e):
        state =self.toggleState(self._pos)
        self.toggleThread(self._pos, state)

    def OnStartAll(self, e):
        self._toggleAll(e, state=1)

    def OnStopAll(self, e):
        self._toggleAll(e, state=0)

    def _toggleAll(self, e, state=1):
        for i in range(self.GetItemCount()):
            self.ToggleItemState(i, state=state)
            self.SetStringItem(
                i, 5, u'已启动' if self.GetItemState(i) else u'已停止'
            )
            self.SetStringItem(
                i, 2, datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S') if self.GetItemState(i) else u'0000-00-00 00:00:00')
            ref = self.GetRefresh(i)
            self.SetStringItem(
                i, 4, datetime.strftime(datetime.now() + timedelta(seconds=60 * ref), '%Y-%m-%d %H:%M:%S') if self.GetItemState(i) else '%d min' % ref)
            self.toggleThread(i, state)

class Dialog(After, wx.Dialog):
    def OnAdd(self):
        print 'OnAdd'
        data = {
            'boss': self.ctrls[1].GetValue(),
            'refresh': self.ctrls[3].GetValue(),
            # 'countdown': self.ctrls[5].GetValue(),
        }
        ele = Element(data)
        ele.eid = db.insert(ele)
        self.GetParent().LC.AddRows([ele])

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
            Label(self, label=u'刷新间隔', fgcolor=fgcolor_val),
            wx.SpinCtrl(self, style=wx.TE_CENTER, name='refresh'),
            # Label(self, label=u'倒计时', fgcolor=fgcolor_val),
            # wx.SpinCtrl(self, style=wx.TE_CENTER, name='countdown'),
            None, None,
            wx.Button(self, wx.ID_CANCEL),
            wx.Button(self, wx.ID_OK),

        ]
        self.ctrls = ctrls
        ctrls[7].SetDefault()
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
        # sizer.Add(ctrls[4], flag=wx.ALIGN_RIGHT | wx.TOP, border=border_val)
        # sizer.Add(ctrls[5], flag=wx.EXPAND | (
        #     wx.ALL ^ wx.BOTTOM), border=border_val)
        sizer.Add(wx.StaticLine(self), flag=(
            wx.TOP | wx.BOTTOM) | wx.EXPAND, border=border_val * 3)
        sizer.Add(wx.StaticLine(self), flag=(
            wx.TOP | wx.BOTTOM) | wx.EXPAND, border=border_val * 3)
        # sizer.AddStretchSpacer()
        sizer.Add(ctrls[6], flag=wx.ALIGN_RIGHT|wx.LEFT|wx.BOTTOM, border=border_val)
        sizer.Add(ctrls[7], flag=wx.ALIGN_RIGHT | wx.RIGHT|wx.BOTTOM, border=border_val)
        proportion = 5
        sizer.AddGrowableCol(0, proportion)  # idx, proportion
        sizer.AddGrowableCol(1, 10 - proportion)

        self.SetSizer(sizer)
        sizer.Fit(self)

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

    def _initListCtrl(self):
        self.LC = ListCtrl(self,
                           style=wx.LC_REPORT,
                           headings=['ID', u'BOSS名称',
                                     u'死亡时间', u'倒计时', '刷新时间', '状态'],
                           # columnFormat=wx.LIST_FORMAT_CENTER,
                           fgcolor='#f40',

                           )
        # ===============
        il = wx.ImageList(16,16)
        il.Add(wx.Bitmap('rat_head2.ico', wx.BITMAP_TYPE_ICON))
        self.LC.AssignImageList(il, wx.IMAGE_LIST_SMALL)
        # ===============
        self.LC.AdaptWidth(6, proportions=[0.5, 2.5, 2.5, 1, 2.5, 1])
        # ===============
        self.LC.initRows(db.all())
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
        self.LC.AdaptWidth(6, proportions=[0.5, 2.5, 2.5, 1, 2.5, 1])
        self.LC.SetClientSize(self.GetClientSize())
