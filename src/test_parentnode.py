import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_default_values(self):
        node = ParentNode(tag="p", children = [LeafNode(value="Simple text")])

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [LeafNode(value="Simple text")])
        self.assertEqual(node.props, None)
    
    def test_children_not_set(self):
        err = None
        try:
            node = ParentNode()
        except ValueError as e:
            err = e
        self.assertEqual(type(err), ValueError)
        self.assertEqual("children not declared" in str(err), True)

    def test_tag_not_set(self):
        err = None
        try:
            node = ParentNode(children = [LeafNode(value="value")])
        except ValueError as e:
            err = e
        self.assertEqual(type(err), ValueError)
        self.assertEqual("tag not declared" in str(err), True)
    
    def test_to_html_children_set_to_none(self):
        err = None

        node = ParentNode(tag="p", children=[LeafNode(value="value")])
        node.children = []

        try:
            node.to_html()
        except ValueError as e:
            err = e

        self.assertEqual(type(err), ValueError)
        self.assertEqual("no children" in str(err), True)
    
    def test_to_html_tag_set_to_none(self):
        err = None

        node = ParentNode(tag="p", children=[LeafNode(value="value")])
        node.tag = ""

        try:
            node.to_html()
        except ValueError as e:
            err = e

        self.assertEqual(type(err), ValueError)
        self.assertEqual("tag is None or" in str(err), True)
    
    def test_props_to_html(self):
        p = {
            "href": "https://www.google.com", 
            "target": "_blank",
            }
        
        node = ParentNode(tag="p", children=[LeafNode(value="value")], props = p)

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_to_html(self):
        p = {
            "href": "https://www.google.com", 
            "target": "_blank",
            }
        
        node = ParentNode(tag="p", children=[LeafNode(value="Simple text")], props = p)

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        self.assertEqual(node.to_html(), '<p href="https://www.google.com" target="_blank">Simple text</p>')
    
    def test_to_html_no_tag_no_props(self):
        p = {
            "href": "https://www.google.com", 
            "target": "_blank",
            }
        
        node = ParentNode(tag="p", children=[LeafNode(value="Simple text")])

        self.assertEqual(node.props_to_html(), '')
        self.assertEqual(node.to_html(), '<p>Simple text</p>')
    
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        s = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        self.assertEqual(node.to_html(), s)
    
    def test_to_html_recursive(self):
        p = {
            "href": "https://www.google.com", 
            "target": "_blank",
            }

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                ParentNode("p", [LeafNode("i", "italic text"), LeafNode("X", "xitalic text", {"bah": 123})], p),
                LeafNode(None, "Normal text"),
            ],
        )

        s = '<p><b>Bold text</b>Normal text<i>italic text</i><p href="https://www.google.com" target="_blank"><i>italic text</i><X bah="123">xitalic text</X></p>Normal text</p>'

        self.assertEqual(node.to_html(), s)

    def test_repr(self):

        s = (
            "tag: p\n"
            "value: None\n"
            "children: [tag: None\n"
            "value: Simple text\n"
            "children: None\n"
            "props: None]\n"
            "props: {'href': 'https://www.google.com', 'target': '_blank'}"
            )
        
        p = {
            "href": "https://www.google.com", 
            "target": "_blank",
            }

        node = ParentNode(tag="p", children=[LeafNode(value="Simple text")], props=p)
        
        self.assertEqual(s, str(node))

if __name__ == "__main__":
    unittest.main()


