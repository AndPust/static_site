from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("value not declared in LeafNode declaration")
        
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value is None")
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}" + self.props_to_html() + f">{self.value}</{self.tag}>"
            
