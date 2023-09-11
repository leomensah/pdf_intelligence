import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from template import css, bot_template, user_template


def handle_pdf_input(pdf_docs):
    """
    Extracts text from multiple PDF documents and concatenates them into a single string.

    Parameters:
    - pdf_docs (list): List of paths to the PDF documents.

    Returns:
    - text (str): Concatenated text from the PDF documents.
    """
    text = ""

    # Iterate over each PDF document in the pdf_docs list
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)

        # Iterate over each page in the PDF document
        for page in pdf_reader.pages:
            # Extract the text content of the current page and append it to the 'text' variable
            text += page.extract_text()

    return text


def handle_chunk_data(raw_text):
    """
    Splits the raw text into smaller chunks of a specified size.

    Parameters:
    - raw_text (str): The text to be split into chunks.

    Returns:
    - chunks (list): List of text chunks.
    """

    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks


def save_chunk_to_database(text_chunks):
    """
    Creates a vector store from the text chunks using OpenAI embeddings.

    Parameters:
    - text_chunks (list): List of text chunks.

    Returns:
    - vectorstore (FAISS): Vector store created from the text chunks.
    """

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def handle_conversation(vectorstore):
    """
    Creates a conversation chain for conversational retrieval using an LLM and vector store.

    Parameters:
    - vectorstore (FAISS): Vector store containing text embeddings.

    Returns:
    - conversation_chain (ConversationalRetrievalChain): Conversation chain for conversational retrieval.
    """

    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vectorstore.as_retriever(), memory=memory
    )
    return conversation_chain


def handle_user_input(user_question):
    """ " Handles user input in the chat app.

    Parameters:
    - user_question (str): The question or message entered by the user

    Returns:
    - None
    """

    # Send user question to the conversation API and update chat history
    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

    # Iterate over the chat history and display messages in the chat application
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            # Display user message using the user template
            st.write(
                user_template.replace("{{MSG}}", message.content),
                unsafe_allow_html=True,
            )
        else:
            # Display bot message using the bot template
            st.write(
                bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True
            )


def main():
    """
    Main function for the PDF Chat App.
    Handles the user interaction, document upload, and initializes the conversation chain.
    """

    load_dotenv()
    st.set_page_config(page_title="PDF Chat App", page_icon=":random:")

    st.write(css, unsafe_allow_html=True)

    # Initialize session state variables if not already present
    st.session_state.setdefault("conversation", None)
    st.session_state.setdefault("chat_history", None)

    st.header("CHAT PDFs :books:")

    # Get user input from a text input field
    user_question = st.text_input("Interact with documents Here!", key="user_input")
    if user_question:
        handle_user_input(user_question)

    with st.sidebar:
        st.subheader("Uploaded Documents")

        # Allow users to upload multiple PDF documents
        pdf_docs = st.file_uploader(
            "Upload Document and Click on Load Button", accept_multiple_files=True
        )
        if st.button("LOAD"):
            with st.spinner("loading.."):
                # Get pdf text content from the uploaded PDF documents
                raw_text = handle_pdf_input(pdf_docs)

                # Split the raw text into smaller chunks for processing
                text_chunks = handle_chunk_data(raw_text)

                # Create vector store from the text chunks
                vectorstore = save_chunk_to_database(text_chunks)

                # Create conversation chain using the vector store
                st.session_state.conversation = handle_conversation(vectorstore)

    # Add a button to clear the chat history
    if st.button("Clear Chat"):
        st.session_state.chat_history = None
        st.session_state.conversation = None


if __name__ == "__main__":
    main()
