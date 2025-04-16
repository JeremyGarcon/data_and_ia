import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np

# === Fonction pour charger et préparer les données ===
def charger_et_preparer_donnees(temp_csv, conso_csv,
                                colonne_date="Date", colonne_temp="Temperature", colonne_conso="Consommation",
                                date_debut="2022-01-01", date_fin="2022-09-30"):
    # Charger température
    df_temp = pd.read_csv(temp_csv, usecols=[colonne_date, colonne_temp])
    df_temp[colonne_date] = pd.to_datetime(df_temp[colonne_date], utc=True)
    df_temp = df_temp[(df_temp[colonne_date] >= date_debut) & (df_temp[colonne_date] < date_fin)]
    df_temp.set_index(colonne_date, inplace=True)
    df_temp[colonne_temp] = df_temp[colonne_temp] - 273.15  # Convertir Kelvin en Celsius si nécessaire
    temp_journalier = df_temp[colonne_temp].resample("D").mean().rename("Temp_Moy")

    # Charger consommation
    df_conso = pd.read_csv(conso_csv, usecols=[colonne_date, colonne_conso], sep=",", on_bad_lines="skip")
    df_conso[colonne_date] = pd.to_datetime(df_conso[colonne_date], errors="coerce", utc=True)
    df_conso.dropna(subset=[colonne_date, colonne_conso], inplace=True)
    df_conso[colonne_conso] = pd.to_numeric(df_conso[colonne_conso], errors="coerce")
    df_conso.dropna(subset=[colonne_conso], inplace=True)
    df_conso = df_conso[(df_conso[colonne_date] >= date_debut) & (df_conso[colonne_date] < date_fin)]
    df_conso.set_index(colonne_date, inplace=True)
    conso_journalier = df_conso[colonne_conso].resample("D").mean().rename("Conso_Moy")

    # Fusionner les deux séries
    df_merged = pd.concat([temp_journalier, conso_journalier], axis=1).dropna()
    return df_merged

# === Fonction de création et d'évaluation du modèle de régression ===
def modele_prediction_conso(df):
    X = df[["Temp_Moy"]]
    y = df["Conso_Moy"]

    # Séparation en jeu d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Création et entraînement du modèle
    modele = LinearRegression()
    modele.fit(X_train, y_train)

    # Prédictions sur le jeu de test
    y_pred = modele.predict(X_test)

    # Évaluation du modèle
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("Évaluation du modèle :")
    print(f"- Coefficient R² : {r2:.2f}")
    print(f"- RMSE : {rmse:.2f} kWh")

    return y_test, y_pred

# === Fonctions de visualisation des résultats ===

# 1. Graphique des erreurs résiduelles
def plot_residuals(y_test, y_pred):
    residuals = y_test - y_pred

    plt.figure(figsize=(10, 6))
    plt.scatter(y_test.index, residuals, color='blue', alpha=0.5)
    plt.axhline(y=0, color='red', linestyle='--')  # Ligne rouge pour 0, erreur nulle
    plt.title("Erreurs résiduelles : Consommation réelle vs prédite")
    plt.xlabel("Date")
    plt.ylabel("Erreur (Consommation réelle - Consommation prédite)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 2. Graphique de la consommation réelle vs prédite
def plot_actual_vs_predicted(y_test, y_pred):
    plt.figure(figsize=(10, 6))
    plt.plot(y_test.index, y_test, label="Consommation réelle", marker="o", color="blue")
    plt.plot(y_test.index, y_pred, label="Consommation prédite", linestyle="--", color="red")
    plt.title("Consommation réelle vs prédite")
    plt.xlabel("Date")
    plt.ylabel("Consommation (kWh)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 3. Scatter plot des prédictions vs réalité
def plot_scatter_actual_vs_predicted(y_test, y_pred):
    plt.figure(figsize=(6, 6))
    plt.scatter(y_test, y_pred, alpha=0.7, edgecolors="k", color="blue")
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2, label="Idéal : y = x")
    plt.xlabel("Consommation réelle (kWh)")
    plt.ylabel("Consommation prédite (kWh)")
    plt.title("Précision des prédictions : Réel vs Prédit")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# === Fonction principale pour tout afficher ===
def visualiser_performance(y_test, y_pred):
    # 1. Affichage des résidus
    plot_residuals(y_test, y_pred)

    # 2. Affichage de la consommation réelle vs prédite
    plot_actual_vs_predicted(y_test, y_pred)

    # 3. Affichage du scatter plot
    plot_scatter_actual_vs_predicted(y_test, y_pred)

# === Utilisation ===
df_fusionne = charger_et_preparer_donnees(
    temp_csv="/home/garcon/Documents/github/data_and_ia/data/donne_meteorologique.csv",
    conso_csv="/home/garcon/Documents/github/data_and_ia/data/Power.csv",
    date_debut="2022-01-01",
    date_fin="2022-09-25"
)

y_test, y_pred = modele_prediction_conso(df_fusionne)

# Visualisation des performances du modèle
visualiser_performance(y_test, y_pred)
