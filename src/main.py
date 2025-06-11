from textnode import *
from htmlnode import *
import re
import os
import shutil
import logging
import sys
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print("Usage: python myscript.py <basepath>")
        sys.exit(1)

    basepath = "https://github.com/ThatOnePersonHere/static_site_generator"
    print("basepath ", sys.argv[1])

    for filename in os.listdir(basepath):
        print(filename)
        
    logger = logger_setup(logging.DEBUG)

    static_page_source = './static/'
    static_page_destination = './docs/'

    if os.path.exists(static_page_destination) == False:
        logging.error(f"Source folder {static_page_source} is missing")
    else:
        if os.path.exists(static_page_destination) == True:
            logger.info(f'Clearing locaion: {static_page_destination}')
            shutil.rmtree(static_page_destination)
        logger.info(f'Remaking location: {static_page_destination}')
        os.mkdir(static_page_destination)
        copy_from_src_to_dest(static_page_source,static_page_destination,os.listdir(path=static_page_source),logger)
        findContent(basepath)

def remove_old_logs(logfile_location,logger):
    if len(os.listdir(path=logfile_location)) > 5:
        oldest_file = min(os.listdir(path=logfile_location))
        logger.info(f'Deleted file: {oldest_file}')
        os.remove(logfile_location+oldest_file)
        remove_old_logs(logfile_location,logger)
    pass


def logger_setup(logging_level):
    logger = logging.getLogger(__name__)
    logfile_location = './logs/'
    if os.path.exists(logfile_location) == False:
        os.mkdir(logfile_location)
    LOGFILENAME = logfile_location + datetime.now().strftime('logfile_%H%M%S_%d%m%Y.log')
    logging.basicConfig(format='%(asctime)s %(message)s',filename=LOGFILENAME, encoding='utf-8', level=logging_level)
    remove_old_logs(logfile_location,logger)
    return logger

def copy_from_src_to_dest(src_loc,copy_dest,obj_list,logger):
    for obj in obj_list:
        obj_path = src_loc + obj
        if os.path.isfile(obj_path):
            logger.info(f'Copy file {obj}\n\t\tsrc path: {src_loc}, dst: {copy_dest}')
            shutil.copy(obj_path,copy_dest)
        else:
            new_dir = copy_dest + obj + "/"
            os.mkdir(new_dir)
            logger.info(f'Created dir {new_dir}')
            copy_from_src_to_dest(obj_path + "/",new_dir,os.listdir(path=obj_path),logger)
        pass
    pass

#Find tag for texttype
def text_node_to_html_node(self):
    if self.text_type not in TextType:
        raise ValueError(f"Invalid text type: {self.text_type}")
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
            raise ValueError(f"No closing delimiter {delimiter} found in the text: {node.text}")
    return node_list

#Finds and returns the image info from text      
def extract_markdown_images(text):
    if len(re.findall(r"!\[", text)) > len(re.findall(r"[\]]", text)) or len(re.findall(r"\]\(", text)) > len(re.findall(r"[\)]", text)):
        raise ValueError("Text markdown is not formatted correctly, check for !,[,],(,)")
    return re.findall(r"!\[([^\]\]]*)\]\(([^\(\)]*)\)", text)


#Finds and returns the link info from text
def extract_markdown_links(text):
    if len(re.findall(r"\[", text)) > len(re.findall(r"[\]]", text)) or len(re.findall(r"\]\(", text)) > len(re.findall(r"[\)]", text)):
        raise ValueError("Text markdown is not formatted correctly, check for [,],(,)")
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

def remove_excessive_marks(text):
    return re.sub(r'(^\W* )|(^\d*\. )', '',text)

def markdown_to_blocks(markdown):
    return list(filter(lambda x: x.strip(' \n') != '',re.split(r'\n\n', markdown)))

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
    test = []
    for line in text_to_textnodes(text):
        if type(line) == list:
            for item in line:
                test.append(text_node_to_html_node(item))
        else:
            test.append(text_node_to_html_node(line))
    return test
    pass

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
    raise Exception("No Header Present")

def generate_page(from_path, template_path, dest_path,"https://github.com/ThatOnePersonHere/static_site_generator"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    source_cont = open(from_path)
    template = open(template_path)
    loc_from = source_cont.read()
    loc_temp = template.read()
    with open(dest_path, 'w', opener=opener) as l:
        print(loc_temp.replace('{{ Content }}',markdown_to_html_node(loc_from).to_html()).replace('{{ Title }}',extract_title(loc_from)).replace('href="/',f'href="{basepath}').replace('href="/',f'href="{basepath}'), file=l)

dir_fd = os.open('./', os.O_RDONLY)

def opener(path, flags):
    return os.open(path, flags, dir_fd=dir_fd)

def test(loc):
    for x in loc:
        if os.path.isfile(os.path.join(loc, x)) == True:
            return os.path.join(loc, x)
        else:
            loca = test(os.path.join(loc, x))
    return loca

def contentRecCall(location, source, dest):
    current_loc = os.path.join(source, location)
    items = []
    if os.path.isfile(current_loc) == False:
        if os.path.exists(os.path.join(dest, location)) == False:
            os.mkdir(os.path.join(dest, location))
        for x in os.listdir(current_loc):
            items.append(contentRecCall(os.path.join(location, x), source,dest))
        return items
    else:
        return location

def sourceFilesToHTML(text, source, dest, template):
    if type(text) == list:
        for i in text:
            sourceFilesToHTML(i, source, dest, template)
    else:
        generate_page(os.path.join(source,text), template, os.path.join(dest,(text[:-2]+'html')),source)

def findContent(source):
    dest = "./docs"
    template = './template.html'
    content_list = []
    for x in os.listdir(source):
        content_list.append(contentRecCall(x, source,dest))
    sourceFilesToHTML(content_list, source, dest, template)
    pass

if __name__ == "__main__":
    main()
