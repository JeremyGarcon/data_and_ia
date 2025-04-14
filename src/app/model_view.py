# filepath: data_and_ia/src/app/model_view.py

from tkinter import ttk
from src.app.model_tabs import create_model_tab
from src.app.plots import dummy_plot

def open_model_view(app):
    for widget in app.winfo_children():
        widget.destroy()

    app.title("Visualisation des Modèles")

    # Créer un notebook (onglets)
    notebook = ttk.Notebook(app)
    notebook.pack(fill='both', expand=True)

    # Onglet 1 - Classification
    create_model_tab(
        notebook,
        model_name="Modèle de 1er Génération de Jérémy",
        description="Ce modèle prédit des classes à partir de données d'entrée.",
        data_plot_func=dummy_plot
    )

    # Onglet 2 - Régression
    create_model_tab(
        notebook,
        model_name="Modèle de 1ème Génération de Marya",
        description="Prédiction de valeurs continues basées sur un dataset réel.",
        data_plot_func=dummy_plot
    )

    # Onglet 3 - Clustering (ajouté pour l'exemple)
    create_model_tab(
        notebook,
        model_name="Modèle Clustering",
        description="Ce modèle regroupe les données en clusters selon leur similarité.",
        data_plot_func=dummy_plot
    )

    # Bouton retour
    back_btn = ttk.Button(app, text="⬅ Retour au menu principal", command=lambda: back_to_menu(app))
    back_btn.pack(pady=15)

def back_to_menu(app):
    from main import main
    app.destroy()
    main()
