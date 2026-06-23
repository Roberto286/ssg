import unittest

from markdown.parser import (
    block_to_block_type,
    extract_markdown_images,
    extract_markdown_links,
)
from enums.block_type import BlockType


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "![alt](https://example.com/img.png)"
        self.assertEqual(
            extract_markdown_images(text), [("alt", "https://example.com/img.png")]
        )

    def test_multiple_images(self):
        text = "![a](https://a.com) and ![b](https://b.com)"
        self.assertEqual(
            extract_markdown_images(text),
            [("a", "https://a.com"), ("b", "https://b.com")],
        )

    def test_no_images(self):
        self.assertEqual(extract_markdown_images("no images here"), [])

    def test_ignores_plain_links(self):
        self.assertEqual(extract_markdown_images("[link](https://example.com)"), [])

    def test_empty_alt(self):
        self.assertEqual(
            extract_markdown_images("![](https://example.com)"),
            [("", "https://example.com")],
        )

    def test_mixed_images_and_links(self):
        text = "![img](https://img.com) and [link](https://link.com)"
        self.assertEqual(extract_markdown_images(text), [("img", "https://img.com")])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "[click here](https://example.com)"
        self.assertEqual(
            extract_markdown_links(text), [("click here", "https://example.com")]
        )

    def test_multiple_links(self):
        text = "[a](https://a.com) and [b](https://b.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("a", "https://a.com"), ("b", "https://b.com")],
        )

    def test_no_links(self):
        self.assertEqual(extract_markdown_links("no links here"), [])

    def test_ignores_images(self):
        self.assertEqual(extract_markdown_links("![img](https://img.com)"), [])

    def test_mixed_images_and_links(self):
        text = "![img](https://img.com) and [link](https://link.com)"
        self.assertEqual(extract_markdown_links(text), [("link", "https://link.com")])

    def test_empty_anchor_text(self):
        self.assertEqual(
            extract_markdown_links("[](https://example.com)"),
            [("", "https://example.com")],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_single(self):
        text = "# Hello"

        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_heading_multiple_hashes(self):
        text = "## Subheading"

        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_heading_no_space(self):
        text = "#NoSpace"

        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_code_block(self):
        text = "```python\ncode\n```"

        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_code_block_unclosed(self):
        text = "```"

        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_quote(self):
        text = "> quoted text"

        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_quote_empty(self):
        text = ">"

        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_unordered_list(self):
        # "- item" → UNORDERED_LIST
        text = "- item"

        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_unordered_list_no_space(self):
        # "-item" → PARAGRAPH (delimiter requires "- " with space)
        text = "-item"

        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_ordered_list_single_digit(self):
        # "1. first item" → ORDERED_LIST
        text = "1. first item"

        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)

    def test_ordered_list_multi_digit(self):
        # "10. tenth item" → ORDERED_LIST (\d+ matches multiple digits)
        text = "10. tenth item"

        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)

    def test_ordered_list_no_space(self):
        # "1.item" → PARAGRAPH (regex requires digit(s) + ". " with space)
        text = "1.item"

        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_ordered_list_letter_prefix(self):
        # "a. item" → PARAGRAPH (letter prefix doesn't match \d+)
        text = "a. item"

        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_paragraph_plain(self):
        # "plain text" → PARAGRAPH (no special prefix)
        text = "plain text"

        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_paragraph_empty(self):
        # "" → PARAGRAPH (empty string matches no prefix)
        text = ""

        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
