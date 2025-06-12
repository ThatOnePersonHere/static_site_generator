from textnode import *
from htmlnode import *
from logger import *
import re
import os
import shutil
import logging
import sys

#initiate function to make log, global as its needed throughout the program
#Print to log, use name.logItem(level, text to log)
log = LogRecord()
log.logger_setup(logging.DEBUG)

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = ""

    #Static info, source and destination
    static_page_source = './static/'
    static_page_destination = './docs/'
    static_content_source = './content'

    if os.path.exists(static_content_source) == False:
        log.logItem('error',f"Content folder {static_content_source} is missing")
    if os.path.exists(static_page_destination) == False:
        log.logItem('error',f"Source folder {static_page_source} is missing")
    else:
        if os.path.exists(static_page_destination) == True:
            log.logItem('info',f'Clearing locaion: {static_page_destination}')
            shutil.rmtree(static_page_destination)
        log.logItem('info',f'Remaking location: {static_page_destination}')
        os.mkdir(static_page_destination)
        copy_from_src_to_dest(static_page_source,static_page_destination,os.listdir(path=static_page_source))
        findContent("./content",basepath)

def handleError(type, text):
    log.logItem('error',text)
    raise type(text)

def copy_from_src_to_dest(src_loc,copy_dest,obj_list):
    for obj in obj_list:
        obj_path = os.path.join(src_loc, obj)
        if os.path.isfile(obj_path):
            log.logItem('info',f'Copy file {obj}\n\t\tsrc path: {src_loc}, dst: {copy_dest}')
            shutil.copy(obj_path,copy_dest)
        else:
            new_dir = os.path.join(copy_dest, obj + "/")
            os.mkdir(new_dir)
            log.logItem('info',f'Created dir {new_dir}')
            copy_from_src_to_dest(obj_path + "/",new_dir,os.listdir(path=obj_path))
        pass
    pass

#Find texttype and return correct leafnode
def text_node_to_html_node(self):
    if self.text_type not in TextType:
        handleError(ValueError,f"Invalid text type: {self.text_type}")
    match TextType(self.text_type):
        case TextType.NORMAL:
            return LeafNode(tag=None, value=self.text, props=None)
        case TextType.BOLD:
            return LeafNode(tag='b', value=self.text, props=None)
        case TextType.ITALIC:
            return LeafNode(tag='i', value=self.text, props=None)
        case TextType.CODE:
            return LeafNode(tag='code', value=self.text, props=None)
        case TextType.LINK:
            return LeafNode(tag='a', value=self.text, props={'href':self.url})
        case TextType.IMAGE:
            return LeafNode(tag='img', value=self.text, props={"src": self.url, "alt": self.text})

#splits text based on text type delimiter
def split_nodes_delimiter(nodes_old, delimiter, text_type):
    node_list = []
    for node in nodes_old:
        if node.text.count(delimiter)%2 == 0:
            string_list = []
            string_list.extend(node.text.split(delimiter))
            for i in range(0,len(string_list)):
                if i%2 != 0:
                    node_list.append(TextNode(string_list[i], text_type))
                else:
                    if node.text_type == None:
                        node_list.append(TextNode(string_list[i], TextType.NORMAL))
                    else:
                        node_list.append(TextNode(string_list[i], node.text_type))
        else:
            handleError(ValueError,f"No closing delimiter {delimiter} found in the text: {node.text}")
    return node_list

#Finds and returns the image info from text      
def extract_markdown_images(text):
    if len(re.findall(r"!\[", text)) > len(re.findall(r"[\]]", text)) or len(re.findall(r"\]\(", text)) > len(re.findall(r"[\)]", text)):
        handleError(ValueError,"Text markdown is not formatted correctly, check for !,[,],(,)")
    return re.findall(r"!\[([^\]\]]*)\]\(([^\(\)]*)\)", text)


#Finds and returns the link info from text
def extract_markdown_links(text):
    if len(re.findall(r"\[", text)) > len(re.findall(r"[\]]", text)) or len(re.findall(r"\]\(", text)) > len(re.findall(r"[\)]", text)):
        handleError(ValueError,"Text markdown is not formatted correctly, check for [,],(,)")
    return re.findall(r"\[([^\]\]]*)\]\(([^\(\)]*)\)", text)

#Extracts image info from textnode and returns as list of textnodes
def split_nodes_image(old_nodes):
    node_list = []
    for node in old_nodes:
        string_list = []
        string_list.extend(extract_markdown_images(node.text))
        node_text_split = (re.split(r"!\[([^\]\]]*)\]\(([^\(\)]*)\)", node.text))
        current_touple = 0
        for i in range(0,len(node_text_split),3):
            if 0 == len(node_text_split)-1 or node.text_type == TextType.LINK:
                node_list.append(node)
            elif i+2 <= len(node_text_split):
                node_list.extend([TextNode(str(node_text_split[i]), TextType.NORMAL),TextNode(str(string_list[current_touple][0]), TextType.IMAGE, str(string_list[current_touple][1]))])
                current_touple+=1
            elif node_text_split[i] != "":
                node_list.append(TextNode(str(node_text_split[i]), TextType.NORMAL))
    return node_list

