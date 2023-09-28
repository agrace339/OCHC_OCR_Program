from google.api_core.client_options import ClientOptions
from google.cloud import documentai
import os

# How to set up authentification
# pip3 install --upgrade google-cloud-documentai
# pip3 install --upgrade google-cloud-storage
# pip3 install --upgrade google-cloud-documentai-toolbox
# Go to https://cloud.google.com/sdk/docs/install to install Google Cloud SDK
# extract archive and run ./google-cloud-sdk/install.sh
# say no, yes, no to the prompts
# then run ./google-cloud-sdk/bin/gcloud init, log into account and select project
# If gcloud command is not found after running this command, run source ~/.bashrc
# Then run gcloud auth application-default login
# It should be all set!


PROJECT_ID = "ochc-ocr"
LOCATION = "us"  # Format is 'us' or 'eu'
PROCESSOR_ID = "3cb371dd084861ed"  # Create processor in Cloud Console

def makeTextFile(file_name, file_path, mime_type):
	# Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()
	
    # Load Binary Data into Document AI RawDocument Object
    raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=RESOURCE_NAME, raw_document=raw_document)

    # Use the Document AI client to process the sample form
    result = docai_client.process_document(request=request)

    document_object = result.document
    output_name = file_name.split(".")[0] + ".txt"
    print(output_name)
    print("Document processing complete.")
    #print(f"Text: {document_object.text}")

    with open(output_name, "w") as text_file:
		    text_file.write(document_object.text)

# Instantiates a client
docai_client = documentai.DocumentProcessorServiceClient(
    client_options=ClientOptions(api_endpoint=f"{LOCATION}-documentai.googleapis.com")
)

# The full resource name of the processor, e.g.:
# projects/project-id/locations/location/processor/processor-id
# You must create new processors in the Cloud Console first
RESOURCE_NAME = docai_client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

path = r"./files"
dir_list = os.listdir(path)

# Refer to https://cloud.google.com/document-ai/docs/file-types
# for supported file types
for i in range(len(dir_list)):
       if ".jpg" in dir_list[i] or ".JPG" in dir_list[i]:
                makeTextFile(dir_list[i],"./files/"+dir_list[i], "image/jpeg")
       elif ".tif" in dir_list[i]:
		        makeTextFile(dir_list[i],"./files/"+dir_list[i], "image/tiff")
       elif ".pdf" in dir_list[i]:
                makeTextFile(dir_list[i],"./files/"+dir_list[i], "application/pdf")