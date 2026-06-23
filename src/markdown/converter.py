import re

from enums.block_type import BlockType
from enums.text_type import TextType
from markdown.parser import block_to_block_type, markdown_to_blocks
from markdown.splitter import text_to_textnodes
from nodes.htmlnode import HTMLNode
from nodes.parentnode import ParentNode
from nodes.textnode import TextNode, text_node_to_html_node


def text_to_children(text: str) -> list[HTMLNode]:
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def paragraph_to_html_node(block: str) -> HTMLNode:
    text = " ".join(block.split("\n"))
    return ParentNode(tag="p", children=text_to_children(text))


def heading_to_html_node(block: str) -> HTMLNode:
    level = len(block) - len(block.lstrip("#"))
    text = block[level + 1 :]
    return ParentNode(tag=f"h{level}", children=text_to_children(text))


def code_to_html_node(block: str) -> HTMLNode:
    text = block[3:-3].strip()
    code_leaf = text_node_to_html_node(TextNode(text, TextType.CODE))
    return ParentNode(tag="pre", children=[code_leaf])


def quote_to_html_node(block: str) -> HTMLNode:
    lines = [line.lstrip(">").strip() for line in block.split("\n")]
    text = " ".join(lines)
    return ParentNode(tag="blockquote", children=text_to_children(text))


def unordered_list_to_html_node(block: str) -> HTMLNode:
    items = [
        HTMLNode(tag="li", children=text_to_children(line[2:]))
        for line in block.split("\n")
    ]
    return ParentNode(tag="ul", children=items)


def ordered_list_to_html_node(block: str) -> HTMLNode:
    items = [
        HTMLNode(tag="li", children=text_to_children(re.sub(r"^\d+\. ", "", line)))
        for line in block.split("\n")
    ]
    return ParentNode(tag="ol", children=items)


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    raise ValueError(f"Unknown block type: {block_type}")


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    return ParentNode(tag="div", children=[block_to_html_node(b) for b in blocks])
