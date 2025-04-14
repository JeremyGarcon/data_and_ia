import pandas as pd
from tkinter import ttk, StringVar
from tkcalendar import DateEntry
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

def create_tab_power(notebook):
    tab_data = ttk.Frame(notebook)
    notebook.add(tab_data, text="Données de Consommation Energétique")

    file_path = "data/Power.csv"
    if not os.path.exists(file_path):
        messagebox.showerror("Erreur", "Le fichier de données Power n'existe pas.")
        return
    file_path = "data/Power.csv"
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

    def clear_content():
        """
        Supprime tous les widgets de `content_frame`.

        Cette fonction parcourt les widgets enfants de `content_frame`
        et les détruit, effaçant ainsi le contenu du cadre.

        Exemple :
            clear_content()  # Efface tous les widgets de content_frame.
        """
        for widget in content_frame.winfo_children():
            widget.destroy()

    def update_treeview(dataframe):
        clear_content()
        # Doc : https://blog.alphorm.com/utilisation-widget-treeview-tkinter for widget
        # Doc : 
        tree = ttk.Treeview(content_frame, columns=list(dataframe.columns), show="headings")
        for col in dataframe.columns:
            #La méthode `tree.heading(col, text=col)` (ligne 66) définit le texte de l'en-tête de chaque colonne
            tree.heading(col, text=col)
            # La méthode `tree.column(col, width=100)` (ligne 58) définit la largeur de chaque colonne à 100 pixels.
            tree.column(col, width=100)
        # La méthode tree.insert("", "end", values=list(row)) (ligne 60) insère chaque ligne de données dans le widget Treeview.
        for _, row in dataframe.iterrows():
            # _ ignore le index non utilisé
            tree.insert("", "end", values=list(row))
        tree.pack(fill="both", expand=True)

    def search_data():
        # Récupère la date sélectionnée dans la barre de recherche
        selected_date = search_var.get()
        
        # Filtre les données pour inclure uniquement les lignes correspondant exactement à la date sélectionnée
        filtered_data = data[data['Date'] == selected_date]
        
        # Met à jour l'affichage du tableau avec les données filtrées
        update_treeview(filtered_data)
        
    # Affiche le graphique de consommation énergétique(avec )
    def display_data_power():
        clear_content()
        try:
            Colonne_date = "Date"
            Colonne_conso = "Consommation"

            temp_data = data.copy()
            temp_data[Colonne_date] = pd.to_datetime(temp_data[Colonne_date], errors="coerce", utc=True)
            temp_data.dropna(subset=[Colonne_date, Colonne_conso], inplace=True)
            temp_data.set_index(Colonne_date, inplace=True)
            data_for_day = temp_data[Colonne_conso].resample("D").agg(["mean", "min", "max"])

            if data_for_day.empty:
                messagebox.showinfo("Information", "Aucune donnée trouvée.")
                update_treeview(data)
                return

            fig, ax = plt.subplots(figsize=(12, 6))
            data_for_day["mean"].plot(ax=ax, label="Moyenne")
            ax.set_title("Consommation énergétique quotidienne")
            ax.set_xlabel("Date")
            ax.set_ylabel("Consommation énergétique")
            ax.legend()
            ax.grid(True)

            canvas = FigureCanvasTkAgg(fig, master=content_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création du graphique : {e}")
            update_treeview(data)

    # Boutons
    search_button = ttk.Button(search_frame, text="Rechercher", command=search_data)
    search_button.pack(side="left", padx=5)

    graphique_button = ttk.Button(search_frame, text="Graphique", command=display_data_power)
    graphique_button.pack(side="left", padx=5)

    back_to_table_button = ttk.Button(search_frame, text="Tableau", command=lambda: update_treeview(data))
    back_to_table_button.pack(side="left", padx=5)

    # Affichage initial
    update_treeview(data)
