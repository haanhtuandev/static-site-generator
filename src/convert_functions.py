from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # old nodes is a list of text nodes with markdown texts
    for old_node in old_nodes:
        new_nodes_ls = []
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes_ls.append(old_node)
        else:
            ls = old_node.split(delimiter)
            if len(ls) < 3:
                raise Exception("Invalid markdown format!")
            else:
                for el in ls:
                    new_nodes_ls.append(TextNode(el, text_type))
    return new_nodes_ls



    # returns a new list of TextNodes


