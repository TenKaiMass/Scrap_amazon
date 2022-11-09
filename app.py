from bs4 import BeautifulSoup
from requests_html import HTMLSession


session = HTMLSession()
produit="camera+vlog"
headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/71.0.3542.0 Safari/537.36"}
#url =  "https://httpbin.org/user-agent"
proxies = {
"http": "http://49.0.2.242:8090",
"https": "https://49.0.2.242:8090",
 }

def getPageRH(url,proxies):
    r = session.get(url,timeout=2)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html. html, 'html.parser')
    return soup

def getMytitleProduct(url,proxies):
    page = getPageRH(url,proxies)
    for item in page.find('div', {'class' : 's-main-slot s-result-list s-search-results sg-row'}).findAll({'div'}) : 
        if item.get("data-component-type") :
            title = item.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).text.strip()[:25]
            try:
                price = item.find('span',{'class': 'a-price-whole'}).text.strip().replace(',','.')
            except AttributeError:
                price = 0
            try:
                avis = item.find('span',{'class': 'a-size-base puis-light-weight-text s-link-centralized-style'}).text.strip()
            except AttributeError:
                avis = 0
            try:
                stars = float(item.find('span',{'class':'a-icon-alt'}).text.strip()[:3].replace(',','.'))
            except AttributeError:
                stars = 0
            print(title, f"Price : {price}; Avis : {avis}; stars : {stars}\n-------")
#res = get_date(url)
#getdeals(res)

for num in range(5):
    url = f"https://www.amazon.fr/s?k={produit}&i=electronics&page={str(num+1)}"
    print(f"page {num+1}:\n")
    getMytitleProduct(url,proxies)
# url = f"https://www.amazon.fr/s?k={produit}&i=electronics&page=1"
# getMytitleProduct(url,proxies)