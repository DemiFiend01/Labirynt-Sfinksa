import os
from huggingface_hub import InferenceClient

Api_file = open("resources/api_key.txt")
API_KEY = Api_file.read()

client = InferenceClient(
    provider="cohere",
    api_key=API_KEY,
)

completion = client.chat.completions.create(
    model="CohereLabs/c4ai-command-a-03-2025",
    messages=[
        {
            "role": "user",
            "content": "Jaka jest twoja ulubiona piosenka? Odpowiedz po polsku ale bez polskich znakow"
        }
    ],
)

print(completion.choices[0].message)
