import tkinter as tk
from TkinterDnD2 import DND_FILES, TkinterDnD

#Install tkdnd2.8 in \tcl of Python install. https://sourceforge.net/projects/tkdnd/
#Install TkinterDnD2 in the \Lib\site-packages of Python install. https://sourceforge.net/projects/tkinterdnd/

#Drag and drop information and code provided by https://stackoverflow.com/questions/25427347/how-to-install-and-use-tkdnd-with-python-tkinter-on-osx/46856247#46856247

text_file = open("example.txt", "w")

def drop_in(event):
	list_box.insert("end", event.data)	
	text_file.write(event.data)
	text_file.write("\n")

#Create Tkinter window.
window = TkinterDnD.Tk()
window.geometry("800x600")
window.title("Drag and drop your files below.")
#greeting = tk.Label(text="Hello, Tkinter")


list_box = tk.Listbox(window, selectmode=tk.SINGLE, background="White")
list_box.pack(fill=tk.X)
list_box.drop_target_register(DND_FILES)
list_box.dnd_bind("<<Drop>>", drop_in)
file_location = [list_box.get(0, last=None)]

window.mainloop()

text_file.close()
