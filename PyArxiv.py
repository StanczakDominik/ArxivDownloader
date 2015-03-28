#!python3
import feedparser, re, urllib.request
feeds = ["http://export.arxiv.org/rss/physics.plasm-ph", "http://export.arxiv.org/rss/physics.comp-ph"]#, "http://export.arxiv.org/rss/quant-ph"]


###logging##
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler=logging.FileHandler('errors.log')
handler.setLevel(logging.INFO)
formatter=logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info('Running PyArxiv')
###end logging###

def check_string(string, stream):
    found = False
    for line in stream:
        if re.search(r'{0}'.format(string),line):
            return True
    return False

d=[feedparser.parse(feed) for feed in feeds]
database=open('database', 'r+')
database.seek(0)
for feed in d:
    print("\n\n\t\t", feed['href'][28:])
    for i in feed['entries']:
        article = i['title']
        match = re.search(r'arXiv:.*? ', article)
        title = re.search(r'^.*? \(arXiv', article).group()[:-8].replace(':', ',').replace('$', '').replace('\\', '')
        print(title)
        if(check_string(title, database)):
            print("\tAlready in database.")
        else:
            database.seek(0, 2)
            database.write(title + "\n")
            artid=match.group()[6:]
            url=('http://www.arxiv.org/pdf/' + artid)
            try:
                urllib.request.urlretrieve(url, "D:\\Desktop\\Arxiv\\" + title + ".pdf")
            except:
                logger.exception('Download failure')
                raise
        
database.close()
print ("WORK COMPLETE.")
input()
