import re

from nodes.textnode import TextNode, TextType


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
    pass


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:

    result: list[TextNode] = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        pointer = 0
        for link in links:
            start = node.text.find(link[0])
            end = start + len(link[0] + link[1])
            text = node.text[pointer : start - 1]
            if text:
                result.append(TextNode(text, TextType.TEXT))
            result.append(TextNode(text=link[0], url=link[1], text_type=TextType.LINK))
            pointer = end + 3

    return result
