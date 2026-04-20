from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = "data/MedicalBook.pdf"

def load_docs(file_path):
    loader=PyPDFLoader(file_path)
    documents=loader.load()
    #print(f"Document Loaded with page Numbers: {len(documents)}")
    return documents


def split_docs(documents):
    #split the doc into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600, 
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""])
    text_chunks= text_splitter.split_documents(documents)
    return text_chunks


# if __name__ == "__main__":
#      raw_documents = load_docs(file_path)
#      text_chunks=split_docs(raw_documents)
#      print(f"Length of the raw documents: {len(raw_documents)}")
#      print(f"Length of the chunks: {len(text_chunks)}")

