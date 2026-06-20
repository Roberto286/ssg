import unittest

from functions import split_nodes_image, split_nodes_link
from nodes.textnode import TextNode, TextType


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode("![alt](https://img.com/a.png)", TextType.TEXT)
        result = split_nodes_image([node])

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0], TextNode("alt", TextType.IMAGE, "https://img.com/a.png")
        )

    def test_image_surrounded_by_text(self):
        node = TextNode("before ![alt](https://img.com/a.png) after", TextType.TEXT)
        result = split_nodes_image([node])

        self.assertEqual(result[0], TextNode("before ", TextType.TEXT))
        self.assertEqual(
            result[1], TextNode("alt", TextType.IMAGE, "https://img.com/a.png")
        )
        self.assertEqual(result[2], TextNode(" after", TextType.TEXT))

    def test_image_at_start(self):
        node = TextNode("![alt](https://img.com/a.png) after", TextType.TEXT)
        result = split_nodes_image([node])

        self.assertEqual(
            result[0], TextNode("alt", TextType.IMAGE, "https://img.com/a.png")
        )

    def test_image_at_end(self):
        node = TextNode("before ![alt](https://img.com/a.png)", TextType.TEXT)
        result = split_nodes_image([node])

        self.assertEqual(result[0], TextNode("before ", TextType.TEXT))
        self.assertEqual(
            result[1], TextNode("alt", TextType.IMAGE, "https://img.com/a.png")
        )

    def test_multiple_images(self):
        node = TextNode("![a](https://a.com) and ![b](https://b.com)", TextType.TEXT)
        result = split_nodes_image([node])

        self.assertEqual(result[0], TextNode("a", TextType.IMAGE, "https://a.com"))
        self.assertEqual(result[1], TextNode(" and ", TextType.TEXT))
        self.assertEqual(result[2], TextNode("b", TextType.IMAGE, "https://b.com"))

    def test_no_images(self):
        node = TextNode("plain text no images", TextType.TEXT)
        result = split_nodes_image([node])

        self.assertEqual(result, [node])

    def test_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_image([node])

        self.assertEqual(result, [node])

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("![a](https://a.com)", TextType.TEXT),
            TextNode("plain", TextType.TEXT),
        ]
        result = split_nodes_image(nodes)

        self.assertEqual(result[0], TextNode("a", TextType.IMAGE, "https://a.com"))
        self.assertEqual(result[1], TextNode("plain", TextType.TEXT))

    def test_image_url_stored_on_node(self):
        node = TextNode("![cat](https://cat.com/cat.jpg)", TextType.TEXT)
        result = split_nodes_image([node])

        self.assertEqual(result[0].url, "https://cat.com/cat.jpg")

    def test_adjacent_images_no_empty_text_nodes(self):
        node = TextNode("![a](https://a.com)![b](https://b.com)", TextType.TEXT)
        result = split_nodes_image([node])

        self.assertEqual(result[0], TextNode("a", TextType.IMAGE, "https://a.com"))
        self.assertEqual(result[1], TextNode("b", TextType.IMAGE, "https://b.com"))


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode("[boot dev](https://www.boot.dev)", TextType.TEXT)
        result = split_nodes_link([node])

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0],
            TextNode(
                text="boot dev", url="https://www.boot.dev", text_type=TextType.LINK
            ),
        )

    def test_link_surrounded_by_text(self):
        node = TextNode("go to [boot dev](https://www.boot.dev) now", TextType.TEXT)
        result = split_nodes_link([node])

        self.assertEqual(result[0], TextNode(text="go to ", text_type=TextType.TEXT))
        self.assertEqual(
            result[1],
            TextNode(
                text="boot dev", url="https://www.boot.dev", text_type=TextType.LINK
            ),
        )
        self.assertEqual(result[2], TextNode(text=" now", text_type=TextType.TEXT))

    def test_link_at_start(self):
        node = TextNode("[boot dev](https://www.boot.dev) is great", TextType.TEXT)
        result = split_nodes_link([node])

        self.assertEqual(
            result[0], TextNode("boot dev", TextType.LINK, "https://www.boot.dev")
        )

    def test_link_at_end(self):
        node = TextNode("visit [boot dev](https://www.boot.dev)", TextType.TEXT)
        result = split_nodes_link([node])

        self.assertEqual(result[0], TextNode("visit ", TextType.TEXT))
        self.assertEqual(
            result[1], TextNode("boot dev", TextType.LINK, "https://www.boot.dev")
        )

    def test_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])

        self.assertEqual(
            result[0], TextNode("This is text with a link ", TextType.TEXT)
        )
        self.assertEqual(
            result[1], TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
        )
        self.assertEqual(result[2], TextNode(" and ", TextType.TEXT))
        self.assertEqual(
            result[3],
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        )

    def test_no_links(self):
        node = TextNode("plain text no links", TextType.TEXT)
        result = split_nodes_link([node])

        self.assertEqual(result, [node])

    def test_non_text_node_unchanged(self):
        node = TextNode("already italic", TextType.ITALIC)
        result = split_nodes_link([node])

        self.assertEqual(result, [node])

    def test_image_syntax_not_treated_as_link(self):
        node = TextNode("![img](https://img.com/a.png)", TextType.TEXT)
        result = split_nodes_link([node])

        self.assertEqual(result, [node])

    def test_link_url_stored_on_node(self):
        node = TextNode("[click](https://example.com)", TextType.TEXT)
        result = split_nodes_link([node])

        self.assertEqual(result[0].url, "https://example.com")

    def test_adjacent_links_no_empty_text_nodes(self):
        node = TextNode("[a](https://a.com)[b](https://b.com)", TextType.TEXT)
        result = split_nodes_link([node])

        self.assertEqual(result[0], TextNode("a", TextType.LINK, "https://a.com"))
        self.assertEqual(result[1], TextNode("b", TextType.LINK, "https://b.com"))

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("[a](https://a.com)", TextType.TEXT),
            TextNode("plain", TextType.TEXT),
        ]
        result = split_nodes_link(nodes)

        self.assertEqual(result[0], TextNode("a", TextType.LINK, "https://a.com"))
        self.assertEqual(result[1], TextNode("plain", TextType.TEXT))
