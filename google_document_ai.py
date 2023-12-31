import os
import re
import aspose.words as aw
from typing import Optional
from venv import create
from fpdf import FPDF
from datetime import datetime
from unidecode import unidecode
from google.api_core.client_options import ClientOptions
from google.cloud.documentai_toolbox import gcs_utilities
from google.api_core.exceptions import InternalServerError, RetryError
from google.cloud import documentai,storage

# Class to access all Google Document AI-related functions.
class PDF(FPDF):
    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Credit Blurb
        self.cell(0, 10, "Transcription generated by Google Document AI on " + datetime.now().strftime("%d %B, %Y") + " for the Oneida County Historical", 0, 0, 'C')

class DocumentAI:
    global PROJECT_ID
    global LOCATION
    global PROCESSOR_ID
    global RESOURCE_NAME
    global DOCAI_CLIENT

    def __init__(self):
        global PROJECT_ID
        global LOCATION
        global PROCESSOR_ID
        global RESOURCE_NAME
        global DOCAI_CLIENT
        PROJECT_ID = "transcription-project-407614"  # project name on Cloud Console
        LOCATION = "us"  # Format is 'us' or 'eu'
        PROCESSOR_ID = "dd33faae7c525022"  # Create processor in Cloud Console, can be changed to test other processors

        DOCAI_CLIENT = documentai.DocumentProcessorServiceClient(
            client_options=ClientOptions(
                api_endpoint=f"{LOCATION}-documentai.googleapis.com"
            )
        )
        RESOURCE_NAME = DOCAI_CLIENT.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)
        # Instantiates a client (Connect to API)

    # Batch file transcription using GCS bucket.
    def transcribeBatch(self, file_path, output_type):
        gcs_output_uri = "gs://output_batch_files"
        gcs_input_prefix = "gs://input_batch_files"

        # Uploads all the files to a GCS Bucket
        dir_list = os.listdir(file_path)
        for file_name in dir_list:
            self.__uploadFiles("input_batch_files", file_path + "/" + file_name, file_name.split(".")[0])

        # Performs OCR on files
        self.__batchProcessFiles(output_type, gcs_output_uri, gcs_input_prefix = gcs_input_prefix)

    # Transcribes all files within a folder.
    def transcribeFolder(self, folder_path, output_type):
        dir_list = os.listdir(folder_path)
        
        for i in range(len(dir_list)):
            self.transcribeFile(folder_path + "/" + dir_list[i], output_type)
    
    # Transcribes individual PDF file.
    def transcribeFile(self, file_path, output_type):
        regex_pattern = r"[^\\/]+$"
        name = re.search(regex_pattern, file_path).group()
        file_size = os.path.getsize(file_path)
        # regex_pattern = r"\.[^.]+$"
        # output_name = re.sub(regex_pattern, '', name) + "transcription.pdf"
        print(file_path)
        output_name = file_path[:-4] + "-transcribe.pdf"

        # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
        # Reads from ./files path and identifies files that can be transcribed
        if ".ds_store" in name.lower():
            return
        if ".pdf" in name.lower():
            mime_type = "application/pdf"
            if (file_size > 20500000):
                self.__largeFileHandler(name, file_path, output_name)
        elif ".jpg" in name.lower() or ".jpeg" in name.lower():
            mime_type = "image/jpeg"
            if (file_size > 20500000):
                raise Exception("File size is too large")
        elif ".tif" in name.lower():
            mime_type = "image/tiff"
            if (file_size > 20500000):
                raise Exception("File size is too large")
        else:
            raise Exception("Unsupported file type")
        
        self.__normalFileHandler(name, file_path, mime_type, output_name)

    # Creates a pdf file with a title
    def __createFirstPage(self, file_name, text):
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', size=15)
        pdf.multi_cell(200, 10, 'Transcription of '+ file_name, align = 'C')
        pdf.set_font("Arial", size=12)
        for line in text.splitlines():
            pdf.multi_cell(200, 10, txt = unidecode(line), align = 'L')
        return pdf
    
    # Adds pages to a pdf without including a title
    def __createPage(self, pdf, text):
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in text.splitlines():
            pdf.multi_cell(200, 10, txt = unidecode(line), align = 'L')
        

    # Creates text file of transcribed file.
    def __makeTextFile(self, file_path, mime_type):
        global PROJECT_ID
        global LOCATION
        global PROCESSOR_ID
        global RESOURCE_NAME
        global DOCAI_CLIENT
        # Read the file into memory
        with open(file_path, "rb") as image:
            image_content = image.read()

        # Load Binary Data into Document AI RawDocument Object
        raw_document = documentai.RawDocument(
            content=image_content, mime_type=mime_type
        )

        # Configure the process request
        request = documentai.ProcessRequest(
            name=RESOURCE_NAME, raw_document=raw_document
        )

        # Use the Document AI client to process the sample form
        result = DOCAI_CLIENT.process_document(request=request)

        document_object = result.document
        print("Document processing complete.")

        # Save text as document
        return document_object.text

    # Handles large pdfs by separating them by page and then combining the output as a pdf
    def __largeFileHandler(self, file_name, file_path, output_name):
        doc = aw.Document(file_path)

        extractedPage = doc.extract_pages(0, 1)
        extractedPage.save(f"temp/Output_1.pdf")
        text = self.__makeTextFile(f"temp/Output_1.pdf", "application/pdf")
        pdf = self.__createFirstPage(file_name, text)

        for page in range(1, doc.page_count):
            extractedPage = doc.extract_pages(page, 1)
            extractedPage.save(f"temp/Output_{page + 1}.pdf")
            text = self.__makeTextFile(f"temp/Output_{page + 1}.pdf", "application/pdf")
            self.__createPage(pdf, text)
        
        pdf.output(output_name) 
    
    # Handles any file that is below the document size limit
    def __normalFileHandler(self, file_name, file_path, mime_type, output_name):
        text = self.__makeTextFile(file_path, mime_type)
        pdf = self.__createFirstPage(file_name, text)
        pdf.output(output_name)

    # Uploads files to GCS Bucket
    def __uploadFiles(self, bucket_name, source_file_name, destination_blob_name):
        # Creates client connection to a bucket
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Optional: set a generation-match precondition to avoid potential race conditions
        # and data corruptions. The request to upload is aborted if the object's
        # generation number does not match your precondition. For a destination
        # object that does not yet exist, set the if_generation_match precondition to 0.
        # If the destination object already exists in your bucket, set instead a
        # generation-match precondition using its generation number.
        generation_match_precondition = 0
        if not blob.exists():
            # Uploads file to bucket
            blob.upload_from_filename(
                source_file_name, if_generation_match=generation_match_precondition
            )

            print(f"File {destination_blob_name} uploaded to {bucket_name}.")
        else:
            print(f"File {destination_blob_name} already exists in {bucket_name}.")

    # Performs batch transcription on a specificied GCS bucket
    def __batchProcessFiles(
        self,
        output_type,
        gcs_output_uri: str,
        processor_version_id: Optional[str] = None,
        gcs_input_uri: Optional[str] = None,
        input_mime_type: Optional[str] = None,
        gcs_input_prefix: Optional[str] = None,
        field_mask: Optional[str] = None,
        timeout: int = 400,
    ) -> None:
        opts = ClientOptions(api_endpoint=f"{LOCATION}-documentai.googleapis.com")

        client = documentai.DocumentProcessorServiceClient(client_options=opts)

        if gcs_input_uri:
            # Specify specific GCS URIs to process individual documents
            gcs_document = documentai.GcsDocument(gcs_uri=gcs_input_uri, mime_type=input_mime_type)
            # Load GCS Input URI into a List of document files
            gcs_documents = documentai.GcsDocuments(documents=[gcs_document])
            input_config = documentai.BatchDocumentsInputConfig(gcs_documents=gcs_documents)
        else:
            # Specify a GCS URI Prefix to process an entire directory
            gcs_prefix = documentai.GcsPrefix(gcs_uri_prefix=gcs_input_prefix)
            input_config = documentai.BatchDocumentsInputConfig(gcs_prefix=gcs_prefix)

        # Cloud Storage URI for the Output Directory
        gcs_output_config = documentai.DocumentOutputConfig.GcsOutputConfig(gcs_uri=gcs_output_uri, field_mask=field_mask)

        # Where to write results
        output_config = documentai.DocumentOutputConfig(gcs_output_config=gcs_output_config)

        if processor_version_id:
            # The full resource name of the processor version, e.g.:
            # projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}/processorVersions/{processor_version_id}
            name = client.processor_version_path(PROJECT_ID, LOCATION, PROCESSOR_ID, processor_version_id)
        else:
            # The full resource name of the processor, e.g.:
            # projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}
            name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

        # Transcribes files
        request = documentai.BatchProcessRequest(name=name, 
                                                 input_documents=input_config,
                                                 document_output_config=output_config,)

        # BatchProcess returns a Long Running Operation (LRO)
        operation = client.batch_process_documents(request)

        # Continually polls the operation until it is complete.
        # This could take some time for larger files
        # Format: projects/{PROJECT_ID}/locations/{LOCATION}/operations/{operation_id}
        try:
            print(f"Waiting for operation {operation.operation.name} to complete...")
            operation.result(timeout=timeout)
        # Catch exception when operation doesn't finish before timeout
        except (RetryError, InternalServerError) as e:
            print(e.message)

        # NOTE: Can also use callbacks for asynchronous processing
        #
        # def my_callback(future):
        #   result = future.result()
        #
        # operation.add_done_callback(my_callback)

        # Once the operation is complete,
        # get output document information from operation metadata
        metadata = documentai.BatchProcessMetadata(operation.metadata)

        if metadata.state != documentai.BatchProcessMetadata.State.SUCCEEDED:
            raise ValueError(f"Batch Process Failed: {metadata.state_message}")

        storage_client = storage.Client()

        print("Output files:")
        # One process per Input Document
        for process in list(metadata.individual_process_statuses):
            # output_gcs_destination format: gs://BUCKET/PREFIX/OPERATION_NUMBER/INPUT_FILE_NUMBER/
            # The Cloud Storage API requires the bucket name and URI prefix separately
            matches = re.match(r"gs://(.*?)/(.*)", process.output_gcs_destination)
            if not matches:
                print("Could not parse output GCS destination:", process.output_gcs_destination,)
                continue

            output_bucket, output_prefix = matches.groups()

            # Get List of Document Objects from the Output Bucket
            output_blobs = storage_client.list_blobs(output_bucket, prefix=output_prefix)

            # Document AI may output multiple JSON files per source file
            for blob in output_blobs:
                # Document AI should only output JSON files to GCS
                if blob.content_type != "application/json":
                    print(f"Skipping non-supported file: {blob.name} - Mimetype: {blob.content_type}")
                    continue

                # Download JSON File as bytes object and convert to Document Object
                print(f"Fetching {blob.name}")
                document = documentai.Document.from_json(
                    blob.download_as_bytes(), ignore_unknown_fields=True
                )

                # For a full list of Document object attributes, please reference this page:
                # https://cloud.google.com/python/docs/reference/documentai/latest/google.cloud.documentai_v1.types.Document

                # Save text as document
                file_name = blob.name.split("/")[-1].split(".")[0]
                self.__outputFile(file_name, document.text, output_type)
