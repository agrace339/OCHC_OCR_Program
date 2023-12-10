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
        pdf_loc = file[0:-4] + ".pdf"
    with open(pdf_loc,"wb") as f:
        f.write(img2pdf.convert(file))
    return pdf_loc

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
    folder_index = folder_name.rindex("/")
    if folder_index != -1:
        # title = folder_name[folder_index+1:] + ".pdf"
        pdf_loc = folder_name + ".pdf"
	#Converts all images in directory to pdfs.
    with open(pdf_loc, "wb") as f:
        f.write(img2pdf.convert(imgs))
    return pdf_loc

def convert(file):
	#Check if cancelled is set True.
    global cancelled
    if cancelled:
        return
	#Regular expressions to determine if input element is file or folder.
    if (os.path.isfile(file) and file.endswith(".jpg")) or (os.path.isfile(file) and file.endswith(".tif")):
        pdf_loc = file_to_pdf(file)
	#If folder is given, convert all image files to pdfs in folder.
    elif os.path.isdir(file):
        pdf_loc = folder_to_pdf(file) #If single file given, convert just that file to a pdf.
    #If argument is invalid, raise exception.
    else:
        raise Exception("Not valid file or folder name.")
    return pdf_loc

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
    pdf_locs = []
    files_completed = 0
    for file in files:
        pdf_locs.append(convert(file))
        files_completed += 1
    return pdf_locs

if __name__ == '__main__':
    main()
