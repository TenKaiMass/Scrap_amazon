from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas

session = HTMLSession()
produit="camera+vlog"
headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/71.0.3542.0 Safari/537.36"}
#url =  "https://httpbin.org/user-agent"
proxies = {
"http": "http://49.0.2.242:8090",
"https": "https://49.0.2.242:8090",
 }

def getPageRH(url : str,proxies : map):
    response = session.get(url,timeout=2)
    response.html.render(sleep=1)
    soup = BeautifulSoup(response.html. html, 'html.parser')
    return soup

def getMytitleProduct(url : str,proxies: map):
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

def getDataframeFromAmazon(url : str,proxies: map):
    list_avis = []
    list_nom = []
    list_prix = []
    list_note = []
    page = getPageRH(url,proxies)
    for item in page.find('div', {'class' : 's-main-slot s-result-list s-search-results sg-row'}).findAll({'div'}) : 
        if item.get("data-component-type") :
            title = item.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).text.strip()[:25]
            list_nom.append(title)
            try:
                price = item.find('span',{'class': 'a-price-whole'}).text.strip().replace(',','.')
            except AttributeError:
                price = 0
            list_prix.append(price)
            try:
                avis = item.find('span',{'class': 'a-size-base puis-light-weight-text s-link-centralized-style'}).text.strip()
            except AttributeError:
                avis = 0
            list_avis.append(avis)
            try:
                stars = float(item.find('span',{'class':'a-icon-alt'}).text.strip()[:3].replace(',','.'))
            except AttributeError:
                stars = 0
            list_note.append(stars)
            #print(title, f"Price : {price}; Avis : {avis}; stars : {stars}\n-------")
    df = pandas.DataFrame.from_dict( {"Product" : list_nom, "Prix" : list_prix, "Nombre_avis" : list_avis, "Note" : list_note})
    return df

def regroupDf(proxies,produit):
    tab = []
    for num in range(5):
        url = f"https://www.amazon.fr/s?k={produit}&i=electronics&page={str(num+1)}"
        #print(f"page {num+1}:\n")
        tab.append(getDataframeFromAmazon(url,proxies))

    df = pandas.concat(tab, sort=False)
    return df


def toCsv(df : pandas.DataFrame, path : str):
    df.to_csv(path_or_buf=path)

df = regroupDf(proxies,produit)

#toCsv(df=df,path="dataset/myDataset.csv")

