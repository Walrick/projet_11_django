# Projet 11 - Améliorez un projet existant en Python

--------------------------------------------------

Le projet a amélioré choisi est le projet 8 de la formation Python d'Openclassrooms, la fonction recherché a était amélioré, des filtres par catégorie et mot clé on était rajouté.

## Utilisation en local

Utiliser python 3.9 et 

> pip install -r requirements.txt

Créer un fichier .env avec la clé django

> SECRET_KEY = ""

Completer le même fichier avec les identifiants de connexion à postgreSQL (le serveur postgreSQL est obligatoire)

> USER = ""
> PASSWORD = ""
> NAME = ""
> PORT = ""

Ajouter aussi la variable STATE pour signifier a django que le lancement est bien en local (a changer en PRODUCTION pour la production)

> STATE = LOCAL

## Utilisation 

Dans la barre de recherche, entre un produit à chercher et valide.
> pain

L'appli propose des aliments se rapprochant du produit contenue dans la base de données.
> pain de mie, pain...

Cliquer sur un sélectionner sous un produit pour que l'appli propose un produit de substitution de la même catégorie et d'un meilleur nutriscore.

Vous pouvez enregistrer le produit de substitution (login nécessaire)

## Api utilisée:

Cette application utilise l'api Openfoodfacts

## Commande

Il y a plusieurs commandes pour mettre à jour la base de données.
- Sous window par exemple
> py -m manage database --help

Mettre à jour la base de données des catégories :

> py -m manage database --category update

ou 

> py -m manage database --category up

Supprimer la base de données des catégories :

> py -m manage database --category del

Mettre à jour la base de données des produits :

> py -m manage database --product update

ou 

> py -m manage database --product up

Supprimer la base de données des produits :

> py -m manage database --product del

## Tableau de la base de données

![modèle de données](data_model.png)
