# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-22 14:35:41
# @Last Modified by:   edward
# @Last Modified time: 2016-07-26 23:12:29
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
class MenuItem(After, wx.MenuItem):
    pass

class ListCtrl(After, wx.ListCtrl):
    def DoAfterInit(self):
        self._threadPool = {}
        self._cache = []
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onLeftDClick)
        self.Bind(EVT_COUNT, self.OnCount)

    def getThread(self, pos):
        eid = self.GetEid(pos)
        return self._threadPool.get(eid)
    def setThread(self, pos, thread):
        eid = self.GetEid(pos)
        self._threadPool[eid] = thread

    def _initThreadPool(self, data):
        new = dict.fromkeys([i.eid for i in data], 0)
        self._threadPool.update(new)

    def OnCount(self, evt):
        pos, s = evt.GetValue()
        thd = self.getThread(pos)
        self.SetStringItem(pos, 3, '%d s' % s)
        if s == 30:
            fr = self.GetParent()
            fr.clock.Play()
            fr.Restore()
        elif s == 0: # finish thread task
            self.toggleUI(pos)
        else:
            if thd.stopped():
                fr.clock.Stop()
   
    def AddRows(self, data_list):
        for row in data_list:
            pos = self.InsertStringItem(self.GetItemCount(), str(row.eid))
            # add values in the other columns on the same row
            self.SetStringItem(pos, 1, row['boss'])
            self.SetStringItem(pos, 2, '0000-00-00 00:00:00')
            self.SetStringItem(pos, 3, '0 s')
            self.SetStringItem(pos, 4, str(row['refresh']) + ' min')
            self.SetStringItem(pos, 5, u'已停止')
        self.addCache(data_list)

    initRows = AddRows

    def addCache(self, rows):
        self._cache.extend(rows)
        self._initThreadPool(rows)

    def GetRefresh(self, pos):
        return self._cache[pos]['refresh']

    @property
    def allStopped(self):
        thds = self._threadPool.values()
        if any(thds):
            for thd in thds:
                if thd != 0 and not thd.stopped():
                    return False
        return True

    @property
    def allStarted(self):
        thds = self._threadPool.values()
        if all(thds):
            for thd in thds:
                if thd.stopped():
                    break
            else:
                return True

        return False

    def getThreadState(self, pos):
        # 0 no thread
        # 0 Stopped
        # 1 Running
        eid = self.GetEid(pos)
        thd = self._threadPool.get(eid)
        if thd != 0:
            return 0 if thd.stopped() else 1
        return thd

    def GetEid(self, pos):
        return self._cache[pos].eid

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
        self.OnToggle(e)

    def onRightClick(self, e):
        print 'onRightClick'
        self._pos = e.GetIndex()
        state = self.getThreadState(self._pos)
        data = {
            'rightClick': [
                # (u'修改', 'mod', 0, self.OnMod),
                MenuItem(text=u'启动', id=-1, kind=0, handler=self.OnToggle, enable=state == 0 and self._pos >= 0)\
                if state == 0 else \
                MenuItem(text=u'停止', id=-1, kind=0, handler=self.OnToggle, enable=state == 1 and self._pos >= 0),
                -1,
                MenuItem(text=u'全部启动', id=-1, kind=0, handler=self.OnStartAll, enable=not self.allStarted),
                MenuItem(text=u'全部停止', id=-1, kind=0, handler=self.OnStopAll, enable=not self.allStopped),
                -1,
                MenuItem(text=u'删除', id=-1, kind=0, handler=self.OnDel, enable=self._pos >= 0 and state == 0),
            ]
        }
        for m, title in create_menu(self.GetParent(), data):
            self.PopupMenu(m)
            break

    def cleanThreadOnClose(self):
        for thd in self._threadPool.values():
            if thd and not thd.stopped():
                thd.stop()

    def cleanByPos(self, pos):
        e = self._cache.pop(pos)
        thd = self._threadPool.pop(e.eid, None)
        if thd and not thd.stopped(): thd.stop()
        db.delete([e.eid])

    def DeleteItem(self, pos):
        self.cleanByPos(pos)
        super(ListCtrl, self).DeleteItem(pos)

    def OnDel(self, e):
        self.DeleteItem(self._pos)

    def OnMod(self, e):
        print 'OnMod'

    def toggleThread(self, pos):
        state = self.getThreadState(pos)
        if state in (None, 0):
            ref = self.GetRefresh(pos)
            worker = CountingThread(self, (ref, pos))
            worker.start()
            self.setThread(pos, worker)
            # print 'start'
        elif state == 1:
            thread = self.getThread(pos)
            if thread is not None and not thread.stopped():
                thread.stop()
                self.SetStringItem(pos, 3, '0 s')
                # print 'stop'

    def toggleUI(self, pos):
        state = self.getThreadState(pos)
        self.SetStringItem(
            pos, 5, u'已启动' if state else u'已停止')
        self.SetStringItem(
            pos, 2, datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S') if state else u'0000-00-00 00:00:00')
        ref = self.GetRefresh(pos)
        self.SetStringItem(
            pos, 4, datetime.strftime(datetime.now() + timedelta(seconds=60 * ref), '%Y-%m-%d %H:%M:%S') if state else '%d min' % ref)

    def OnToggle(self, e):
        self.toggleThread(self._pos)
        self.toggleUI(self._pos)

    def OnStartAll(self, e):
        self._toggleAll(state=1)

    def OnStopAll(self, e):
        self._toggleAll(state=0)

    def _toggleAll(self, state=1):
        for i in range(self.GetItemCount()):
            if self.getThreadState(i) == state: # em
                continue
            self.toggleThread(i)
            self.toggleUI(i)

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
        self.Bind(wx.EVT_CLOSE, self.OnClose)
    def _initListCtrl(self):
        self.LC = ListCtrl(self,
                           style=wx.LC_REPORT,
                           headings=['ID', u'BOSS名称',
                                     u'死亡时间', u'倒计时', u'刷新时间', u'状态'],
                           # columnFormat=wx.LIST_FORMAT_CENTER,
                           fgcolor='#f40',

                           )
        # ===============
        # w = h = 16
        # il = wx.ImageList(w, h)
        # il.Add(wx.Bitmap('rat_head16.ico', wx.BITMAP_TYPE_ICO))
        # self.LC.AssignImageList(il, wx.IMAGE_LIST_SMALL)
        # ===============
        self.LC.AdaptWidth(6, proportions=[0.5, 2.5, 2.5, 1, 2.5, 1])
        # ===============
        self.LC.initRows(db.all())
        # 0 will insert at the start of the list

    def _initMenuBar(self):
        _OD = OrderedDict()

        _OD[u'操作(&O)'] = [
            MenuItem(text=u'添加倒计时\tCtrl+N', id=-1, kind=0, handler=self.OnAdd),
            -1,
            MenuItem(text=u'退出\tCtrl+Q', id=-1, kind=0, handler=self.OnQuit),
        ]
        _OD[u'查看(&V)'] = [
            MenuItem(text=u'窗口置顶', id=-1, kind=1, handler=self.OnSwitchTop),
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
        dlg.Center()
        dlg.ShowModal()

    def OnSwitchTop(self, e):
        if e.IsChecked():
            self.SetWindowStyle(self.GetWindowStyle() | wx.STAY_ON_TOP)
        else:
            self.SetWindowStyle(self.GetWindowStyle() ^ wx.STAY_ON_TOP)

    def OnResize(self, e):
        self.LC.AdaptWidth(6, proportions=[0.5, 2.5, 2.5, 1, 2.5, 1])
        self.LC.SetClientSize(self.GetClientSize())

    def OnClose(self, e):
        self.LC.cleanThreadOnClose()
        self.Destroy()
    OnQuit = OnClose