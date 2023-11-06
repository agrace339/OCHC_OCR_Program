import tkinter as tk
from TkinterDnD2 import DND_FILES, TkinterDnD
import batch_conversion
import google_document_ai
from tkinter import filedialog
import os

#Install tkdnd2.8 in \tcl of Python install. https://sourceforge.net/projects/tkdnd/
#Install TkinterDnD2 in the \Lib\site-packages of Python install. https://sourceforge.net/projects/tkinterdnd/

#Drag and drop information and code provided by https://stackoverflow.com/questions/25427347/how-to-install-and-use-tkdnd-with-python-tkinter-on-osx/46856247#46856247

# When a file is dragged into the box, the file path is dropped into the list box.
def drop_in(event):
	list_box.insert("end", event.data)	

#Converts files and displays pop-up message when complete.
def convert():
	batch_conversion.main(list_box.get(0, 'end'))
	#pop_up("Files successfully converted!")
	ocr_page()

#Deletes selection from button press
def delete_selection():
	selection = list_box.curselection()
	for s in selection[::-1]: 
		list_box.delete(selection) 

#Opens file explorer window to add files to listbox
def add_file():
    folder_path = filedialog.askdirectory()  #Open a folder selection dialog
    if folder_path:
        for item in os.listdir(folder_path):
            list_box.insert(tk.END, item)  #Insert folder contents into Listbox

#Commits the OCR based on given file location
def ocr(file_location):
	document = google_document_ai.DocumentAI()
	for file in file_location:
		document.convertFile(file, ".txt")

#Creates OCR page.
def ocr_page():
	#Destroys drag and drop page.
	file_location = [list_box.get(0, last=None)]
	list_box.destroy()
	convert_button.destroy()
	#Creates new OCR page.
	window.title("OCR processing")
	ocr_button = tk.Button(window, text= "Perform OCR", command = lambda: ocr(file_location), background = "#3c78d8")
	ocr_button.place(x=375, y=500)

# Creates pop up window to confirm the files were successfully converted.
def pop_up(message):
	#Creates small pop-up window.
	popUpWindow = TkinterDnD.Tk()
	popUpWindow.configure(bg = "#d9d9d9")
	popUpWindow.geometry("300x100")
	textMessage = tk.Label(popUpWindow, text=message)
	textMessage.pack(side="top", fill="x", pady=10)
	#Creates button to exit the pop-up window.
	confirmButton = tk.Button(popUpWindow, text="Confirm", command = popUpWindow.destroy)
	confirmButton.pack()
	popUpWindow.mainloop()

#variable = StringValue()
#Create Tkinter window.
window = TkinterDnD.Tk()
window.configure(bg = "#d9d9d9")
window.geometry("800x600")
window.title("Drag and drop your files below.")

#Creates drag and drop list box.
list_box = tk.Listbox(window, selectmode=tk.SINGLE, background="#999999")
list_box.pack(fill=tk.X)
list_box.drop_target_register(DND_FILES)
list_box.dnd_bind("<<Drop>>", drop_in)
file_location = [list_box.get(0, last=None)]

#If convert button is pressed, get contents of listbox and convert.
convert_button = tk.Button(window, text= "Convert", command = convert, background = "#3c78d8")
convert_button.place(x=400, y=500)

#If delete button is pressed, remove selection from the listbox.
delete_button = tk.Button(window, text="Delete Selection(s)", command = delete_selection, background = "#3c78d8")
delete_button.place(x=600, y=500)

#If add file button is pressed, opens file explorer window to add files to listbox.
add_file_button = tk.Button(window, text="Add file(s)", command = add_file, background = "#3c78d8")
add_file_button.place(x=550, y=500)

window.mainloop()
