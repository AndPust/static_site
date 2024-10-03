import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_default_values(self):
        node = HTMLNode(value = "value")

        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "value")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
    
    def test_both_value_and_children_none(self):
        err = None
        try:
            node = HTMLNode()
        except ValueError as e:
            err = e
        self.assertEqual(type(err), ValueError)
    
    def test_props_to_html(self):
        p = {
            "href": "https://www.google.com", 
            "target": "_blank",
            }
        
        node = HTMLNode(value = "value", props = p)

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_repr(self):

        s = (
            "tag: None\n"
            "value: value\n"
            "children: None\n"
            "props: {'href': 'https://www.google.com', 'target': '_blank'}"
            )
        
        p = {
            "href": "https://www.google.com", 
            "target": "_blank",
            }

        node = HTMLNode(value = "value", props = p)
        
        self.assertEqual(s, str(node))

if __name__ == "__main__":
    unittest.main()


