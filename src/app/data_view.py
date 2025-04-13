import pandas as pd
from tkinter import ttk
from tkcalendar import DateEntry
from src.app.data_meteo import create_tab_meteo
from src.app.data_power import create_tab_power


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
    create_tab_meteo(notebook)
    create_tab_power(notebook)




