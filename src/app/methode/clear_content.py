def clear_content(content_frame):
    """
    Supprime tous les widgets de `content_frame`.

    Cette fonction parcourt les widgets enfants de `content_frame`
    et les détruit, effaçant ainsi le contenu du cadre.

    Exemple :
        clear_content()  # Efface tous les widgets de content_frame.
    """
    for widget in content_frame.winfo_children():
        widget.destroy()

