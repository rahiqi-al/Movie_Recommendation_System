# Système de Recommandation de Films - Jay-Z Entertainment

## Description du Projet
Ce projet vise à développer un système de recommandation de films en temps réel en exploitant les données de MovieLens. Il intègre l'analyse Big Data et l'apprentissage automatique pour offrir une expérience utilisateur personnalisée. Les principales technologies utilisées sont Apache Spark, Elasticsearch, Kibana et Flask.

---

## Objectifs
- Collecter, traiter et analyser les données de MovieLens.
- Construire un modèle de recommandation performant.
- Intégrer les données dans Elasticsearch pour une recherche efficace.
- Visualiser les résultats avec Kibana.
- Développer une API REST pour obtenir des recommandations personnalisées.
- Assurer la conformité au RGPD et mettre en place une gouvernance des données efficace.

---

## Technologies Utilisées
- **Apache Spark** : Prétraitement et analyse des données.
- **Elasticsearch** : Stockage et recherche des données recommandées.
- **Kibana** : Visualisation et suivi des performances.
- **Flask** : API REST pour l'accès aux recommandations.
- **Dataset MovieLens** : Base de données des interactions utilisateur et métadonnées des films.

---

## Configuration de l'Environnement
### Installation des dépendances :
- Apache Spark
- Elasticsearch
- Kibana
- Flask

### Acquisition des Données :
- Téléchargement des fichiers MovieLens
- Préparation et nettoyage des données

---

## Prétraitement des Données avec Apache Spark
- Chargement des données
- Gestion des valeurs manquantes
- Conversion des types de données
- Division des genres en liste
- Fusion des notes moyennes avec les films

---

## Construction du Modèle de Recommandation
- Choix du modèle : **Alternating Least Squares (ALS)**.
- Entraînement et évaluation du modèle.
- Génération des recommandations.

---

## Intégration des Données dans Elasticsearch
- Transformation et ingestion des données.

---

## Visualisation avec Kibana
- **Top 10 des films populaires**
- **Distribution des genres**
- **Activité des utilisateurs**
- **Notes moyennes par film**

---

## Développement de l'API Flask
- Endpoint pour recevoir un titre de film.
- Identification des utilisateurs ayant interagi avec ce film.
- Utilisation de leurs IDs pour générer des recommandations.
- Récupération des recommandations depuis Elasticsearch.

---

## Conformité au RGPD & Gouvernance des Données
- Assurer la protection des données personnelles.
- Mettre en place des politiques de gouvernance des données.
- Maintenir un catalogue de données détaillé pour la traçabilité.

---

## Installation & Exécution
1. Cloner le projet :
   ```bash
   git clone https://github.com/rahiqi-al/Movie_Recommendation_System.git
   ```
2. Installer les dépendances Python :
   ```bash
   pip install -r requirements.txt
   ```
3. Lancer Elasticsearch et Kibana.
4. Démarrer l'API Flask :
   ```bash
   python app.py
   ```
5. Accéder à Kibana pour la visualisation.

