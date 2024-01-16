
from langchain.chains.summarize import load_summarize_chain
from astrapy.db import AstraDB
import os
from langchain.chat_models import ChatOpenAI
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv(), override=True)


def init_astra_db():
    db = AstraDB(
        namespace="neji",
        token=os.environ["ASTRA_DB_APPLICATION_TOKEN"],
        api_endpoint=os.environ["ASTRA_DB_API_ENDPOINT"])

    print(f"Connected to Astra DB: {db.get_collections()}")


def load_any_document(file):

    name, extension = os.path.splitext(file)

    if extension == ".pdf":
        from langchain.document_loaders import PyPDFLoader

        print(f"loading file {file}")
        loader = PyPDFLoader(file)

    elif extension == ".docx":
        from langchain.document_loaders import Docx2txtLoader

        print(f"loading file {file}")
        loader = Docx2txtLoader(file)
    elif extension == ".txt":
        from langchain.document_loaders import TextLoader

        print(f"loading file {file}")
        loader = TextLoader(file)

    else:
        print("Non supported document format")
        return None

    data = loader.load()

    return data


def chunk_data(doc, chunk_size=256, chunk_overlap=10, metadata={}):
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=["\n", " \n"]
    )

    docs = text_splitter.split_documents(doc)
    for doc in docs:
        doc.metadata = metadata

    return docs

#ITERATE OVER FILES THAT USER UPLOADED
def create_docs(user_pdf_list, unique_id):
    output_docs = []
    file_names = []
    for document in user_pdf_list:
        bytes_data = document.read()
        file_names.append(document.name)

        file_name = os.path.join("./uploads", document.name)
        with open(file_name, "wb") as f:
            f.write(bytes_data)
        docs = load_any_document(file_name)

        chunks = chunk_data(doc=docs,
            chunk_size = 1000,
            chunk_overlap = 200,
            metadata={"name": document.name,
                      "type": document.type,
                      "size": document.size,
                      "unique_id": unique_id},)
        output_docs.extend(chunks)



    return output_docs



def get_summary(current_doc):
    llm = ChatOpenAI()
    chain = load_summarize_chain(llm=llm, chain_type="map_reduce")
    summary = chain.run([current_doc])
    return summary
