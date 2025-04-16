import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# === Chargement et enrichissement des données ===
def charger_donnees_ameliores(temp_csv, conso_csv, date_debut, date_fin):
    # Données de température
    df_temp = pd.read_csv(temp_csv, usecols=["Date", "Temperature"])
    df_temp["Date"] = pd.to_datetime(df_temp["Date"], utc=True)
    df_temp = df_temp[(df_temp["Date"] >= date_debut) & (df_temp["Date"] <= date_fin)]
    df_temp.set_index("Date", inplace=True)
    df_temp["Temperature"] = df_temp["Temperature"] - 273.15
    temp_journalier = df_temp["Temperature"].resample("D").mean().rename("Temp_Moy")

    # Données de consommation
    df_conso = pd.read_csv(conso_csv, usecols=["Date", "Consommation"])
    df_conso["Date"] = pd.to_datetime(df_conso["Date"], utc=True, errors="coerce")
    df_conso.dropna(subset=["Date", "Consommation"], inplace=True)
    df_conso["Consommation"] = pd.to_numeric(df_conso["Consommation"], errors="coerce")
    df_conso.set_index("Date", inplace=True)
    df_conso = df_conso[(df_conso.index >= date_debut) & (df_conso.index <= date_fin)]
    conso_journalier = df_conso["Consommation"].resample("D").mean().rename("Conso_Moy")

    # Fusion
    df = pd.concat([temp_journalier, conso_journalier], axis=1).dropna()

    # Features temporelles
    df["Jour_semaine"] = df.index.dayofweek
    df["Mois"] = df.index.month

    # Moyenne glissante température & conso (3 jours)
    df["Temp_Moy_3j"] = df["Temp_Moy"].rolling(window=3).mean()
    df["Conso_Lag1"] = df["Conso_Moy"].shift(1)
    df.dropna(inplace=True)

    return df

# === Modèle amélioré ===
def entrainer_modele(df):
    X = df[["Temp_Moy", "Temp_Moy_3j", "Jour_semaine", "Mois", "Conso_Lag1"]]
    y = df["Conso_Moy"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modele = RandomForestRegressor(n_estimators=100, random_state=42)
    modele.fit(X_train, y_train)

    y_pred = modele.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print(f"➡️ R² : {r2:.2f}")
    print(f"➡️ RMSE : {rmse:.2f} kWh")

    return y_test, y_pred

# === Visualisation ===
def plot_scatter(y_test, y_pred):
    plt.figure(figsize=(6, 6))
    plt.scatter(y_test, y_pred, alpha=0.7, edgecolors="k", color="green")
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2)
    plt.xlabel("Consommation réelle (kWh)")
    plt.ylabel("Consommation prédite (kWh)")
    plt.title("Réel vs Prédit (Modèle Random Forest)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# === Lancement ===
df = charger_donnees_ameliores(
    temp_csv="/home/garcon/Documents/github/data_and_ia/data/donne_meteorologique.csv",
    conso_csv="/home/garcon/Documents/github/data_and_ia/data/Power.csv",
    date_debut="2022-01-01",
    date_fin="2022-09-25"
)

y_test, y_pred = entrainer_modele(df)
plot_scatter(y_test, y_pred)



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_erreur_mensuelle(y_test, y_pred):
    # Création DataFrame avec réel, prédit, erreur
    df_resultats = pd.DataFrame({
        "Reel": y_test,
        "Pred": y_pred
    }, index=y_test.index)

    df_resultats["Erreur_Abs"] = np.abs(df_resultats["Reel"] - df_resultats["Pred"])
    df_resultats["Mois"] = df_resultats.index.to_series().dt.to_period("M").astype(str)

    # Erreur moyenne par mois
    erreur_mensuelle = df_resultats.groupby("Mois")["Erreur_Abs"].mean()

    # Plot
    plt.figure(figsize=(12, 6))
    erreur_mensuelle.plot(kind="bar", color="coral", edgecolor="black")
    plt.title("Erreur absolue moyenne par mois", fontsize=14)
    plt.ylabel("Erreur moyenne (kWh)")
    plt.xlabel("Mois")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_erreur_mensuelle_courbe(y_test, y_pred):
    # Créer un DataFrame avec les vraies valeurs, les prédictions et les dates
    df_resultats = pd.DataFrame({
        "Reel": y_test,
        "Pred": y_pred
    }, index=y_test.index)

    # Erreur absolue
    df_resultats["Erreur_Abs"] = np.abs(df_resultats["Reel"] - df_resultats["Pred"])
    df_resultats["Mois"] = df_resultats.index.to_series().dt.to_period("M").astype(str)

    # Moyenne de l'erreur par mois
    erreur_mensuelle = df_resultats.groupby("Mois")["Erreur_Abs"].mean()

    # Tracé de la courbe
    plt.figure(figsize=(12, 6))
    plt.plot(erreur_mensuelle.index, erreur_mensuelle.values, marker="o", linestyle="-", color="crimson")
    plt.title("Évolution mensuelle de l'erreur absolue moyenne", fontsize=14)
    plt.xlabel("Mois")
    plt.ylabel("Erreur moyenne (kWh)")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()


plot_erreur_mensuelle(y_test, y_pred)
plot_erreur_mensuelle_courbe(y_test, y_pred)