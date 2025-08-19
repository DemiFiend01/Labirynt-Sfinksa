import csv
import random
import pygame as pg
from collections import deque

# from google import genai
import google.generativeai as genai  # type: ignore
from google.generativeai import types  # type: ignore
# from google.genai import types

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

        self.top_border_height = HEIGHT * 2/3
        self.height_of_dialog_box = HEIGHT * 1/3
        self.length_of_dialog_box = WIDTH * 2/3
        self.quarter_screen_width = WIDTH * 1/6

        self.screen = self.game.screen
        self.font = self.game.font

        self.font_height = self.font.get_height()
        self.font_offset = self.font_height / 2
        self.text_offset = (self.quarter_screen_width + self.font_height,
                            self.top_border_height + self.font_height)

        self.dialog_box_texture = pg.image.load(
            "resources/textures/text_box.png").convert_alpha()

        # self.dialog_box = pg.Rect(self.quarter_screen_width, self.top_border_height,
        #                           self.length_of_dialog_box, self.height_of_dialog_box - 2*self.font_height)
        self.dialog_box = pg.transform.scale(self.dialog_box_texture, (self.length_of_dialog_box,
                                                                       self.height_of_dialog_box - 2*self.font_height))

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
        self.text_log.append(self.wrap_text(
            "Witaj śmiałku!\nCzy jesteś na tyle odważny i mądry, aby podołać moim trzem zagadkom? Odpowiedz poprawnie na przynajmniej dwie a pozwolę ci kontynuować twoją podróż. Oto pierwsza ma zagadka!"))
        self.text_log.append(self.riddles[self.current_riddle][0])

    def update(self):
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
                        self.player_responses.append(
                            self.wrap_text(self.input_text))
                        self.generate_judging(
                            self.riddles[self.current_riddle], self.input_text, self.current_riddle)
                        if self.current_riddle > 2:
                            self.judge_the_results()
                            self.finished_all_riddles = True
                        else:
                            self.text_log.append(
                                self.wrap_text(self.riddles[self.current_riddle][0]))
                    elif event.key == pg.K_BACKSPACE:
                        # delete one character
                        self.input_text = self.input_text[:-1]
                    else:
                        if len(self.input_text) < 40:
                            self.input_text += event.unicode  # add the new character to the input text

    def wrap_text(self, _text):
        max_width = self.dialog_box.get_width() - 2 * self.font_height

        lines = []

        for para in _text.split('\n'):
            words = para.split(' ')
            current_line = ""
            for word in words:
                text_line = current_line + (" " if current_line else "") + word
                if self.font.size(text_line)[0] < max_width:
                    current_line = text_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
        return "\n".join(lines)

    def draw(self):
        if self.game.finished_riddles == True:
            result_line = "Zagadki:"
            text = self.font.render(result_line, True, self.game.font_colour)
            self.screen.blit(text, (self.font_height, self.font_height))
            for i in range(0, 3):
                result_line = f"{i+1}: " + self.riddles[i][0]
                text = self.font.render(
                    result_line, True, self.game.font_colour)

                self.screen.blit(
                    text, (self.font_height,  2*self.font_height + i * 2.5*self.font_height))
                result_line = " Odpowiedź poprawna: " + \
                    self.riddles[i][1] + " Odpowiedź gracza: " + \
                    self.player_responses[i]
                text = self.font.render(
                    result_line, True, self.game.font_colour)
                self.screen.blit(
                    text, (self.font_height, 2*self.font_height + i * 2.5*self.font_height + self.font_height))
                pass
            return

        self.screen.blit(self.dialog_box,
                         (self.quarter_screen_width, self.top_border_height))
        # pg.draw.rect(self.screen, (27, 27, 27), self.dialog_box)
        if self.is_reading:
            lines = self.text_log[0].split("\n")
            for i, line in enumerate(lines):
                reading_text = self.font.render(
                    line, True, self.game.font_colour)
                self.screen.blit(
                    reading_text, (self.text_offset[0], self.text_offset[1] + i * self.font.get_linesize()))
            # reading_text = self.font.render(
            #     self.text_log[0], True, self.game.font_colour)
            # self.screen.blit(reading_text, self.text_offset)

        elif self.is_typing:
            writing_text = self.font.render(
                self.input_text, True, self.game.font_colour)
            message = self.font.render(
                "Napisz swoją odpowiedź: ", True, self.game.font_colour)
            self.screen.blit(message, self.text_offset)
            message_width = message.get_width()
            self.screen.blit(
                writing_text, (self.text_offset[0] + message_width, self.text_offset[1]))

    def generate_judging(self, question, answer, number_of_riddle):
        response = self.model.generate_content(

            contents=(f"Zachowuj się jak tajemnicza, fantastyczna, niesamowicie {self.personality_type[0]} Sfinks,"
                      f"oceniająca i analizująca odpowiedź młodego gracza na zagadkę."
                      # f"Zachowuj się jak tajemniczy, fantastyczny Sfinks oceniający i analizujący odpowiedź młodego gracza na zagadkę, który."
                      f"Nie zadawaj pytań. Nie dodawaj komentarzy dla gracza. Nie mów także, że odpowiedź jest idealna, że się zgadza z odpowiedzią poprawną."
                      f"WAŻNE: Akceptuj też niedoskonałe odpowiedzi, które znaczą to samo co poprawna odpowiedź."
                      f"Odpowiedź poprawna to jedyna prawdziwa prawidłowa odpowiedź. Sfinks nigdy nie kwestionuje tej odpowiedzi."
                      f"Porównaj odpowiedź gracza do odpowiedzi poprawnej i oceniaj wyłącznie na podstawie tej odpowiedzi."
                      f"Zagadkę: {question[0]}."
                      f"Odpowiedź gracza: {answer}."
                      f"Odpowiedź poprawna: {question[1]}."
                      f"Pisząc odpowiedź, używaj przynajmniej trzech długich zdań. Używaj kobiecych zaimków mówiąc o sobie."
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

        self.text_log.append(self.wrap_text(raw_text))
        self.current_riddle += 1
        # return completion.choices[0].message.content.strip()

    def judge_the_results(self):
        response = ""
        if self.all_points == 0:
            response = "Ach śmiałku, niestety nie udało ci się poprawnie odpowiedzieć na żadną z moich zagadek.\n" \
                "Wróć do mnie jak zdobędziesz siłę na kolejną mą próbę! Nie martw się, śmiertelniku...\n" \
                "Zwycięstwo do wytrwałych należy!"
        elif self.all_points == 1:
            response = "Ach śmiałku, byłeś blisko, ale niestety nie udało ci się przejść przez moje wyzwanie. Odpowiedziałeś poprawnie jedynie na jedną z moich zagadek. Wróć do mnie jak zdobędziesz siłę na kolejną mą próbę!\nNie martw się, śmiertelniku...\n" \
                "Zwycięstwo do wytrwałych należy!"
        elif self.all_points == 2:
            response = "Gratulacje, śmiałku! Udało ci się odpowiedzieć poprawnie" \
                " na dwie z moich trzech zagadek. To wyczyn godny chwały i punktu ode mnie.\n" \
                "Teraz możesz iść dalej, zmierzyć się z resztą wyzwań albo jeżeli tego pragnie twoja nienasycona dusza...\n" \
                "Możesz spróbować zmierzyć się ze mną jeszcze raz, spróbować zdobyć lepszy wynik."
        elif self.all_points == 3:
            response = "Gratulacje! Przechytrzyłeś mnie, dzielny wędrowcze.\n" \
                "Odpowiedziałeś poprawnie na wszystkie moje łamigłówki!" \
                " Jestem pod wrażeniem, nie tak łatwo mnie pokonać. Dostajesz ode mnie punkt!\n" \
                "Teraz idź, nadeszła twoja pora. Musisz zmierzyć się z resztą wyzwań..."
        self.text_log.append(self.wrap_text(response))

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
                riddle_text = row['riddle'].replace('\\\\n', '\n')
                result.append((riddle_text, row['answer']))

        return result

    def read_personalities(self):
        with open('resources/personality.csv', 'r', encoding='utf-8') as csvin:
            reader = csv.DictReader(
                # fieldnames so that the DictReader doesn't eat the first line
                csvin, delimiter=';', fieldnames=['personality'])
            result = []
            for row in reader:  # read all lines and add them to the list of riddles
                result.append(tuple(row[field]
                                    for field in reader.fieldnames))

        return result
