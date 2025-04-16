
---

# 🧠 Projet : Modèles d'IA avec Scikit-learn  

Ce projet est un **MVP (Minimum Viable Product)** en Python qui explore la relation entre la **consommation énergétique** et les **données météorologiques**. Il s'appuie sur **Scikit-learn** pour modéliser les données et **Tkinter** pour l'interface graphique.  

---

## 📁 Structure du projet  

```plaintext
.
├── data/                  # Données d'entrée (consommation et météo)
├── src/                   # Code source principal
│   ├── app/               # Scripts pour interface et analyse
│   └── view_data/         # Visualisation des données brutes
├── main.py                # Point d'entrée de l'application
├── requirements.txt       # Liste des dépendances
├── Taskfile.yml           # Automatisation des tâches avec Task
└── README.md              # Documentation
```

---

## ⚙️ Fonctionnalités principales  

### 🔍 Analyse des données  
- Visualisation de la consommation d’énergie et des températures.  
- Statistiques par jour, graphiques, courbes d’évolution.

### 🤖 Modélisation IA  
- Régression linéaire avec **Scikit-learn**.  
- Prédiction de la consommation moyenne à partir de la température moyenne.  
- Affichage des performances du modèle (R², RMSE).  

### 📊 Visualisation interactive  
- Interface Tkinter simple et intuitive.  
- Affichage de résultats dans des onglets.  
- Accès au contenu du README depuis l’interface.  

---

## 🚀 Lancer l'application  

### 1. Cloner le dépôt  
```bash
git clone https://github.com/JeremyGarcon/data_and_ia.git
cd data_and_ia
```

### 2. Lancer l'application avec Task  
```bash
task run
```

---

## 🛠️ Installation de Task (si nécessaire)

### Sous Linux  
```bash
sudo snap install task --classic
```

### Ou consulter la doc officielle 👉 [taskfile.dev](https://taskfile.dev/installation/)

---

## 🔄 Tâches disponibles (via `Taskfile.yml`)  

### 🔧 Environnement virtuel  
- **Créer un environnement virtuel + installer les dépendances** :  
  ```bash
  task create_env
  ```

- **Supprimer l’environnement virtuel** :  
  ```bash
  task delete_env
  ```

---

### 📊 Visualiser les données  
- **Consommation énergétique (MWh)** :  
  ```bash
  task view_power
  ```

- **Températures (°C)** :  
  ```bash
  task view_temperature
  ```

---

### ⚙️ Construction de l'exécutable  
- **Créer un exécutable avec PyInstaller** :  
  ```bash
  task build
  ```

- **Supprimer les fichiers de build (dist/, build/)** :  
  ```bash
  task destroy_build
  ```

- **Lancer l'exécutable compilé** :  
  ```bash
  task run_build
  ```

---

## 🎯 Objectifs futurs  

- Ajouter d'autres Data Pour élargir nos test des différent model  
- Créer une interface Web avec **React(Next.Js)**.  
- Connecter une **base PostgreSQL** pour stocker les données.  

---
