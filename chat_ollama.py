from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def call_ollama(inputs):
    inputs = inputs + ", 使用中文回答，并且内容尽量精简，最好不要超过20个字。"
    llm = ChatOllama(base_url="http://127.0.0.1:11434", model="llama3:latest")
    prompt = ChatPromptTemplate.from_template(inputs)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({})
