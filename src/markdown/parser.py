import re

from enums.block_type import BlockType


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def markdown_to_blocks(text: str):
    return [block.strip() for block in text.split("\n\n") if block.strip()]


def extract_title(markdown: str):
    if markdown.startswith("# "):
        title = markdown[2:].split("\n")[0].strip()
        if not title:
            raise Exception("Empty title")
        return title
    raise Exception("No header found in: ", markdown)


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
