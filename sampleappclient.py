from langserve import RemoteRunnable

remote_chain = RemoteRunnable("http://localhost:8000/prompt/")
result = remote_chain.invoke("What is jaundice caused by?")
print(result)