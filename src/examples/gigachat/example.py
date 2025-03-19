from gigachat import GigaChat

# Используйте ключ авторизации, полученный в личном кабинете, в проекте GigaChat API.
with GigaChat(credentials="OGVjYmIxNWUtN2ViMC00ZTY2LTgyODMtMjkzYWIwMjA4ZDQ4OjkzOTg3OTc1LWYxMTUtNDhmZS1hMDRmLWYxYTU3MWFlMTE0Nw==",
              ca_bundle_file="russian_trusted_root_ca.cer") as giga:
    response = giga.chat("Какие факторы влияют на стоимость страховки на дом?")
    print(response.choices[0].message.content)