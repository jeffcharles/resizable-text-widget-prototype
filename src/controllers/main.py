from models.text_note import TextNote 

class MainController:
    
    def __init__(self):
        self._text_note = TextNote()
    
    def text_changed(self, new_text):
        self._text_note.text = new_text