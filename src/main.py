from config import INDEX_PATH, PUBLIC_DIR, TEMPLATE_PATH
from generator import generate_page
from utils.files import copy_files_to_dir


def main():
    copy_files_to_dir("./static", "./public")
    generate_page(INDEX_PATH, TEMPLATE_PATH, f"{PUBLIC_DIR}/index.html")


main()
