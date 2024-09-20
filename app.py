import streamlit as st 
import os 
from pypdf import PdfReader 


from langchain_huggingface import HuggingFaceEndpoint

from langchain import LLMChain
from langchain_core.output_parsers import StrOutputParser



from src.pdfreader import get_text_from_pdf 
from src.TextProcessor import get_text_splitter 
from src.model import get_retriver_chain 



os.environ['HUGGINGFACEHUB_API_TOKEN'] ='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' 

st.title("Chat with PDF ") 

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"]) 

if uploaded_file is not None:
    text = get_text_from_pdf(uploaded_file) 
    chunk = get_text_splitter(text)
    chain = get_retriver_chain(chunk)
    query = st.text_input('Ask Quenstion ')
    if st.button(label='answer'):
        response = chain.invoke({'input':query})
        st.write("Answer:", response['answer']) 
    


#     # Load the PDF fileST
  

# 
#          


        

#         retriver = db.as_retriever() 

#         retriver_chain =create_retrieval_chain (retriver,document_chain) 
        

# query = st.text_input("Ask a question")

# responce = retriver_chain.invoke({'input':query})

# if st.button(label='answer'): 
#     st.write("Answer:",responce['answer'])  










             


        


