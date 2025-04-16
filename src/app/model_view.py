# filepath: data_and_ia/src/app/model_view.py

"""
Ce module gère l'affichage et l'analyse d'un modèle de régression linéaire dans l'interface graphique de l'application.

Fonctionnalités principales :
- `view_model_1(frame)`: Affiche dans un onglet Tkinter les résultats d’un modèle IA de 1ère génération.
  Il s’agit d’un modèle de régression linéaire simple qui prédit la consommation d’énergie moyenne à partir de la température moyenne.
  Cette fonction affiche également un graphique de comparaison entre les valeurs réelles et prédites pour évaluer visuellement les performances du modèle.
  Les métriques affichées sont le R² (coefficient de détermination) et le RMSE (erreur quadratique moyenne).

- `load_data()`: Fonction utilitaire qui fusionne deux sources de données (température et consommation),
  applique un traitement de nettoyage et de transformation (resampling journalier, conversion de format),
  et retourne un DataFrame prêt à être utilisé pour l’entraînement du modèle.

Ce module utilise :
- `sklearn` pour la modélisation,
- `matplotlib` pour l'affichage graphique dans Tkinter,
- `tkinter.ttk` pour les widgets de l'interface graphique.

Ce script est conçu pour être intégré dans l'application principale de visualisation IA via le bouton "Voir les Modèles".
"""

# === Import des bibliothèques nécessaires ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score   

# === Import des modules de l'application ===
from src.app.methode.clear_content import clear_content 


def view_model_1(frame):
    """
    Affiche un modèle simple de régression linéaire dans une interface Tkinter.

    Args:
        frame (tk.Frame): Le conteneur Tkinter où le modèle sera affiché.
    """
    # Nettoyer le contenu actuel du cadre
    clear_content(frame)

    try:
        # Charger et fusionner les données météo et consommation
        df = load_data()

        # === Préparation des données pour la régression ===
        X = df[["Temp_Moy"]]  # Variable indépendante : température moyenne
        y = df["Conso_Moy"]   # Variable dépendante : consommation moyenne

        # Séparer les données en jeu d'entraînement et de test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # === Entraînement du modèle ===
        modele = LinearRegression()
        modele.fit(X_train, y_train)
        y_pred = modele.predict(X_test)

        # === Évaluation du modèle ===
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # Affichage des scores dans l'interface
        perf_label = ttk.Label(
            frame,
            text=f"Modèle de 1ère génération\nR² = {r2:.2f} | RMSE = {rmse:.2f} kWh",
            font=("Arial", 12, "bold")
        )
        perf_label.pack(pady=10)

        # === Affichage graphique : Réel vs Prédit ===
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.scatter(y_test, y_pred, alpha=0.7, edgecolors="k", color="blue")
        ax.plot(
            [y_test.min(), y_test.max()],
            [y_test.min(), y_test.max()],
            "r--",
            lw=2,
            label="Idéal : y = x"
        )
        ax.set_xlabel("Consommation réelle (kWh)")
        ax.set_ylabel("Consommation prédite (kWh)")
        ax.set_title("Précision des prédictions : Réel vs Prédit")
        ax.grid(True)
        ax.legend()

        # Intégrer le graphique dans Tkinter
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    except Exception as e:
        # Gestion des erreurs d'affichage ou de calcul
        messagebox.showerror("Erreur", f"Analyse IA échouée : {e}")


def load_data():
    """
    Charge et fusionne les données de consommation et de température
    pour une analyse conjointe.

    Returns:
        DataFrame: Données journalières combinées prêtes pour l'analyse.
    """

    # === Données de consommation énergétique ===
    # Lecture des données de consommation énergétique depuis un fichier CSV
    # - `usecols`: Sélectionne uniquement les colonnes "Date" et "Consommation"
    # - `sep`: Définit le séparateur de colonnes comme une virgule
    # - `on_bad_lines`: Ignore les lignes mal formatées
    df_conso = pd.read_csv(
        "data/Power.csv", usecols=["Date", "Consommation"], sep=",", on_bad_lines="skip"
    )
    
    # Conversion de la colonne "Date" en type datetime avec gestion des erreurs
    # - `utc`: Définit le fuseau horaire en UTC
    # - `errors`: Définit le comportement en cas d'erreur (ici, "coerce" remplace les erreurs par NaT)
    df_conso["Date"] = pd.to_datetime(df_conso["Date"], utc=True, errors="coerce")

    # Suppression des lignes contenant des valeurs manquantes
    df_conso.dropna(inplace=True)
    
    # Conversion de la colonne "Consommation" en type numérique avec gestion des erreurs
    # - `errors`: Définit le comportement en cas d'erreur (ici, "coerce" remplace les erreurs par NaN)
    df_conso["Consommation"] = pd.to_numeric(df_conso["Consommation"], errors="coerce")
    # Définition de la colonne "Date" comme index du DataFrame
    # Cela permet de manipuler les données temporelles plus facilement
    df_conso.set_index("Date", inplace=True)
    
    # Agrégation des données par jour pour calculer la moyenne journalière de consommation
    # - `resample("D")`: Regroupe les données par jour
    # - `mean()`: Calcule la moyenne pour chaque groupe
    # - `rename`: Renomme la série résultante en "Conso_Moy" pour plus de clarté
    conso_journalier = df_conso["Consommation"].resample("D").mean().rename("Conso_Moy")

    # === Données météo (température) ===
    # Lecture des données météorologiques depuis un fichier CSV
    # - `usecols`: Sélectionne uniquement les colonnes "Date" et "Temperature"
    df_temp = pd.read_csv("data/donne_meteorologique.csv", usecols=["Date", "Temperature"])
    
    # Conversion de la colonne "Date" en type datetime pour une manipulation temporelle
    # - `utc`: Définit le fuseau horaire en UTC
    df_temp["Date"] = pd.to_datetime(df_temp["Date"], utc=True)
    
    # Définition de la colonne "Date" comme index du DataFrame
    df_temp.set_index("Date", inplace=True)
    
    # Conversion de la température de Kelvin à Celsius
    # - La conversion est effectuée en soustrayant 273.15
    df_temp["Temperature"] = df_temp["Temperature"] - 273.15
    
    # Agrégation des données par jour pour calculer la moyenne journalière de température
    # - `resample("D")`: Regroupe les données par jour
    # - `mean()`: Calcule la moyenne pour chaque groupe
    # - `rename`: Renomme la série résultante en "Temp_Moy" pour plus de clarté
    temp_journalier = df_temp["Temperature"].resample("D").mean().rename("Temp_Moy")

    # === Fusion des deux séries de données ===
    df_merged = pd.concat([temp_journalier, conso_journalier], axis=1).dropna()

    return df_merged
