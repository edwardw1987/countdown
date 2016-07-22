import wx
from util import set_default_result
import ui

class App(wx.App):
    def OnInit(self):
        ui.Frame(None, title="RatHead CountDown").SetIcon(wx.Icon('rat_head.ico')) .Show().Center()
        return True     

def main():
    app = App()
    app.MainLoop()
if __name__ == '__main__':
    main()