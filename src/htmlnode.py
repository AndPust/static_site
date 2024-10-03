import copy

class HTMLNode(object):
    def __init__(self, tag=None, value=None, children=None, props=None):
        if value is None and children is None:
            raise ValueError("Both value and children are None")

        self.tag = tag
        self.value = value

        if children is None:
            self.children = children 
        else:
            self.children = [x for x in children]

        if props is None:
            self.props = props 
        else:
            self.props = copy.deepcopy(props)
    
    def __repr__(self):
        s = "tag: " + str(self.tag) + "\n"
        s += "value: " + str(self.value) + "\n"
        s += "children: " + str(self.children) + "\n"
        s += "props: " + str(self.props)

        return s

    def __eq__(self, second):
        return self.tag == second.tag and self.value == second.value and self.children == second.children and self.props == second.props
    
    def to_html(self):
        raise NotImplementedError("HTML render not implemented in this class")

    def props_to_html(self):
        s = ""

        if not self.props:
            return s

        for k in self.props:
            s += " " + str(k) + "=" + '"' + str(self.props[k]) + '"'
        
        return s

