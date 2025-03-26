import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "qoute"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

# def block_to_block_type(markdown: str) -> BlockType:
#     if re.match(r'\#{1,6}\s', markdown):
#         return BlockType.HEADING
#     if re.match(r'```', markdown):
#         return BlockType.CODE
    
#     lst = markdown.split("\n")
#     check_quote = [True if line[0] ==">" else False for line in lst]
#     if all(check_quote):
#         return BlockType.QUOTE
    
#     check_unordered_list = [True if re.match(r'-\s', line) else False for line in lst]
#     if all(check_unordered_list):
#         return BlockType.ULIST
    
#     check_ordered_list = [True if re.match(r'\d.\s', line) else False for line in lst]
#     if all(check_ordered_list):
#         return BlockType.OLIST
    
#     return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)
        
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.OLIST:
            return olist_to_html_node(block)
        case BlockType.ULIST:
            return ulist_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case _:
            raise ValueError("invalid block type")
        
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    par = " ".join(lines)
    children = text_to_children(par)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char =="#":
            level +=1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f'Invalid heading level: {level}')
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid qoute block")
        new_lines.append(line.strip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)