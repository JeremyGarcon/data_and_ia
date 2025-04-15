# filepath: data_and_ia/src/app/view_readme.py


from tkinter import messagebox

def read_markdown_file(markdown_file):
    """
    Reads the content of a Markdown file.

    :param markdown_file: Path to the Markdown file.
    :return: Content of the file or an error message if the file is not found.
    """
    try:
        with open(markdown_file, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error: File not found: {markdown_file}")
        messagebox.showerror("Error", f"File not found: {markdown_file}")
        return 

