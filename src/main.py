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


def main():
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    print(new_nodes)


main()
