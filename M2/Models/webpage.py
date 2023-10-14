import lxml
from lxml import html,etree
import json

bookkeeping_path = "/Users/farzintavakoli/Desktop/CS/Project 3/bookkeeping.json"
webpages_path = "/Users/farzintavakoli/Desktop/CS/webpages"

with open(bookkeeping_path) as bk:
    bookkeeping = json.load(bk)

class Webpage:
    def __init__(self,dID):
        self.dID = dID
        self.url = self.getURL()
        self.tree = self.readDoc()
        self.title = self.getTitle()
        self.description = self.getDescription()

        

    def getTitle(self):
        if self.tree == None:
            return "No Title"
        return " ".join(self.tree.xpath("//title/text()"))


    def readDoc(self):
        folder_number = self.dID.split("/")[0]
        file_number = self.dID.split("/")[1]
        # open doc and parse it
        with open(f"{webpages_path}/{folder_number}/{file_number}","rb") as doc:
            html_content = doc.read()
            parser = etree.HTMLParser()
            html_tree = etree.fromstring(html_content,parser)
            return html_tree

    def getContent(self):
        folder_number = self.dID.split("/")[0]
        file_number = self.dID.split("/")[1]
        with open(f"{webpages_path}/{folder_number}/{file_number}","rb") as doc:
            html_content = doc.read()
            
            return html.tostring(html.fromstring(html_content))
        
    def getURL(self):
        return bookkeeping[self.dID]

    def getDescription(self):
        if self.tree == None:
            return "No Description"
        return " ".join(self.tree.xpath("//text()[normalize-space() and not(ancestor::style) and not(ancestor::script) and not(ancestor::title) and not(title) ]"))[0:150]
        
