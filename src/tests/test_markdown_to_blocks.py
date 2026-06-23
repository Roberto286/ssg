import unittest

from markdown.parser import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_block(self):
        blocks = markdown_to_blocks("just one paragraph")

        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0], "just one paragraph")

    def test_empty_string(self):
        blocks = markdown_to_blocks("")

        self.assertEqual(blocks, [])

    def test_only_whitespace(self):
        blocks = markdown_to_blocks("   \n\n   \n\n   ")

        self.assertEqual(blocks, [])

    def test_leading_trailing_whitespace_stripped(self):
        blocks = markdown_to_blocks("  hello  \n\n  world  ")

        self.assertEqual(blocks[0], "hello")
        self.assertEqual(blocks[1], "world")

    def test_multiple_blank_lines_between_blocks(self):
        blocks = markdown_to_blocks("block one\n\n\n\nblock two")

        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "block one")
        self.assertEqual(blocks[1], "block two")

    def test_single_newline_stays_in_block(self):
        blocks = markdown_to_blocks("line one\nline two\n\nblock two")

        self.assertEqual(blocks[0], "line one\nline two")
        self.assertEqual(blocks[1], "block two")

    def test_three_blocks(self):
        blocks = markdown_to_blocks("a\n\nb\n\nc")

        self.assertEqual(blocks[0], "a")
        self.assertEqual(blocks[1], "b")
        self.assertEqual(blocks[2], "c")

    def test_block_with_markdown_inline(self):
        blocks = markdown_to_blocks("**bold** text\n\n`code` here")

        self.assertEqual(blocks[0], "**bold** text")
        self.assertEqual(blocks[1], "`code` here")
