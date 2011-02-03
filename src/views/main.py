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
        
        self._cursor = None
        self._left = None
        self._right = None
        self._top = None
        self._bottom = None
        
        self._RESIZABLE_CONTROLS = (TextNode,)
        self._MARGIN = 5
    
    def _ChangeMouseCursor(self, event):
        cursor_left, cursor_right, cursor_top, cursor_bottom = \
            self._GetMousePositions(event.GetPositionTuple(), event.GetEventObject().GetSizeTuple())

        if cursor_left and cursor_top:
            self._cursor = wx.CURSOR_SIZENWSE
        elif cursor_right and cursor_top:
            self._cursor = wx.CURSOR_SIZENESW
        elif cursor_left and cursor_bottom:
            self._cursor = wx.CURSOR_SIZENESW
        elif cursor_right and cursor_bottom:
            self._cursor = wx.CURSOR_SIZENWSE
        elif cursor_left:
            self._cursor = wx.CURSOR_SIZEWE
        elif cursor_right:
            self._cursor = wx.CURSOR_SIZEWE
        elif cursor_top:
            self._cursor = wx.CURSOR_SIZENS
        elif cursor_bottom:
            self._cursor = wx.CURSOR_SIZENS
        else:
            self._cursor = wx.CURSOR_ARROW
    
    def _GetMousePositions(self, event_pos, obj_size):
        """
        Returns a tuple of where the mouse is in relation to the event object.
        
        event_pos - a tuple of event positions by x and y coordinates (e.g., (3, 5))
        obj_size - a tuple of event object's width and height (e.g., (4, 5))
        
        Returns a tuple of mouse positions by left, right, top, and bottom
        """
        xpos, ypos = event_pos
        p_width, p_height = obj_size

        cursor_left = 0 < xpos <= 5
        cursor_right = 0 < (p_width - xpos) <= 5
        cursor_top = 0 < ypos <= 5
        cursor_bottom = 0 < (p_height - ypos) <= 5
        
        return (cursor_left, cursor_right, cursor_top, cursor_bottom)
    
    def OnMouseMotion(self, event):
        if type(event.GetEventObject()) in self._RESIZABLE_CONTROLS:
            if self._cursor is None: 
                self._ChangeMouseCursor(event)
            event.GetEventObject().SetCursor(wx.StockCursor(self._cursor))
        
        if not event.Dragging():
            self.selected_element = None
            self.resize_in_progress = False
            self._cursor = None
            self._left = None
            self._right = None
            self._top = None
            self._bottom = None
            return
        
        if self.selected_element is None:
            self.selected_element = event.GetEventObject()
        
        if type(self.selected_element) not in self._RESIZABLE_CONTROLS:
            self.selected_element = None
            return
        
        if [self._left, self._right, self._top, self._bottom] == [None, None, None, None]:
            self._left, self._right, self._top, self._bottom = \
                self._GetMousePositions(event.GetPositionTuple(), self.selected_element.GetSizeTuple())
            
        if True in [self._left, self._right, self._top, self._bottom]:
            old_xpos, old_ypos = self.selected_element.GetPositionTuple()
            old_width, old_height = self.selected_element.GetSize()
            
            NO_CHANGE = 0
            CHANGE_W_OFFSET = 1
            CHANGE_WO_OFFSET = 2
        
            if self._top and self._left:
                xpos_change = True
                ypos_change = True
                width_change = CHANGE_W_OFFSET
                height_change = CHANGE_W_OFFSET
            elif self._top and self._right:
                xpos_change = False
                ypos_change = True
                width_change = CHANGE_WO_OFFSET
                height_change = CHANGE_W_OFFSET
            elif self._bottom and self._left:
                xpos_change = True
                ypos_change = False
                width_change = CHANGE_W_OFFSET
                height_change = CHANGE_WO_OFFSET
            elif self._bottom and self._right:
                xpos_change = False
                ypos_change = False
                width_change = CHANGE_WO_OFFSET
                height_change = CHANGE_WO_OFFSET
            elif self._top:
                xpos_change = False
                ypos_change = True
                width_change = NO_CHANGE
                height_change = CHANGE_W_OFFSET
            elif self._bottom:
                xpos_change = False
                ypos_change = False
                width_change = NO_CHANGE
                height_change = CHANGE_WO_OFFSET
            elif self._left:
                xpos_change = True
                ypos_change = False
                width_change = CHANGE_W_OFFSET
                height_change = NO_CHANGE
            elif self._right:
                xpos_change = False
                ypos_change = False
                width_change = CHANGE_WO_OFFSET
                height_change = NO_CHANGE
            
            new_xpos = old_xpos + event.GetX() if xpos_change else old_xpos
            new_ypos = old_ypos + event.GetY() if ypos_change else old_ypos
            new_width = (old_width - event.GetX() if width_change == CHANGE_W_OFFSET 
                                else event.GetX() if width_change == CHANGE_WO_OFFSET
                                else old_width)
            new_height = (old_height - event.GetY() if height_change == CHANGE_W_OFFSET
                                  else event.GetY() if height_change == CHANGE_WO_OFFSET 
                                  else old_height)
            
            # Check that new width and height are greater or equal to the minimum width and height
            if new_width < self.selected_element.min_width:
                new_xpos = old_xpos
                new_width = self.selected_element.min_width
            if new_height < self.selected_element.min_height:
                new_ypos = old_ypos
                new_height = self.selected_element.min_height
                
            # Check that there is no overlap with other elements
            event_src = event.GetEventObject()
            if event_src is not self.selected_element and \
                event_src is not self.selected_element.GetParent() and \
                event_src not in self.selected_element.GetChildren():
                
                return
            
            siblings = self.selected_element.GetParent().GetChildren()
            for sibling in siblings:
                if sibling is self.selected_element:
                    continue
                
                sibling_left_border, sibling_top_border = sibling.GetPositionTuple()
                sibling_left_border -= self._MARGIN
                sibling_top_border -= self._MARGIN
                sibling_width, sibling_height = sibling.GetSizeTuple()
                sibling_right_border = sibling_left_border + sibling_width + 2 * self._MARGIN
                sibling_bottom_border = sibling_top_border + sibling_height + 2 * self._MARGIN
                
                old_node_left_border = old_xpos - self._MARGIN
                old_node_top_border = old_ypos - self._MARGIN
                old_node_width = old_width
                old_node_height = old_height
                old_node_right_border = old_node_left_border + old_node_width + 2 * self._MARGIN
                old_node_bottom_border = old_node_top_border + old_node_height + 2 * self._MARGIN
                
                new_node_left_border = new_xpos - self._MARGIN
                new_node_top_border = new_ypos - self._MARGIN
                new_node_width = new_width
                new_node_height = new_height
                new_node_right_border = new_node_left_border + new_node_width + 2 * self._MARGIN
                new_node_bottom_border = new_node_top_border + new_node_height + 2 * self._MARGIN
                
                old_horizontal_overlap = (
                    False if old_node_right_border < sibling_left_border or
                             old_node_left_border > sibling_right_border
                          else True
                )
                
                old_vertical_overlap = (
                    False if old_node_bottom_border < sibling_top_border or
                             old_node_top_border > sibling_bottom_border
                    else True
                )
                
                new_horizontal_overlap = (
                    False if new_node_right_border < sibling_left_border or 
                             new_node_left_border > sibling_right_border 
                          else True
                )
                new_vertical_overlap = (
                    False if new_node_bottom_border < sibling_top_border or 
                             new_node_top_border > sibling_bottom_border 
                    else True
                )
                
                if not old_horizontal_overlap and new_horizontal_overlap and new_vertical_overlap:
                    # Stop x or width changes
                    new_xpos = old_xpos
                    new_width = old_width
                if not old_vertical_overlap and new_vertical_overlap and new_horizontal_overlap:
                    # Stop y or height changes
                    new_ypos = old_ypos
                    new_height = old_height
                    
            # Check that element handles are not being dragged off of the parent panel
            parent = self.selected_element.GetParent()
            parent_left, parent_top = parent.GetPositionTuple()
            parent_width, parent_height = parent.GetSizeTuple()
            parent_right = parent_left + parent_width
            parent_bottom = parent_top + parent_height
            
            new_node_left = new_xpos - self._MARGIN
            new_node_top = new_ypos - self._MARGIN
            new_node_width = new_width
            new_node_height = new_height
            new_node_right = new_node_left + new_width + 2 * self._MARGIN
            new_node_bottom = new_node_top + new_height + 2 * self._MARGIN
            
            dragged_too_far_left = True if new_node_left < parent_left else False
            dragged_too_far_up = True if new_node_top < parent_top else False
            dragged_too_far_right = True if new_node_right > parent_right else False
            dragged_too_far_down = True if new_node_bottom > parent_bottom else False
            
            if dragged_too_far_left:
                new_xpos = old_xpos
                new_width = old_width
            if dragged_too_far_up:
                new_ypos = old_ypos
                new_height = old_height
            if dragged_too_far_right:
                new_width = old_width
            if dragged_too_far_down:
                new_height = old_height
                
            self.selected_element.Move(wx.Point(new_xpos, new_ypos))
            self.selected_element.SetSize(wx.Size(new_width, new_height))

class TextNode(wx.Panel):
    
    def __init__(self, controller, resize_manager, parent, pos):
        super(TextNode, self).__init__(parent, pos=pos, size=wx.Size(200, 50))
        self._controller = controller
        xpos, ypos = pos
        self._text_note = self._controller.create_text_note(xpos, ypos)
        
        self.min_width = 150
        self.min_height = 50
        self._resize_manager = resize_manager
        
        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.text_ctrl.Bind(wx.EVT_TEXT, self.OnTextChanged)
        self.text_ctrl.Bind(wx.EVT_MOTION, self._resize_manager.OnMouseMotion)
        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.text_ctrl, 1, wx.ALL|wx.EXPAND, 5)
        
        self.Bind(wx.EVT_MOTION, self._resize_manager.OnMouseMotion)
        
        self.SetAutoLayout(True)
        self.SetSizer(self.sizer)
        self.Layout()
    
    def OnTextChanged(self, event):
        self._controller.text_changed(self._text_note, event.GetEventObject().Value)

app = wx.App(redirect=False)
top = MainWindow()
top.Show()
app.MainLoop()
