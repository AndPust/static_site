import unittest

from leafnode import LeafNode
from textnode import TextNode
from transformers import text_node_to_html_node, split_nodes_delimiter, \
                         extract_markdown_images, extract_markdown_links, \
                         split_nodes_image, split_nodes_link, text_to_textnodes

class TestTransformFunction(unittest.TestCase):
    def test_bad_tag(self):
        node = TextNode(text="abcd", text_type="bubla")

        err = ""
        try:
            text_node_to_html_node(node)
        except RuntimeError as e:
            err = e

        self.assertEqual(type(err), RuntimeError)
        self.assertEqual(str(err), "Not known TextNode type")

    def test_plain_text(self):
        node = TextNode(text="Jam Tech Scrooge", text_type="text", url=123123123)

        self.assertEqual(text_node_to_html_node(node), LeafNode(value="Jam Tech Scrooge"))
        self.assertEqual(text_node_to_html_node(node).to_html(), "Jam Tech Scrooge")


    def test_bold(self):
        node = TextNode(text="Jam Tech Scrooge", text_type="bold", url=123123123)

        self.assertEqual(text_node_to_html_node(node), LeafNode(tag="b", value="Jam Tech Scrooge"))
        self.assertEqual(text_node_to_html_node(node).to_html(), "<b>Jam Tech Scrooge</b>")


    def test_italic(self):
        node = TextNode(text="Jam Tech Scrooge", text_type="italic", url=123123123)

        self.assertEqual(text_node_to_html_node(node), LeafNode(tag="i", value="Jam Tech Scrooge"))
        self.assertEqual(text_node_to_html_node(node).to_html(), "<i>Jam Tech Scrooge</i>")

    def test_code(self):
        node = TextNode(text="Jam Tech Scrooge", text_type="code", url=123123123)

        self.assertEqual(text_node_to_html_node(node), LeafNode(tag="code", value="Jam Tech Scrooge"))
        self.assertEqual(text_node_to_html_node(node).to_html(), "<code>Jam Tech Scrooge</code>")

    def test_link(self):
        node = TextNode(text="Jam Tech Scrooge", text_type="link", url="tarnow.pl")

        self.assertEqual(text_node_to_html_node(node), LeafNode(tag="a", value="Jam Tech Scrooge", props={"href": "tarnow.pl"}))
        self.assertEqual(text_node_to_html_node(node).to_html(), '<a href="tarnow.pl">Jam Tech Scrooge</a>')

    def test_image(self):
        node = TextNode(text="Jam Tech Scrooge", text_type="image", url="https://www.agh.edu.pl")

        self.assertEqual(text_node_to_html_node(node), LeafNode(tag="img", value="", props={"src":"https://www.agh.edu.pl", "alt":"Jam Tech Scrooge"}))
        self.assertEqual(text_node_to_html_node(node).to_html(), '<img src="https://www.agh.edu.pl" alt="Jam Tech Scrooge"></img>')

    def test_split_no_nodes(self):
        self.assertEqual(split_nodes_delimiter([], "delimiter", "tag"), [])

    def test_split_no_delimiter(self):
        node = TextNode(text="AAAA", text_type="text", url="https://www.agh.edu.pl")

        self.assertEqual(split_nodes_delimiter([node], "delimiter", "tag"), [node])

    def test_multiple_nodes_split_no_delimiter(self):
        node = TextNode(text="AAAA", text_type="text", url="https://www.agh.edu.pl")

        self.assertEqual(split_nodes_delimiter([node, node, node], "delimiter", "tag"), [node, node, node])

    def test_split_uneven_delimiters(self):
        node = TextNode(text="AAAAdelimiterBBBBdelimiterCCCCdelimiter", text_type="text", url="https://www.agh.edu.pl")

        err = ""
        try:
            l = split_nodes_delimiter([node], "delimiter", "tag")
        except RuntimeError as e:
            err = e

        self.assertEqual(str(err), "Uneven number of delimiters found in text node")

    def test_split_delimiters_at_edge_front(self):
        node = TextNode(text="delimiterBBBBdelimiterCCCC", text_type="text", url="https://www.agh.edu.pl")

        l = split_nodes_delimiter([node], "delimiter", "tag")

        check = [
            TextNode("BBBB", "tag", "https://www.agh.edu.pl"),
            TextNode("CCCC", "text", "https://www.agh.edu.pl")
        ]
        
        self.assertEqual(l, check)


    def test_split_delimiters_at_edge_back(self):
        node = TextNode(text="AAAAdelimiterBBBBdelimiter", text_type="text", url="https://www.agh.edu.pl")

        l = split_nodes_delimiter([node], "delimiter", "tag")

        check = [
            TextNode("AAAA", "text", "https://www.agh.edu.pl"),
            TextNode("BBBB", "tag", "https://www.agh.edu.pl")
        ]
        
        self.assertEqual(l, check)


    def test_split_delimiters_at_edge_both(self):
        node = TextNode(text="delimiterBBBBdelimiter", text_type="text", url="https://www.agh.edu.pl")

        l = split_nodes_delimiter([node], "delimiter", "tag")

        check = [
            TextNode("BBBB", "tag", "https://www.agh.edu.pl")
        ]
        
        self.assertEqual(l, check)

    def test_split_one_node_one_delimiter(self):
        node = TextNode(text="AAAAxkdcBBBBxkdcCCCC", text_type="text", url="https://www.agh.edu.pl")

        l = split_nodes_delimiter([node], "xkdc", "type2")

        check = [
            TextNode(text="AAAA", text_type="text", url="https://www.agh.edu.pl"),
            TextNode(text="BBBB", text_type="type2", url="https://www.agh.edu.pl"),
            TextNode(text="CCCC", text_type="text", url="https://www.agh.edu.pl")
        ]

        self.assertEqual(l, check)

    def test_split_three_nodes_one_delimiter(self):
        node = TextNode(text="AAAAxkdcBBBBxkdcCCCC", text_type="text", url="https://www.agh.edu.pl")

        l = split_nodes_delimiter([node, node, node], "xkdc", "type2")

        check = [
            TextNode(text="AAAA", text_type="text", url="https://www.agh.edu.pl"),
            TextNode(text="BBBB", text_type="type2", url="https://www.agh.edu.pl"),
            TextNode(text="CCCC", text_type="text", url="https://www.agh.edu.pl"),
            TextNode(text="AAAA", text_type="text", url="https://www.agh.edu.pl"),
            TextNode(text="BBBB", text_type="type2", url="https://www.agh.edu.pl"),
            TextNode(text="CCCC", text_type="text", url="https://www.agh.edu.pl"),
            TextNode(text="AAAA", text_type="text", url="https://www.agh.edu.pl"),
            TextNode(text="BBBB", text_type="type2", url="https://www.agh.edu.pl"),
            TextNode(text="CCCC", text_type="text", url="https://www.agh.edu.pl")
        ]

        self.assertEqual(l, check)

    def test_split_bold_in_italics(self):
        node = TextNode(text="AAAA**BBBB**CCCC", text_type="italic", url="https://www.agh.edu.pl")

        l = split_nodes_delimiter([node], "**", "bold")

        check = [
            TextNode(text="AAAA", text_type="italic", url="https://www.agh.edu.pl"),
            TextNode(text="BBBB", text_type="bold", url="https://www.agh.edu.pl"),
            TextNode(text="CCCC", text_type="italic", url="https://www.agh.edu.pl")
        ]

        self.assertEqual(l, check)

    def test_split_italic_in_bold(self):
        node = TextNode(text="AAAA*BBBB*CCCC", text_type="bold", url="https://www.agh.edu.pl")

        l = split_nodes_delimiter([node], "*", "italic")

        check = [
            TextNode(text="AAAA", text_type="bold", url="https://www.agh.edu.pl"),
            TextNode(text="BBBB", text_type="italic", url="https://www.agh.edu.pl"),
            TextNode(text="CCCC", text_type="bold", url="https://www.agh.edu.pl")
        ]

        self.assertEqual(l, check)
    
    def test_markdown_images_no_images(self):

        self.assertEqual(extract_markdown_images("No images or anything in here"), [])
    
        
    def test_markdown_images_one_image(self):

        self.assertEqual(extract_markdown_images("Here be image: ![AGH](https://www.agh.edu.pl)"), [("AGH", "https://www.agh.edu.pl")])
        
    def test_markdown_images_three_images(self):
        text = "Here be image: ![AGH](https://www.agh.edu.pl), and another!: ![one Two three!](tarnow.pl)"

        self.assertEqual(extract_markdown_images(text), [("AGH", "https://www.agh.edu.pl"), ("one Two three!", "tarnow.pl")])
        
    def test_markdown_links(self):

        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
    
    def test_split_nodes_links(self):
        text_type_text = "text"
        text_type_link = "link"
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        check = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode(
                "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
            ),
        ]

        self.assertEqual(new_nodes, check)
    
    def test_text_to_textnodes(self):
        text_type_text = "text"
        text_type_link = "link"
        text_type_bold = "bold"
        text_type_italic = "italic"
        text_type_image = "image"
        text_type_code = "code"
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        nodes = text_to_textnodes(text)

        check = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]

        self.assertEqual(nodes, check)

if __name__ == "__main__":
    unittest.main()


