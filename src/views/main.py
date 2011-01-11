import wx

class MainWindow(wx.Frame):
    """
    Main GUI window
    """

    def __init__(self):
        super(MainWindow, self).__init__(None, title="Notetastic")
        
        self.main_text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.main_text_ctrl, 1, wx.EXPAND)
        
        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)
        self.Layout()
        
app = wx.App(redirect=False)
top = MainWindow()
top.Show()
app.MainLoop()