#Extracts link info from textnode and returns as list of textnodes
def split_nodes_link(old_nodes):
    node_list = []
    for node in old_nodes:
        string_list = []
        string_list.extend(extract_markdown_links(node.text))
        node_text_split = (re.split(r"\[([^\]\]]*)\]\(([^\(\)]*)\)", node.text))
        current_touple = 0
        for i in range(0,len(node_text_split),3):
            if 0 == len(node_text_split)-1 or node.text_type == TextType.IMAGE:
                node_list.append(node)
            elif i+2 <= len(node_text_split):
                if node_text_split[i] == "":
                    node_list.extend([TextNode(str(string_list[current_touple][0]), TextType.LINK, str(string_list[current_touple][1]))])
                else:
                    node_list.extend([TextNode(str(node_text_split[i]), TextType.NORMAL),TextNode(str(string_list[current_touple][0]), TextType.LINK, str(string_list[current_touple][1]))])
                current_touple+=1
            elif node_text_split[i] != "":
                node_list.append(TextNode(str(node_text_split[i]), TextType.NORMAL))
    return node_list

#Takes in text, and returns list of text nodes
def text_to_textnodes(text):
    test_nodes = []
    test_nodes.extend(split_nodes_link(
            split_nodes_image(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        split_nodes_delimiter([TextNode(text,TextType.NORMAL)],"**",TextType.BOLD)
                        ,"_",TextType.ITALIC)
                    ,"`",TextType.CODE)
                    )
                )
            )
    return test_nodes

#Removes markup for HTML nodes
def remove_excessive_marks(text):
    return re.sub(r'(^\W* )|(^\d*\. )', '',text)

#Splits whole markdown to list of paragraph blocks
def markdown_to_blocks(markdown):
    return list(filter(lambda x: x.strip(' \n') != '',re.split(r'\n\n', markdown)))

#Generates header nodes
def htmlHeaderNode(block):
   text_nodes = []
   for item in text_to_textnodes(remove_excessive_marks(block)):
        text_nodes.append(text_node_to_html_node(item))
   return ParentNode(tag='h' + str(block.count('#')), children = text_nodes) 
     
def generateQuoteBlock(block):
    bricks = []
    for quote_brick in re.split(r'\n(?=>)', block):
        bricks.append(LeafNode(tag=None, value=(quote_brick.lstrip('> ').rstrip())))
    return ParentNode("blockquote",bricks)

def listLineCleanup(text):
    newHtmlNodes = []
    for line in text_to_textnodes(text):
        if type(line) == list:
            for item in line:
                newHtmlNodes.append(text_node_to_html_node(item))
        else:
            newHtmlNodes.append(text_node_to_html_node(line))
    return newHtmlNodes

def generateListBlock(block, tag):
    bricks = []
    for list_brick in re.split(r'\n', block):
        bricks.append(ParentNode(tag='li', children=listLineCleanup(remove_excessive_marks(list_brick))))
    return ParentNode(tag,bricks)

def block_to_node(block):
    if block.startswith("#"):
        return htmlHeaderNode(block)
    elif block.startswith("```") and block.endswith("```"):
        return ParentNode("pre",[LeafNode(tag='code', value=re.sub(r'(\n)+( *)', '\n',block.strip('`')).lstrip('\n'))])
    elif block.startswith("> "):
        return generateQuoteBlock(block)
    elif block.startswith("- "):
        return generateListBlock(block, 'ul')
    elif re.match((r"(^\d+\. )"), block) != None:
        return generateListBlock(block, 'ol')
    else:
        bricks = []
        for brick in text_to_textnodes(block):
            bricks.append(text_node_to_html_node(brick))
        return ParentNode("p",bricks)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    node_list = []
    for block in blocks:
        node_list.append(block_to_node(block))
    return ParentNode("div",node_list)

def extract_title(markdown):
    for block in markdown_to_blocks(markdown):
        if block.startswith("#"):
            return remove_excessive_marks(block)
    handleError(Exception,"No Header Present")

def generate_page(from_path, template_path, dest_path,basepath):
    log.logItem('info',f"Generating page from {from_path} to {dest_path} using {template_path}")
    source_cont = open(from_path)
    template = open(template_path)
    loc_from = source_cont.read()
    loc_temp = template.read()
    with open(dest_path, 'w', opener=opener) as l:
        page_output = loc_temp.replace('{{ Content }}',markdown_to_html_node(loc_from).to_html())
        page_output = page_output.replace('{{ Title }}',extract_title(loc_from))
        page_output = page_output.replace('src="/',f'src="{basepath}/')
        page_output = page_output.replace('href="/',f'href="{basepath}/')
        print(page_output, file=l)
    log.logItem('info',f"Page Generated:{dest_path}")

dir_fd = os.open('./', os.O_RDONLY)

def opener(path, flags):
    log.logItem('info', f'open file: {path}, {flags}, {dir_fd}')
    return os.open(path, flags, dir_fd=dir_fd)

def contentRecCall(location, source, dest):
    current_loc = os.path.join(source, location)
    items = []
    if os.path.isfile(current_loc) == False:
        if os.path.exists(os.path.join(dest, location)) == False:
            log.logItem('info',f'creating directory: {os.path.join(dest, location)}')
            os.mkdir(os.path.join(dest, location))
        for x in os.listdir(current_loc):
            items.append(contentRecCall(os.path.join(location, x), source,dest))
        return items
    else:
        return location

def sourceFilesToHTML(text, source, dest, template,basepath):
    if type(text) == list:
        for i in text:
            sourceFilesToHTML(i, source, dest, template,basepath)
    else:
        generate_page(os.path.join(source,text), template, os.path.join(dest,(text[:-2]+'html')),basepath)

def findContent(source,basepath):
    dest = "./docs"
    template = './template.html'
    content_list = []
    for x in os.listdir(source):
        content_list.append(contentRecCall(x, source,dest))
    sourceFilesToHTML(content_list, source, dest, template,basepath)
    pass

if __name__ == "__main__":
    main()
