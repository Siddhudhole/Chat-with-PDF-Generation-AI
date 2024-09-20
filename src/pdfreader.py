import os 
from pypdf import PdfReader



def get_text_from_pdf(file):
    try:
        text = "" 
        if file is not None : 
            reader = PdfReader(file) 
            for page in reader.pages:
                text += page.extract_text()  
        return text 

    except Exception as e :
        return "Error: Failed to upload file"         