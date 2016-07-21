import wx
import TestFrame2
import Library

modules ={u'Library': [0, '', u'Library.py'], u'TestFrame2': [0, '', u'TestFrame2.py']}

class TestApp(wx.App):
    def OnInit(self):
        self.main = TestFrame2.TestFrame(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = TestApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()