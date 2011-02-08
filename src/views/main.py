from controllers.main import MainController
from views.resize_manager import ResizeManager
from views.text_node import TextNode
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
        
        self._resize_manager = ResizeManager(self.main_panel)
        #self.main_panel.Bind(wx.EVT_MOTION, self._resize_manager.OnMouseMotion)
        
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.main_panel, 1, wx.EXPAND)
        
        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)
        self.Layout()
    
    def OnMainPanelClick(self, event):
        xpos, ypos = event.GetPositionTuple()
        if not TextNode.IsOverlapping((xpos, ypos), self.main_panel):
            TextNode(self._controller, self._resize_manager, self.main_panel, pos=(xpos, ypos))

app = wx.App(redirect=False)
top = MainWindow()
top.Show()
app.MainLoop()