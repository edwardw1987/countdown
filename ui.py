# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-22 13:20:16
# @Last Modified by:   edward
# @Last Modified time: 2016-07-22 13:54:33
from util import Default
import wx

MATCHES = {
    True, False, None
}

METHODS = {
    'SetIcon', 'Show', 'Center'
}
class Frame(wx.Frame, Default):
    def __init__(self, *args, **kwargs):
        super(Frame, self).__init__(*args, **kwargs)
        self.set_default_result(
            matches=MATCHES,
            methods=METHODS,
        )