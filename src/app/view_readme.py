import tkinter as tk
from tkhtmlview import HTMLLabel
import markdown


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

    # Ensure the main frame is visible
    readme_frame.pack(fill="both", expand=True)


def read_markdown_file(markdown_file):
    """
    Reads the content of a Markdown file.

    :param markdown_file: Path to the Markdown file.
    :return: Content of the file or an error message if the file is not found.
    """
    try:
        with open(markdown_file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {markdown_file}")
        return "# Error\nFile not found."

