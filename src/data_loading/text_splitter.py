from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text(data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)
    return all_splits