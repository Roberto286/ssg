from pathlib import Path

from markdown.converter import markdown_to_html_node
from markdown.parser import extract_title


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(
        "Generating page from: ",
        from_path,
        " to: ",
        dest_path,
        " using: ",
        template_path,
    )

    with open(from_path, "r") as f:
        md_file_content = f.read()
    with open(template_path, "r") as f:
        template_file_content = f.read()

    html_node = markdown_to_html_node(md_file_content)
    html_string = html_node.to_html()
    title = extract_title(md_file_content)

    print(template_file_content)
    new_content = template_file_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_string
    )

    dest_path_as_path = Path(dest_path)
    dest_path_as_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path_as_path, "w") as f:
        _ = f.write(new_content)
