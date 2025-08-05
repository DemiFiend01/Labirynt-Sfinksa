from huggingface_hub import InferenceClient
import csv
import random
import pygame


class AI_Sphinx:
    def __init__(self, game):
        self.api_file = open("resources/api_key.txt")
        self.API_KEY = self.api_file.read()
        self.client = InferenceClient(
            provider="cohere",
            api_key=self.API_KEY,
        )

        self.riddles = self.read_riddles()
        random.shuffle(self.riddles)
        print(self.riddles)
        self.one_cycle(game)

    def generate_judging(self, question, answer):
        completion = self.client.chat.completions.create(
            model="CohereLabs/c4ai-command-a-03-2025",
            messages=[
                {
                    "role": "user",
                    "content": (f"Zachowuj sie jak tajemniczy Sfinks oceniający odpowiedź na zagadkę: "
                                f"{question[0]} odpowiedz gracza: {answer} odpowiedz poprawna: {question[0]}."
                                f"Przyznaj punkt, jeżeli odpowiedź gracza jest poprawna")
                }
            ],
        )

        print(completion.choices[0].message)
        return completion.choices[0].message.content.strip()

    def get_text_input(self, screen, font, question):
        input_text = ""
        active = True
        clock = pygame.time.Clock()

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            screen.fill((30, 30, 30))
            q_surf = font.render(question, True, (255, 255, 255))
            a_surf = font.render(input_text, True, (0, 255, 0))
            screen.blit(q_surf, (50, 50))
            screen.blit(a_surf, (50, 100))
            pygame.display.flip()
            clock.tick(30)

        return input_text

    def one_cycle(self, game):
        line = self.riddles[0]
        question = line[0]
        correct_answer = line[1]
        print(question)
        font = pygame.font.Font(None, 32)
        answer = self.get_text_input(game.screen, font, question)
        judge = self.generate_judging(line, answer)
        showing_result = True
        while showing_result:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    showing_result = False
                    return
                elif event.type == pygame.KEYDOWN:
                    showing_result = False  # exit when any key pressed

            game.screen.fill((30, 30, 30))
            q_surf = font.render(judge, True, (255, 255, 255))
            game.screen.blit(q_surf, (50, 50))
            pygame.display.flip()
            game.clock.tick(30)

    def read_riddles(self):
        with open('resources/riddles.csv', 'r') as csvin:
            reader = csv.DictReader(
                # fieldnames so that the DictReader doesn't eat the first line
                csvin, delimiter=';', fieldnames=['riddle', 'answer'])
            result = []
            for row in reader:  # read all lines and add them to the list of riddles
                result.append(tuple(row[field] for field in reader.fieldnames))

            return result
