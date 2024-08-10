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
                "content": config.chat_ollama_system_prompt
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
