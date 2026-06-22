from __future__ import annotations
from dataclasses import dataclass


@dataclass
class HTMLNode:
    tag: str | None = None
    value: str | None = None
    children: list[HTMLNode] | None = None
    props: dict[str, str] | None = None

    def to_html(self):
        if self.children:
            inner = "".join(child.to_html() for child in self.children)
            return f"<{self.tag}{self.props_to_html()}>{inner}</{self.tag}>"
        if self.value is not None:
            if self.tag is None:
                return self.value
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        raise NotImplementedError

    def props_to_html(self):
        result = ""

        if self.props:
            for prop in self.props:
                result += f' {prop}="{self.props[prop]}"'
        return result
