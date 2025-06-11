class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag #String representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value #String representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children #List of HTMLNode objects representing the children of this node
        self.props = props #Dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self): #To be overridden by child class to render as HTML
        raise NotImplementedError

    def props_to_html(self): #return a string that represents the HTML attributes of the node
        if self.props == None:
            return ""
        
        full_html_attributes = []

        for item in self.props.items():
           full_html_attributes.append(f' {item[0]}="{item[1]}"')

        return ''.join(full_html_attributes)
    
    def __repr__(self):
        return f'HTMLNode({self.tag},{self.value},{self.children},{self.props})'
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None: #Check for empty value
            raise ValueError("LeafNode must have a value")

        super().__init__(tag, value, None, props) #Construct with no children

    def to_html(self):
        if self.tag == None:
            return str(self.value)
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None): #tag and children are required
        if tag == None:
            raise ValueError("ParentNode must have a tag")
        elif children == None:
            raise ValueError("ParentNode must include children")
        
        super().__init__(tag, None, children, props) #Construct with no value

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        elif self.children == None:
            raise ValueError("ParentNode must include children")
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'