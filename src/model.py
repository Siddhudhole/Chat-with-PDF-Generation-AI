from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain 
from langchain.prompts import ChatPromptTemplate
def get_retriver_chain(chunk):
    """
    Given a user query, this function will return an appropriate answer using the provided tools.
    """
    # Preprocess the query
    prompt=ChatPromptTemplate.from_template(
            """You are an AI assistant. You will be given a task. You must generate a detailed and long answer. 
            <context>
            {context} 
            Question: {input}""") 


        # Create a chain of LLM models
    llm = HuggingFaceEndpoint(repo_id='microsoft/Phi-3-mini-4k-instruct',max_new_tokens=100)
    document_chain = create_stuff_documents_chain(llm=llm,prompt=prompt)  
    # Load embeddings
    embeddings = HuggingFaceEmbeddings()
    # Create a vectorstore using FAISS
    vectorstore = FAISS.from_texts(chunk,embeddings) 
    # Create a retrieval chain
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    chain = create_retrieval_chain(retriever,document_chain) 
    return chain 
    