# Documentation Technique et Fonctionnelle du Projet

## Introduction

Ce projet combine une application de scraping web utilisant Scrapy et une API avec Flask, le tout orchestré avec Docker. Les données extraites via le spider Scrapy sont sauvegardées dans une base de données MongoDB. Une interface web permet de visualiser les artistes, et une authentification basée sur JWT sécurise l'accès aux fonctionnalités.

Le projet comprend les éléments suivants :
- **Scraping avec Scrapy** : Extraction des informations sur les artistes depuis last.fm et insertion directe dans la base de donnée MongoDB via des pipelines
- **Base de données MongoDB** : Stockage des artistes extraits et des utilisateurs
- **API Flask avec authentification JWT** : Interface pour accéder et manipuler les données
- **Docker** : Facilitation du déploiement et de la gestion des dépendances

Les artistes sont catégorisés par genre musical (RnB, Pop, Hip-Hop, Alternative, Blues, Jazz, Indie, 80s, et Rap) et regroupés en une base de données contenant près de 2000 artistes.

---

## Prérequis

Avant de démarrer, assurez-vous d'avoir installé les outils suivants :
1. **Docker** et **Docker Compose** pour l'orchestration des conteneurs.
2. **Python 3.9+** si vous souhaitez exécuter localement sans Docker.
3. Une installation de **MongoDB** (incluse dans Docker si vous suivez les étapes ci-dessous).

---

## Lancement du projet

### Étapes avec Docker

1. Clonez le projet :
   ```bash
   git clone <url_du_dépôt>
   cd <répertoire_du_projet>
   ```

2. Démarrez le projet avec Docker Compose :
   ```bash
   docker-compose up --build
   ```

3. **Option pour le scraping** :  
   Par défaut, le scraping se lance automatiquement lors de l'exécution de `docker-compose up`. Pour désactiver cette étape (et éviter une nouvelle insertion des données à chaque démarrage), commentez la ligne suivante dans le Dockerfile du dossier `Scrapy` :
   ```dockerfile
   CMD ["scrapy", "crawl", "artistsFM"]
   ```
   Et décommentez la ligne suivante :
   ```dockerfile
   CMD ["tail", "-f", "/dev/null"]
   ```

4. Une fois lancé, l'interface web sera disponible à l'adresse suivante (par défaut) :  
   [http://localhost:5000](http://localhost:5000).

---

## Fonctionnalités

### 1. **Scraping des artistes**

Le spider Scrapy extrait des données des pages de genres musicaux sur last.fm. Voici les principales étapes:
- Parcours de 10 pages par genre (RnB, Pop, Hip-Hop, etc.)
- Extraction des informations principales (nom, auditeurs, albums, chansons et tags)
- Sauvegarde des données dans MongoDB, base de donnée

### 2. **API avec authentification JWT**

- **Enregistrement** (`/register`) : Permet aux utilisateurs de créer un compte.
- **Connexion** (`/login`) : Génère un jeton JWT pour accéder aux données.
- **Accès aux artistes** (`/artists`) : Affiche les artistes paginés et/ou filtrés par genre. L'accès nécessite un jeton JWT valide.

### 3. **Pagination et filtres**

- **Pagination** : Naviguez entre les pages des artistes avec les paramètres `page` et `limit` 
  Exemple : `http://localhost:5000/artists?page=2&limit=10`.
- **Filtrage par genre** : Filtrez les artistes par genre avec le paramètre `genre`
  Exemple : `http://localhost:5000/artists?genre=pop`

### 4. **Base de données MongoDB**

- La base de données MongoDB est utilisée pour stocker :
  - Les informations des artistes extraits.
  - Les utilisateurs et leurs mots de passe (hachés).

---

## Structure du projet

### **Docker**

- **Dockerfile (Scrapy)** : Contient la configuration pour exécuter le spider et insérer les données dans MongoDB.
- **Dockerfile (API Flask)** : Configure l'environnement pour l'application web et l'API.
- **docker-compose.yml** : Orchestre les services pour Scrapy, Flask et MongoDB.

### **Scrapy**

- **Fichier** : `artists_spider.py`
- **Pipeline MongoDB** : Automatiquement configuré pour insérer les artistes extraits dans la base

### **API Flask**

- **Fichier** : `affiche.py`
- **Routes principales** :
  - `/register` : Inscription
  - `/login` : Connexion
  - `/artists` : Accès sécurisé aux artistes

### **Base de données MongoDB**

- **Service Docker MongoDB** : Lance un conteneur MongoDB pour stocker les données

---

## Exemple d'utilisation

### 1. Inscription

- Accédez à [http://localhost:5000/register](http://localhost:5000/register).
- Entrez un nom d'utilisateur et un mot de passe
- Une fois inscrit, connectez-vous

### 2. Connexion

- Accédez à [http://localhost:5000/login](http://localhost:5000/login)
- Entrez vos identifiants
- Une fois connecté, un cookie contenant un token JWT sera généré pour accéder aux artistes

### 3. Visualisation des artistes

- Accédez à [http://localhost:5000/artists](http://localhost:5000/artists) pour voir la liste des artistes

---

## Notes importantes

1. **Scraping initial** : La première exécution peut prendre quelques minutes car Scrapy extrait et insère les données dans MongoDB
2. **Dépendances MongoDB** : Si vous n'utilisez pas Docker, assurez-vous que MongoDB est installé et accessible à l'adresse `mongodb://localhost:27017`

---

## Problèmes courants et solutions

- **Page vide dans l'interface**  
  Attendez la fin du scraping (visible dans la console) et actualisez la page


