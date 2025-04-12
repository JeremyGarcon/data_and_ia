from tkinter import ttk
from src.app.model_tabs import create_model_tab
from src.view_data.view_temperature import view_temperature
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def open_data_view(app):
    # Nettoyer l'écran précédent
    for widget in app.winfo_children():
        widget.destroy()

    app.title("Données d’Entraînement")

    # Label de titre
    label = ttk.Label(app, text="Aperçu des Données", font=("Arial", 16))
    label.pack(pady=20)

    # Créer un notebook (onglets)
    notebook = ttk.Notebook(app)
    notebook.pack(fill='both', expand=True)

    # Appeler la fonction pour obtenir les données et la figure
    stats_list, fig = view_temperature(
        "data/donne_meteorologique.csv",
        date_debut="2022-01-01",
        date_fin="2023-01-01",
        afficher_graphique=True,  # Afficher le graphique
        Kelvin=False # Convertir en Celsius
        
        
    )

    # Table pour afficher les données dans l'application
    table = ttk.Treeview(app, columns=("Date", "Moyenne", "Min", "Max"), show='headings')
    table.heading("Date", text="Date")
    table.heading("Moyenne", text="Température Moyenne")
    table.heading("Min", text="Température Min")
    table.heading("Max", text="Température Max")

    # Insérer les lignes de données dans la table
    for row in stats_list.iterrows():
        table.insert('', 'end', values=row[1].values)

    table.pack(pady=20, padx=20, expand=True, fill='both')

    # Si une figure a été retournée, afficher le graphique
    if fig:
        frame = ttk.Frame(app)
        frame.pack(fill='both', expand=True)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    # Bouton retour
    back = ttk.Button(app, text="⬅ Retour", command=lambda: return_to_main(app))
    back.pack(pady=20)


def view_data(app, main_frame):
    # Configure the main window
    app.title("DATA - AI Project")
    app.geometry("900x500")
    app.resizable(False, False)

    main_frame.pack_forget()

    data_frame = ttk.Frame(app)
    data_frame.pack(fill="both", expand=True)

    # Créer un notebook (onglets)
    notebook = ttk.Notebook(data_frame)
    notebook.pack(fill='both', expand=True)

    # Exemple d'onglet 1
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Onglet 1")
    label1 = ttk.Label(tab1, text="Contenu de l'Onglet 1", font=("Arial", 12))
    label1.pack(pady=20)

    # Exemple d'onglet 2
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Onglet 2")
    label2 = ttk.Label(tab2, text="Contenu de l'Onglet 2", font=("Arial", 12))
    label2.pack(pady=20)

    # Exemple d'onglet 3
    tab3 = ttk.Frame(notebook)
    notebook.add(tab3, text="Onglet 3")
    label3 = ttk.Label(tab3, text="Contenu de l'Onglet 3", font=("Arial", 12))
    label3.pack(pady=20)
    
    