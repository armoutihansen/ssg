from textnode import TextNode, TextType
import re

def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType
    ) -> list[TextNode]:
    
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        split_nodes = []
        
        sections = node.text.split(delimiter)
        
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown syntax: Closing delimiter not found")
        
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
                
        new_nodes.extend(split_nodes)
        
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes = []
    
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        node_text = node.text
        imgs = extract_markdown_images(node.text)
        
        if imgs == []:
            new_nodes.append(node)
            continue
        
        for img in imgs:
            sections = node_text.split(f"![{img[0]}]({img[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown format: Image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))
            node_text = sections[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
            
    return new_nodes
                
                
def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    
    new_nodes = []
    
    for node in old_nodes:
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        node_text = node.text
        
        links = extract_markdown_links(node.text)
        
        if links == []:
            new_nodes.append(node)
            continue
        
        split_nodes = []
        
        for i in range(len(links)):
            link_text, link_url = links[i]
            
            sections = node_text.split(f"[{link_text}]({link_url})", 1)
            
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
                split_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            else:
                split_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            node_text = sections[1]
            
        if node_text != "":
            split_nodes.append(TextNode(node_text, TextType.TEXT))
        new_nodes.extend(split_nodes)
        
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    
   nodes = [TextNode(text, TextType.TEXT)] 
   nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
   nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
   nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
   nodes = split_nodes_image(nodes)
   nodes = split_nodes_links(nodes)
   
   return nodes