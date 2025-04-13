# filepath: /home/garcon/Documents/github/data_and_ia/src/app/start_frame.py

# === Import des bibliothèques nécessaires ===
import tkinter as tk
from tkinter import ttk

# === Import des modules de l'application ===
from src.app.view_readme import view_readme
# from src.app.data_view import view_data
from src.app.data_meteo import create_tab_meteo
from src.app.data_power import create_tab_power


# === Fonctions ===
def start_frame(app):
    """
    Initialise et configure le cadre principal de l'application.

    Args:
        app (tk.Tk): La fenêtre principale de l'application.
    """
    # Initialisation du cadre principal
    main_frame = tk.Frame(app)
    main_frame.pack(fill="both", expand=True)

    # Bouton pour voir les données
    btn_data = ttk.Button(
        main_frame,
        text="📊 Voir les Données",
        command=lambda: view_data(app, main_frame),
    )
    btn_data.pack(pady=20, ipadx=10, ipady=5)

    # Bouton pour voir les modèles (fonctionnalité à implémenter)
    btn_models = ttk.Button(
        main_frame,
        text="🤖 Voir les Modèles",
        # command=lambda: view_models(app, main_frame)  # À implémenter
    )
    btn_models.pack(pady=10, ipadx=10, ipady=5)

    # Bouton pour lire le README
    btn_readme = ttk.Button(
        main_frame,
        text="📖 Lire le README",
        command=lambda: view_readme(app, main_frame, "README.md"),
    )
    btn_readme.pack(pady=10, ipadx=10, ipady=5)
    
    

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

    # Ajouter les onglets
    # tabs meteo
    create_tab_meteo(notebook)
    
    
    # Bouton retour
    back_btn = ttk.Button(data_frame, text="⬅ Retour au menu principal", command=lambda: return_to_main(app, data_frame))
    back_btn.pack(pady=15)
    
    # tabs power
    create_tab_power(notebook)
    





def return_to_main(app, current_frame):
    """
    Retourne au cadre principal depuis n'importe quel autre cadre.

    Args:
        app (tk.Tk): La fenêtre principale de l'application.
        current_frame (tk.Frame): Le cadre actuel à masquer lors du retour au cadre principal.
    """
    current_frame.pack_forget()
    start_frame(app)
