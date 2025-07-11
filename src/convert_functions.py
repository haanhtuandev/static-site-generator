from textnode import TextNode, TextType
import re
from blocks import *
from htmlnode import HTMLNode, ParentNode, LeafNode
# This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # old nodes is a list of text nodes with markdown texts
    new_nodes_ls = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT or delimiter not in old_node.text:
            new_nodes_ls.append(old_node)
        else:
            ls = old_node.text.split(delimiter)
            if len(ls) < 3:
                raise Exception("Invalid markdown format!")
            else:
                for i in range(len(ls)):
                    if ls[i].strip() == "":
                        continue
                    if i % 2 == 0:
                        new_nodes_ls.append(TextNode(ls[i], TextType.NORMAL_TEXT))
                    elif i % 2 != 0:
                        new_nodes_ls.append(TextNode(ls[i], text_type))
    return new_nodes_ls

def extract_markdown_images(text):
    alt_text = re.findall(r"!\[(.*?)\]", text)
    url = re.findall(r"\((.*?)\)", text)
    zipper = zip(alt_text, url)
    return list(zipper)
def extract_markdown_links(text):
    alt_text = re.findall(r"\[(.*?)\]", text)
    url = re.findall(r"\((.*?)\)", text)
    zipper = zip(alt_text, url)
    return list(zipper)

def split_nodes_image(old_nodes):
    new_node_ls = []
    for old_node in old_nodes:
        img_ls = extract_markdown_images(old_node.text)
        remaining = old_node.text
        if len(img_ls) == 0:
            new_node_ls.append(old_node)
            continue
        else:
            for img in img_ls:
                splitter = remaining.split(f"![{img[0]}]({img[1]})", 1)
                remaining = "".join(splitter[1:])
                if splitter[0] != "":
                    new_node_ls.append(TextNode(splitter[0], TextType.NORMAL_TEXT))
                new_node_ls.append(TextNode(img[0], TextType.IMAGES, img[1]))
            if remaining.strip() != "":
                new_node_ls.append(TextNode(remaining, TextType.NORMAL_TEXT,))
    return new_node_ls
def split_nodes_link(old_nodes):
    new_node_ls = []
    for old_node in old_nodes:
        link_ls = extract_markdown_links(old_node.text)
        remaining = old_node.text
        if len(link_ls) == 0:
            new_node_ls.append(old_node)
        else:
            for link in link_ls:
                splitter = old_node.text.split(f"[{link[0]}]({link[1]})", 1)
                remaining = "".join(splitter[1:])
                if splitter[0] != "":
                    new_node_ls.append(TextNode(splitter[0], TextType.NORMAL_TEXT))
                new_node_ls.append(TextNode(link[0], TextType.LINKS, link[1]))
            if remaining.strip() != "":
                new_node_ls.append(TextNode(remaining, TextType.NORMAL_TEXT,))
    return new_node_ls

def text_to_textnodes(text):
    node = [TextNode(text,TextType.NORMAL_TEXT,)]
    nodes = split_nodes_delimiter(node, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    processed_blocks = []
    for block in blocks:
        # Strip each line and rejoin with \n
        stripped_block = "\n".join(line.strip() for line in block.split("\n"))
        if stripped_block:  # Skip empty blocks
            processed_blocks.append(stripped_block.strip())
    return processed_blocks


def count_heading_level(text):
    count = 0
    i = 0
    while(text[i] == "#"):
        count += 1
        i += 1
    return count


def markdown_to_html_node(markdown):
    final_children = []
    processed_blocks = markdown_to_blocks(markdown)
    for block in processed_blocks:
        type = block_to_block_type(block)
        tag = ""

        if type == BlockType.HEADING:
            level = count_heading_level(block)
            tag =  f"h{level}"
            content = list(map(lambda node : node.text_node_to_html_node(), text_to_textnodes(block.lstrip("#").lstrip().lstrip("\n").rstrip("\n"))))
            # for node in content:
            #     node = node.text_node_to_html_node()
            final_children.append(ParentNode(tag, content))
        elif type == BlockType.PARAGRAPH:
            processed = block.replace("\n", " ")
            content = list(map(lambda node : node.text_node_to_html_node(), text_to_textnodes(processed)))
            final_children.append(ParentNode("p", content))
        elif type == BlockType.UNORDERED_LIST:
            children = []
            tag = "ul"
            for line in block.split("\n"):
                content = list(map(lambda node : node.text_node_to_html_node(), text_to_textnodes(line.lstrip("-").lstrip().replace("\n", " "))))
                children.append(ParentNode("li" , content))
            final_children.append(ParentNode(tag, children))
        elif type == BlockType.ORDERED_LIST:
            children = []
            tag = "ol"
            for line in block.split("\n"):
                content = list(map(lambda node : node.text_node_to_html_node(), text_to_textnodes(line[3:].replace("\n", " "))))
                children.append(ParentNode("li" , content))
            final_children.append(ParentNode(tag, children))
        elif type == BlockType.QUOTE:
            tag = "blockquote"
            content = list(map(lambda node : node.text_node_to_html_node(), text_to_textnodes(block.replace(">","").lstrip())))
            final_children.append(ParentNode(tag, content))
        elif type == BlockType.CODE:
            content = block.lstrip("```").rstrip("```").lstrip().rstrip() + "\n"
            final_children.append(ParentNode("pre", [LeafNode("code", content)]))
        else:
            print("No match for: ", block)
            raise Exception("No matched type!")
    return ParentNode("div", final_children)
    


string = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """
print("original string: \n", string)
string = string.replace("\n", "")
print("Processsed:\n",string)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#"):
            return line.lstrip("#").lstrip()

print(extract_title("#Hello          "))

