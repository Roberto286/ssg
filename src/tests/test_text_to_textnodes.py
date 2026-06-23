import unittest

from enums.text_type import TextType
from markdown.splitter import text_to_textnodes
from nodes.textnode import TextNode


class TestTextToTextnodes(unittest.TestCase):
    def test_plain_text(self):
        result = text_to_textnodes("just plain text")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], TextNode("just plain text", TextType.TEXT))

    def test_bold(self):
        result = text_to_textnodes("this is **bold** text")

        self.assertEqual(result[0], TextNode("this is ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(result[2], TextNode(" text", TextType.TEXT))

    def test_italic(self):
        result = text_to_textnodes("this is _italic_ text")

        self.assertEqual(result[0], TextNode("this is ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(result[2], TextNode(" text", TextType.TEXT))

    def test_code(self):
        result = text_to_textnodes("this is `code` text")

        self.assertEqual(result[0], TextNode("this is ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("code", TextType.CODE))
        self.assertEqual(result[2], TextNode(" text", TextType.TEXT))

    def test_image(self):
        result = text_to_textnodes("look ![alt](https://img.com/a.png) here")

        self.assertEqual(result[0], TextNode("look ", TextType.TEXT))
        self.assertEqual(
            result[1], TextNode("alt", TextType.IMAGE, "https://img.com/a.png")
        )
        self.assertEqual(result[2], TextNode(" here", TextType.TEXT))

    def test_link(self):
        result = text_to_textnodes("visit [boot dev](https://www.boot.dev) now")

        self.assertEqual(result[0], TextNode("visit ", TextType.TEXT))
        self.assertEqual(
            result[1], TextNode("boot dev", TextType.LINK, "https://www.boot.dev")
        )
        self.assertEqual(result[2], TextNode(" now", TextType.TEXT))

    def test_all_types_combined(self):
        result = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://example.com/image.png) and a [link](https://boot.dev)"
        )

        self.assertEqual(result[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("text", TextType.BOLD))
        self.assertEqual(result[2], TextNode(" with an ", TextType.TEXT))
        self.assertEqual(result[3], TextNode("italic", TextType.ITALIC))
        self.assertEqual(result[4], TextNode(" word and a ", TextType.TEXT))
        self.assertEqual(result[5], TextNode("code block", TextType.CODE))
        self.assertEqual(result[6], TextNode(" and an ", TextType.TEXT))
        self.assertEqual(
            result[7],
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
        )
        self.assertEqual(result[8], TextNode(" and a ", TextType.TEXT))
        self.assertEqual(
            result[9],
            TextNode("link", TextType.LINK, "https://boot.dev"),
        )

    def test_bold_and_code(self):
        result = text_to_textnodes("**bold** and `code`")

        self.assertEqual(result[0], TextNode("bold", TextType.BOLD))
        self.assertEqual(result[1], TextNode(" and ", TextType.TEXT))
        self.assertEqual(result[2], TextNode("code", TextType.CODE))

    def test_image_and_link(self):
        result = text_to_textnodes(
            "![img](https://img.com) and [link](https://link.com)"
        )

        self.assertEqual(result[0], TextNode("img", TextType.IMAGE, "https://img.com"))
        self.assertEqual(result[1], TextNode(" and ", TextType.TEXT))
        self.assertEqual(result[2], TextNode("link", TextType.LINK, "https://link.com"))

    def test_no_empty_text_nodes(self):
        result = text_to_textnodes("**bold**")

        self.assertEqual(result, [TextNode("bold", TextType.BOLD)])

    def test_multiple_bold(self):
        result = text_to_textnodes("**a** and **b**")

        self.assertEqual(result[0], TextNode("a", TextType.BOLD))
        self.assertEqual(result[1], TextNode(" and ", TextType.TEXT))
        self.assertEqual(result[2], TextNode("b", TextType.BOLD))

    def test_unclosed_delimiter_raises(self):
        def call():
            _ = text_to_textnodes("`not closed")

        self.assertRaises(Exception, call)
