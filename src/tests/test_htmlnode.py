import unittest
from nodes.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_handle_None_props(self):
        htmlnode = HTMLNode(None, None, None, None)
        self.assertEqual(htmlnode.props_to_html(), "")

    def test_to_html_should_raise(self):
        htmlnode = HTMLNode(None, None, None, None)

        self.assertRaises(NotImplementedError, htmlnode.to_html)

    def test_repr(self):

        htmlnode = HTMLNode(None, None, None, {"href": "https://google.com"})
        self.assertEqual(
            "HTMLNode(tag=None, value=None, children=None, props={'href': 'https://google.com'})",
            repr(htmlnode),
        )

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )
