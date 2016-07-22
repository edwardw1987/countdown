# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-22 12:30:24
# @Last Modified by:   edward
# @Last Modified time: 2016-07-22 16:59:40
import wx


def result(matches=[], default=None):
    def _decoractor(f):
        def fn(*args, **kwds):
            r = f(*args, **kwds)
            return  default if r in matches else r
        return fn
    return _decoractor

def set_default_result(instance, matches, methods):
    default_result = result(matches=matches, default=instance)
    for n in methods:
        raw_method = getattr(instance, n)
        setattr(instance, n, default_result(raw_method))

def create_menubar(frame, data):
    mb = wx.MenuBar()
    # create menu
    for title, items in data.items():
        m = wx.Menu()
        mb.Append(m, title)
        d = {}
        for label, name, act, ehandler in items:
            mi = None
            if act == 0:
                mi = m.Append(
                    -1,
                    text=label,
                )
            elif act == 1: #check
                pass
            elif act == 2: #radio
                pass
            elif act == 3: #seprator
                m.AppendSeparator()
            if mi is not None:
                frame.Bind(wx.EVT_MENU, ehandler, mi)
    return mb, d

class Default:
    def set_default_result(self, *args, **kwds):
        return set_default_result(self, *args, **kwds)

class After(object):

    def __init__(self, *args, **kw):
        kw = self._popArgs(**kw)
        super(After, self).__init__(*args, **kw)
        self._doAfterInit()

    def _popArgs(self, **kw):
        _keys = {
            'icon',
        }
        for k in _keys:
            v = kw.pop(k, None)
            setattr(self, k, v)
        return kw

    def _doAfterInit(self):
        icon = getattr(self, 'icon', None)
        if icon: self.SetIcon(wx.Icon(icon))
        self.DoAfterInit()

    def DoAfterInit(self):
        pass

def main():
    default_result = result(matches=[None], default=1)
    class A:
        def greet(self, name):
            print 'Hello,%s!' % name
    a = A()
    print a.greet('Edward')
    for n in (i for i in dir(a) if not i.startswith('_')):
        raw_mth = getattr(a, n)
        setattr(a, n, default_result(raw_mth))
    print a.greet('Edward')
    
if __name__ == '__main__':
    main()
