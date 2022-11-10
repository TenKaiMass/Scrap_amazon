# Scrap_amazon

## Preambule
n'en n'avez vous pas marre de chercher pendant des heures les meilleurs produits amazon.
vous voulez une tele, un ordi ou un slip mais le catalogue est trop vaste pour vous permettre de trouvé en quelques cliques le produit souhaiter.

## Problématique 
c'est la qu'intervient ce projet, il vous permettra en quelque phrase d'obtenir les produits les mieux notés de leur catégotries.
le resultat de votre rechrche se présentera sous forme de graphe, facilitant le choix du produit à acheter.

## Datasets
Les datasets ont generés au fil du projet au format csv, ils sont stockés
dans le dossier `dataset/`avec le nom `dataset_produit_num-dispo.csv`

Lorsque que vous scraper un produit sur amazone le resultat sera lui aussi transformé automatiquement en un dataset avec la nomination du dessus.


## Application
l'app pyhton `app.py` gère le traitement des données de A à Z
- Scrap sur amazon les données
- formatage des données
- implémentation de celle-ci dans un dataframe
- transformation en fichier `.csv`
- affichage en graph 

le fichier `demo.ipynb` est simplement la pour tester les fonction contenu dans le `app.py`.

Nous avons également le `stats.ipynb` qui va rendre visuelles les données recuperer en se basant sur le csv.

Il met donc les données en forme avec un graph permettant de trouvé les meilleurs produits de ça catégorie

> exemple si dessus avec la recherche `camera`

<img src="assets/graph1.png" 
width="800"
height="600">

## Utilisation
l'appication se lance pour le moment avec 
```bash
python3 app.py
```
Plusieurs possibilité s'offre à vous :
- vous pouvez scraper les données sur amazon
- ou utiliser le dataset disponible qui à été implementé par scraping

Lorsque que vous scraper les données, il faudra indiquer le pattern recherché (ex. tele, iphone+13, ...). Le resultat sera alors automatiquement enregistrées dans un fichier comme dit précédement, ce qui vous permettra de le réutilisé par la suite.
Le graphe affiché prends en compte le type de produit recherché, il vous sera alors demander d'inscrire le nom du produit, lorsque vous voudez utilisé un fichier afin d'avoir un titre sur le graph

> des questions vous seront poser tout au long de l'utilisation afin de vous guider 

> La partie scraping rencontre parfois un soucis sur une données particulières, il faudra alors relancer le programme, une simple boucle de requet ne fonctionne pas








