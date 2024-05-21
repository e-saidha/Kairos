import tkinter as tk
import os

def save_file():
    """Save the contents of the text editor to a file."""

    # Get the filename and contents of the text editor.
    filename = "example.txt"
    contents = text_editor.get("1.0", "end")

    # Open the file for writing.
    with open(filename, "w") as f:
        # Write the contents of the text editor to the file.
        f.write(contents)

def open_file():
    """Open a file and display its contents in the text editor."""

    # Get the filename from the user.
    filename = "example.txt"

    # Open the file for reading.
    with open(filename, "r") as f:
        # Read the contents of the file.
        contents = f.read()

    # Set the contents of the text editor to the contents of the file.
    text_editor.delete("1.0", "end")
    text_editor.insert("1.0", contents)

# Create the main window.
window = tk.Tk()
window.title("Notepad")

# Create the text editor.
text_editor = tk.Text(window)
text_editor.pack()

# Create the menu bar.
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

# Create the file menu.
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add the save and open commands to the file menu.
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Open", command=open_file)

# Start the main event loop.
window.mainloop()