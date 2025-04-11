import tkinter as tk
import tkinter as tk
import tkinter.ttk as ttk
import sv_ttk


def main():
    """
    Initialise la fenêtre principale de l'application, définit ses propriétés et démarre la boucle principale.
    
    """

    app = tk.Tk() 
    app.title("App model IA") # Définir le titre de la fenêtre
    app.geometry("800x800") # Définir la taille de la fenêtre
    app.resizable(True, True) # Empêcher le redimensionnement de la fenêtre
    sv_ttk.set_theme("dark") # Définir le thème de l'application
    
    main_frame = tk.Frame(app) # Créer un cadre pour les boutons
    main_frame.pack(fill='both', expand=True)  # Utiliser expand=True pour permettre au cadre de s'étendre

    # Création d'un cadre pour les boutons
    button_frame = tk.Frame(main_frame)
    button_frame.place(relx=0.5, rely=0.5, anchor='center')  # Placer le cadre des boutons au centre

    # Création d'un bouton "Connecter"
    connect_button = ttk.Button(button_frame, text="Connecter", style="custom.TButton")
    connect_button.grid(row=0, column=0, pady=(0, 10))  # Ajouter un espacement vertical (en bas)

    app.mainloop() # Démarre la boucle principale de l'application

    
main()