from huggingface_hub import InferenceClient
import csv


class AI_Sphinx:
    def __init__(self, game):
        self.api_file = open("resources/api_key.txt")
        self.API_KEY = self.api_file.read()
        self.client = InferenceClient(
            provider="cohere",
            api_key=self.API_KEY,
        )

        self.riddles = self.read_riddles()
        print(self.riddles)

    def generate_judging(self, question, answer):
        completion = self.client.chat.completions.create(
            model="CohereLabs/c4ai-command-a-03-2025",
            messages=[
                {
                    "role": "user",
                    "content": "Zachowuj sie jak tajemniczy Sfinks oceniający odpowiedź na zagadkę: Mam duzo nog, kim jestem? odpowiedz gracza: antylopa odpowiedz poprawna: stonoga. Powiedz czy przyznalbys punkt graczowi za jego opowiedz"
                }
            ],
        )

        print(completion.choices[0].message)
        pass

    def read_riddles(self):
        with open('resources/riddles.csv', 'r') as csvin:
            reader = csv.DictReader(
                csvin, delimiter=';', fieldnames=['riddle', 'answer'])
            result = []
            for row in reader:
                result.append(tuple(row[field] for field in reader.fieldnames))

            return result
