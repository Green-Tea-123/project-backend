from langserve import RemoteRunnable

remote_chain = RemoteRunnable("http://localhost:8000/prompt/")
result = remote_chain.invoke({"question": "What is jaundice caused by?"})
print(result)