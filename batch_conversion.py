import sys
import os
import img2pdf
import re

def jpg_to_pdf(file):
#Converts single JPEG file to a PDF.
	#CITE: https://github.com/josch/img2pdf
	#DESC: Open source code from IMG2PDF github
	#Open input file and convert to pdf.
	with open("name.pdf","wb") as f:
		f.write(img2pdf.convert(file))

def batch_jpg_to_pdf(folder_name):
#Convert all JPEG files in a folder into one multi-page pdf file.
	#Get current working directory.
	
	img_dir = os.getcwd() + folder_name

	#CITE: https://github.com/josch/img2pdf
	#DESC: Open source code from IMG2PDF github
	#Find all images within the directory.
	imgs = []
	for r, _, f in os.walk(img_dir):
		for fname in f:
			if not fname.endswith(".jpg") and not fname.endswith(".tif"):
				continue
			imgs.append(os.path.join(r, fname))
	#Converts all images in directory to pdfs.
	with open("name.pdf","wb") as f:
		f.write(img2pdf.convert(imgs))

	# multiple inputs (variant 2)
	#with open("name.pdf","wb") as f:
	#	f.write(img2pdf.convert(["test1.jpg", "test2.png"]))

def main():
	#If no JPEG or TIFF file given, raise error.
	if (len(sys.argv) <= 1):
		raise Exception("No file given.")

	#Take argument from command line as input file.
	in_element = sys.argv[1]

	#regular expression to determine if input element is file or folder.
	in_file = re.match(r"[a-zA-Z0-9]+.(jpg|tif)", in_element)
	in_folder = re.match(r"/[a-zA-Z0-9]+", in_element)

	#If single file given, convert just that file.
	if in_file:
		print("file")
		jpg_to_pdf(in_element)
	#If folder is given, convert all jpeg files in folder.
	elif in_folder:
		print("folder!")
		batch_jpg_to_pdf(in_element)
	else:
		print("Not valid file or folder name.")

if __name__ == '__main__':
	main()
