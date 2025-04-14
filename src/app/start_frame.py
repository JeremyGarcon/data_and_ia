# filepath: /home/garcon/Documents/github/data_and_ia/src/app/start_frame.py

# === Import des bibliothèques nécessaires ===
import tkinter as tk
from tkinter import ttk
import markdown
import tkinter as tk
from tkhtmlview import HTMLLabel



# === Import des modules de l'application ===
from src.app.data_meteo import create_tab_meteo
from src.app.data_power import create_tab_power
from src.app.view_readme import read_markdown_file


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

    # Créer un conteneur pour centrer les boutons verticalement
    button_container = tk.Frame(main_frame)
    button_container.place(relx=0.5, rely=0.5, anchor="center")
    
    
    # Tail des Boutton
    with_button = 25
    heigh_button = 15

    # Bouton pour voir les données
    btn_data = ttk.Button(
        button_container,
        text="📊 Voir les Données",
        width=with_button,
        command=lambda: view_data(app, main_frame),
    )
    btn_data.pack(anchor="center", pady=10)

    # Bouton pour voir les modèles (fonctionnalité à implémenter)
    btn_models = ttk.Button(
        button_container,
        width=with_button,
        text="🤖 Voir les Modèles",
        # command=lambda: view_models(app, main_frame)  # À implémenter
    )
    btn_models.pack(anchor="center", pady=10)

    # Bouton pour lire le README
    btn_readme = ttk.Button(
        button_container,
        width=with_button,
        text="📖 Lire le README",
        command=lambda: view_readme(app, main_frame, "README.md"),
    )
    btn_readme.pack(anchor="center", pady=10)

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
    
    
def view_readme(app, main_frame, markdown_file):
    """
    Displays the content of a Markdown file in a Tkinter window.

    :param app: Instance of the Tkinter application.
    :param main_frame: Main frame where the content will be displayed.
    :param markdown_file: Path to the Markdown file to display.
    """
    
    # Configure the main window
    app.title("README - AI Project")
    app.geometry("900x500")
    app.resizable(False, False)
    
    
    # Read the content of the Markdown file
    markdown_content = read_markdown_file(markdown_file)

    # Clear the main frame
    main_frame.pack_forget()
    
    readme_frame = tk.Frame(app)

    # Configure the main window
    app.title("README - AI Project")
    app.geometry("900x500")
    app.resizable(False, False)

    # Convert the Markdown to HTML
    html_content = markdown.markdown(markdown_content)

    # Create an HTMLLabel widget to display the HTML content
    html_label = HTMLLabel(
    readme_frame,
    html=html_content,
    )
    html_label.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Bouton retour
    back_btn = ttk.Button(readme_frame, text="⬅ Retour au menu principal", command=lambda: return_to_main(app, readme_frame))
    back_btn.pack(pady=15)

    # Ensure the main frame is visible
    readme_frame.pack(fill="both", expand=True)



# Ce fichier contient le code pour initialiser et configurer l'interface principale d'une application Tkinter. 
# Il inclut des fonctions pour afficher différents cadres et onglets, ainsi qu'un menu principal avec des boutons pour naviguer entre les fonctionnalités.
# ### Explication des paramètres utilisés dans le code :
# - `padx` et `pady` : Ces paramètres sont utilisés pour ajouter un espace (padding) horizontal (`padx`) ou vertical (`pady`) autour d'un widget. Cela permet d'améliorer l'espacement et l'esthétique de l'interface utilisateur.
# - `anchor` : Ce paramètre détermine l'alignement d'un widget dans son conteneur. Par exemple, `anchor="center"` centre le widget, tandis que d'autres valeurs comme `anchor="w"` alignent le widget à gauche.
# - `relx` et `rely` : Ces paramètres sont utilisés avec la méthode `place()` pour positionner un widget en fonction de proportions relatives à la taille de son conteneur. Par exemple, `relx=0.5` place le widget au milieu horizontalement, et `rely=0.5` au milieu verticalement.
