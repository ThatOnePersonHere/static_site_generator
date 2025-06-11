import unittest

from main import *

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    
    def test_eq(self):
        node = TextNode("Test value", TextType.LINK, "htts://www.boot.dev")
        node3 = TextNode("Second Test Node", TextType.CODE)
        node4 = TextNode("Second Test Node", TextType.CODE)
        self.assertEqual(node.__repr__(), 'TextNode(Test value, TextType.LINK, htts://www.boot.dev)') #Basic node test
        self.assertEqual(node3, node4) #Duplicate test
        self.assertNotEqual(node, None) #Not empty test

    def test_text_to_html(self): #Test each texttype to leaf node
        node0 = TextNode("Test value normal", 'text')
        self.assertEqual(str(text_node_to_html_node(node0)), "HTMLNode(None,Test value normal,None,None)")
        node1 = TextNode("Test value bold", 'bold')
        self.assertEqual(str(text_node_to_html_node(node1)), "HTMLNode(b,Test value bold,None,None)")
        node2 = TextNode("Test value italic", 'italic')
        self.assertEqual(str(text_node_to_html_node(node2)), "HTMLNode(i,Test value italic,None,None)")
        node3 = TextNode("Test value code", 'code')
        self.assertEqual(str(text_node_to_html_node(node3)), "HTMLNode(code,Test value code,None,None)")
        node4 = TextNode("Test value link", 'link', "https://www.boot.dev")
        self.assertEqual(str(text_node_to_html_node(node4)), "HTMLNode(a,Test value link,None,{'href': 'https://www.boot.dev'})")
        node5 = TextNode("Test value image", 'image', "https://www.boot.dev")
        self.assertEqual(str(text_node_to_html_node(node5)), "HTMLNode(img,Test value image,None,{'src': 'https://www.boot.dev', 'alt': 'Test value image'})")

    def test_text_to_leaf_assertRaised(self):
        with self.assertRaises(ValueError): #Test exception is raised when text type is not in enum
            node = TextNode(TEXT="Test Text",url="www.google.com", TEXT_TYPE="Not_A_Type")
            text_node_to_html_node(node)

    def test_split_node(self):
        bold_node = TextNode("This is text with a **bold block** word", TextType.NORMAL)
        italics_node = TextNode("This is text with a _italics block_ word", TextType.NORMAL)
        code_node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_bold_nodes = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        new_italics_nodes = split_nodes_delimiter([italics_node], "_", TextType.ITALIC)
        new_code_nodes = split_nodes_delimiter([code_node], "`", TextType.CODE)
        self.assertEqual(new_bold_nodes,[
                                            TextNode("This is text with a ", TextType.NORMAL),
                                            TextNode("bold block", TextType.BOLD),
                                            TextNode(" word", TextType.NORMAL),
                                        ])
        self.assertEqual(new_italics_nodes,[
                                            TextNode("This is text with a ", TextType.NORMAL),
                                            TextNode("italics block", TextType.ITALIC),
                                            TextNode(" word", TextType.NORMAL),
                                        ])
        self.assertEqual(new_code_nodes,[
                                            TextNode("This is text with a ", TextType.NORMAL),
                                            TextNode("code block", TextType.CODE),
                                            TextNode(" word", TextType.NORMAL),
                                        ])

    def test_split_node_assertRaised(self):
        with self.assertRaises(ValueError): #Test exception is raised when text type is not in enum
            bad_node = TextNode("This is text with out a **closing delimiter", TextType.NORMAL)
            split_nodes_delimiter([bad_node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        extracted_img_touples = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(extracted_img_touples,[('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])

    def test_extract_markdown_links(self):
        extracted_links_touples = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(extracted_links_touples,[('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')])

    def test_extract_markdown_assertRaised(self):
        with self.assertRaises(ValueError):
            extract_markdown_links("This is text with a bad markdown [to boot dev(https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
            extract_markdown_links("This is text with a bad markdown [to boot dev](https://www.boot.dev and [to youtube](https://www.youtube.com/@bootdotdev)")
            extract_markdown_images("This is text with a bad markdown ![to boot dev(https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
            extract_markdown_images("This is text with a bad markdown ![to boot dev](https://www.boot.dev and [to youtube](https://www.youtube.com/@bootdotdev)")
            extract_markdown_images("This is text with a bad markdown [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")

    def test_split_nodes(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        node1 = TextNode(
            "This is text with an [link](https://www.google.com) and another [second link](https://www.boot.dev)",
            TextType.NORMAL,
        )
        self.assertEqual(str(split_nodes_image([node])),"[TextNode(This is text with an , TextType.NORMAL, None), TextNode(image, TextType.IMAGE, https://i.imgur.com/zjjcJKZ.png), TextNode( and another , TextType.NORMAL, None), TextNode(second image, TextType.IMAGE, https://i.imgur.com/3elNhQu.png)]")
        self.assertEqual(str(split_nodes_link([node1])),"[TextNode(This is text with an , TextType.NORMAL, None), TextNode(link, TextType.LINK, https://www.google.com), TextNode( and another , TextType.NORMAL, None), TextNode(second link, TextType.LINK, https://www.boot.dev)]")

    def test_text_to_textnodes(self):
        test_list = ["This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
                 "This is `code block` with an **bold** word and another `code block` and a [link](https://boot.dev)",
                 "This is plain text",
                 "This an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) with an _italic_ word",
                 "This an _italic_ word and **bold**",
                 "This is just a [link](https://boot.dev)",
                 "[This is just a link](https://boot.dev)",
                    ]
        Answer_List = ['[TextNode(This is , TextType.NORMAL, None), TextNode(text, TextType.BOLD, None), TextNode( with an , TextType.NORMAL, None), TextNode(italic, TextType.ITALIC, None), TextNode( word and a , TextType.NORMAL, None), TextNode(code block, TextType.CODE, None), TextNode( and an , TextType.NORMAL, None), TextNode(obi wan image, TextType.IMAGE, https://i.imgur.com/fJRm4Vk.jpeg), TextNode( and a , TextType.NORMAL, None), TextNode(link, TextType.LINK, https://boot.dev)]',
                        '[TextNode(This is , TextType.NORMAL, None), TextNode(code block, TextType.CODE, None), TextNode( with an , TextType.NORMAL, None), TextNode(bold, TextType.BOLD, None), TextNode( word and another , TextType.NORMAL, None), TextNode(code block, TextType.CODE, None), TextNode( and a , TextType.NORMAL, None), TextNode(link, TextType.LINK, https://boot.dev)]',
                        '[TextNode(This is plain text, TextType.NORMAL, None)]',
                        '[TextNode(This an , TextType.NORMAL, None), TextNode(obi wan image, TextType.IMAGE, https://i.imgur.com/fJRm4Vk.jpeg), TextNode( with an , TextType.NORMAL, None), TextNode(italic, TextType.ITALIC, None), TextNode( word, TextType.NORMAL, None)]',
                        '[TextNode(This an , TextType.NORMAL, None), TextNode(italic, TextType.ITALIC, None), TextNode( word and , TextType.NORMAL, None), TextNode(bold, TextType.BOLD, None), TextNode(, TextType.NORMAL, None)]',
                        '[TextNode(This is just a , TextType.NORMAL, None), TextNode(link, TextType.LINK, https://boot.dev)]',
                        '[TextNode(This is just a link, TextType.LINK, https://boot.dev)]',
                        ]
        for i in range(0,len(test_list)):
            self.assertEqual(str(text_to_textnodes(test_list[i])),str(Answer_List[i]))

    def test_block_text_to_blocks(self):
        test_list = ["""
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
""",
"""
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
""",
"""
This is `code` paragraph

```This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line```

. This is a list
. with items
""",
"""
This is normal paragraph

>This is a quote paragraph with _italic_ text and `code` here
>This is the same quote paragraph on a new line
""",
            ]
        answer_list = [
            ['# This is a heading', 'This is a paragraph of text. It has some **bold** and _italic_ words inside of it.', '- This is the first list item in a list block - This is a list item - This is another list item'],
            ['This is **bolded** paragraph', 'This is another paragraph with _italic_ text and `code` here This is the same paragraph on a new line', '- This is a list - with items'],
            ['This is `code` paragraph', '```This is another paragraph with _italic_ text and `code` here This is the same paragraph on a new line```', '. This is a list . with items'],
            ['This is normal paragraph', '>This is a quote paragraph with _italic_ text and `code` here >This is the same quote paragraph on a new line'],
            ]
        block_type_answers = [
                            [BlockType.HEADER,BlockType.PARAGRAPH,BlockType.UNORDERED_LIST],
                            [BlockType.PARAGRAPH,BlockType.PARAGRAPH,BlockType.UNORDERED_LIST],
                            [BlockType.PARAGRAPH,BlockType.CODE,BlockType.ORDERED_LIST],
                            [BlockType.PARAGRAPH,BlockType.QUOTE],
                            ]
        #for i in range(0,len(test_list)):
            #self.assertEqual(str(markdown_to_blocks(test_list[i])),str(answer_list[i]))
            #self.assertEqual(block_to_block_type(markdown_to_blocks(test_list[i])),block_type_answers[i])

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        #self.assertEqual(
        #    html,
        #    "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        #)

if __name__ == "__main__":
    unittest.main()