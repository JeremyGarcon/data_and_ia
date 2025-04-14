# filepath: data_and_ia/src/app/view_readme.py



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

