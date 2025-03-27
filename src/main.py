import os
import shutil
from copystatic import copy_files_recursively
from generate_page import generate_page_recursive
import sys

if len(sys.argv) != 2:
    basepath = "./"
else:
    basepath = sys.argv[1]

static_dir = "./static"
public_dir = "./docs"
content_dir = "./content"
template_path = "./template.html"


def main():
    print("Deleting public directory...") 
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
        
    print("Copying static files to public directory...")
    copy_files_recursively(static_dir, public_dir)
    
    generate_page_recursive(content_dir, template_path, public_dir, basepath)

main()