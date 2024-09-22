import streamlit as st
import os

# Function to save the uploaded file
def save_uploadedfile(uploadedfile, directory):
    if uploadedfile is not None : 
        # Ensure the directory exists
        if not os.path.exists(directory):
            os.makedirs(directory,exist_ok=True)
        # Save the file
        with open(os.path.join(directory, uploadedfile.name), "wb") as f:
            f.write(uploadedfile.getbuffer()) 


with st.sidebar:
    st.title("PDF Uploader")
    st.text("Upload your PDF files to this app.")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"]) 

    
    if uploaded_file is not None:
        directory = "pdfs"
        save_uploadedfile(uploaded_file, directory)
        st.success(f"File uploaded successfully ") 
        if st.button('Remove PDF'):
            for i in os.walk('pdfs'):
                 for file in i[2]:
                    os.remove(os.path.join(i[0], file)) 
            st.success(f"Removed all uploaded files") 



    





