import os.path
from time import sleep

from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas
import numpy as np
import matplotlib.pyplot as plt


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
            except AttributeError or ValueError:
                price = float(0)
            list_prix.append(price)
            try:
                avis = item.find('span',{'class': 'a-size-base puis-light-weight-text s-link-centralized-style'}).text.strip()
                avis = int("".join(avis.split()))
            except AttributeError:
                avis = 0
            list_avis.append(avis)
            try:
                stars = float(item.find('span',{'class':'a-icon-alt'}).text.strip()[:3].replace(',','.'))
            except AttributeError or ValueError:
                stars = float(0)
            list_note.append(stars)

    df = pandas.DataFrame.from_dict( {"Product" : list_nom, "Prix" : list_prix, "Nombre_avis" : list_avis, "Note" : list_note})
    return df

def regroupDf(proxies,produit):
    tab = []
    for num in range(5):
        url = f"https://www.amazon.fr/s?k={produit}&page={str(num+1)}"
        print(f"page {num+1}:\n Recuperation des données :\n")
        df_tmp = getDataframeFromAmazon(url,proxies)
        tab.append(df_tmp)
    df = pandas.concat(tab,ignore_index=True)
    return df

def scraping(proxies,produit):

    df = regroupDf(proxies,produit)
    if df['Nombre_avis'].max() == 0:
        print("problème sur la recuperation des data de type avis nous allons refaire la requete...")
        valide = 0
        q = input("Voulez vous utiliser un fichier existant (sinon redemarrer le programme) ? (y/n) : ")
        if q == 'n':
            print('fin du programme...')
            exit(0)
        else:
            path = input('Entrez le nom du fichier : ')
            while valide == 0:
                try:
                    df = pandas.read_csv(f"dataset/{path}")
                except FileNotFoundError:
                    print('Erreur non du fichier...')
                    path = input('Entrez le nom du fichier : ')
                else:
                    valide = 1   
                    affichageGraph(df,produit)
    else:
        print('Recuperation terminé')
        toCsv(df=df,produit=produit)
        getStat(produit,df)

def toCsv(df : pandas.DataFrame, produit : str):
    produit = produit.replace('+','_')
    pre_path = 'dataset/'
    save = 0
    num_dispo = 1
    while save == 0: 
        if os.path.isfile(f'{os.getcwd()}/{pre_path}dataset_{produit}{num_dispo}.csv'):
            num_dispo += 1
        else:
            save = 1
            path = f"dataset/dataset_{produit}{num_dispo}.csv"
            df.to_csv(path_or_buf=path)
            print(f"le fichier {path} à été enregistré.")

def valuelabel(note,nb_avis,df2):
        for i in range(len(note)):
            if nb_avis[i] > 2500:
                plt.text(note[i],nb_avis[i],df2['Product'][i],ha='center',
                    bbox = dict(facecolor = 'cyan', alpha =0.8),size=7,)  

def getStat(produit,df):
    q = input("Voulez vous prendre le dataframe actuelle ? (y/n) : ")
    if q == 'y':
        pass
    elif q == 'n':
        valide = 0
        path = input('Entrez le nom du fichier : ')
        while valide == 0:
            try:
                df = pandas.read_csv(f"dataset/{path}")
            except FileNotFoundError:
                print('Erreur non du fichier...')
                path = input('Entrez le nom du fichier : ')
            else:
                valide = 1
    else: 
        print('erreur champs, passage par defaut == y')
    affichageGraph(df,produit)

def affichageGraph(df,produit):
    df2 = df
    nb_avis = df2['Nombre_avis']
    note = df2['Note'] 
    plt.figure(figsize= (15,10))
    plt.bar(df2['Note'],df2['Nombre_avis'],color=np.random.rand(len(df['Product']),3),width=0.5)
    valuelabel(note=note,nb_avis=nb_avis,df2=df2)
    plt.xlabel("Nombre d'avis")
    plt.ylabel("Nombre d'etoile") 
    plt.title(f'Les {produit} les plus noté selon leur note sur Amazon')
    plt.show()

session = HTMLSession()
# rentrer mnuellement a l'avenir
produit="camera+vlog"
headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/71.0.3542.0 Safari/537.36"}
url_test =  "https://httpbin.org/user-agent"
proxies = {
"http": "http://49.0.2.242:8090",
"https": "https://49.0.2.242:8090",

 }
def start():
    q = input("Voulez vous scraper les donnée (n = utiliser un fichier pour afficher son graph) ? (y/n) : ")
    if q == 'y':
       scraping(proxies,produit)
    else:
        valide = 0
        path = input('Entrez le nom du fichier : ')
        while valide == 0:
            try:
                df = pandas.read_csv(f"dataset/{path}")
            except FileNotFoundError:
                print('Erreur non du fichier...')
                path = input('Entrez le nom du fichier : ')
            else:
                valide = 1   
                affichageGraph(df,produit)

start()
exit(0)

