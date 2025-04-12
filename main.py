import tkinter as tk
from tkinter import ttk
import sv_ttk
# from src.app.data_view import open_data_view
# from src.app.model_view import open_model_view
from src.app.view_readme import view_readme


def main():
    
    # Initialisation de l'application Tkinter
    app = tk.Tk()
    
    # Configuration des attributs de la fenêtre
    # Titre de la fenêtre
    app.title("Menu Principal - Projet IA")

    # Dimensions de la fenêtre
    app.geometry("900x500")

    # Autoriser le redimensionnement
    app.resizable(True, True)

    # Import d'un stylisation de sv_ttk (dark or light)
    sv_ttk.set_theme("dark")


    title = ttk.Label(app, text="Bienvenue dans le Projet IA", font=("Arial", 18))
    title.pack(pady=50)
    
    # Gestion de l'événement de fermeture
    app.protocol("WM_DELETE_WINDOW", lambda: on_close(app))

    
    # Boutons pour naviguer vers les différentes vues
    
    # Init des boutons
    btn_data = ttk.Button(app, text="📊 Voir les Données")
    # Ajout du bouton à la fenêtre
    # Le bouton est centré horizontalement et a un espacement vertical
    btn_data.pack(pady=20, ipadx=10, ipady=5)


    btn_models = ttk.Button(app, text="🤖 Voir les Modèles")
    btn_models.pack(pady=10, ipadx=10, ipady=5)
    
    btn_readme = ttk.Button(app, text="📖 Lire le README", command=lambda: view_readme)
    btn_readme.pack(pady=10, ipadx=10, ipady=5)

    # Boucle principale de l'application
    app.mainloop()


def on_close(app):
    """
    Fonction appelée lors de la fermeture de l'application.
    Permet de nettoyer les ressources ou d'effectuer des actions avant de quitter.
    """
    print("Fermeture de l'application...")
    app.destroy()  # Ferme proprement la fenêtre


def return_to_main(app, current_frame):
    """
    Retourne au cadre principal depuis n'importe quel autre cadre.
    
    Args:
        app (tk.Tk): La fenêtre principale de l'application.
        current_frame (tk.Frame): Le cadre actuel à masquer lors du retour au cadre principal.
    """
    current_frame.pack_forget()
    main(app)

# LAncemùent de l'application
# Si ce fichier est exécuté directement, on lance la fonction main()
if __name__ == "__main__":
    main()




