import re

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import config
import chatollama.chat_ollama_api as chat_ollama_api
import time

def call_ollama(inputs):
    start = time.perf_counter()
    if config.use_chat_ollama:
        result = chat_ollama_api.chat(inputs)
        result = filter_chat_ollama(result)
        end = time.perf_counter()
        print('LLM处理时间为：{}秒'.format(end - start))
        return result
    else:
        inputs = inputs + ", 使用中文回答，并且内容尽量精简，最好不要超过20个字。"
        llm = ChatOllama(base_url="http://127.0.0.1:11434", model="llama3:latest")
        prompt = ChatPromptTemplate.from_template(inputs)
        chain = prompt | llm | StrOutputParser()
        result = chain.invoke({})
        end = time.perf_counter()
        print('LLM处理时间为：{}秒'.format(end - start))
        return result


def filter_chat_ollama(inputs):
    if config.chat_ollama_use_knowledgebase:
        search_result = re.search(r'```markdown\n##.*?\n\n(.*?)```', inputs, re.M | re.I | re.S)
        if search_result and search_result.group(1):
            return search_result.group(1)
    return inputs
