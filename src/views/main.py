from controllers.main import MainController
import wx

class MainWindow(wx.Frame):
    """
    Main GUI window
    """

    def __init__(self):
        super(MainWindow, self).__init__(None, title="Notetastic")
        
        self._controller = MainController()
        
        self.main_text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.main_text_ctrl.Bind(wx.EVT_TEXT, self.OnTextChanged)
        
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.main_text_ctrl, 1, wx.EXPAND)
        
        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)
        self.Layout()
    
    def OnTextChanged(self, event):
        self._controller.text_changed(self.main_text_ctrl.Value)
        
app = wx.App(redirect=False)
top = MainWindow()
top.Show()
app.MainLoop()
