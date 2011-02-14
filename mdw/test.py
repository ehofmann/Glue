import urllib2
from BeautifulSoup import BeautifulSoup

page = urllib2.urlopen("http://www.spiegel.de")
soup = BeautifulSoup(page)
for header in soup('h3'):
    print header

