from __future__ import annotations
from dataclasses import dataclass


@dataclass
class HTMLNode:
    tag: str | None = None
    value: str | None = None
    children: list[HTMLNode] | None = None
    props: dict[str, str] | None = None

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ""

        if self.props:
            for prop in self.props:
                result += f' {prop}="{self.props[prop]}"'
        return result
