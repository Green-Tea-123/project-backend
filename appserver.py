import bs4
from langchain_chroma import Chroma
from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langserve import add_routes
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

"""
**PLEASE READ BEFORE YOU USE**
A Groq API key and Langsmith API key is needed in the .env file before the below code is called.
Additionally, to use Ollama's embeddings, Ollama must be installed and the llama3 model must be pulled.
To use this code, you need to run this python script, then run sampleappclient.py on a separate terminal. After it's run, just type in your prompt into the sampleappclient terminal and you will receive a response.
"""
load_dotenv()

# Initialise model (Groq with llama)
model = ChatGroq(model="llama3-8b-8192")

# Initialise prompt template
promptTemplate = ChatPromptTemplate.from_template("You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use five sentences maximum and keep the answer concise.\
Question: {question} \
Context: {context} \
Answer:")

# Initialise parser
parser = StrOutputParser()

# Initialise DB   TODO: get this part to work cos it sure as hell isn't right now, replace chroma or embedding maybe
# bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))
loader = WebBaseLoader(
    web_paths = ("https://www.cgh.com.sg/patient-care/conditions-treatments/jaundice",
#                 "https://www.singhealth.com.sg/patient-care/conditions-treatments/jaundice", 
#                 "https://www.sgh.com.sg/patient-care/conditions-treatments/jaundice", 
#                 "https://my.clevelandclinic.org/health/symptoms/15367-adult-jaundice", 
#                 "https://www.healthxchange.sg/digestive-system/liver/obstructive-jaundice-symptoms-treatment-options", 
                 "https://www.drthngyongxian.com/jaundice-treatment-singapore/"),
)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
embeddings = OllamaEmbeddings(model="llama3",)
# this can be changed in the future to have a persistent vector store that is loaded from memory.
vectorstore = InMemoryVectorStore(embedding=embeddings)
vectorstore.add_documents(documents=docs)
# TODO: implement a max retrieval for the tokens
retriever = vectorstore.as_retriever()

# function for formatting docs
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Create chain
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | promptTemplate
    | model
    | parser
)

# Initialise app
app = FastAPI(
    title = "server", 
    version = "1.0", 
    description = "A server created in the exploration of langchain",
)

# Add route to the server
add_routes(
    app, 
    chain, 
    path = "/prompt"
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host = "localhost", port = 8000)