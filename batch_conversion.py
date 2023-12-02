import sys
import os
import img2pdf
import re

cancelled = False

#Install img2pdf by typing command "pip3 install img2pdf" in terminal

def file_to_pdf(file):
#Converts single JPEG file to a PDF.
	#CITE: https://github.com/josch/img2pdf
	#DESC: Open source code from IMG2PDF github
	#Open input file and convert to pdf.
	global cancelled
	if cancelled:
		return
	match = re.search(r"(\w)+.(jpg|tif)", file)
	if match:
		title = (match.group())[0:-4] + ".pdf"
	with open(title,"wb") as f:
		f.write(img2pdf.convert(file))

def folder_to_pdf(folder_name):
#Convert all JPEG files in a folder into one multi-page pdf file.
	#Get current working directory.
	img_dir = folder_name

	#CITE: https://github.com/josch/img2pdf
	#DESC: Open source code from IMG2PDF github
	#Find all images within the directory.
	global cancelled
	if cancelled:
		return
	imgs = []
	for r, _, f in os.walk(img_dir):
		for fname in f:
			if not fname.endswith(".jpg") and not fname.endswith(".tif"):
				continue
			imgs.append(os.path.join(r, fname))
	#Converts all images in directory to pdfs.
	with open("name.pdf","wb") as f:
		f.write(img2pdf.convert(imgs))

def convert(file):
	#Check if cancelled is set True.
	global cancelled
	if cancelled:
		return
	#Regular expressions to determine if input element is file or folder.
	in_file = re.match(r"[/a-zA-Z0-9 ]+.(jpg|tif)", file)
	in_folder = re.match(r"/[a-zA-Z0-9 ]+", file)

	#If single file given, convert just that file to a pdf.
	if in_file:
		file_to_pdf(file)
	#If folder is given, convert all image files to pdfs in folder.
	elif in_folder:
		folder_to_pdf(file)
	#If argument is invalid, raise exception.
	else:
		raise Exception("Not valid file or folder name.")

def set_cancelled():
	#Function to set the 'cancelled' variable
	cancelled = True
	exit()
	#Relaunch program with saved list box elements

def main(files):
	global cancelled
	if cancelled:
		return
	#If no JPEG or TIFF file given, raise error.
	if not files:
		raise Exception("No file given.")
	
	#Convert all files from list.
	files_completed = 0
	for file in files:
		convert(file)
		files_completed += 1


if __name__ == '__main__':
	main()
