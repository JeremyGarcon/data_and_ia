import pandas as pd
from tkinter import ttk, StringVar
from tkcalendar import DateEntry
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from src.app.methode.update_treeview import update_treeview
from src.app.methode.clear_content import clear_content


def create_tab_power(notebook):
    tab_data = ttk.Frame(notebook)
    notebook.add(tab_data, text="Données de Consommation Energétique")

    file_path = "data/Power.csv"
    if not os.path.exists(file_path):
        messagebox.showerror("Erreur", "Le fichier de données Power n'existe pas.")
        return
    data = pd.read_csv(file_path, delimiter=",", usecols=range(7))

    # Barre de recherche
    search_frame = ttk.Frame(tab_data)
    search_frame.pack(fill="x", pady=10)

    search_label = ttk.Label(search_frame, text="Rechercher par date (Calendrier) :")
    search_label.pack(side="left", padx=5)

    # Doc : https://www.askpython.com/python-modules/tkinter/stringvar-with-examples
    search_var = StringVar()
    date_entry = DateEntry(search_frame, textvariable=search_var, date_pattern="yyyy-mm-dd")
    date_entry.pack(side="left", padx=5)

    # Frame pour contenu dynamique
    content_frame = ttk.Frame(tab_data)
    content_frame.pack(fill="both", expand=True)


    def search_data():
        # Récupère la date sélectionnée dans la barre de recherche
        selected_date = search_var.get()
        
        # Filtre les données pour inclure uniquement les lignes correspondant exactement à la date sélectionnée
        filtered_data = data[data['Date'] == selected_date]
        
        # Met à jour l'affichage du tableau avec les données filtrées
        update_treeview(filtered_data, content_frame)
        
    
    def display_data_power(content_frame):
        clear_content(content_frame)
        try:
            Colonne_date = "Date"
            Colonne_conso = "Consommation"
            Title = "Consommation énergétique"
            ylabel = "Consommation énergétique"

            temp_data = data.copy()
            temp_data[Colonne_date] = pd.to_datetime(temp_data[Colonne_date], errors="coerce", utc=True)
            temp_data.dropna(subset=[Colonne_date, Colonne_conso], inplace=True)
            temp_data.set_index(Colonne_date, inplace=True)
            data_for_day = temp_data[Colonne_conso].resample("D").agg(["mean", "min", "max"])

            if data_for_day.empty:
                messagebox.showinfo("Information", "Aucune donnée trouvée.")
                update_treeview(data, content_frame)
                return
            # Doc : https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html#
            fig, ax = plt.subplots(figsize=(12, 6)) # Crée une figure et un axe
            # Doc : https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html
            data_for_day["mean"].plot(ax=ax, label="Moyenne") # Moyenne
            ax.set_title(Title) # Titre du graphique
            ax.set_xlabel(Colonne_date) # Titre de l'axe des x
            ax.set_ylabel(ylabel) # Titre de l'axe des y
            ax.legend()
            ax.grid(True) # Affiche une grille sur le graphique

            # Crée un widget pour afficher le graphique dans le cadre, par défaut plt affiche dans une nouvelle fenêtre
            canvas = FigureCanvasTkAgg(fig, master=content_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création du graphique : {e}")
            update_treeview(data, content_frame)

    # Boutons
    search_button = ttk.Button(search_frame, text="Rechercher", command=lambda:search_data)
    search_button.pack(side="left", padx=5)

    graphique_button = ttk.Button(search_frame, text="Graphique", command=lambda:display_data_power(content_frame))
    graphique_button.pack(side="left", padx=5)

    back_to_table_button = ttk.Button(search_frame, text="Tableau", command=lambda: update_treeview(data, content_frame))
    back_to_table_button.pack(side="left", padx=5)

    # Affichage initial
    update_treeview(data, content_frame)

        # Doc https://matplotlib.org/stable/api/figure_api.html
        # plt.figure(figsize=(12, 6))
        # data_for_day["mean"].plot(label="Moyenne")
        # plt.title(f"Consommation énergétique quotidienne ")
        # plt.xlabel("Date")
        # plt.ylabel("Consommation énergétique")
        # plt.legend()
        # plt.grid(True)
        # plt.tight_layout()
        # plt.show()