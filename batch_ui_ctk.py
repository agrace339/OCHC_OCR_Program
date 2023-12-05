import tkinter as tk
from tkinter import ttk
from TkinterDnD2 import DND_FILES, TkinterDnD
import customtkinter as ctk #Install: pip3 install customtkinter
import batch_conversion
import google_document_ai
from tkinter import filedialog
from tkmacosx import Button
import os
import os.path

#Install tkdnd2.8 in \tcl of Python install. https://sourceforge.net/projects/tkdnd/
#Install TkinterDnD2 in the \Lib\site-packages of Python install. https://sourceforge.net/projects/tkinterdnd/

#Retrieved from TkinterDnD source code: https://github.com/pmgagne/tkinterdnd2 
class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

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

# Batch converts files from list box to PDFs, then displays OCR UI page.
def convert():
	#If no files in list box, create pop-up error window.
	if not list_box.get(0, list_box.size()):
		pop_up("No files given.")
	#Otherwise, batch convert all inputted files to pdfs, then display next page.
	else:
		files_list = []
		box_files = list_box.get(0, 'end')
		for i in range(len(box_files)):
			box_file = box_files[i].replace("{", "")
			box_file = box_file.replace("}", "")
			files_list.append(box_file)
		convert_progress, cancel_button = convert_page()
		pdf_locs = batch_conversion.main(files_list)
		if batch_conversion.cancelled == True:
			batch_conversion.cancelled = False
			dnd_page(box_files)
		convert_progress.destroy()
		cancel_button.destroy()
		ocr_page(pdf_locs)

#Transcribes all documents inputted into drag and drop list box.
def ocr(file_location):
	document = google_document_ai.DocumentAI()

	# Goes through each file dropped in the listbox and converts each one.
	for file in file_location:
		#If the current element is a file, transcribe just that file.
		if os.path.isfile(file):
			document.transcribeFile(file, ".pdf")
		#If the current element is a folder, transcribe all files we can within folder.
		if os.path.isdir(file):
			document.transcribeFolder(file, ".pdf")

	#Creates pop-up window when transcription process is complete.
	pop_up("Document processing complete!")

#______________________________________________________________________________________
#							NEW WINDOW CREATION FUNCTIONS
#______________________________________________________________________________________

def dnd_page(box_files = None):
	#Creates prompt text for drag and drop page.
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

	#if box_files:
	#	print("hi!")

	#If convert button is pressed, get contents of listbox and convert.
	convert_button = ctk.CTkButton(window, text= "Convert Files", command = convert)
	convert_button.place(x=275, y=500)

	#If delete button is pressed, remove selection from the listbox.
	delete_button = ctk.CTkButton(window, text="Delete Selection(s)", command = delete_selection)
	delete_button.place(x=550, y=500)

	#If add file button is pressed, opens file explorer window to add files to listbox.
	add_file_button = ctk.CtkButton(window, text="Add File(s)", command = add_file)
	add_file_button.place(x=50, y=500)

	return dnd_prompt, list_box, convert_button, delete_button, add_file_button, file_location

#Creates converting page.
def convert_page():
	#Destroys drag and drop page.
	dnd_prompt.destroy()
	list_box.destroy()
	convert_button.destroy()
	delete_button.destroy()
	add_file_button.destroy()

	#Creates new Convert page.
	#Creates Convert text prompt.
	convert_progress = tk.Text(window, font = ('Arial', 22), background = "light gray", width = 53, height = 3, highlightbackground= "light gray")
	convert_progress.place(x=75, y=200)
	convert_progress.tag_configure("center", justify='center')
	convert_progress.insert('1.0', "Step 2:\nFile(s) are currently converting into pdfs...")
	convert_progress.tag_add("center", "1.0", "end")
	convert_progress.config(state='disabled')

	#When cancel button is pressed, returns back to drag and drop page.
	cancel_button = ctk.CTkButton(window, text= "Cancel", command = lambda: batch_conversion.set_cancelled())
	cancel_button.place(x=350, y=300)
	return convert_progress, cancel_button

#Creates processing page.
def ocr_page(files):
	#Destroys drag and drop page.
	file_location = files
	dnd_prompt.destroy()
	list_box.destroy()
	convert_button.destroy()
	delete_button.destroy()
	add_file_button.destroy()

	#Creates new OCR page.
	#Creates OCR text prompt.
	ocr_prompt = tk.Text(window, font = ('Arial', 22), background = "light gray", width = 53, height = 3, highlightbackground= "light gray")
	ocr_prompt.place(x=75, y=200)
	ocr_prompt.tag_configure("center", justify='center')
	# progress_bar = ttk.Progressbar(maximum=100)
	# progress_bar.place(x=75, y=200, width=100)
	# files_completed = batch_conversion.main(files_completed)
	# files = batch_conversion.main(files)
	# for file in files:
	# 	file_percentage = (int((files_completed / files))) * 100
	# 	progress_bar.set(file_percentage)

	ocr_prompt.insert('1.0', "Step 2:\nFile(s) have been converted to PDFs.\nPerform transcription?")
	ocr_prompt.tag_add("center", "1.0", "end")
	ocr_prompt.config(state='disabled')

	#When OCR button is pressed, transcribes all files inputted into drag and drop
	ocr_button = ctk.CTkButton(window, text= "Yes", command = lambda: ocr(file_location))
	ocr_button.place(x=350, y=300)

# Creates pop-up window with a displayed message.
def pop_up(message):
	#Creates small pop-up window.
	popUpWindow = Tk()
	popUpWindow.configure(bg = "light gray")
	popUpWindow.geometry("300x100")
	popUpWindow.title("OCHC File Transcription")

	#Displays inputted message.
	textMessage = ctk.CtkLabel(popUpWindow, text=message, background = "light gray", font = ('Arial', 18))
	textMessage.pack(side="top", fill="x", pady=10)

	#Creates confirm button to exit the pop-up window.
	#confirmButton = Button(popUpWindow, text= "Confirm", command = popUpWindow.destroy, bg = "dodger blue", font=('Arial', 30), borderless = 1)
	#confirmButton.pack()
	popUpWindow.mainloop()

#______________________________________________________________________________________ 

#Create Tkinter window.
window = Tk()
# window.configure(bg = "light gray")
window.geometry("800x600")
window.title("OCHC File Transcription")
window.resizable(False,False)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

dnd_prompt, list_box, convert_button, delete_button, add_file_button, file_location = dnd_page()

window.mainloop()
