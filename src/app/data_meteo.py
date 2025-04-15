import pandas as pd
from tkinter import ttk, StringVar
from tkcalendar import DateEntry
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from src.app.methode.update_treeview import update_treeview
from src.app.methode.clear_content import clear_content


def create_tab_meteo(notebook):
    tab_data = ttk.Frame(notebook)
    notebook.add(tab_data, text="Données Météorologiques")

    file_path = "data/donne_meteorologique.csv"
    if not os.path.exists(file_path):
        messagebox.showerror("Erreur", "Le fichier de données météorologiques n'existe pas.")
        return
    data = pd.read_csv(file_path, delimiter=",", usecols=range(7))

    # Barre de recherche
    search_frame = ttk.Frame(tab_data)
    search_frame.pack(fill="x", pady=10)

    search_label = ttk.Label(search_frame, text="Rechercher par date (Calendrier) :")
    search_label.pack(side="left", padx=5)

    search_var = StringVar()
    date_entry = DateEntry(search_frame, textvariable=search_var, date_pattern="yyyy-mm-dd")
    date_entry.pack(side="left", padx=5)

    # Frame pour contenu dynamique
    content_frame = ttk.Frame(tab_data)
    content_frame.pack(fill="both", expand=True)

    def search_data():
        selected_date = search_var.get()
        filtered_data = data[data['Date'] == selected_date]
        update_treeview(filtered_data, content_frame)

    def display_data_meteo(content_frame):
        clear_content(content_frame)
        try:
            col_date = "Date"
            col_temp = "Temperature"  # Remplacez par la colonne pertinente
            title = "Température quotidienne"
            ylabel = "Température (°C)"

            temp_data = data.copy()
            temp_data[col_date] = pd.to_datetime(temp_data[col_date], errors="coerce", utc=True)
            temp_data.dropna(subset=[col_date, col_temp], inplace=True)
            temp_data.set_index(col_date, inplace=True)
            data_for_day = temp_data[col_temp].resample("D").agg(["mean", "min", "max"])

            if data_for_day.empty:
                messagebox.showinfo("Information", "Aucune donnée trouvée.")
                update_treeview(data, content_frame)
                return

            fig, ax = plt.subplots(figsize=(12, 6))
            data_for_day["mean"].plot(ax=ax, label="Moyenne")
            ax.set_title(title)
            ax.set_xlabel(col_date)
            ax.set_ylabel(ylabel)
            ax.legend()
            ax.grid(True)

            canvas = FigureCanvasTkAgg(fig, master=content_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création du graphique : {e}")
            update_treeview(data, content_frame)

    # Boutons
    search_button = ttk.Button(search_frame, text="Rechercher", command=lambda:search_data)
    search_button.pack(side="left", padx=5)

    graphique_button = ttk.Button(search_frame, text="Graphique", command=lambda: display_data_meteo(content_frame))
    graphique_button.pack(side="left", padx=5)

    back_to_table_button = ttk.Button(search_frame, text="Tableau", command=lambda: update_treeview(data, content_frame))
    back_to_table_button.pack(side="left", padx=5)

    # Affichage initial
    update_treeview(data, content_frame)
