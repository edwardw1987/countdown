# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-21 12:19:52
# @Last Modified by:   edward
# @Last Modified time: 2016-07-21 12:19:54
import wx
import Library

class TestFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, id=-1, name=u'TestFrame',
              parent = None, pos=wx.Point(480, 275), size=wx.Size(1280, 733),
              style=wx.DEFAULT_FRAME_STYLE, title=u'Menu testing program')
        self.SetClientSize(wx.Size(1280, 733))
        self.CreateStatusBar()
        menuData=Library.readXML("menu.xml")
        Library.createMenus(self,menuData,self)

    def OnOpen(self,event):
        wx.MessageBox("You selected the open menu item")

    def OnSave(self,event):
        wx.MessageBox("You selected the save menu item")

    def OnClose(self,event):
        wx.MessageBox("You selected the close menu item")

    def OnExit(self,event):
        wx.MessageBox("You selected the exit menu item")
        self.Close()

    def OnFind(self,event):
        wx.MessageBox("You selected the find menu item")

    def OnReplace(self,event):
        wx.MessageBox("You selected the replace menu item")
        self.Close()

    def OnOthers1(self,event):
        wx.MessageBox("You selected the others1 menu item")

    def OnSubmenu1(self,event):
        wx.MessageBox("You selected the submenu item 1")

    def OnSubmenu2(self,event):
        wx.MessageBox("You selected the submenu item 2")

    def OnSubmenu3(self,event):
        wx.MessageBox("You selected the submenu item 3")

    def OnCheck1(self,event):
        wx.MessageBox("You checked item 1")

    def OnCheck2(self,event):
        wx.MessageBox("You checked item 2")

    def OnCheck3(self,event):
        wx.MessageBox("You checked item 3")

    def OnRadio1(self,event):
        wx.MessageBox("You selected radio item 1")

    def OnRadio2(self,event):
        wx.MessageBox("You selected radio item 2")

    def OnRadio3(self,event):
        wx.MessageBox("You selected radio item 3")