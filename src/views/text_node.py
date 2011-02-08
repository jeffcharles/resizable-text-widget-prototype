import wx

class OverlapException(Exception):
    pass

class TextNode(wx.Panel):

    MARGIN = 5
        
    INITIAL_WIDTH = 200
    INITIAL_HEIGHT = 50
    
    def __init__(self, controller, resize_manager, parent, pos):
        # Check that there are no siblings where the panel will be initialized first
        if self.IsOverlapping(pos, parent):
            raise OverlapException("The last text node if created would have overlapped another node")
                    
        super(TextNode, self).__init__(parent, pos=pos, size=wx.Size(self.INITIAL_WIDTH, self.INITIAL_HEIGHT))
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
        
    @classmethod
    def IsOverlapping(self, pos, parent):
        """
        Returns whether or not a text node created at pos with parent parent will overlap another node
        """
        for sibling in parent.GetChildren():
            node_left, node_top = pos
            node_left -= self.MARGIN
            node_top -= self.MARGIN
            node_right = node_left + self.INITIAL_WIDTH + 2 * self.MARGIN
            node_bottom = node_top + self.INITIAL_HEIGHT + 2 * self.MARGIN
            '''
Created on 2011-02-08

@author: jeff
'''
            sibling_left, sibling_top = sibling.GetPositionTuple()
            sibling_left -= self.MARGIN
            sibling_top -= self.MARGIN
            sibling_width, sibling_height = sibling.GetSizeTuple()
            sibling_right = sibling_left + sibling_width + 2 * self.MARGIN
            sibling_bottom = sibling_top + sibling_height + 2 * self.MARGIN
            
            horizontal_overlap = False if node_right < sibling_left or node_left > sibling_right else True
            vertical_overlap = False if node_bottom < sibling_top or node_top > sibling_bottom else True
            
            if horizontal_overlap and vertical_overlap:
                return True
        return False
    
    def OnTextChanged(self, event):
        self._controller.text_changed(self._text_note, event.GetEventObject().Value)