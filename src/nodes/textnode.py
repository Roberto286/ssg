from dataclasses import dataclass
from enum import Enum

from nodes.leafnode import LeafNode


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    TEXT = "text"
    ITALIC = "italic"


@dataclass
class TextNode:
    text: str
    text_type: TextType
    url: str | None = None

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: "TextNode"):
    text_type = text_node.text_type

    if text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    if text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    if text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    if text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    if text_type == TextType.LINK:
        return LeafNode(
            tag="a", props={"href": text_node.url or ""}, value=text_node.text
        )
    if text_type == TextType.IMAGE:
        return LeafNode(
            tag="img",
            value="",
            props={"src": text_node.url or "", "alt": text_node.text},
        )

    raise Exception()
