from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if children is None or len(children) == 0:
            raise ValueError("children not declared in ParentNode declaration")
        if tag is None:
            raise ValueError("tag not declared in ParentNode declaration")
        
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("tag is None or an empty string")
        if len(self.children) == 0 or self.children is None:
            raise ValueError("no children while rendering to HTML")

        s = f"<{self.tag}" + self.props_to_html() + ">"

        for c in self.children:
            s += c.to_html()
        
        s += f"</{self.tag}>"

        return s