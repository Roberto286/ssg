from textnode import TextNode, TextType


def main():
    node1 = TextNode("This is some anchor text", TextType.LINK, "https://boot.dev")
    print(node1)


main()
