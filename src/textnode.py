from enum import Enum
from htmlnode import LeafNode
class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINKS = "links"
    IMAGES = "images"
class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def text_node_to_html_node(self):
        match self.text_type:
            case TextType.NORMAL_TEXT:
                return LeafNode(None,self.text,None)
            case TextType.BOLD_TEXT:
                return LeafNode("b", self.text, None)
            case TextType.ITALIC_TEXT:
                return LeafNode("i", self.text, None)
            case TextType.CODE_TEXT:
                return LeafNode("code", self.text, None)
            case TextType.LINKS:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMAGES:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise Exception

    def __eq__(self, value):
        return True if self.text == value.text and self.text_type == value.text_type and self.url == value.url else False
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
