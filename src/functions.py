import re

from enums.block_type import BlockType
from enums.text_type import TextType
from nodes.htmlnode import HTMLNode
from nodes.parentnode import ParentNode
from nodes.textnode import TextNode, text_node_to_html_node


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    new_list: list[TextNode] = list()
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_list.append(old_node)
            continue

        parts = old_node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("delimiter not closed")

        for i in range(len(parts)):
            part = parts[i]

            if not part:
                continue

            node = None
            if i % 2 == 0:
                node = TextNode(part, TextType.TEXT)
            else:
                node = TextNode(part, text_type)

            new_list.append(node)

    return new_list


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

    return re.findall(pattern, text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        text = node.text
        images = extract_markdown_images(node.text)

        for image in images:
            img_in_markdown = f"![{image[0]}]({image[1]})"
            parts = text.split(img_in_markdown, 1)

            text_part = parts[0]

            if text_part:
                result.append(TextNode(text_part, TextType.TEXT))

            result.append(TextNode(image[0], TextType.IMAGE, image[1]))

            text = parts[1]

        if text:
            result.append(TextNode(text, TextType.TEXT))
    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:

    result: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        text = node.text
        links = extract_markdown_links(node.text)

        for link in links:
            link_in_markdown = f"[{link[0]}]({link[1]})"
            parts = text.split(link_in_markdown, 1)

            text_part = parts[0]
            if text_part:
                result.append(TextNode(text=text_part, text_type=TextType.TEXT))
            result.append(TextNode(text=link[0], url=link[1], text_type=TextType.LINK))

            text = parts[1]

        if text:
            result.append(TextNode(text=text, text_type=TextType.TEXT))
    return result


def text_to_textnodes(text: str):
    result: list[TextNode] = [TextNode(text, TextType.TEXT)]
    delimiters: list[tuple[str, TextType]] = [
        ("**", TextType.BOLD),
        ("__", TextType.ITALIC),
        ("`", TextType.CODE),
    ]

    for sign, text_type in delimiters:
        result = split_nodes_delimiter(result, sign, text_type)

    result = split_nodes_image(result)
    result = split_nodes_link(result)

    return result


def markdown_to_blocks(text: str):
    return [block.strip() for block in text.split("\n\n") if block.strip()]


def block_to_block_type(text: str) -> BlockType:

    if text.startswith("#"):
        return BlockType.HEADING
    if text.startswith("```"):
        return BlockType.CODE
    if text.startswith(">"):
        return BlockType.QUOTE
    if text.startswith("- "):
        return BlockType.UNORDERED_LIST
    if re.match(r"^\d+\. ", text):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


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
