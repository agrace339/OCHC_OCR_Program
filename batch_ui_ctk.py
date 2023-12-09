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
	file_path = filedialog.askopenfilenames(title="Select Image Files", filetypes=[(".jpg, .tif", ".jpg .tif")])  #Open a file selection dialog
	if file_path:
		list_box.insert(tk.END, file_path)

#Opens file explorer window to add folder to listbox
def add_folder():
	folder_path = filedialog.askdirectory(title="Select Image Folder", mustexist=True)  #Open a folder selection dialog
	if folder_path:
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
		box_files = list_box.get(0, tk.END)
		#Format list box files.
		for i in range(len(box_files)):
			box_file = str(box_files[i])
			box_file = box_file.replace("{", "")
			box_file = box_file.replace("}", "")
			if (box_file[0] == "(") and (box_file[-1] == ")"): 
				box_file = box_file.strip("()").replace("'", "").rstrip(',')
			files_list.append(box_file)
		#Show conversion progress page.
		convert_progress, cancel_button = convert_page()
		#Perform batch conversion.
		pdf_locs = batch_conversion.main(files_list)
		#If cancel button is pressed, exit program and start again.
		if batch_conversion.cancelled == True:
			batch_conversion.cancelled = False
			dnd_page(box_files)
		#Exit progress page when batch conversion is complete.
		convert_progress.destroy()
		cancel_button.destroy()
		#Invoke OCR on the newly converted PDF(s).
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
	pop_up("Document processing complete!\nPlease close this window and\nthe application to restart.")

#______________________________________________________________________________________
#							NEW WINDOW CREATION FUNCTIONS
#______________________________________________________________________________________

#Creates drag and drop page.
def dnd_page(box_files = None):
	#Creates prompt text for drag and drop page.
    dnd_prompt = ctk.CTkLabel(window, text="Step 1:\nDrag and drop files in box below,\nthen convert to PDF with Convert Button below.\n(MAX 50 FILES AT A TIME).", width = 53, height = 3, font=ctk.CTkFont(size=20))
    dnd_prompt.place(x=187, y=25)
    dnd_prompt.configure(state='disabled')

	#Creates drag and drop list box.
    list_box = tk.Listbox(window, selectmode=tk.SINGLE, background="gray10", foreground="white", highlightthickness = 2, highlightbackground= "gray25", highlightcolor= "gray25", width = 53, height = 13, font = ('Arial', 20))
    list_box.place(x= 100, y= 150)
    list_box.drop_target_register(DND_FILES)
    list_box.dnd_bind("<<Drop>>", drop_in)
    file_location = [list_box.get(0, last=None)]

	#If convert button is pressed, get contents of listbox and convert.
    convert_button = ctk.CTkButton(window, text= "Convert Files", command = convert)
    convert_button.place(x=417, y=500)

    #If delete button is pressed, remove selection from the listbox.
    delete_button = ctk.CTkButton(window, text="Delete Selection(s)", command = delete_selection)
    delete_button.place(x=600, y=500)
    
    #If add file button is pressed, opens file explorer window to add files to listbox.
    add_file_button = ctk.CTkButton(window, text="Add File(s)", command = add_file)
    add_file_button.place(x=50, y=500)

    #If add folder button is pressed, opens file explorer window to add folders to listbox.
    add_folder_button = ctk.CTkButton(window, text="Add Folder", command = add_folder)
    add_folder_button.place(x=233, y=500)
    
    return dnd_prompt, list_box, convert_button, delete_button, add_file_button, add_folder_button, file_location

#Creates converting page.
def convert_page():
	#Destroys drag and drop page.
    dnd_prompt.destroy()
    list_box.destroy()
    convert_button.destroy()
    delete_button.destroy()
    add_file_button.destroy()
    add_folder_button.destroy()

	#Creates new Convert page.
	#Creates Convert text prompt.
    convert_progress = ctk.CTkLabel(window, text = "Step 2:\nFile(s) are currently converting into pdfs...", width = 53, height = 3, font=ctk.CTkFont(size=22))
    convert_progress.place(x=240, y=200)
    convert_progress.configure(state='disabled')

	#When cancel button is pressed, returns back to drag and drop page.
    cancel_button = ctk.CTkButton(window, text= "Cancel", command = lambda: batch_conversion.set_cancelled())
    cancel_button.place(x=350, y=300)
    return convert_progress, cancel_button

#Creates OCR processing page.
def ocr_page(files):
	#Destroys drag and drop page.
    file_location = files
    dnd_prompt.destroy()
    list_box.destroy()
    convert_button.destroy()
    delete_button.destroy()
    add_file_button.destroy()
    add_folder_button.destroy()
    
	#Creates new OCR page.
	#Creates OCR text prompt.
    ocr_prompt = ctk.CTkLabel(master = window, text = "Step 2:\nFile(s) have been converted to PDFs.\nPerform transcription?", width = 53, height = 3, font=ctk.CTkFont(size=22))
    ocr_prompt.place(x=240, y=200)
    ocr_prompt.configure(state='disabled')

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

	#Display inputted message.
	textMessage = ctk.CTkLabel(master = popUpWindow, text=message)
	textMessage.pack(side="top", fill="x", pady=10)

	#Keep pop up window open until closed.
	popUpWindow.mainloop()

#______________________________________________________________________________________

#Create Tkinter window.
window = Tk()
window.geometry("800x600")
window.title("OCHC File Transcription")
window.resizable(False,False)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#Create first invocation of drag and drop page.
dnd_prompt, list_box, convert_button, delete_button, add_file_button, add_folder_button, file_location = dnd_page()

#Keep window up until closed.
window.mainloop()
