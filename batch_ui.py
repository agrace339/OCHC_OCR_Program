import tkinter as tk
from TkinterDnD2 import DND_FILES, TkinterDnD
import batch_conversion

#Install tkdnd2.8 in \tcl of Python install. https://sourceforge.net/projects/tkdnd/
#Install TkinterDnD2 in the \Lib\site-packages of Python install. https://sourceforge.net/projects/tkinterdnd/

#Drag and drop information and code provided by https://stackoverflow.com/questions/25427347/how-to-install-and-use-tkdnd-with-python-tkinter-on-osx/46856247#46856247

def drop_in(event):
	list_box.insert("end", event.data)	

def convert():
	batch_conversion.main(list_box.get('0', 'end'))
	pop_up("Files successfully converted!")

def pop_up(message):
	popUpWindow = TkinterDnD.tk()
	popUpWindow.geometry("300x200")
	textMessage = tk.Label(popUpWindow, text=message)
	textMessage.pack(side="top", fill="x", pady=10)
	confirmButton = tk.Button(popUpWindow, text="Confirm", command = popUpWindow.destroy)
	confirmButton.pack()
	popUpWindow.mainloop()

#Create Tkinter window.
window = TkinterDnD.Tk()
window.geometry("800x600")
window.title("Drag and drop your files below.")
#greeting = tk.Label(text="Hello, Tkinter")

list_box = tk.Listbox(window, selectmode=tk.SINGLE, background="d9d9d9")
list_box.pack(fill=tk.X)
list_box.drop_target_register(DND_FILES)
list_box.dnd_bind("<<Drop>>", drop_in)
file_location = [list_box.get(0, last=None)]

#If convert button is pressed, get contents of listbox and convert.
convert_button = tk.Button(window, text= "Hello!", command = convert)
convert_button.place(x=400, y=500)

window.mainloop()
