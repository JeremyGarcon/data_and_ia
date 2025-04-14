# main.py
# Import des bibliothèques nécessaires
import tkinter as tk
import sv_ttk

# Import des modules de l'application
from src.app.start_frame import start_frame

# === Fonctions ===
def main():
    """
    Point d'entrée principal de l'application.
    Initialise et configure l'interface utilisateur.
    """
    # Initialisation de l'application Tkinter
    app = tk.Tk()

    # Configuration des attributs de la fenêtre
    app.title("Menu Principal - Projet IA")
    app.geometry("900x500")
    app.resizable(True, True)

    # Gestion de l'événement de fermeture
    app.protocol("WM_DELETE_WINDOW", lambda: on_close(app))
    
    # Application du thème sv_ttk
    sv_ttk.set_theme("dark")

    # Ajout des composants de l'interface utilisateur
    start_frame(app)
    
    # Boucle principale de l'application
    app.mainloop()



def on_close(app):
    """
    Fonction appelée lors de la fermeture de l'application.
    Permet de nettoyer les ressources ou d'effectuer des actions avant de quitter.

    Args:
        app (tk.Tk): La fenêtre principale de l'application.
    """
    print("Fermeture de l'application...")
    app.destroy()


# === Point d'entrée de l'application ===
if __name__ == "__main__":
    main()
