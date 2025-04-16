import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# === 1. Chargement et préparation des données (12H) ===
def charger_donnees_12h(temp_csv, conso_csv,
                        colonne_date="Date", colonne_temp="Temperature", colonne_conso="Consommation",
                        date_debut="2022-01-01", date_fin="2022-09-30"):
    # Température
    df_temp = pd.read_csv(temp_csv, usecols=[colonne_date, colonne_temp])
    df_temp[colonne_date] = pd.to_datetime(df_temp[colonne_date], utc=True)
    df_temp = df_temp[(df_temp[colonne_date] >= date_debut) & (df_temp[colonne_date] < date_fin)]
    df_temp.set_index(colonne_date, inplace=True)
    df_temp[colonne_temp] = df_temp[colonne_temp] 
    temp_12h = df_temp[colonne_temp].resample("12H").mean().rename("Temp_Moy")

    # Consommation
    df_conso = pd.read_csv(conso_csv, usecols=[colonne_date, colonne_conso], sep=",", on_bad_lines="skip")
    df_conso[colonne_date] = pd.to_datetime(df_conso[colonne_date], utc=True, errors="coerce")
    df_conso.dropna(subset=[colonne_date, colonne_conso], inplace=True)
    df_conso[colonne_conso] = pd.to_numeric(df_conso[colonne_conso], errors="coerce")
    df_conso = df_conso[(df_conso[colonne_date] >= date_debut) & (df_conso[colonne_date] < date_fin)]
    df_conso.set_index(colonne_date, inplace=True)
    conso_12h = df_conso[colonne_conso].resample("12H").mean().rename("Conso_Moy")

    # Fusion
    df_fusion = pd.concat([temp_12h, conso_12h], axis=1).dropna()
    return df_fusion

# === 2. Modèle de prédiction ===
def modele_prediction(df):
    X = df[["Temp_Moy"]]
    y = df["Conso_Moy"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modele = LinearRegression()
    modele.fit(X_train, y_train)

    y_pred = modele.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print(f"➡️ R² : {r2:.2f}")
    print(f"➡️ RMSE : {rmse:.2f} kWh")

    return y_test, y_pred



# === 4. Utilisation ===
df_12h = charger_donnees_12h(
    temp_csv="data/donne_meteorologique.csv",
    conso_csv="data/Power.csv",
    date_debut="2022-01-01",
    date_fin="2022-09-25"
)

y_test_12h, y_pred_12h = modele_prediction(df_12h)




import matplotlib.pyplot as plt
import numpy as np

# === Fonction pour afficher une courbe sinusoïdale comparant consommation réelle vs prédite ===
def plot_sinusoidal_comparison(y_test, y_pred):
    plt.figure(figsize=(12, 6))

    # Création d'une plage de valeurs pour une courbe sinusoïdale
    time_index = np.arange(len(y_test))  # index des dates

    # Plot de la consommation réelle (bleu)
    plt.plot(time_index, y_test, label="Consommation réelle", color="blue", linestyle='-', linewidth=2)

    # Plot de la consommation prédite (rouge)
    plt.plot(time_index, y_pred, label="Consommation prédite", color="red", linestyle="--", linewidth=2)

    # Ajouter un effet sinusoïdal pour mieux visualiser les variations
    plt.plot(time_index, np.sin(time_index * 2 * np.pi / len(time_index)) * 10, label="Comportement cyclique simulé", color="green", linestyle=":", linewidth=2)

    plt.title("Comparaison : Consommation réelle vs Prédite (Effet Sinusoïdal)")
    plt.xlabel("Date (index temps)")
    plt.ylabel("Consommation (kWh)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# === Utilisation ===
plot_sinusoidal_comparison(y_test_12h, y_pred_12h)
