import unittest
from functions import split_nodes_delimiter
from nodes.textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_basic(self):
        node = TextNode("This has a `code` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        # verifica:
        # testo normale prima
        # testo code in mezzo
        # testo normale dopo

    def test_split_bold_basic(self):
        node = TextNode("This has **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        # verifica che "bold" abbia TextType.BOLD

    def test_split_italic_basic(self):
        node = TextNode("This has _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        # verifica che "italic" abbia TextType.ITALIC

    def test_multiple_delimited_sections(self):
        node = TextNode("A `one` and `two` example", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        # verifica che "one" e "two" siano CODE
        # e che il testo tra/fuori sia TEXT

    def test_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        # verifica che il nodo rimanga uguale, senza essere splittato

    def test_unclosed_delimiter_raises(self):
        node = TextNode("This has an `unclosed code block", TextType.TEXT)

        # verifica che venga sollevata un'eccezione

    def test_delimiter_at_start(self):
        node = TextNode("`code` then text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        # verifica che non crei nodi vuoti inutili
        # e che "code" sia CODE

    def test_delimiter_at_end(self):
        node = TextNode("text then `code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        # verifica testo normale prima + code alla fine
