from enum import Enum

class TextType(Enum):
	NORMAL = "text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADER = "header"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered list"
	ORDERED_LIST = "ordered list"

class TextNode:
	def __init__(self, TEXT=None, TEXT_TYPE=None, url=None):
		if TEXT is None or TEXT_TYPE is None:
			raise ValueError('Text and Text type are required')
		self.text = TEXT
		self.text_type = TEXT_TYPE
		self.url = url

	def __eq__(self, other): #test to see if two nodes are equal
		if not isinstance(other, TextNode): #verify if other is a TextNode
			return False
		return (self.text == other.text and self.text_type == other.text_type and self.url == other.url)
	
	def __repr__(self):
		return f'TextNode({self.text}, {self.text_type}, {self.url})'

