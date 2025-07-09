from enum import Enum
import re
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")
    if re.match(r"^\#{1,6} ", block):
        return BlockType.HEADING
    elif re.match(r"^```(.|\n)*```$", block):
        return BlockType.CODE
    elif all(line.startswith("> ") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(
        line.startswith(f"{i+1}. ")
        for i, line in enumerate(lines)
    ):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

md = """``` This is a list
> with items ```"""
type = block_to_block_type(md)
print(type)