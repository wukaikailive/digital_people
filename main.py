from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms.ollama import Ollama

llm = Ollama(base_url="http://localhost:11434", model="llama3:latest", )


def get_completion_ollama(prompt):
    return llm.invoke(prompt)


prompt = '微软是什么，使用中文回答'
res = get_completion_ollama(prompt=prompt)
print(res)