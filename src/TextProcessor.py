from langchain.text_splitter import RecursiveCharacterTextSplitter


def get_text_splitter(text):
    """
    This function uses RecursiveCharacterTextSplitter to split a long text into manageable chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        
    )
    text = text_splitter.split_text(text)
    return text