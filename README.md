# Projet : Modèles d'IA avec Scikit-learn  

Ce projet est un **MVP (Minimum Viable Product)** développé en Python, utilisant la bibliothèque **Scikit-learn** pour construire et analyser des modèles d'intelligence artificielle. L'objectif principal est d'explorer les relations entre la consommation énergétique et les données météorologiques, tout en fournissant des visualisations et des analyses pertinentes.  

## Arborescence du projet  

Voici la structure du projet :  

```
/data_and_ia  
├── data/  
│   ├── data_énergie_trié_modifié.csv  
│   ├── donne_meteorologique.csv  
│   └── eCO2mix_RTE_Bretagne_Annuel-Definitif_2022.csv  
├── env_panda/  
│   ├── bin/  
│   ├── lib/  
│   └── pyvenv.cfg  
├── src/  
│   ├── main.py  
│   ├── test_power.py  
│   ├── test_meteo.py  
│   ├── test.py  
│   ├── view_power.py  
│   └── view_temperature.py  
├── requirements.txt  
├── Taskfile.yml  
└── README.md  
```  

### Description des dossiers et fichiers  

- **`data/`** : Contient les fichiers de données nécessaires pour l'entraînement et l'analyse des modèles.  
- **`env_panda/`** : Environnement virtuel Python pour isoler les dépendances du projet.  
- **`src/`** : Contient les scripts Python pour l'analyse des données, la visualisation et la création des modèles.  
    - **`main.py`** : Point d'entrée principal du projet.  
    - **`view_power.py`** : Analyse détaillée de la consommation énergétique quotidienne.  
    - **`view_temperature.py`** : Analyse détaillée des températures quotidiennes.  
- **`requirements.txt`** : Liste des dépendances Python nécessaires pour exécuter le projet.  
- **`Taskfile.yml`** : Automatisation des tâches courantes (exécution des scripts, visualisation des données, etc.).  

## Fonctionnalités principales  

### 1. Analyse des données  
- Visualisation des tendances de consommation énergétique et des températures.  
- Calcul des statistiques (moyenne, minimum, maximum) sur des périodes définies.  

### 2. Modélisation IA  
- Utilisation de **Scikit-learn** pour entraîner un modèle de régression linéaire.  
- Prédiction de la consommation énergétique en fonction des températures.  

### 3. Visualisation  
- Graphiques interactifs pour explorer les données et les résultats des modèles.  

## Installation  

1. Clonez le dépôt :  
   ```bash  
   git clone https://github.com/JeremyGarcon/data_and_ia.git 
   cd data_and_ia  
   ```  

2. Activez l'environnement virtuel :  
   ```bash  
   source env_panda/bin/activate  
   ```  

## Visualisation des données :  

1. Visualiser les données de la consommation en MWH de 2022 :  
   ```bash  
   task view_power  
   ```  

2. Visualiser les données de la température de 2022 :  
   ```bash  
   task view_temperature  
   ```  

3. Explorez les données et les résultats des modèles via les scripts dédiés dans le dossier **`src/`**.  

## Objectifs futurs  

- Ajouter des modèles plus complexes (forêts aléatoires, réseaux neuronaux).  
- Intégrer une interface utilisateur pour une meilleure interaction Web (React).  
- Étendre l'analyse à d'autres périodes.  
- Intégrer plus de données météorologiques dans le modèle ayant une corrélation sur la consommation énergétique.  
- Intégration d'une BDD PostgreSQL.  

---  
Ce projet constitue une première étape pour démontrer la faisabilité d'utiliser des modèles d'IA dans l'analyse des données énergétiques et météorologiques.  
