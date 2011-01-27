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
        
        self._resize_manager = ResizeManager(self.main_panel)
        #self.main_panel.Bind(wx.EVT_MOTION, self._resize_manager.OnMouseMotion)
        
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.main_panel, 1, wx.EXPAND)
        
        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)
        self.Layout()
    
    def OnMainPanelClick(self, event):
        xpos, ypos = event.GetPositionTuple()
        self._controller.create_text_note(xpos, ypos)
        TextNode(self._controller, self._resize_manager, self.main_panel, pos=(xpos, ypos))

class ResizeManager(object):
    
    def __init__(self, top_panel):
        self.top_panel = top_panel
        self.selected_element = None
        self.resize_in_progress = False
        
        self._prev_xpos = None
        self._prev_ypos = None
        self._left = None
        self._right = None
        self._top = None
        self._bottom = None
    
    def OnMouseMotion(self, event):
        if not event.Dragging():
            self.selected_element = None
            self.resize_in_progress = False
            self._left = None
            self._right = None
            self._up = None
            self._down = None
        else:
            if self.selected_element is None:
                self.selected_element = event.GetEventObject()
            
            if [self._left, self._right, self._up, self._down] == [None, None, None, None]:
                xpos, ypos = event.GetPositionTuple()
                p_width, p_height = self.selected_element.GetSizeTuple()
        
                self._left = 0 < xpos <= 5
                self._right = 0 < (p_width - xpos) <= 5
                self._top = 0 < ypos <= 5
                self._bottom = 0 < (p_height - ypos) <= 5
            
            if True in [self._left, self._right, self._up, self._down]:
                old_xpos, old_ypos = self.selected_element.GetPositionTuple()
                old_width, old_height = self.selected_element.GetSize()
            
            if self._top and self._left:
                new_xpos = event.GetX() + old_xpos
                new_ypos = event.GetY() + old_ypos
                new_width = old_width + (old_xpos - new_xpos)
                new_height = old_height + (old_ypos - new_ypos)
            elif self._top and self._right:
                new_xpos = old_xpos
                new_ypos = event.GetY() + old_ypos
                new_width = event.GetX()
                new_height = old_height + (old_ypos - new_ypos)
            elif self._bottom and self._left:
                new_xpos = event.GetX() + old_xpos
                new_ypos = old_ypos
                new_width = old_width + (old_xpos - new_xpos)
                new_height = event.GetY()
            elif self._bottom and self._right:
                new_xpos = old_xpos
                new_ypos = old_ypos
                new_width = event.GetX()
                new_height = event.GetY()
            
            if True in [self._left, self._right, self._up, self._down]:
                self.selected_element.Move(wx.Point(new_xpos, new_ypos))
                self.selected_element.SetSize(wx.Size(new_width, new_height))

class TextNode(wx.Panel):
    
    def __init__(self, controller, resize_manager, parent, pos):
        super(TextNode, self).__init__(parent, pos=pos, size=wx.Size(200, 50))
        self._controller = controller
        xpos, ypos = pos
        self._text_note = self._controller.create_text_note(xpos, ypos)
        
        self._resize_manager = resize_manager
        
        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.text_ctrl.Bind(wx.EVT_TEXT, self.OnTextChanged)
        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.text_ctrl, 1, wx.ALL|wx.EXPAND, 5)
        
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_MOTION, self._resize_manager.OnMouseMotion)
        
        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)
        self.Layout()
    
    def OnMouseMotion(self, event):
        xpos, ypos = event.GetPositionTuple()
        p_width, p_height = self.GetSizeTuple()

        cursor_left = 0 < xpos <= 5
        cursor_right = 0 < (p_width - xpos) <= 5
        cursor_top = 0 < ypos <= 5
        cursor_bottom = 0 < (p_height - ypos) <= 5
        
        if cursor_left and cursor_top:
            cursor = wx.CURSOR_SIZENWSE
        elif cursor_right and cursor_top:
            cursor = wx.CURSOR_SIZENESW
        elif cursor_left and cursor_bottom:
            cursor = wx.CURSOR_SIZENESW
        elif cursor_right and cursor_bottom:
            cursor = wx.CURSOR_SIZENWSE
        elif cursor_left:
            cursor = wx.CURSOR_SIZEWE
        elif cursor_right:
            cursor = wx.CURSOR_SIZEWE
        elif cursor_top:
            cursor = wx.CURSOR_SIZENS
        elif cursor_bottom:
            cursor = wx.CURSOR_SIZENS
        else:
            cursor = wx.CURSOR_ARROW
        self.SetCursor(wx.StockCursor(cursor))
        
    def OnTextChanged(self, event):
        self._controller.text_changed(self._text_note, event.GetEventObject().Value)

app = wx.App(redirect=False)
top = MainWindow()
top.Show()
app.MainLoop()
