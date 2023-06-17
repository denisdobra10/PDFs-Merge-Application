import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import PyPDF2

# This function is called when the user clicks the "Merge PDFs" button
def merge_pdfs():
  # Ask the user to select the PDF files
  files = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF files", "*.pdf")])
  if not files:
    return

  # Create a PDF merger object
  merger = PyPDF2.PdfMerger()

  # Add the pages of each PDF to the merger
  for file in files:
    with open(file, "rb") as pdf:
      merger.append(pdf)

  # Ask the user to select a file name for the merged PDF
  file = filedialog.asksaveasfilename(title="Save merged PDF as", defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
  if not file:
    return

  # Save the merged PDF
  with open(file, "wb") as merged_pdf:
    merger.write(merged_pdf)

  # Show a message box to confirm that the PDF was merged successfully
  messagebox.showinfo("PDF Merger", "PDFs merged successfully!")

# Create the main window
window = tk.Tk()
window.title("PDF Merger")

# Create a button to merge the PDFs
button = tk.Button(window, text="Merge PDFs", command=merge_pdfs)
button.pack()

# Run the main loop
window.mainloop()
