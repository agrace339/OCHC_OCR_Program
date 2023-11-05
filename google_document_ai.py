from venv import create
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from google.cloud.documentai_toolbox import gcs_utilities
import os

# How to set up authentification
# pip3 install --upgrade google-cloud-documentai
# pip3 install --upgrade google-cloud-storage
# pip3 install --upgrade google-cloud-documentai-toolbox
# Go to https://cloud.google.com/sdk/docs/install to install Google Cloud SDK
# Extract archive and run ./google-cloud-sdk/install.sh
# Say no, yes, no to the prompts
# Then run ./google-cloud-sdk/bin/gcloud init, log into account and select project
# If gcloud command is not found after running this command, run source ~/.bashrc
# Then run gcloud auth application-default login
# It should be all set!

class DocumentAI:

    def __init__(self, PROJECT_ID = "ochc-ocr", LOCATION = "us", PROCESSOR_ID = "3cb371dd084861ed"):
        self.docaiclient = documentai.DocumentProcessorServiceClient(
            client_options=ClientOptions(api_endpoint=f"{LOCATION}-documentai.googleapis.com")
        )
        self.resource_name = self.docaiclient.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)
        # Instantiates a client (Connect to API)
            

    def convertBatch(self, file_path, output_type, batch_size = 50):
        # Get list of files from path
        dir_list = os.listdir(file_path)
        __createBatch()

    def convertFile(self, file_path, output_type):
        dir_list = os.listdir(file_path)
        # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
        # Reads from ./files path and identifies files that can be transcribed
        for i in range(len(dir_list)):
            if ".jpg" in dir_list[i].lower():
                self.__makeTextFile(dir_list[i],"./files/"+dir_list[i], "image/jpeg", output_type)
            elif ".tif" in dir_list[i].lower():
                self.__makeTextFile(dir_list[i],"./files/"+dir_list[i], "image/tiff", output_type)
            elif ".pdf" in dir_list[i].lower():
                self.__makeTextFile(dir_list[i],"./files/"+dir_list[i], "application/pdf", output_type)

    def __makeTextFile(self, file_name, file_path, mime_type, output_type):
        # Read the file into memory
        with open(file_path, "rb") as image:
            image_content = image.read()
        
        # Load Binary Data into Document AI RawDocument Object
        raw_document = documentai.RawDocument(content=image_content, mime_type=mime_type)

        # Configure the process request
        request = documentai.ProcessRequest(name=self.resource_name, raw_document=raw_document)

        # Use the Document AI client to process the sample form
        result = self.docaiclient.process_document(request=request)

        document_object = result.document
        print("Document processing complete.")

        # Create .txt file with transcribed text
        output_name = "./txt_files/" + file_name.split(".")[0] + output_type
        with open(output_name, "w") as text_file:
                text_file.write(document_object.text)

    def __createBatch(self, gcs_bucket_name, file_path, batch_size = 50):
    # Creating batches of documents for processing
        batches = gcs_utilities.create_batches(
            gcs_bucket_name=gcs_bucket_name, gcs_prefix=gcs_prefix, batch_size=batch_size
        )

        print(f"{len(batches)} batch(es) created.")
        for batch in batches:
            print(f"{len(batch.gcs_documents.documents)} files in batch.")
            print(batch.gcs_documents.documents)

            # Use as input for batch_process_documents()
            # Refer to https://cloud.google.com/document-ai/docs/send-request
            # for how to send a batch processing request
            request = documentai.BatchProcessRequest(
                name="processor_name", input_documents=batch
            )
