import csv
import random
import pygame as pg
from collections import deque

#from google import genai
import google.generativeai as genai
from google.generativeai import types
#from google.genai import types

from settings import *


class AI_Sphinx:
    def __init__(self, game):
        # setting up the AI client
        self.api_file = open("resources/api_key.txt")
        self.API_KEY = self.api_file.read()
        # self.client = genai.Client(api_key=self.API_KEY)
        genai.configure(api_key=self.API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash-lite")


        # reading all riddles and randomizing their order
        self.game = game
        self.level = self.game.level

        self.riddles = self.read_riddles(self.level)
        random.shuffle(self.riddles)
        self.personality_type = self.read_personalities()
        random.shuffle(self.personality_type)
        self.player_responses = deque()

        self.three_quarters_screen_height = HEIGHT * 3/4
        self.quarter_screen_height = HEIGHT * 1/4
        self.half_screen_width = WIDTH * 1/2
        self.quarter_screen_width = WIDTH * 1/4

        self.screen = self.game.screen
        self.font = self.game.font
        self.font_height = self.font.get_height()
        self.font_offset = self.font_height / 2
        self.text_offset = (self.quarter_screen_width + self.font_height,
                            self.three_quarters_screen_height + self.font_height)

        self.text_log = deque()
        self.input_text = ""
        self.is_typing = False
        self.is_reading = True
        self.finished_all_riddles = False
        self.all_points = 0

    def start_riddles(self):
        self.game.player.set_angle(0)
        self.current_riddle = 0
        self.all_points = 0
        # append the first question
        self.text_log.append(
            "Witaj śmiałku!\nCzy jesteś na tyle odważny i mądry, aby podołać moim trzem zagadkom?\nOdpowiedz poprawnie na przynajmniej dwie a pozwolę ci kontynuować twoją podróż.\nOto pierwsza ma zagadka!")
        self.text_log.append(self.riddles[self.current_riddle][0])

    def update(self):
        # if self.current_riddle > 2:
        #     self.finished_all_riddles = True
        #     return
        if self.game.finished_riddles:
            return

        for event in self.game.events:
            if self.is_reading:
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    # remove the currently reading line
                    self.text_log.popleft()

                if len(self.text_log) == 0:
                    # apparently we've read all we could, we didnt finish, now let's type in the answer
                    self.is_typing = True
                    self.is_reading = False
                    self.input_text = ""  # clear the input
                    if self.finished_all_riddles == True:
                        self.game.finished_riddles = True
                        return

            elif self.is_typing:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.is_reading = True
                        self.is_typing = False
                        self.player_responses.append(self.input_text)
                        self.generate_judging(
                            self.riddles[self.current_riddle], self.input_text, self.current_riddle)
                        if self.current_riddle > 2:
                            self.judge_the_results()
                            self.finished_all_riddles = True
                        else:
                            self.text_log.append(
                                self.riddles[self.current_riddle][0])
                    elif event.key == pg.K_BACKSPACE:
                        # delete one character
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode  # add the new character to the input text

    def draw(self):
        if self.game.finished_riddles == True:
            result_line = "Zagadki:"
            text = self.font.render(result_line, True, (240, 255, 240))
            self.screen.blit(text, (self.font_height, self.font_height))
            for i in range(0, 3):
                result_line = f"{i+1}: " + self.riddles[i][0]
                text = self.font.render(
                    result_line, True, (240, 255, 240))
                self.screen.blit(
                    text, (self.font_height, 2*self.font_height + i * 2.5*self.font_height))
                result_line = " Odpowiedź poprawna: " + \
                    self.riddles[i][1] + " Odpowiedź gracza: " + \
                    self.player_responses[i]
                text = self.font.render(
                    result_line, True, (240, 255, 240))
                self.screen.blit(
                    text, (self.font_height, 2*self.font_height + i * 2.5*self.font_height + self.font_height))
                pass
            return

        pg.draw.rect(self.screen, (27, 27, 27), (self.quarter_screen_width,
                     self.three_quarters_screen_height, self.half_screen_width, self.quarter_screen_height - 2*self.font_height))
        if self.is_reading:
            lines = self.text_log[0].split("\n")
            for i, line in enumerate(lines):
                reading_text = self.font.render(
                    line, True, (240, 255, 240))
                self.screen.blit(
                    reading_text, (self.text_offset[0], self.text_offset[1] + i * self.font.get_linesize()))
            # reading_text = self.font.render(
            #     self.text_log[0], True, (240, 255, 240))
            # self.screen.blit(reading_text, self.text_offset)

        elif self.is_typing:
            writing_text = self.font.render(
                self.input_text, True, (240, 255, 240))
            message = self.font.render(
                "Napisz swoją odpowiedź: ", True, (240, 255, 240))
            self.screen.blit(message, self.text_offset)
            message_width = message.get_width()
            self.screen.blit(
                writing_text, (self.text_offset[0] + message_width, self.text_offset[1]))

    def generate_judging(self, question, answer, number_of_riddle):
        # response = self.client.models.generate_content(
        # response = self.client.models.generate_content( 
        #     model="gemini-2.5-flash-lite",
        #     contents=(f"Zachowuj się jak tajemniczy, fantastyczny, niesamowicie {self.personality_type[0]} Sfinks,"
        #               f"oceniający i analizujący odpowiedź młodego gracza na zagadkę."
        #               # f"Zachowuj się jak tajemniczy, fantastyczny Sfinks oceniający i analizujący odpowiedź młodego gracza na zagadkę, który."
        #               f"Nie zadawaj pytań. Nie dodawaj komentarzy dla gracza. Nie mów także, że odpowiedź jest idealna, że się zgadza z odpowiedzią poprawną."
        #               f"WAŻNE: Akceptuj też niedoskonałe odpowiedzi, które znaczą to samo co poprawna odpowiedź."
        #               f"Odpowiedź poprawna to jedyna prawdziwa prawidłowa odpowiedź. Sfinks nigdy nie kwestionuje tej odpowiedzi."
        #               f"Porównaj odpowiedź gracza do odpowiedzi poprawnej i oceniaj wyłącznie na podstawie tej odpowiedzi."
        #               f"Zagadkę: {question[0]}."
        #               f"Odpowiedź gracza: {answer}."
        #               f"Odpowiedź poprawna: {question[1]}."
        #               #   f"{self.personality_type[0]}, uwielbiasz o tym wszystkim opowiadać non stop, naprawdę non stop."
        #               # f"To {number_of_riddle+1} próba (Trzecia - 3 - to ostatnia). "
        #               #   f"Pisząc odpowiedź, używaj kilku zdań. Nie mogą być bardzo długie, ale powinny być normalne i nie za krótkie."
        #               f"Pisząc odpowiedź, używaj przynajmniej trzech długich zdań."
        #               #   f"Nie używaj przecinków, myślników ani wielokropek ('...'). "
        #               f"Odpowiedź musi zaczynać się dokładnie od '[TAK]' lub '[NIE]' bez spacji lub znaków interpunkcyjnych po nich."
        #               f"Przykład: [TAK]Poprawnie śmiertelniku. Rozpoznałeś się na mojej zagadce, niczym mądra Atena."
        #               f"Lub: [NIE]Ach, błędny wędrowcze, twoja odpowiedź nie jest tą, której szukam. Nie zrozumiałeś natury mojej zagadki."
        #               ),
        #     config=types.GenerateContentConfig(
        #         thinking_config=types.ThinkingConfig(
        #             thinking_budget=0)  # Disables thinking
        #     ),

        # )
        response = self.model.generate_content( 
            contents=(f"Zachowuj się jak tajemniczy, fantastyczny, niesamowicie {self.personality_type[0]} Sfinks,"
                      f"oceniający i analizujący odpowiedź młodego gracza na zagadkę."
                      # f"Zachowuj się jak tajemniczy, fantastyczny Sfinks oceniający i analizujący odpowiedź młodego gracza na zagadkę, który."
                      f"Nie zadawaj pytań. Nie dodawaj komentarzy dla gracza. Nie mów także, że odpowiedź jest idealna, że się zgadza z odpowiedzią poprawną."
                      f"WAŻNE: Akceptuj też niedoskonałe odpowiedzi, które znaczą to samo co poprawna odpowiedź."
                      f"Odpowiedź poprawna to jedyna prawdziwa prawidłowa odpowiedź. Sfinks nigdy nie kwestionuje tej odpowiedzi."
                      f"Porównaj odpowiedź gracza do odpowiedzi poprawnej i oceniaj wyłącznie na podstawie tej odpowiedzi."
                      f"Zagadkę: {question[0]}."
                      f"Odpowiedź gracza: {answer}."
                      f"Odpowiedź poprawna: {question[1]}."
                      #   f"{self.personality_type[0]}, uwielbiasz o tym wszystkim opowiadać non stop, naprawdę non stop."
                      # f"To {number_of_riddle+1} próba (Trzecia - 3 - to ostatnia). "
                      #   f"Pisząc odpowiedź, używaj kilku zdań. Nie mogą być bardzo długie, ale powinny być normalne i nie za krótkie."
                      f"Pisząc odpowiedź, używaj przynajmniej trzech długich zdań."
                      #   f"Nie używaj przecinków, myślników ani wielokropek ('...'). "
                      f"Odpowiedź musi zaczynać się dokładnie od '[TAK]' lub '[NIE]' bez spacji lub znaków interpunkcyjnych po nich."
                      f"Przykład: [TAK]Poprawnie śmiertelniku. Rozpoznałeś się na mojej zagadce, niczym mądra Atena."
                      f"Lub: [NIE]Ach, błędny wędrowcze, twoja odpowiedź nie jest tą, której szukam. Nie zrozumiałeś natury mojej zagadki."
                      ),
            generation_config=types.GenerationConfig(
                temperature=0.7
            )
        )
        raw_text = response.text

        if raw_text.upper().startswith("[TAK]"):
            self.all_points += 1
        raw_text = raw_text[5:].strip()

        char_limit = 80
        current_idx = char_limit

        modified_text = ""
        while raw_text:
            if len(raw_text) <= char_limit:
                modified_text += raw_text
                break
            current_idx = char_limit
            while raw_text[current_idx] != ' ':
                current_idx -= 1
                if current_idx < 0:
                    break  # error
            modified_text += raw_text[:current_idx+1]+"\n"
            raw_text = raw_text[current_idx+1:]
        self.text_log.append(modified_text)

        self.current_riddle += 1
        # return completion.choices[0].message.content.strip()

    def judge_the_results(self):
        response = ""
        if self.all_points == 0:
            response = "Ach śmiałku, niestety nie udało ci się poprawnie odpowiedzieć\n" \
                "na żadną z moich zagadek. Wróć do mnie jak zdobędziesz siłę\n" \
                "na kolejną mą próbę! Nie martw się, śmiertelniku...\n" \
                "Zwycięstwo do wytrwałych należy!"
        elif self.all_points == 1:
            response = "Ach śmiałku, byłeś blisko, ale niestety nie udało ci się przejść\n"\
                "przez moje wyzwanie. Odpowiedziałeś poprawnie jedynie na jedną z moich zagadek.\n"\
                "Wróć do mnie jak zdobędziesz siłę\n" \
                "na kolejną mą próbę! Nie martw się, śmiertelniku...\n" \
                "Zwycięstwo do wytrwałych należy!"
        elif self.all_points == 2:
            response = "Gratulacje, śmiałku! Udało ci się odpowiedzieć poprawnie\n" \
                "na dwie z moich trzech zagadek. To wyczyn godny chwały i punktu ode mnie.\n" \
                "Teraz możesz iść dalej, zmierzyć się z resztą wyzwań\n" \
                "albo jeżeli tego pragnie twoja nienasycona dusza...\n" \
                "Możesz spróbować zmierzyć się ze mną jeszcze raz, spróbować zdobyć lepszy wynik."
        elif self.all_points == 3:
            response = "Gratulacje! Przechytrzyłeś mnie, dzielny wędrowcze.\n" \
                "Odpowiedziałeś poprawnie na wszystkie moje łamigłówki!\n" \
                "Jestem pod wrażeniem, nie tak łatwo mnie pokonać. Dostajesz ode mnie punkt!\n" \
                "Teraz idź, nadeszła twoja pora. Musisz zmierzyć się z resztą wyzwań..."
        self.text_log.append(response)

    def read_riddles(self, _level):
        if _level == 'easy':
            file = 'resources/riddles.csv'
        else:
            file = 'resources/riddles_hard.csv'
        with open(file, 'r', encoding='utf-8') as csvin:
            reader = csv.DictReader(
                # fieldnames so that the DictReader doesn't eat the first line
                csvin, delimiter=';', fieldnames=['riddle', 'answer'])
            result = []
            for row in reader:  # read all lines and add them to the list of riddles
                result.append(tuple(row[field] for field in reader.fieldnames))

            return result

    def read_personalities(self):
        with open('resources/personality.csv', 'r', encoding='utf-8') as csvin:
            reader = csv.DictReader(
                # fieldnames so that the DictReader doesn't eat the first line
                csvin, delimiter=';', fieldnames=['personality'])
            result = []
            for row in reader:  # read all lines and add them to the list of riddles
                result.append(tuple(row[field] for field in reader.fieldnames))

            return result
