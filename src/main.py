from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode

def main():
    test = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(test)
    
        
    

main()