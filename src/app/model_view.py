import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score   
from src.app.methode.clear_content import clear_content 


def view_model_1(frame):
    clear_content(frame)
    try:
        # Chargement des données météo
        df_temp = pd.read_csv("data/donne_meteorologique.csv", usecols=["Date", "Temperature"])
        df_temp["Date"] = pd.to_datetime(df_temp["Date"], utc=True)
        df_temp.set_index("Date", inplace=True)
        df_temp["Temperature"] = df_temp["Temperature"] - 273.15  # Kelvin -> Celsius
        temp_journalier = df_temp["Temperature"].resample("D").mean().rename("Temp_Moy")

        # Chargement des données de consommation
        df_conso = pd.read_csv("data/Power.csv", usecols=["Date", "Consommation"], sep=",", on_bad_lines="skip")
        df_conso["Date"] = pd.to_datetime(df_conso["Date"], utc=True, errors="coerce")
        df_conso.dropna(inplace=True)
        df_conso["Consommation"] = pd.to_numeric(df_conso["Consommation"], errors="coerce")
        df_conso.set_index("Date", inplace=True)
        conso_journalier = df_conso["Consommation"].resample("D").mean().rename("Conso_Moy")

        # Fusion des deux datasets
        df = pd.concat([temp_journalier, conso_journalier], axis=1).dropna()

        # Modèle de régression linéaire
        X = df[["Temp_Moy"]]
        y = df["Conso_Moy"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        modele = LinearRegression()
        modele.fit(X_train, y_train)
        y_pred = modele.predict(X_test)

        # Évaluation
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # Affichage des performances
        perf_label = ttk.Label(frame, text=f"Modèle de 1ère génération\nR² = {r2:.2f} | RMSE = {rmse:.2f} kWh", font=("Arial", 12, "bold"))
        perf_label.pack(pady=10)

        # --- Nouveau graphique : Scatter Réel vs Prédit ---
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.scatter(y_test, y_pred, alpha=0.7, edgecolors="k", color="blue")
        ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2, label="Idéal : y = x")
        ax.set_xlabel("Consommation réelle (kWh)")
        ax.set_ylabel("Consommation prédite (kWh)")
        ax.set_title("Précision des prédictions : Réel vs Prédit")
        ax.grid(True)
        ax.legend()

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    except Exception as e:
        messagebox.showerror("Erreur", f"Analyse IA échouée : {e}")
