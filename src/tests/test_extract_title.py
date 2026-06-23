import unittest

from markdown.parser import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        result = extract_title("# Hello")

        self.assertEqual(result, "Hello")

    def test_title_with_multiple_words(self):
        result = extract_title("# My Blog Post")

        self.assertEqual(result, "My Blog Post")

    def test_no_header_raises(self):
        def call():
            return extract_title("plain paragraph text")

        self.assertRaises(Exception, call)

    def test_wrong_level_h2_raises(self):
        def call():
            return extract_title("## Subheader")

        self.assertRaises(Exception, call)

    def test_wrong_level_h3_raises(self):
        def call():
            return extract_title("### Section")

        self.assertRaises(Exception, call)

    def test_hash_without_space_raises(self):
        def call():
            return extract_title("#NoSpace")

        self.assertRaises(Exception, call)

    def test_empty_string_raises(self):
        def call():
            return extract_title("")

        self.assertRaises(Exception, call)

    def test_only_hash_raises(self):
        def call():
            return extract_title("#")

        self.assertRaises(Exception, call)

    def test_title_only_space_after_hash(self):
        def call():
            return extract_title("# ")

        self.assertRaises(Exception, call)

    def test_title_with_inline_markdown(self):
        result = extract_title("# Hello **world**")

        self.assertEqual(result, "Hello **world**")

    def test_multiline_returns_only_first_line(self):
        result = extract_title("# Title\nSome body text")

        self.assertEqual(result, "Title")

    def test_title_with_leading_space_before_hash_raises(self):
        def call():
            return extract_title(" # Indented")

        self.assertRaises(Exception, call)

    def test_title_with_numbers(self):
        result = extract_title("# Chapter 1")

        self.assertEqual(result, "Chapter 1")

    def test_title_with_special_characters(self):
        result = extract_title("# Hello, World!")

        self.assertEqual(result, "Hello, World!")

    def test_title_with_trailing_whitespace(self):
        result = extract_title("# Title   ")

        self.assertEqual(result, "Title")
