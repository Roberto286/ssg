import unittest
from enums.text_type import TextType
from markdown.splitter import split_nodes_delimiter
from nodes.textnode import TextNode


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_basic(self):
        node = TextNode("This has a `code` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_split_bold_basic(self):
        node = TextNode("This has **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result[1].text_type, TextType.BOLD)

    def test_split_italic_basic(self):
        node = TextNode("This has _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result[1].text_type, TextType.ITALIC)

    def test_multiple_delimited_sections(self):
        node = TextNode("A `one` and `two` example", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        for i in range(len(result)):
            el = result[i]
            if i % 2 == 0:
                self.assertEqual(el.text_type, TextType.TEXT)
            else:
                self.assertEqual(el.text_type, TextType.CODE)

    def test_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(node, result[0])

    def test_unclosed_delimiter_raises(self):
        node = TextNode("This has an `unclosed code block", TextType.TEXT)

        def call():
            return split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertRaises(Exception, call)

    def test_delimiter_at_start(self):
        node = TextNode("`code` then text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        for res in result:
            if "code" in res.text:
                self.assertEqual(res.text_type, TextType.CODE)
            else:
                self.assertNotEqual(res.text, "")

    def test_delimiter_at_end(self):
        node = TextNode("text then `code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text_type, TextType.CODE)
