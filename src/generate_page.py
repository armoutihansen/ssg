from block_markdown import markdown_to_html_node
from extract_title import extract_title
import os

def generate_page_recursive(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if not os.path.exists(from_path):
        raise ValueError(f'Content directory: {from_path} does not exist')
    
    if not os.path.exists(template_path):
        raise ValueError(f'Template {template_path} does not exist')
    
    with open(template_path, "r") as file:
        template = file.read()
    
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
        
    for file in os.listdir(from_path):
        print(file, from_path)
        from_path_ = os.path.join(from_path, file)
        if os.path.isfile(from_path_):
            dest_path_ = os.path.join(dest_path, file.replace(".md", ".html"))
        else:
            dest_path_ = os.path.join(dest_path, file)
        
        print(f" * {from_path_} -> {dest_path_} ")
        
        if os.path.isfile(from_path_):
            with open(from_path_, "r") as file:
                md = file.read()
                
            md_to_html = markdown_to_html_node(md).to_html()
            title = extract_title(md)
            
            content = template.replace("{{ Title }}", title).replace("{{ Content }}", md_to_html)
            
            with open(dest_path_, "w") as file:
                file.write(content)
                
        else:
            generate_page_recursive(from_path_, template_path, dest_path_)
                    