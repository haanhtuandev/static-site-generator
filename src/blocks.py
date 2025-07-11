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
    lines = [line.strip() for line in block.split("\n")]
    if re.match(r"^\#{1,6} ", block):
        print("Block for check style: \n", block)
        return BlockType.HEADING
    elif re.match(r"^```(.|\n)*```$", block):
        print("Block for check style: \n", block)
        return BlockType.CODE
    # elif all(line.startswith("> ") for line in lines):
    #     print("Block for check style: \n", block)
    #     return BlockType.QUOTE
    elif all(re.match(r"^>\s*", line) for line in lines if line):
        return BlockType.QUOTE

    elif all(line.startswith("- ") for line in lines):
        print("Block for check style: \n", block)
        return BlockType.UNORDERED_LIST
    elif all(
        line.startswith(f"{i+1}. ")
        for i, line in enumerate(lines)
    ):
        print("Block for check style: \n", block)
        return BlockType.ORDERED_LIST
    else:
        print("Block for check style: \n", block)
        return BlockType.PARAGRAPH

md = """``` This is a list
> with items ```"""
type = block_to_block_type(md)
print(type)