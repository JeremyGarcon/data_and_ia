 === Import des bibliothèques nécessaires ===
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




def view_model_2(frame):
    """
    Affiche un modèle de régression linéaire basé sur des données resamplées toutes les 12 heures,
    avec une visualisation sinusoïdale dans l'interface Tkinter.

    Args:
        frame (tk.Frame): Le conteneur Tkinter où le modèle sera affiché.
    """
    clear_content(frame)

    try:
        # === Données 12H ===
        df = load_data_12h()

        X = df[["Temp_Moy"]]
        y = df["Conso_Moy"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        modele = LinearRegression()
        modele.fit(X_train, y_train)
        y_pred = modele.predict(X_test)

        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # Affichage des performances
        perf_label = ttk.Label(
            frame,
            text=f"Modèle 12H\nR² = {r2:.2f} | RMSE = {rmse:.2f} kWh",
            font=("Arial", 12, "bold")
        )
        perf_label.pack(pady=10)

        # === Courbe sinusoïdale ===
        fig, ax = plt.subplots(figsize=(8, 5))

        time_index = np.arange(len(y_test))
        y_test_sorted = y_test.reset_index(drop=True)
        y_pred_sorted = pd.Series(y_pred).reset_index(drop=True)

        ax.plot(time_index, y_test_sorted, label="Consommation réelle", color="blue", linewidth=2)
        ax.plot(time_index, y_pred_sorted, label="Consommation prédite", color="red", linestyle="--", linewidth=2)
        ax.plot(time_index, np.sin(time_index * 2 * np.pi / len(time_index)) * 10,
        label="Comportement cyclique simulé", color="green", linestyle=":", linewidth=2)

        ax.set_title("Comparaison : Réel vs Prédit")
        ax.set_xlabel("Index Temps")
        ax.set_ylabel("Consommation (kWh)")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    except Exception as e:
        messagebox.showerror("Erreur", f"Analyse IA 12H échouée : {e}")


def load_data_12h():
    """
    Charge et fusionne les données de température et consommation, échantillonnées toutes les 12 heures.

    Returns:
        DataFrame: Données prêtes pour le modèle de prédiction 12H.
    """
    df_temp = pd.read_csv("data/donne_meteorologique.csv", usecols=["Date", "Temperature"])
    df_temp["Date"] = pd.to_datetime(df_temp["Date"], utc=True)
    df_temp.set_index("Date", inplace=True)
    df_temp["Temperature"] = df_temp["Temperature"] - 273.15
    temp_12h = df_temp["Temperature"].resample("12H").mean().rename("Temp_Moy")

    df_conso = pd.read_csv("data/Power.csv", usecols=["Date", "Consommation"], sep=",", on_bad_lines="skip")
    df_conso["Date"] = pd.to_datetime(df_conso["Date"], utc=True, errors="coerce")
    df_conso["Consommation"] = pd.to_numeric(df_conso["Consommation"], errors="coerce")
    df_conso.dropna(inplace=True)
    df_conso.set_index("Date", inplace=True)
    conso_12h = df_conso["Consommation"].resample("12H").mean().rename("Conso_Moy")

    df_merged = pd.concat([temp_12h, conso_12h], axis=1).dropna()
    return df_merged
  
