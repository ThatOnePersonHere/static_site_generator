import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node0 = HTMLNode("p", None,"paint")
        node1 = HTMLNode(
            "a", 
            "I need help", 
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            })
        node2 = HTMLNode(
            None, 
            None, 
            None,
            {
                "src": "img_girl.jpg",
            })
        node3 = HTMLNode(
            "title", 
            "I cant eat Milk", 
            "children",
            {
                "href": "https://www.duckduckgo.com",
                "src": "img_girl.jpg",
                "alt": "Girl with a jacket",
                "width": "500",
                "height": "600",
            })
        self.assertEqual(node0.__repr__(), 'HTMLNode(p,None,paint,None)')#basic node generation
        self.assertEqual(node0.props_to_html(), '') #no prop test
        self.assertEqual(node1.props_to_html(), ' href="https://www.google.com" target="_blank"') #two prop test
        self.assertEqual(node2.props_to_html(), ' src="img_girl.jpg"') #single prop test
        self.assertEqual(node3.props_to_html(), ' href="https://www.duckduckgo.com" src="img_girl.jpg" alt="Girl with a jacket" width="500" height="600"')#mult prop test
        self.assertNotEqual(node0, node1)

    def test_leaf_to_html(self):
        node0 = LeafNode("p", "Hello, world!")
        node1 = LeafNode(None, "I'm just raw text")
        node2 = LeafNode("a", "This is a props test",             
            {
                "href": "https://www.duckduckgo.com",
                "src": "img_girl.jpg",
            })
        node3 = LeafNode("h1","Google!",{"href": "https://www.google.com",})
        self.assertEqual(node0.to_html(), "<p>Hello, world!</p>") #Basic Node Generation
        self.assertEqual(node1.to_html(), "I'm just raw text") #Raw text Node Generation
        self.assertEqual(node2.to_html(), '<a href="https://www.duckduckgo.com" src="img_girl.jpg">This is a props test</a>') #Multiple props Node Generation
        self.assertNotEqual(node3,None) #Not None test

    def test_leaf_assertRaised(self):
        with self.assertRaises(ValueError):
            LeafNode("p")

    def test_to_html_with_multiple_children(self):
        child_node0 = LeafNode("span", "child0")
        child_node1 = LeafNode("h1", "child1")
        child_node2 = LeafNode("p", "child2")
        child_node3 = LeafNode("b", "child3")
        parent_node = ParentNode("div", [child_node0,child_node1,child_node2,child_node3])
        self.assertEqual(parent_node.to_html(), "<div><span>child0</span><h1>child1</h1><p>child2</p><b>child3</b></div>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_assertRaised(self):
        with self.assertRaises(ValueError): #No Child assert
            ParentNode("p", None)
        with self.assertRaises(ValueError): #No Tag Assert
            child_node = LeafNode("span", "child") 
            ParentNode(None, [child_node])

if __name__ == "__main__":
    unittest.main()