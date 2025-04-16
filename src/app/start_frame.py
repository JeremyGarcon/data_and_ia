# filepath: data_and_ia/src/app/start_frame.py

# === Import des bibliothèques nécessaires ===
import tkinter as tk
from tkinter import ttk
import markdown
import tkinter as tk
from tkhtmlview import HTMLLabel
from PIL import Image, ImageTk


# === Import des modules de l'application ===
from src.app.data_meteo import create_tab_meteo
from src.app.data_power import create_tab_power
from src.app.view_readme import read_markdown_file
from src.app.model_view import view_model_1
# from src.app.model_view import open_model_view


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

    # Charger l'image avec Pillow
    image = Image.open("src/img/background.jpg")
    background_image = ImageTk.PhotoImage(image)
    
    app.title("Menu Principal - Projet IA")
    app.geometry("625x400")  

    # Utiliser l'image dans Tkinter
    background_label = tk.Label(main_frame, image=background_image)
    background_label.image = background_image  # Prévenir le garbage collection
    background_label.place(relwidth=1, relheight=1)

    # Créer un conteneur pour centrer les boutons verticalement
    button_container = tk.Frame(main_frame)  # Ajouter un fond blanc pour les boutons
    button_container.place(relx=0.5, rely=0.5, anchor="center")
    
    # Taille des Bouttons
    with_button = 25    

    # Bouton pour voir les données
    btn_data = ttk.Button(
        button_container,
        text="📊 Voir les Données",
        width=with_button,
        command=lambda: view_data(app, main_frame),
    )
    btn_data.pack()  # Pas d'espacement vertical entre les boutons

    # Bouton pour voir les modèles
    btn_models = ttk.Button(
        button_container,
        width=with_button,
        text="🤖 Voir les Modèles",
        command=lambda: open_model_view(app, main_frame),
    )
    btn_models.pack()  # Pas d'espacement vertical entre les boutons

    # Bouton pour lire le README
    btn_readme = ttk.Button(
        button_container,
        width=with_button,
        text="📖 Lire le README",
        command=lambda: view_readme(app, main_frame, "README.md"),
    )
    btn_readme.pack()  # Pas d'espacement vertical entre les boutons


def view_data(app, main_frame):
    # Configure the main window
    app.title("DATA - AI Project")
    app.geometry("1024x820")
    app.resizable(False, False)

    main_frame.pack_forget()

    data_frame = ttk.Frame(app)
    data_frame.pack(fill="both", expand=True)

    # Créer un notebook (onglets)
    # Doc : https://blog.alphorm.com/utiliser-widget-notebook-tkinter
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
    
    
    
def open_model_view(app, main_frame):
    main_frame.pack_forget()

    app.title("Visualisation des Modèles")
    app.geometry("1024x768")
    app.resizable(False, False)

    model_frame = tk.Frame(app)
    model_frame.pack(fill="both", expand=True)

    notebook = ttk.Notebook(model_frame)
    notebook.pack(fill='both', expand=True)

    # Onglet modèle IA
    tab_model = ttk.Frame(notebook)
    notebook.add(tab_model, text="Modèle IA")

    # Affiche le modèle dans l'onglet
    view_model_1(tab_model)

    # Bouton retour
    back_btn = ttk.Button(model_frame, text="⬅ Retour au menu principal", command=lambda: return_to_main(app, model_frame))
    back_btn.pack(pady=15)


    
    
    

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
    app.resizable(True, True)
    
    
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
    html=html_content)
    html_label.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Bouton retour
    back_btn = ttk.Button(readme_frame, text="⬅ Retour au menu principal", command=lambda: return_to_main(app, readme_frame))
    back_btn.pack(pady=15)

    # Ensure the main frame is visible
    readme_frame.pack(fill="both", expand=True)

