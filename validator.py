# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-23 12:29:49
# @Last Modified by:   edward
# @Last Modified time: 2016-07-23 13:13:17
import wx


class NotEmptyValidator(wx.PyValidator):  # 创建验证器子类
    def __init__(self, message, level="Error", to_window_callback=None, from_window_callback=None):
        wx.PyValidator.__init__(self)
        self.message = message
        self.level = "Error"
        self.to_window_callback = to_window_callback
        self.from_window_callback = from_window_callback
    def Clone(self):
        """
        Note that every validator must implement the Clone() method.
        """
        return NotEmptyValidator(
            self.message,
            self.level,
            self.to_window_callback,
            self.from_window_callback,
            )

    def Validate(self, win):  # 1 使用验证器方法
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()
        if len(text) == 0:
            wx.MessageBox(self.message, self.level)
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour(
                wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
            return True

    def TransferToWindow(self):
        # raise
        if self.to_window_callback is not None:
            self.to_window_callback()
        return True

    def TransferFromWindow(self):
        if self.from_window_callback is not None:
            self.from_window_callback()
        return True
