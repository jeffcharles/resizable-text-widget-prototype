from views.text_node import TextNode
import wx

class ResizeManager(object):
    
    _NO_CHANGE = 0
    _CHANGE_W_OFFSET = 1
    _CHANGE_WO_OFFSET = 2
    
    def __init__(self, top_panel):
        self.top_panel = top_panel
        self.selected_element = None
        
        self._cursor = None
        self._left = None
        self._right = None
        self._top = None
        self._bottom = None
        
        self._RESIZABLE_CONTROLS = (TextNode,)
    
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
            
    def _GetDimensionChanges(self):
        """
        Returns a tuple of integers indicating whether the width or height should change.
        """
        width_change = (
                             self._CHANGE_W_OFFSET if self._left 
                        else self._CHANGE_WO_OFFSET if self._right 
                        else self._NO_CHANGE
                       )
        height_change = (
                              self._CHANGE_W_OFFSET if self._top 
                         else self._CHANGE_WO_OFFSET if self._bottom 
                         else self._NO_CHANGE
                        )
        return width_change, height_change
    
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
    
    def _GetNewPositions(self, old_xpos, old_ypos, mouse_pos_x, mouse_pos_y):
        """
        Returns the new x and y positions given the mouse cursor position.
        """ 
        xpos_change, ypos_change = self._GetPositionChanges()
        new_xpos = old_xpos + mouse_pos_x if xpos_change else old_xpos
        new_ypos = old_ypos + mouse_pos_y if ypos_change else old_ypos
        return new_xpos, new_ypos
    
    def _GetPositionChanges(self):
        """
        Returns a tuple of booleans indicating whether the x or y positions should change.
        """
        xpos_change = self._left
        ypos_change = self._top
        return xpos_change, ypos_change
    
    def _OnMouseDrag(self, event):
        # Determine selected element
        if self.selected_element is None:
            self.selected_element = event.GetEventObject()
        
        # Make sure selected element is resizable
        if type(self.selected_element) not in self._RESIZABLE_CONTROLS:
            self.selected_element = None
            return
        
        # Establish a mouse position
        if [self._left, self._right, self._top, self._bottom] == [None, None, None, None]:
            self._left, self._right, self._top, self._bottom = \
                self._GetMousePositions(event.GetPositionTuple(), self.selected_element.GetSizeTuple())
            
        # If there is at least one mouse position
        if True in [self._left, self._right, self._top, self._bottom]:
            self._OnResize(event)
    
    def OnMouseMotion(self, event):
        # Update mouse cursor
        if type(event.GetEventObject()) in self._RESIZABLE_CONTROLS:
            if self._cursor is None: 
                self._ChangeMouseCursor(event)
            event.GetEventObject().SetCursor(wx.StockCursor(self._cursor))
        
        # Reset if not dragging
        if not event.Dragging():
            self.selected_element = None
            self._cursor = None
            self._left = None
            self._right = None
            self._top = None
            self._bottom = None
            return
        
        self._OnMouseDrag(event)
        
    def _OnResize(self, event):
        # Get current x and y positions as well as current width and height
        old_xpos, old_ypos = self.selected_element.GetPositionTuple()
        old_width, old_height = self.selected_element.GetSize()

        
        width_change, height_change = self._GetDimensionChanges()
        
        new_xpos, new_ypos = self._GetNewPositions(old_xpos, old_ypos, event.GetX(), event.GetY())
        new_width = (old_width - event.GetX() if width_change == self._CHANGE_W_OFFSET 
                            else event.GetX() if width_change == self._CHANGE_WO_OFFSET
                            else old_width)
        new_height = (old_height - event.GetY() if height_change == self._CHANGE_W_OFFSET
                              else event.GetY() if height_change == self._CHANGE_WO_OFFSET 
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
            sibling_left_border -= sibling.MARGIN
            sibling_top_border -= sibling.MARGIN
            sibling_width, sibling_height = sibling.GetSizeTuple()
            sibling_right_border = sibling_left_border + sibling_width + 2 * sibling.MARGIN
            sibling_bottom_border = sibling_top_border + sibling_height + 2 * sibling.MARGIN
            
            old_node_left_border = old_xpos - self.selected_element.MARGIN
            old_node_top_border = old_ypos - self.selected_element.MARGIN
            old_node_width = old_width
            old_node_height = old_height
            old_node_right_border = old_node_left_border + old_node_width + 2 * self.selected_element.MARGIN
            old_node_bottom_border = old_node_top_border + old_node_height + 2 * self.selected_element.MARGIN
            
            new_node_left_border = new_xpos - self.selected_element.MARGIN
            new_node_top_border = new_ypos - self.selected_element.MARGIN
            new_node_width = new_width
            new_node_height = new_height
            new_node_right_border = new_node_left_border + new_node_width + 2 * self.selected_element.MARGIN
            new_node_bottom_border = new_node_top_border + new_node_height + 2 * self.selected_element.MARGIN
            
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
        
        new_node_left = new_xpos - self.selected_element.MARGIN
        new_node_top = new_ypos - self.selected_element.MARGIN
        new_node_width = new_width
        new_node_height = new_height
        new_node_right = new_node_left + new_width + 2 * self.selected_element.MARGIN
        new_node_bottom = new_node_top + new_height + 2 * self.selected_element.MARGIN
        
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
        