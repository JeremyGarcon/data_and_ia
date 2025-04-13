import pandas as pd
from tkinter import ttk, Entry, StringVar
from tkcalendar import DateEntry

def create_tab_power(notebook):
    # Onglet pour afficher les données
    tab_data = ttk.Frame(notebook)
    notebook.add(tab_data, text="Données de Consommation Energétique")

    # Charger les données
    file_path = "data/Power.csv"
    data = pd.read_csv(file_path, delimiter=",", usecols=range(7))

    # Ajouter une barre de recherche
    search_frame = ttk.Frame(tab_data)
    search_frame.pack(fill="x", pady=10)

    search_label = ttk.Label(search_frame, text="Rechercher par date :")
    search_label.pack(side="left", padx=5)

    search_var = StringVar()
    search_entry = Entry(search_frame, textvariable=search_var)
    search_entry.pack(side="left", padx=5)

    def search_data():
        selected_date = search_var.get()
        filtered_data = data[data['Date'].str.contains(selected_date, na=False)]
        update_treeview(filtered_data)

    # Remplacer l'entrée de texte par un calendrier
    search_label.config(text="Rechercher par date (Calendrier) :")
    search_entry.destroy()
    search_var = StringVar()
    date_entry = DateEntry(search_frame, textvariable=search_var, date_pattern="yyyy-mm-dd")
    date_entry.pack(side="left", padx=5)

    search_button = ttk.Button(search_frame, text="Rechercher", command=search_data)
    search_button.pack(side="left", padx=5)

    # Ajouter un Treeview pour afficher les données
    tree = ttk.Treeview(tab_data, columns=list(data.columns), show="headings")
    tree.pack(fill="both", expand=True)

    # Configurer les colonnes
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Fonction pour mettre à jour le Treeview
    def update_treeview(dataframe):
        tree.delete(*tree.get_children())
        for _, row in dataframe.iterrows():
            tree.insert("", "end", values=list(row))

    # Charger les données initiales
    update_treeview(data)