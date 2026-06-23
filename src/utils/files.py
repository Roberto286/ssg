import os
import shutil


def copy_files_to_dir(source: str, dest: str):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    _copy_recursive(source, dest)


def _copy_recursive(source: str, dest: str):
    os.makedirs(dest, exist_ok=True)
    for entry in os.listdir(source):
        current_path = os.path.join(source, entry)
        dest_path = os.path.join(dest, entry)
        if os.path.isfile(current_path):
            print(f"copying: {current_path} to: {dest}")
            _ = shutil.copy(current_path, dest)
        else:
            _copy_recursive(current_path, dest_path)
