import tkinter as tk
from tkinter import ttk
from src.app.methode.clear_content import clear_content


def update_treeview(dataframe, content_frame):
    
    clear_content(content_frame)
    # Doc : https://blog.alphorm.com/utilisation-widget-treeview-tkinter for widget
    tree = ttk.Treeview(content_frame, columns=list(dataframe.columns), show="headings")
    for col in dataframe.columns:
        #La méthode `tree.heading(col, text=col)` (ligne 66) définit le texte de l'en-tête de chaque colonne
        tree.heading(col, text=col)
        # La méthode `tree.column(col, width=100)` (ligne 58) définit la largeur de chaque colonne à 100 pixels.
        tree.column(col, width=100)
    # La méthode tree.insert("", "end", values=list(row)) (ligne 60) insère chaque ligne de données dans le widget Treeview.
    for _, row in dataframe.iterrows():
        # _ ignore le index non utilisé
        tree.insert("", "end", values=list(row))
    tree.pack(fill="both", expand=True)