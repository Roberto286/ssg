import unittest

from functions import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "![alt](https://example.com/img.png)"
        self.assertEqual(extract_markdown_images(text), [("alt", "https://example.com/img.png")])

    def test_multiple_images(self):
        text = "![a](https://a.com) and ![b](https://b.com)"
        self.assertEqual(extract_markdown_images(text), [("a", "https://a.com"), ("b", "https://b.com")])

    def test_no_images(self):
        self.assertEqual(extract_markdown_images("no images here"), [])

    def test_ignores_plain_links(self):
        self.assertEqual(extract_markdown_images("[link](https://example.com)"), [])

    def test_empty_alt(self):
        self.assertEqual(extract_markdown_images("![](https://example.com)"), [("", "https://example.com")])

    def test_mixed_images_and_links(self):
        text = "![img](https://img.com) and [link](https://link.com)"
        self.assertEqual(extract_markdown_images(text), [("img", "https://img.com")])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "[click here](https://example.com)"
        self.assertEqual(extract_markdown_links(text), [("click here", "https://example.com")])

    def test_multiple_links(self):
        text = "[a](https://a.com) and [b](https://b.com)"
        self.assertEqual(extract_markdown_links(text), [("a", "https://a.com"), ("b", "https://b.com")])

    def test_no_links(self):
        self.assertEqual(extract_markdown_links("no links here"), [])

    def test_ignores_images(self):
        self.assertEqual(extract_markdown_links("![img](https://img.com)"), [])

    def test_mixed_images_and_links(self):
        text = "![img](https://img.com) and [link](https://link.com)"
        self.assertEqual(extract_markdown_links(text), [("link", "https://link.com")])

    def test_empty_anchor_text(self):
        self.assertEqual(extract_markdown_links("[](https://example.com)"), [("", "https://example.com")])
