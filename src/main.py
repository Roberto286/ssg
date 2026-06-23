import sys

from config import CONTENT_DIR, OUTPUT_DIR, STATIC_DIR, TEMPLATE_PATH
from generator import generate_pages_recursive
from utils.files import copy_files_to_dir

basepath = sys.argv[1] if len(sys.argv) > 1 else "/"


def main():
    copy_files_to_dir(STATIC_DIR, OUTPUT_DIR)
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, OUTPUT_DIR, basepath)


main()
