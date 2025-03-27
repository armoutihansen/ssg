import os
import shutil
from copystatic import copy_files_recursively
from generate_page import generate_page_recursive

static_dir = "./static"
public_dir = "./public"
content_dir = "./content"


def main():
    print("Deleting public directory...") 
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
        
    print("Copying static files to public directory...")
    copy_files_recursively(static_dir, public_dir)
    
    generate_page_recursive(content_dir, "template.html", public_dir)

main()