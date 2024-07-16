import json

import requests

import config


def chat(inputs):
    data = {
        "family": config.chat_ollama_family,
        "knowledgebaseId": config.chat_ollama_knowledgebase_id if config.chat_ollama_use_knowledgebase else None,
        "model": config.chat_ollama_model,
        "messages": [
            {
                "role": "system",
                "content": "请忽略之前的对话,"
                           "你现在充当一个直播平台的主播，为观众提供有趣的回答，你的回答不能出现markdown的公式，如果遇到公式、数字、表达式等，请转换为能直接读出来的语言。并且记住，"
                           "你的回答不能出现任何表情、反动、政治敏感、色情、赌博、毒品等内容，如果你认为出现了这些内容，你直接回复我不知道即可。"
            },
            {
                "role": "user",
                "content": inputs,
                "model": f"{config.chat_ollama_family}/{config.chat_ollama_model}",
            }
        ],
        "stream": False
    }
    url = config.chat_ollama_server_url + "/api/models/chat"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Chat-Ollama-Keys': '{"ollama":{"endpoint":"http://host.docker.internal:11434",'
                              '"username":"812166094@qq.com","password":"123456"},"openai":{"key":"","endpoint":"",'
                              '"proxy":false},"azureOpenai":{"key":"","endpoint":"","deploymentName":"",'
                              '"proxy":false},"anthropic":{"key":"","endpoint":"","proxy":false},"moonshot":{'
                              '"key":"","endpoint":""},"gemini":{"key":"","proxy":false,"endpoint":""},'
                              '"groq":{"key":"","endpoint":"","proxy":false},"custom":[]}'
    }
    json_data = json.dumps(data, ensure_ascii=False)

    response = requests.post(url, headers=headers, data=json_data.encode("utf-8"))
    result = response.json()
    print(result)
    return result["message"]["content"]
