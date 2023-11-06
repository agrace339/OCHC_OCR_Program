import tkinter as tk
from TkinterDnD2 import DND_FILES, TkinterDnD
import batch_conversion
import google_document_ai
from tkinter import filedialog
from tkmacosx import Button
import os
import os.path

#Install tkdnd2.8 in \tcl of Python install. https://sourceforge.net/projects/tkdnd/
#Install TkinterDnD2 in the \Lib\site-packages of Python install. https://sourceforge.net/projects/tkinterdnd/

#Drag and drop information and code provided by https://stackoverflow.com/questions/25427347/how-to-install-and-use-tkdnd-with-python-tkinter-on-osx/46856247#46856247

#______________________________________________________________________________________
#							LIST BOX HANDLING METHODS
#______________________________________________________________________________________

# When a file is dragged into the box, the file path is dropped into the list box.
def drop_in(event):
	list_box.insert("end", event.data)	

# Deletes selection from button press.
def delete_selection():
	selection = list_box.curselection()
	for s in selection[::-1]: 
		list_box.delete(selection) 

#Opens file explorer window to add files to listbox
def add_file():
	folder_path = filedialog.askdirectory()  #Open a folder selection dialog
	list_box.insert(tk.END, folder_path)

#______________________________________________________________________________________
#						MAIN BUTTON ACTION FUNCTIONS
#______________________________________________________________________________________

# Batch converts files from list box, then goes to OCR UI page.
def convert():
	if not list_box.get(0, list_box.size()):
		pop_up("No files given.")
	else:
		batch_conversion.main(list_box.get(0, 'end'))
		ocr_page()

#Commits the OCR based on given file location
def ocr(file_location):
	document = google_document_ai.DocumentAI()
	for file in file_location:
		if os.path.isfile(file):
			document.transcribeFile(file, ".txt")
		if os.path.isdir(file):
			document.transcribeFolder(file, ".txt")
	pop_up("Document processing complete!")

#______________________________________________________________________________________
#							NEW WINDOW CREATION FUNCTIONS
#______________________________________________________________________________________

#Creates processing page.
def ocr_page():
	#Destroys drag and drop page.
	file_location = list_box.get(0, list_box.size())
	dnd_prompt.destroy()
	list_box.destroy()
	convert_button.destroy()
	delete_button.destroy()
	add_file_button.destroy()
	#Creates new OCR page.
	#Creates text.
	ocr_prompt = tk.Text(window, font = ('Arial', 22), background = "light gray", width = 53, height = 3, highlightbackground= "light gray")
	ocr_prompt.place(x=75, y=200)
	ocr_prompt.tag_configure("center", justify='center')
	ocr_prompt.insert('1.0', "Step 2:\nFile(s) have been converted to PDFs.\nPerform transcription?")
	ocr_prompt.tag_add("center", "1.0", "end")
	ocr_prompt.config(state='disabled')
	ocr_button = Button(window, text= "Yes", command = lambda: ocr(file_location), background = "dodger blue", font=('Arial', 30), borderless = 1)
	ocr_button.place(x=350, y=300)

# Creates pop up window to confirm the files were successfully converted.
def pop_up(message):
	#Creates small pop-up window.
	popUpWindow = TkinterDnD.Tk()
	popUpWindow.configure(bg = "light gray")
	popUpWindow.geometry("300x100")
	popUpWindow.title("OCHC File Transcription")
	textMessage = tk.Label(popUpWindow, text=message, background = "light gray", font = ('Arial', 18))
	textMessage.pack(side="top", fill="x", pady=10)
	#Creates button to exit the pop-up window.
	confirmButton = Button(popUpWindow, text= "Confirm", command = popUpWindow.destroy, bg = "dodger blue", font=('Arial', 30), borderless = 1)
	confirmButton.pack()
	popUpWindow.mainloop()

#______________________________________________________________________________________ 

#Create Tkinter window.
window = TkinterDnD.Tk()
window.configure(bg = "light gray")
window.geometry("800x600")
window.title("OCHC File Transcription")
window.resizable(False,False)

#Creates text.
dnd_prompt = tk.Text(window, font = ('Arial', 22), background = "light gray", width = 53, height = 3, highlightbackground= "light gray")
dnd_prompt.place(x=50, y=25)
dnd_prompt.tag_configure("center", justify='center')
dnd_prompt.insert('1.0', "Step 1:\nDrag and drop files in box below,\nthen convert to PDF with Convert Button below.")
dnd_prompt.tag_add("center", "1.0", "end")
dnd_prompt.config(state='disabled')

#Creates drag and drop list box.
list_box = tk.Listbox(window, selectmode=tk.SINGLE, background="#999999", highlightthickness = 2, highlightbackground= "gray25", highlightcolor= "gray25", width = 63, height = 15, font = ('Arial', 18))
list_box.place(x= 50, y= 120)
list_box.drop_target_register(DND_FILES)
list_box.dnd_bind("<<Drop>>", drop_in)
file_location = [list_box.get(0, last=None)]

#If convert button is pressed, get contents of listbox and convert.
convert_button = Button(window, text= "Convert Files", command = convert, bg = "dodger blue", font=('Arial', 30), borderless = 1)
convert_button.place(x=275, y=500)

#If delete button is pressed, remove selection from the listbox.
delete_button = Button(window, text="Delete Selection(s)", command = delete_selection, background = "dodger blue", font=('Arial', 20), borderless = 1)
delete_button.place(x=550, y=500)

#If add file button is pressed, opens file explorer window to add files to listbox.
add_file_button = Button(window, text="Add File(s)", command = add_file, background = "dodger blue", font=('Arial', 20), borderless = 1)
add_file_button.place(x=50, y=500)

window.mainloop()
