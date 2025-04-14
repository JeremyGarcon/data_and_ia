import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np

import matplotlib.pyplot as plt

def charger_et_preparer_donnees(temp_csv, conso_csv,
                                colonne_date="Date", colonne_temp="Temperature", colonne_conso="Consommation",
                                date_debut="2022-01-01", date_fin="2022-09-25"):
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

def modele_prediction_conso(df):
    X = df[["Temp_Moy"]]
    y = df["Conso_Moy"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Utilisation d'un modèle Random Forest
    modele = RandomForestRegressor(n_estimators=100, random_state=42)
    modele.fit(X_train, y_train)

    y_pred = modele.predict(X_test)

    # Évaluation
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("Évaluation du modèle :")
    print(f"- Coefficient R² : {r2:.2f}")
    print(f"- RMSE : {rmse:.2f} kWh")

    # Affichage du graphe
    plt.figure(figsize=(10, 5))
    plt.plot(y_test.index, y_test, label="Conso Réelle", marker="o")
    plt.plot(y_test.index, y_pred, label="Conso Prédite", linestyle="--", marker="x")
    plt.title("Prédiction de la consommation énergétique à partir de la température")
    plt.xlabel("Date")
    plt.ylabel("Consommation (kWh)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # === Graphique : prédictions vs réalité ===
    plt.figure(figsize=(6, 6))
    plt.scatter(y_test, y_pred, alpha=0.7, edgecolors="k")
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2, label="Idéal : y = x")
    plt.xlabel("Consommation réelle (kWh)")
    plt.ylabel("Consommation prédite (kWh)")
    plt.title("Précision des prédictions")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Optionnel : afficher l’erreur moyenne en pourcentage
    erreur_absolue = abs(y_test - y_pred)
    erreur_relative_pct = (erreur_absolue / y_test) * 100
    print(f"Erreur moyenne relative : {erreur_relative_pct.mean():.2f}%")

    return modele

# === Utilisation ===
df_fusionne = charger_et_preparer_donnees(
    temp_csv="/home/garcon/Documents/github/data_and_ia/data/donne_meteorologique.csv",
    conso_csv="/home/garcon/Documents/github/data_and_ia/data/Power.csv",
    date_debut="2022-01-01",
    date_fin="2022-01-25"
)

modele = modele_prediction_conso(df_fusionne)