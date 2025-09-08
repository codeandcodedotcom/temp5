from openai import AzureOpenAI


client = AzureOpenAI(
    azure_endpoint="https://azureai.openai.azure.com/",
    api_key="787dab688---cd008702e6",
    api_version="2025-01-01-preview",
)

response = client.chat.completions.create(
    model="o4-mini",
    messages=[{"role": "user", "content": "What is time"}],
    max_tokens=500,
    temperature=0
)

print(response.choices[0].message.content)

