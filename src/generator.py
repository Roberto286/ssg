import os
from pathlib import Path

from markdown.converter import markdown_to_html_node
from markdown.parser import extract_title


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
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

    new_content = (
        template_file_content.replace("{{ Title }}", title)
        .replace("{{ Content }}", html_string)
    )

    if basepath != "/":
        new_content = (
            new_content.replace('href="/', f'href="{basepath}')
            .replace('src="/', f'src="{basepath}')
        )

    dest_path_as_path = Path(dest_path)
    dest_path_as_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path_as_path, "w") as f:
        _ = f.write(new_content)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str
):
    for entry in os.listdir(dir_path_content):
        src = os.path.join(dir_path_content, entry)
        if os.path.isdir(src):
            generate_pages_recursive(
                src, template_path, os.path.join(dest_dir_path, entry), basepath
            )
        elif entry.endswith(".md"):
            dest = os.path.join(dest_dir_path, entry.replace(".md", ".html"))
            generate_page(src, template_path, dest, basepath)
