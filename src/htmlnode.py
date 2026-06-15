from __future__ import annotations
from dataclasses import dataclass


@dataclass
class HTMLNode:
    tag: str | None
    value: str | None
    children: list[HTMLNode] | None
    props: dict[str, str] | None

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ""

        if self.props:
            for prop in self.props:
                result += f' {prop}="{self.props[prop]}"'
        return result
