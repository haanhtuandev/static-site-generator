class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        html_format = " "
        for prop in self.props.items():
            html_format += f'{prop[0]}="{prop[1]}" '
        return html_format.rstrip()
    def __repr__(self):
        print(f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}")

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    def to_html(self):
        if self.tag == None:
            raise ValueError
        if self.children == None:
            raise ValueError("Parent node must have children")
        return f"<{self.tag}>{self.to_html()}</{self.tag}>"