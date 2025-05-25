import unittest

from htmlnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "loremsomethingsomething")
        node2 = HTMLNode("p", "loremsomethingsomething")
        node3 = HTMLNode("a", None, ["p","p"], {
                        "href": "https://www.google.com",
                        "target": "_blank",
        })

        self.assertEqual(node3.props_to_html(),  ' href="https://www.google.com" target="_blank"')
        self.assertEqual(node2.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("a", "Link to google", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Link to google</a>')
    


    


 

if __name__ == "__main__":
    unittest.main()