from leafnode import LeafNode
from textnode import TextNode
import re

def text_node_to_html_node(text_node):
    def text_type_text():
        return LeafNode(value=text_node.text)
    def text_type_bold():
        return LeafNode(tag="b", value=text_node.text)
    def text_type_italic():
        return LeafNode(tag="i", value=text_node.text)
    def text_type_code():
        return LeafNode(tag="code", value=text_node.text)
    def text_type_link():
        return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
    def text_type_image():
        return LeafNode(tag="img", value="", props={"src":text_node.url, "alt":text_node.text})
    def default():
        raise RuntimeError("Not known TextNode type")

    switch = {
        "text":text_type_text,
        "bold":text_type_bold,
        "italic":text_type_italic,
        "code":text_type_code,
        "link":text_type_link,
        "image":text_type_image,
    }

    return switch.get(text_node.text_type, default)()

# Assume you check for bold markdown first and then for italics
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if len(old_nodes) == 0:
        return []

    l = []

    for n in old_nodes:
        if n.text_type not in ["text", "bold", "italic"]\
           or (n.text_type == "bold" and text_type!="italic")\
           or (n.text_type == "italic" and text_type!="bold")\
           or delimiter not in n.text:
            l.append(n)
            continue

        if len(n.text.split(delimiter)) % 2 != 1:
            raise RuntimeError("Uneven number of delimiters found in text node")

        tt = [n.text_type, text_type]
        splits = n.text.split(delimiter)
        for idx, s in enumerate(splits):
            if len(s) == 0:
                continue
            l.append(TextNode(s, tt[idx%2], n.url))

    return l

IMAGES_REGEX = r"\!\[([^\[\]]*)\]\(([^\(\)]*)\)"

LINKS_REGEX = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

def extract_markdown_images(text):
    found = re.findall(IMAGES_REGEX, text)
    return found
        

def extract_markdown_links(text):
    found = re.findall(LINKS_REGEX, text)
    return found
        
def split_nodes_link(text):
    if len(text) == 0:
        return []
    
    if len(extract_markdown_links("   ".join([t.text for t in text]))) == 0:
        return text

    l = []

    for n in text:
        if len(extract_markdown_links(n.text)) == 0:
            l.append(n)
            continue

        found = extract_markdown_links(n.text)
        t = n.text

        for f in found:
            # "(?<!!) [ ([^\[\]]*) ]( ([^\(\)]*) )"
            splitter = f"[{f[0]}]({f[1]})"
            split = t.split(splitter)

            # print("splitter: " + f"![{f[0]}]({f[1]})")
            # print("splat:")
            # print(split)

            if len(split[0]) > 0:
                l.append(TextNode(split[0], n.text_type, n.url))
            l.append(TextNode(text=f[0], text_type="link", url=f[1]))

            if len(split) == 2:
                t = split[1]
            else:
                t = splitter.join(split[1:])

        if len(t) > 0:
            l.append(TextNode(t, n.text_type, n.url))

    return l

def split_nodes_image(text):
    if len(text) == 0:
        return []
    
    if len(extract_markdown_images("   ".join([t.text for t in text]))) == 0:
        return text

    l = []

    for n in text:
        if len(extract_markdown_images(n.text)) == 0:
            l.append(n)
            continue

        found = extract_markdown_images(n.text)
        t = n.text

        for f in found:
            # "![ ([^\[\]]*) ]( ([^\(\)]*) )"
            splitter = f"![{f[0]}]({f[1]})"
            split = t.split(splitter)

            if len(split[0]) > 0:
                l.append(TextNode(split[0], n.text_type, n.url))
            l.append(TextNode(text=f[0], text_type="image", url=f[1]))

            if len(split) == 2:
                t = split[1]
            else:
                t = splitter.join(split[1:])

        if len(t) > 0:
            l.append(TextNode(t, n.text_type, n.url))

    return l

def text_to_textnodes(text):
    # print(text)
    nodes = [TextNode(text=text, text_type="text")]

    # print(nodes)

    nodes = split_nodes_image(nodes)
    # print(nodes)
    nodes = split_nodes_link(nodes)
    # print(nodes)

    nodes = split_nodes_delimiter(nodes, "**", "bold")
    # print(nodes)
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    # print(nodes)
    nodes = split_nodes_delimiter(nodes, "`", "code")

    # print(nodes)

    return nodes
