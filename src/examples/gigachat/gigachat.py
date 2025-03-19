import requests
import json

url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

payload = json.dumps({
  "model": "GigaChat",
  "messages": [
    {
      "role": "system",
      "content": "Ты профессиональный переводчик на английский язык. Переведи точно сообщение пользователя."
    },
    {
      "role": "user",
      "content": "GigaChat — это сервис, который умеет взаимодействовать с пользователем в формате диалога, писать код, создавать тексты и картинки по запросу пользователя."
    }
  ],
  "stream": False,
  "update_interval": 0
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'OGVjYmIxNWUtN2ViMC00ZTY2LTgyODMtMjkzYWIwMjA4ZDQ4OjkzOTg3OTc1LWYxMTUtNDhmZS1hMDRmLWYxYTU3MWFlMTE0Nw=='
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)