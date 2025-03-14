import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")

        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "tarnow.pl")

        self.assertEqual(str(node), f"TextNode(This is a text node, bold, tarnow.pl)")

    def test_default_values(self):
        node = TextNode()

        self.assertEqual(node.text, "")
        self.assertEqual(node.text_type, "")
        self.assertEqual(node.url, None)

    def test_not_default_type(self):
        node = TextNode()
        node2 = TextNode(text_type = "italic")

        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()


