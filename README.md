# OCHC_OCR_Program

batch_ui.py - User Interface for the Batch Conversion code
<br>In order to currently run the user interface, you will need to install TkinterDnD package:
<br>Download and install tkdnd2.8 in \tcl of Python install. https://sourceforge.net/projects/tkdnd/
<br>Download and install TkinterDnD2 in the \Lib\site-packages of Python install. https://sourceforge.net/projects/tkinterdnd/
<br>Make sure that the interpreter you use to run and compiler batch_ui.py is using the same install folder of Python that the TkinterDnD is installed.

# How to Set Up Authentification For Google Document AI
>pip3 install --upgrade google-cloud-documentai
>pip3 install --upgrade google-cloud-storage
>pip3 install --upgrade google-cloud-documentai-toolbox
<br>Go to https://cloud.google.com/sdk/docs/install to install Google Cloud SDK
<br>Extract archive and run ./google-cloud-sdk/install.sh
<br>Say no, yes, no to the prompts
<br>Then run ./google-cloud-sdk/bin/gcloud init, log into account and select project
<br>If gcloud command is not found after running this command, run source ~/.bashrc
<br>Then run gcloud auth application-default login
<br>Commands may need to be run multiple times
<br>It should be all set!
