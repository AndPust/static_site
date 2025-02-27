
class TextNode(object):

    def __init__(self, text="", text_type="", url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, second):
        return self.text == second.text and self.text_type == second.text_type and self.url == second.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

