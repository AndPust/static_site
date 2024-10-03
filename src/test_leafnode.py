import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_default_values(self):
        node = LeafNode(value = "value")

        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "value")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
    
    def test_value_not_set(self):
        err = None
        try:
            node = LeafNode()
        except ValueError as e:
            err = e
        self.assertEqual(type(err), ValueError)
        self.assertEqual("declaration" in str(err), True)
    
    def test_to_html_value_set_to_none(self):
        err = None

        node = LeafNode(value = "val")
        node.value = None

        try:
            node.to_html()
        except ValueError as e:
            err = e

        self.assertEqual(type(err), ValueError)
        self.assertEqual("None" in str(err), True)

    # def test_to_html_value_set_to_empty_string(self):
    #     err = None

    #     node = LeafNode(value = "val")
    #     node.value = ""

    #     try:
    #         node.to_html()
    #     except ValueError as e:
    #         err = e

    #     self.assertEqual(type(err), ValueError)
    #     self.assertEqual("empty" in str(err), True)
    
    def test_props_to_html(self):
        p = {
            "href": "https://www.google.com", 
            "target": "_blank",
            }
        
        node = LeafNode(value = "value", props = p)

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_to_html(self):
        p = {
            "href": "https://www.google.com", 
            "target": "_blank",
            }
        
        node = LeafNode(tag = "a", value = "value", props = p)

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">value</a>')
    
    def test_to_html_no_tag_no_props(self):
        p = {
            "href": "https://www.google.com", 
            "target": "_blank",
            }
        
        node = LeafNode(value = "value")

        self.assertEqual(node.props_to_html(), '')
        self.assertEqual(node.to_html(), 'value')
    
    def test_to_html_no_tag(self):
        p = {
            "href": "https://www.google.com", 
            "target": "_blank",
            }
        
        node = LeafNode(value = "value", props = p)

        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        self.assertEqual(node.to_html(), 'value')

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

        node = LeafNode(value = "value", props = p)
        
        self.assertEqual(s, str(node))

if __name__ == "__main__":
    unittest.main()


