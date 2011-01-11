from models.text_note import TextNote 

class MainController:
    
    def create_text_note(self, xpos, ypos):
        return TextNote(
            xpos=xpos, 
            ypos=ypos
        )
    
    def text_changed(self, text_note, new_text):
        text_note.text = new_text