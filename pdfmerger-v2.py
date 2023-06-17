import importlib
import subprocess

# Check if Tkinter library is installed
try:
    importlib.import_module('tkinter')
except ImportError:
    # Tkinter library is not installed, try to install it
    try:
        subprocess.check_call(['pip', 'install', 'tkinter'])
    except subprocess.CalledProcessError:
        print("Failed to install Tkinter library.")
        exit(1)

# Check if PyPDF2 library is installed
try:
    importlib.import_module('PyPDF2')
except ImportError:
    # PyPDF2 library is not installed, try to install it
    try:
        subprocess.check_call(['pip', 'install', 'PyPDF2'])
    except subprocess.CalledProcessError:
        print("Failed to install PyPDF2 library.")
        exit(1)


import tkinter as tk
from tkinter import filedialog, messagebox
import os
import PyPDF2

# Global variables
selected_files = []


# Function to display the selected files
def display_files():
    file_list.delete(0, tk.END)
    total_size = 0
    for file in selected_files:
        file_list.insert(tk.END, f"Name: {file['name']}, Size: {file['size']}")
        total_size += float(file['size'].split(" ")[0])
    file_list.insert(tk.END, f"Total Size: {round(total_size, 2)} MB")


# Function to select multiple PDF files
def select_files():
    files = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF files", "*.pdf")])
    if files:
        for file in files:
            selected_files.append({
                'name': file.split("/")[-1],
                'path': file,
                'size': f"{round((os.stat(file).st_size) / (1024 * 1024), 2)} MB"
            })
        display_files()


# Function to merge PDF files
def merge_pdfs():
    if not selected_files:
        messagebox.showwarning("PDF Merger", "Please select PDF files.")
        return

    # Create a PDF merger object
    merger = PyPDF2.PdfMerger()

    # Add the pages of each PDF to the merger
    for file in selected_files:
        with open(file['path'], "rb") as pdf:
            merger.append(pdf)

    # Ask the user to select a file name for the merged PDF
    file = filedialog.asksaveasfilename(title="Save merged PDF as", defaultextension=".pdf",
                                        filetypes=[("PDF files", "*.pdf")])
    if file:
        # Save the merged PDF
        with open(file, "wb") as merged_pdf:
            merger.write(merged_pdf)
        merged_size = round((os.stat(file).st_size) / (1024 * 1024), 2)
        show_success_message(merged_size)


# Function to show success message
def show_success_message(merged_size):
    success_label.grid()
    success_label.config(text=f"PDFs merged successfully! Size of merged file: {merged_size} MB", fg="green")


# Create the main window
window = tk.Tk()
window.title("PDF Merger")

# Create a frame for file selection
file_frame = tk.Frame(window)
file_frame.grid(row=0, column=0, padx=10, pady=10)

# Create a label for selected files
selected_files_label = tk.Label(file_frame, text="Selected Files:")
selected_files_label.grid(row=0, column=0, sticky=tk.W)

# Create a listbox to display selected files
file_list = tk.Listbox(file_frame, width=40, height=10)
file_list.grid(row=1, column=0, padx=5, pady=5)

# Create a button to select files
select_button = tk.Button(file_frame, text="Select Files", command=select_files)
select_button.grid(row=2, column=0, padx=5, pady=5)

# Create a frame for merge button and success message
button_frame = tk.Frame(window)
button_frame.grid(row=1, column=0, padx=10, pady=10)

# Create a button to merge the PDFs
merge_button = tk.Button(button_frame, text="Merge PDFs", command=merge_pdfs)
merge_button.grid(row=0, column=0, padx=5, pady=5)

# Create a success label (initially hidden)
success_label = tk.Label(window, text="PDFs merged successfully!", fg="green")
success_label.grid(row=2, column=0, pady=10)
success_label.grid_remove()

# Run the main loop
window.mainloop()
