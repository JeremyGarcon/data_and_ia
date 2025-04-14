# Projet : Modèles d'IA avec Scikit-learn  

Ce projet est un **MVP (Minimum Viable Product)** en Python utilisant **Scikit-learn** pour analyser les relations entre la consommation énergétique et les données météorologiques. Il inclut des visualisations et des analyses pertinentes.  

---

## 📂 Structure du projet  

```plaintext
 .
├── data/                  # Données nécessaires pour l'analyse et l'entraînement
├── src/                   # Scripts Python pour l'analyse, la visualisation et les modèles
│   ├── app/               # Scripts pour la gestion des données et des modèles
│   ├── view_data/         # Scripts pour visualiser les données
│   ├── main.py            # Point d'entrée principal
├── requirements.txt       # Dépendances Python
├── Taskfile.yml           # Automatisation des tâches
└── README.md              # Documentation du projet
```  

---

## ✨ Fonctionnalités principales  

### 1. Analyse des données  
- Visualisation des tendances de consommation énergétique et des températures.  
- Calcul des statistiques (moyenne, minimum, maximum).  

### 2. Modélisation IA  
- Modèle de régression linéaire avec **Scikit-learn**.  
- Prédiction de la consommation énergétique en fonction des températures.  

### 3. Visualisation  
- Graphiques interactifs pour explorer les données et les résultats.  

---

## 🚀 Installation  

### Étape 1 : Cloner le dépôt  
```bash  
git clone https://github.com/JeremyGarcon/data_and_ia.git 
cd data_and_ia  
```  

### Étape 2 : Lancer l'application  
```bash  
task run  
```  

---

## 🛠️ Installation de Task  

### Sous Linux  
1. Téléchargez Task :  
   ```bash  
   sudo snap install task --classic
   ```  
2. Vérifiez l'installation :  
   ```bash  
   task --version  
   ```  

1. Suivez les instructions d'installation sur [la page officielle de Task](https://taskfile.dev/installation/).  

4. Vérifiez l'installation :  
   ```cmd  
   task --version  
   ```  

---

## 📊 Visualisation des données  

- **Pensez à créer l'environnement avant**  
   ```bash  
   task create_env  
   ```  

- **Consommation énergétique (MWh) de 2022** :  
   ```bash  
   task view_power  
   ```  

- **Températures de 2022** :  
   ```bash  
   task view_temperature  
   ```  

---

## ⚙️ Automatisation avec Taskfile  

Le fichier `Taskfile.yml` utilise **version: '3'** pour automatiser les tâches courantes :  

- **Créer l'environnement virtuel** :  
   ```bash  
   task create_env  
   ```  

- **Supprimer l'environnement virtuel** :  
   ```bash  
   task delete_env  
   ```  

- **Lancer l'application** :  
   ```bash  
   task run  
   ```  

---

## 🎯 Objectifs futurs  

- Ajouter des modèles avancés (forêts aléatoires, réseaux neuronaux).  
- Intégrer une interface utilisateur Web (React).  
- Étendre l'analyse à d'autres périodes et intégrer plus de données météorologiques.  
- Ajouter une base de données PostgreSQL.  

---

Ce projet est une première étape pour démontrer l'utilisation de l'IA dans l'analyse des données énergétiques et météorologiques.  

