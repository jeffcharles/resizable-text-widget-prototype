'''
Created on 2011-01-11

@author: jeff
'''

class TextNote(object):

    def __init__(self, text=''):
        self._text = text
    
    def _get_text(self):
        return self._text
    def _set_text(self, value):
        self._text = value
    def _del_text(self):
        self._text = ''
    text = property(_get_text, _set_text, _del_text)