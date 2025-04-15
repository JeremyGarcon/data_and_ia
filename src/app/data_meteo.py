import pandas as pd
import matplotlib.pyplot as plt
from tkinter import ttk, StringVar
from tkcalendar import DateEntry
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

from src.app.methode.update_treeview import update_treeview
from src.app.methode.clear_content import clear_content


def create_tab_meteo(notebook):
    tab_data = ttk.Frame(notebook)
    notebook.add(tab_data, text="Données Météorologiques")

    file_path = "data/donnees-synop-essentielles-omm.csv"
    if not os.path.exists(file_path):
        messagebox.showerror("Erreur", "Le fichier de données météorologiques n'existe pas.")
        return

    try:
        # Chargement des données
        data = pd.read_csv(file_path, delimiter=";", encoding='ISO-8859-1', header=0)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de lecture du fichier : {e}")
        return

    # Vérification colonne Date
    if "Date" not in data.columns:
        messagebox.showerror("Erreur", "Colonne 'Date' non trouvée dans les données.")
        return

    # Conversion des dates
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce", utc=True)

    # Interface de recherche
    search_frame = ttk.Frame(tab_data)
    search_frame.pack(fill="x", pady=10)

    ttk.Label(search_frame, text="Rechercher par date (Calendrier) :").pack(side="left", padx=5)

    search_var = StringVar()
    date_entry = DateEntry(search_frame, textvariable=search_var, date_pattern="yyyy-mm-dd")
    date_entry.pack(side="left", padx=5)

    content_frame = ttk.Frame(tab_data)
    content_frame.pack(fill="both", expand=True)

    # Recherche par date
    def search_data():
        selected_date = search_var.get()
        if selected_date:
            filtered_data = data[data["Date"].dt.strftime('%Y-%m-%d') == selected_date]
            if filtered_data.empty:
                messagebox.showinfo("Information", "Aucune donnée trouvée pour cette date.")
            else:
                update_treeview(filtered_data, content_frame)
        else:
            messagebox.showinfo("Information", "Veuillez sélectionner une date.")

    # Affichage du graphique température
    def display_data_meteo(content_frame):
        clear_content(content_frame)
        try:
            col_date = "Date"

            # Recherche automatique d'une colonne de température
            temp_cols = "Temperature"
            if not temp_cols:
                messagebox.showerror("Erreur", "Aucune colonne contenant 'Température' trouvée.")
                update_treeview(data, content_frame)
                return

            col_temp = temp_cols # Première colonne contenant "Température"

            temp_data = data[[col_date, col_temp]].dropna().copy()
            temp_data.set_index(col_date, inplace=True)

            if not pd.api.types.is_datetime64_any_dtype(temp_data.index):
                messagebox.showerror("Erreur", "La colonne 'Date' n'est pas au bon format.")
                return

            # Regroupement par jour
            daily_data = temp_data.resample("D")[col_temp].agg(["mean", "min", "max"])

            if daily_data.empty:
                messagebox.showinfo("Information", "Aucune donnée trouvée pour le graphique.")
                update_treeview(data, content_frame)
                return

            # Création du graphique
            fig, ax = plt.subplots(figsize=(12, 6))
            daily_data["mean"].plot(ax=ax, label="Moyenne", marker="o", linestyle="-")
            daily_data["min"].plot(ax=ax, label="Min", linestyle="--")
            daily_data["max"].plot(ax=ax, label="Max", linestyle="--")

            ax.set_title("Température quotidienne")
            ax.set_xlabel("Date")
            ax.set_ylabel("Température (°C)")
            ax.legend()
            ax.grid(True)

            canvas = FigureCanvasTkAgg(fig, master=content_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage du graphique : {e}")
            update_treeview(data, content_frame)

    # Boutons
    ttk.Button(search_frame, text="Rechercher", command=search_data).pack(side="left", padx=5)
    ttk.Button(search_frame, text="Graphique", command=lambda: display_data_meteo(content_frame)).pack(side="left", padx=5)
    ttk.Button(search_frame, text="Tableau", command=lambda: update_treeview(data, content_frame)).pack(side="left", padx=5)

    # Affichage initial des données dans le tableau
    update_treeview(data, content_frame)
