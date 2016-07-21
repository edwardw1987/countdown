# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-21 12:18:09
# @Last Modified by:   edward
# @Last Modified time: 2016-07-21 12:18:31
#this section is the main routine code
import wx
import xml.sax.handler
import sys

def readXML(xmlfile):
    file=open(xmlfile,'r')
    fixedData= file.read()
    file.close()
    return fixedData.replace( "&", "&amp;" )


def createMenus(self,menuData,frame):

    class MenuBuilder(xml.sax.handler.ContentHandler):
        def __init__(self):
            self.menuStack = []
            self.text=""
            self.menu=""
            self.itemName=""
            self.type=""
            self.handler=""
            self.help=""
            self.helpStack={}
            self.item=""
            self.nameStack=[]

        def startElement(self, name, attrs):
            self.text=""
            if name=="menuItem":
                self.type=""
                self.help=""
            elif name=="menubar":
                menuBar=wx.MenuBar()
                self.menuStack.append((menuBar,"bar"))
            elif name=="menuName":
                self.menu=""
            elif name=="itemName":
                self.itemName=""
            elif name=="kind":
                self.type=""
            elif name=="handler":
                self.handler=""
            elif name=="help":
                self.help=""
            elif name=="menu":
                pass
            elif name=="separator":
                pass
            else:
                raise ValueError, "Invalid menu component %s" % name

        def endElement(self, name):
            if name=="menuItem":
                try:
                    self.help=self.helpStack[self.itemName]
                    del self.helpStack[self.itemName]
                except:
                    self.help=""
                if self.type=="" or self.type=="normal":
                    self.item=self.menuStack[-1][0].Append(id=wx.NewId(), text=self.itemName, help=self.help)
                elif self.type=="check":
                    self.item=self.menuStack[-1][0].AppendCheckItem(id=wx.NewId(), text=self.itemName, help=self.help)
                elif self.type=="radio":
                    self.item=self.menuStack[-1][0].AppendRadioItem(id=wx.NewId(), text=self.itemName, help=self.help)
                else:
                    raise ValueError, "Unknown item type %s" % self.type
                frame.Bind(wx.EVT_MENU,self.handler,self.item)
            elif name=="menu":
                if self.menuStack[-2][1]=="bar":
                    self.menuStack[-2][0].Append(menu=self.menuStack[-1][0],title=self.menuStack[-1][1])
                else:
                    try:
                        self.help=self.helpStack[self.menuStack[-1][1]]
                        del self.helpStack[self.menuStack[-1][1]]
                    except:
                        self.help=""
                    self.menuStack[-2][0].AppendSubMenu(submenu=self.menuStack[-1][0],text=self.menuStack[-1][1],help=self.help)
                self.menuStack.pop()
            elif name=="separator":
                self.menuStack[-1][0].AppendSeparator()
            elif name=="menubar":
                frame.SetMenuBar(self.menuStack[-1][0])
            elif name=="menuName":
                self.menu=wx.Menu()
                self.menuStack.append((self.menu,self.text))
                self.nameStack.append(self.text)
            elif name=="itemName":
                self.itemName=self.text
                self.nameStack.append(self.text)
            elif name=="kind":
                self.type=self.text
            elif name=="handler":
                self.handler=getattr(frame,self.text)
            elif name=="help":
                self.help=self.text
                self.helpStack[self.nameStack[-1]]=self.help
                self.nameStack.pop()
            else:
                raise ValueError, "Invalid menu component %s" % name

        def characters(self, content):
            self.text+=content

    builder = MenuBuilder()
    xml.sax.parseString(menuData, builder)