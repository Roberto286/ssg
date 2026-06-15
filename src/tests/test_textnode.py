import unittest

from nodes.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is different", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_url_is_None_by_default(self):
        node = TextNode("This is a text node", TextType.LINK)

        self.assertEqual(node.url, None)

    def test_if_text_type_is_instance_of_text_type_class(self):
        node = TextNode("This is a link node", TextType.LINK, "https://google.com")

        self.assertIsInstance(node.text_type, TextType)


if __name__ == "__main__":
    _ = unittest.main()
