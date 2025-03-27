import os
import shutil


def copy_files_recursively(src_path: str, dest_path: str):
    if not os.path.exists(src_path):
        raise ValueError(f'Source directory: {src_path} does not exist')

    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
        
    for file in os.listdir(src_path):
        from_path = os.path.join(src_path, file)
        to_path = os.path.join(dest_path, file)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            copy_files_recursively(from_path, to_path)