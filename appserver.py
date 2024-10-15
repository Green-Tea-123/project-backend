from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes

"""
A Groq API key and Langsmith API key is needed in the .env file before the below code is called.
"""
load_dotenv()

# Initialise model (Groq with llama)
model = ChatGroq(model="llama3-8b-8192")

# Initialise prompt template
systemTemplate = "Please respond to this user's query"
promptTemplate = ChatPromptTemplate.from_messages([
    ("system", systemTemplate), 
    ("user", "{text}")
])

# Initialise parser
parser = StrOutputParser()

# Create chain
chain = promptTemplate | model | parser

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