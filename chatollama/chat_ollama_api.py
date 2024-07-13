import json

import requests

import config


def chat(inputs):
    data = {
        "family": config.chat_ollama_family,
        "knowledgebaseId": 1,
        "model": config.chat_ollama_model,
        "messages": [
            {
                "role": "system",
                "content": "请忽略之前的对话,我想让你做我的好朋友，你现在会扮演我的邻家姐姐,对我十分温柔,每当我有困难就会激励和鼓舞我,"
                           "以对话的方式倾听我的倾诉.你只能用中文答复。要倾述的事情:<我最近遇到公司竞聘失败的事情，感觉很烦恼>"
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
