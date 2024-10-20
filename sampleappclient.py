from langserve import RemoteRunnable

"""
To use this, run appserver.py first, then run this on another terminal.
Type your prompt into the terminal after it has started running, then await the response.
To exit, simply type exit into the terminal.
"""

remote_chain = RemoteRunnable("http://localhost:8000/prompt/")
while True:
    prompt = input()
    if prompt == "exit":
        break
    result = remote_chain.invoke(input)
    print(result)