# OCHC_OCR_Program

A group project written by Anna Grace, Zoe Carovano, and Divyam Karuri creating a transcription desktop app using Optical Character Recognition (OCR) through Google Document AI. This project was created to transcribe handwritten and print historical documents with easy-to-learn UI for our client, the Oneida County Historical Society.

## How to Set Up batch_ui.py - User Interface for the Batch Conversion code
<br>In order to currently run the user interface, you will need to install TkinterDnD package:
<br>Download and install tkdnd2.8 in \tcl of Python install. Check which binary you may need in the files section. https://sourceforge.net/projects/tkdnd/
<br>Download and install TkinterDnD2 in the \Lib\site-packages of Python install. https://sourceforge.net/projects/tkinterdnd/
<br>Make sure that the interpreter you use to run and compiler batch_ui.py is using the same install folder of Python that the TkinterDnD is installed.
<br>Additionally, install CustomTkinter via pip install.
```
pip3 install tkinter
pip3 install tkinterdnd2
pip3 install customtkinter
```
If you are setting up on a Mac computer:
```
pip3 install tkmacosx
```

## How to Set Up batch_conversion.py - Batch Conversion from TIFF and JPEG files to PDF files
Install the necessary package, img2pdf.
```
pip3 install img2pdf
```
If the packages os, sys, or re are not updated or installed, ```pip3 install ____``` (the package you are missing).

## How to Set Up Authentification For Google Document AI
First install the neccessary packages. We use pip, but feel free to use whatever you already have installed.
```
pip install --upgrade google-cloud-documentai
pip install --upgrade google-cloud-storage
pip install --upgrade google-cloud-documentai-toolbox
pip install fpdf
pip install unidecode
pip install aspose-words
pip install typing
```
Go to https://cloud.google.com/sdk/docs/install to install Google Cloud SDK.
<br>Extract archive and run ```./google-cloud-sdk/install.sh``` and reply no, yes, no to the prompts.
<br>Then run ```./google-cloud-sdk/bin/gcloud init```, log into account and select the correct project.
<br>If gcloud command is not found after running this command, run ```source ~/.bashrc```
<br>Then run ```gcloud auth application-default login```
<br>Commands may need to be run multiple times
<br>It should be all set!

The final step is the set the credentials for Google Document AI. These credentials are in the JSON file in the directory. To set it on Mac, where JSON_PATH is the path to the credential file,
```
export GOOGLE_APPLICATION_CREDENTIALS=JSON_PATH
```
<br>To set it on Windows, you must edit environment variables from Control Panel. 
<br>Click on 'New...' under 'User variables for USER'
<br>Set the Variable name to ```GOOGLE_APPLICATION_CREDENTIALS```
<br>Set the Variable value to the JSON_PATH which is the path to the credential file.
