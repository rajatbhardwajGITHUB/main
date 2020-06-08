import urllib.request
from urllib import parse
from html.parser import HTMLParser
import os
import mysql.connector
# all the unusal print() statements are just for small debugging

connect = mysql.connector.connect(user = 'USER_NAME', 
                                  password = 'PASSWORD', 
                                  host = 'HOST_NAME', 
                                  database = 'DATABASE_NAME')
cursor = connect.cursor()

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
files('project', 'https://automatetheboringstuff.com/')

r = open("project/queue.txt", "r")

#capturing the content of tge file
cont = r.read()
r.close()
print(cont)

re = urllib.request.urlopen(cont)

#checking the content-type of the page
if re.getheader('content-type') == 'text/html' or 'text/css':
    #print(re)
    html = re.read()
    #print(html)
    strings = html.decode('utf-8')
    #print(strings)

#htmlpraser subclass for collecting the urls
class finder(HTMLParser):
    def __init__(self, base):
        super().__init__()      #for accessing the instance-attributes of the mainclass
        self.base = base        
        self.links = []      

    def handle_starttag(self, tag, attrs):
        #checking for the 'anchor' tags and 'href' attributes
        
        if tag == 'a':
            print("entring the data")
            for (attr, value) in attrs:
                if attr == 'href':
                    url = urllib.parse.urljoin(self.base, value + "," + "\n") #for completing the url if any is incomplete
                    self.links.append(url)

    

fq = finder("https://automatetheboringstuff.com/") #main or homapage for the completion of any incomplete url
fq.feed(strings)        #feeding the parser with the html/css code


def store_links(lik):
    
    for i, value in enumerate(lik):
        if i == len(lik):
            
             break
        else:
          # convert the list of string into list of tuple as the function executemany() takes only
          #list of tuples as parameter
            
            tuple_list = [tuple(map(str, sub.split(', '))) for sub in lik]
            #print(i)    
            formula = ("""INSERT INTO table_name (url) VALUES (%s);""")
            #print(tuple_list)

            cursor.executemany(formula, tuple_list)
            connect.commit()
    
    
    
store_links(fq.links)
cursor.close()
connect.close()
