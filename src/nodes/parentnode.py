from typing_extensions import override

from nodes.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)

    @override
    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is required")

        if not self.children:
            raise ValueError("children is required")

        result: str = ""
        for child in self.children:
            result += child.to_html()

        return result
