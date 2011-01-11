from controllers.main import MainController
import wx

class MainWindow(wx.Frame):
    """
    Main GUI window
    """

    def __init__(self):
        super(MainWindow, self).__init__(None, title="Notetastic")
        
        self._controller = MainController()
        
        self.main_panel = wx.Panel(self)
        self.main_panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.main_panel.Bind(wx.EVT_LEFT_DOWN, self.OnMainPanelClick)
        
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.main_panel, 1, wx.EXPAND)
        
        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)
        self.Layout()
    
    def OnMainPanelClick(self, event):
        xpos, ypos = event.GetPositionTuple()
        self._controller.create_text_note(xpos, ypos)
        
        text_node = TextNode(self.main_panel, pos=(xpos, ypos))
        text_node.Bind(wx.EVT_TEXT, self.OnTextChanged)
    
    def OnTextChanged(self, event):
        event.GetEventObject().OnTextChanged(event.GetEventObject().Value)

class TextNode(wx.TextCtrl):
    
    def __init__(self, parent, pos):
        super(TextNode, self).__init__(parent, pos=pos, style=wx.TE_MULTILINE)
        self._controller = MainController()
        xpos, ypos = pos
        self._text_note = self._controller.create_text_note(xpos, ypos)
    
    def OnTextChanged(self, new_text):
        self._controller.text_changed(self._text_note, new_text)

app = wx.App(redirect=False)
top = MainWindow()
top.Show()
app.MainLoop()
