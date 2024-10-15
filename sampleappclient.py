from langserve import RemoteRunnable

remote_chain = RemoteRunnable("http://localhost:8000/prompt/")
result = remote_chain.invoke({"text": "I want to know how to treat jaundice"})
print(result)