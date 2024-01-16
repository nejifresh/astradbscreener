import os
from langchain.embeddings import OpenAIEmbeddings
import streamlit as st
import uuid
from utils import *
from dotenv import find_dotenv, load_dotenv
from langchain.vectorstores import AstraDB


def main():
    load_dotenv(find_dotenv(), override=True)
    st.set_page_config(page_title="Resume Screening Assistant")
    st.title('HR - Resume Screening Assistant')
    st.subheader('I can help you screen candidates')
    load_dotenv(find_dotenv(), override=True)

    init_astra_db()

    job_description = st.text_area("Please past the 'JOB DESCRIPTION' here..", key=1)
    document_count = st.text_input("No. of matching RESUMES to return ", key=2)

    # upload the resumes
    pdfs = st.file_uploader("Upload resumes here. Only PDF files are allowed", type=["pdf"], accept_multiple_files=True)
    submit = st.button('Analyze resumes')

    if submit:
        with st.spinner('Uploading and analyzing documents'):

            st.session_state["unique_id"] = uuid.uuid4().hex
            # create the documents list from all the uploaded pdfs
            docs = create_docs(pdfs, st.session_state["unique_id"])
            # display the count of resumes that have been uploaded
            st.write(len(docs))

            # create emebeddings instance
            embedding = OpenAIEmbeddings()
            vstore = AstraDB(
                namespace="neji",
                embedding=embedding,
                collection_name="resumes",
                token=os.environ["ASTRA_DB_APPLICATION_TOKEN"],
                api_endpoint=os.environ["ASTRA_DB_API_ENDPOINT"],
            )

            inserted_docs = vstore.add_documents(docs)
            st.write(f"\nInserted {len(inserted_docs)} documents into vector store.")

            #now perform similarity search to show candidates
            relevant_docs = (vstore.similarity_search(job_description, k=document_count))

            for item in range(len(relevant_docs)):
                st.subheader("👉" + str(item + 1))
                # display the filepath
                st.write("**File** : " + relevant_docs[item].metadata["name"])
                # add expander
                with st.expander("Display Summary 👀"):
                    summary = get_summary(relevant_docs[item])
                    st.write(summary)
            st.success('Hope I was able to save your time... Thanks')


if __name__ == '__main__':
    main()