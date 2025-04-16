import pandas as pd
import matplotlib.pyplot as plt
from tkinter import ttk, StringVar, messagebox
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

from src.app.methode.update_treeview import update_treeview
from src.app.methode.clear_content import clear_content


def create_tab_meteo(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Données Météo de 1er Génération")

    file_path = "data/donne_meteorologique.csv"
    if not os.path.exists(file_path):
        messagebox.showerror("Erreur", "Le fichier de données météorologiques est introuvable.")
        return

    try:
        df = pd.read_csv(file_path, delimiter=",", encoding="ISO-8859-1")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de lecture du fichier : {e}")
        return

    if "Date" not in df.columns:
        messagebox.showerror("Erreur", "Colonne 'Date' absente dans les données.")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True)

    # Interface de recherche par date
    search_frame = ttk.Frame(tab)
    search_frame.pack(fill="x", pady=10)

    ttk.Label(search_frame, text="Rechercher par date :").pack(side="left", padx=5)
    date_var = StringVar()
    date_entry = DateEntry(search_frame, textvariable=date_var, date_pattern="yyyy-mm-dd")
    date_entry.pack(side="left", padx=5)

    content_frame = ttk.Frame(tab)
    content_frame.pack(fill="both", expand=True)

    def search_data():
        date = date_var.get()
        if date:
            result = df[df["Date"].dt.strftime("%Y-%m-%d") == date]
            if result.empty:
                messagebox.showinfo("Information", "Aucune donnée trouvée pour cette date.")
            update_treeview(result, content_frame)
        else:
            messagebox.showinfo("Information", "Veuillez sélectionner une date.")

    def display_graph():
        clear_content(content_frame)
        try:
            # Trouver la première colonne contenant "température"
            temp_cols = "Temperature"
            if not temp_cols:
                messagebox.showerror("Erreur", "Aucune colonne de température trouvée.")
                update_treeview(df, content_frame)
                return

            temp_col = temp_cols
            temp_df = df[["Date", temp_col]].dropna().copy()
            temp_df.set_index("Date", inplace=True)

            daily = temp_df.resample("D")[temp_col].agg(["mean", "min", "max"])

            if daily.empty:
                messagebox.showinfo("Information", "Aucune donnée pour le graphique.")
                update_treeview(df, content_frame)
                return

            fig, ax = plt.subplots(figsize=(12, 6))
            daily["mean"].plot(ax=ax, label="Moyenne", marker="o")
            daily["min"].plot(ax=ax, label="Min", linestyle="--")
            daily["max"].plot(ax=ax, label="Max", linestyle="--")

            ax.set_title("Température quotidienne")
            ax.set_xlabel("Date")
            ax.set_ylabel("Température (°C)")
            ax.legend()
            ax.grid(True)

            canvas = FigureCanvasTkAgg(fig, master=content_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur d'affichage du graphique : {e}")
            update_treeview(df, content_frame)

    # Boutons
    ttk.Button(search_frame, text="Rechercher", command=search_data).pack(side="left", padx=5)
    ttk.Button(search_frame, text="Graphique", command=display_graph).pack(side="left", padx=5)
    ttk.Button(search_frame, text="Tableau", command=lambda: update_treeview(df, content_frame)).pack(side="left", padx=5)

    update_treeview(df, content_frame)
