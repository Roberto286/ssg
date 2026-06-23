import unittest

from markdown.converter import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraph(self):
        node = markdown_to_html_node("Hello world")
        self.assertEqual(node.to_html(), "<div><p>Hello world</p></div>")

    def test_paragraph_multiline_joins_with_space(self):
        node = markdown_to_html_node("line one\nline two")
        self.assertEqual(node.to_html(), "<div><p>line one line two</p></div>")

    def test_paragraph_inline_bold(self):
        node = markdown_to_html_node("This is **bold** text")
        self.assertEqual(node.to_html(), "<div><p>This is <b>bold</b> text</p></div>")

    def test_heading_h1(self):
        node = markdown_to_html_node("# Title")
        self.assertEqual(node.to_html(), "<div><h1>Title</h1></div>")

    def test_heading_h2(self):
        node = markdown_to_html_node("## Subtitle")
        self.assertEqual(node.to_html(), "<div><h2>Subtitle</h2></div>")

    def test_heading_h6(self):
        node = markdown_to_html_node("###### Deep")
        self.assertEqual(node.to_html(), "<div><h6>Deep</h6></div>")

    def test_heading_with_inline_bold(self):
        node = markdown_to_html_node("# Hello **world**")
        self.assertEqual(node.to_html(), "<div><h1>Hello <b>world</b></h1></div>")

    def test_code_block(self):
        node = markdown_to_html_node("```\nprint('hi')\n```")
        self.assertEqual(node.to_html(), "<div><pre><code>print('hi')</code></pre></div>")

    def test_code_block_no_inline_parsing(self):
        node = markdown_to_html_node("```\n**not bold**\n```")
        self.assertEqual(node.to_html(), "<div><pre><code>**not bold**</code></pre></div>")

    def test_quote(self):
        node = markdown_to_html_node("> This is a quote")
        self.assertEqual(node.to_html(), "<div><blockquote>This is a quote</blockquote></div>")

    def test_quote_multiline(self):
        node = markdown_to_html_node("> line one\n> line two")
        self.assertEqual(node.to_html(), "<div><blockquote>line one line two</blockquote></div>")

    def test_unordered_list(self):
        node = markdown_to_html_node("- item one\n- item two")
        self.assertEqual(node.to_html(), "<div><ul><li>item one</li><li>item two</li></ul></div>")

    def test_unordered_list_inline_bold(self):
        node = markdown_to_html_node("- **bold** item")
        self.assertEqual(node.to_html(), "<div><ul><li><b>bold</b> item</li></ul></div>")

    def test_ordered_list(self):
        node = markdown_to_html_node("1. first\n2. second\n3. third")
        self.assertEqual(node.to_html(), "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>")

    def test_ordered_list_inline(self):
        node = markdown_to_html_node("1. **bold** first")
        self.assertEqual(node.to_html(), "<div><ol><li><b>bold</b> first</li></ol></div>")

    def test_multiple_blocks(self):
        md = "# Heading\n\nA paragraph.\n\n- item"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading</h1><p>A paragraph.</p><ul><li>item</li></ul></div>",
        )

    def test_returns_div_wrapper(self):
        node = markdown_to_html_node("hello")
        self.assertEqual(node.tag, "div")


if __name__ == "__main__":
    unittest.main()
