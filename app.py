from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib import request

session = HTMLSession()
produit="camera+vlog"
url = f"https://www.amazon.fr/s?k={produit}&i=electronics&page=1"


def get_date(url):
    r = session.get(url)
    r.html.render (sleep=1)
    soup = BeautifulSoup(r.html. html, 'html.parser')
    return soup



def getdeals (soup) :
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    for item in products:
        #title = item.find('a',{'class': 'a-link-normal a-text-normal'}).text.strip()
        short_title = item.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).text.strip()[:25]
        #link = item.find('a', {'class':'a-link-normal a-text-normal'})['href']
        print(short_title)

def getPage(url):
    request_text = request.urlopen(url).read()
    return BeautifulSoup(request_text, 'lxml')

def getMytitleProduct(url):
    page = getPage(url)
    for item in page.find('div', {'class' : 's-main-slot s-result-list s-search-results sg-row'}).findAll({'div'}) : 
        if item.get("data-component-type") :
            title = item.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).text.strip()[:25]
            print(title,"\n-------")
#res = get_date(url)
#getdeals(res)

getMytitleProduct(url)