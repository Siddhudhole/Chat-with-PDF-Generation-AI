import streamlit as st  
from dotenv import load_dotenv 
from pypdf import PdfReader 
from langchain.text_splitter import CharacterTextSplitter 
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain.vectorstores import FAISS 
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain



def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf) 
        for page in pdf_reader.pages: 
            text += page.extract_text()
    return text 

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(chunk_size=1000,
                                          separator="\n\n",
                                          chunk_overlap=200,
                                          length_function=len)
    chunks = text_splitter.split_text(raw_text)
    return chunks 

def get_chunk_retriver(text_chunk):
    embedding = HuggingFaceEmbeddings(
    model_name="hkunlp/instructor-large",
    model_kwargs= {'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
    ) 
    vectorstore = FAISS.from_texts(text_chunk,embedding=embedding)
    retriver = vectorstore.as_retriever()
    return retriver  


def get_conversation_chain(retriever):
    llm = llm = HuggingFaceEndpoint(
    repo_id="microsoft/Phi-3-mini-4k-instruct",
    task="text-generation",
    max_new_tokens=100,
    do_sample=False,
    repetition_penalty=1.03)

    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context.
        Think step by step before answering the question.
        <context>
        {context}
        </context>
        question:{input}""")
    

    document_chain = create_stuff_documents_chain(llm, prompt)
    
    conversation_chain =  create_retrieval_chain(retriever, document_chain)
    
    return conversation_chain 
 






def main():
    st.set_page_config(page_title='ChatWIthPdf',page_icon=':books:') 
    load_dotenv() 
    st.title("Chat With PDF AI :books:")
    quenstion = st.text_input('Ask a question about your documents') 
    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    with st.sidebar:
        st.subheader('Your Documents') 
        pdf_docs = st.file_uploader('Upload your PDF documents', type=['pdf'],
                         accept_multiple_files=True) 
        if st.button('Process'):
            with st.spinner('Processing'):
                #get the pdf text
                raw_text = get_pdf_text(pdf_docs)

                #get the text chunk 
                text_chunk = get_text_chunks(raw_text)
                
                # get the chunk embedding
            
                retriever = get_chunk_retriver(text_chunk)
                
                # get the conversation chain
    
                st.session_state.conversation = get_conversation_chain(retriever)

                st.success('Procession completed successfully')
                
    
    if st.button('Answer'):
        with st.spinner('Answering'):
            responce = st.session_state.conversation.invoke({'input':quenstion})
            st.write(responce['answer'])  
                 
            
    
        





if __name__ == "__main__":
    main() 