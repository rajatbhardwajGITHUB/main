import urllib.request
from urllib import parse
from html.parser import HTMLParser
import os

# creating the directories
def direct(name):
    if not os.path.exists(name):
        os.makedirs(name)

# creating files
def files(dir, base_url):
    queue = os.path.join(dir, 'queue.txt')
    crawl = os.path.join(dir, "crawl.txt")
    if not os.path.isfile(queue):
        f = open(queue, "w+")
        f.write(base_url)
    if not os.path.isfile(crawl):
        f2 = open(crawl, "w+")
        f2.write('')

direct('project')
files('project', 'https://www.geeksforgeeks.org/python-custom-list-split/')

r = open("project/queue.txt", "r")

#capturing the content of tge file
cont = r.read()
r.close()
print(cont)

re = urllib.request.urlopen(cont)

#checking the content-type of the page
if re.getheader('content-type') == 'text/html':
    print(re)
    html = re.read()
    strings = html.decode('utf-8')
    print(strings)

#htmlpraser subclass for collecting the urls
class finder(HTMLParser):
    def __init__(self, base):
        super().__init__()      #for accessing the instance-attributes of the mainclass
        self.base = base        
        self.links = set()      

    def handle_starttag(self, tag, attrs):
        #checking for the 'anchor' tags and 'href' attributes
        if tag == 'a':
            for (attr, value) in attrs:
                if attr == 'href':
                    url = urllib.parse.urljoin(self.base, value) #for completing the url if any is incomplete
                    self.links.add(url)

    #def link(self):
    #   print(self.links)
    
    #storing the links in the file created
    def store_links(self):
        #convert the set() into string 
        emp = str(self.links) 
        file = open('queue.txt', 'a')
        file.write(emp)
        file.close()


fq = finder("https://www.geeksforgeeks.org/") #main or homapage for the completion of any incomplete url
fq.feed(strings)        #feeding the parser with the html/css code
fq.store_links()
