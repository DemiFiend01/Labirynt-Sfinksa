import tkinter as tk
from tkinter import ttk
from game import *
from settings import *


class Game_Manager:
    def __init__(self):
        # self.game = Game()
        self.start()
        pass

    def create_new_window(self):
        self.window = tk.Tk()
        self.window.title = "Main Menu"
        self.running = True
        self.window.protocol("WM_DELETE_WINDOW", self.quit)
        self.window.geometry(f'{WIDTH}x{HEIGHT}')
        try:
            self.window.state('zoomed')  # Works on Windows
        except tk.TclError:
            self.window.attributes('-fullscreen', True)  # Works on most Linux distros
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure("TButton", font=(
            "Helvetica", 16), foreground='blue', background='violet', padding=5)
        self.main_menu()

    def clear_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_screen()
        self.game_button = ttk.Button(
            self.window,
            text="Game",
            command=lambda: self.game_select_menu("normal")
        )
        self.game_button.pack(
            ipadx=5,
            ipady=6,
            expand=True
        )
        self.game_quick_button = ttk.Button(
            self.window,
            text="Quick",
            command=lambda: self.game_select_menu("quick")
        )
        self.game_quick_button.pack(
            ipadx=5,
            ipady=6,
            expand=True
        )
        self.game_quit_button = ttk.Button(
            self.window,
            text="Quit",
            command=lambda: self.quit()
        )
        self.game_quit_button.pack(
            ipadx=5,
            ipady=7,
            expand=True
        )

    def game_select_menu(self, _game_mode):
        self.game_mode = _game_mode
        self.clear_screen()
        self.game_easy_button = ttk.Button(
            self.window,
            text="Uczeń",
            command=lambda: self.run_game('easy')
        )
        self.game_easy_button.pack(
            ipadx=5,
            ipady=6,
            expand=True
        )
        self.game_hard_button = ttk.Button(
            self.window,
            text="Mistrz",
            command=lambda: self.run_game('hard')
        )
        self.game_hard_button.pack(
            ipadx=5,
            ipady=6,
            expand=True
        )
        self.game_go_back_button = ttk.Button(
            self.window,
            text="Go back",
            command=lambda: self.main_menu()
        )
        self.game_go_back_button.pack(
            ipadx=5,
            ipady=7,
            expand=True
        )

    def update(self):
        self.window.update_idletasks()
        self.window.update()

    def render(self):
        pass

    def start(self):
        self.create_new_window()
        while self.running:
            self.update()
            self.render()

    def run_game(self, _level):
        self.quit()
        self.game = Game(_level, self.game_mode)
        self.start()

    def quit(self):
        self.running = False
        self.window.destroy()


if __name__ == '__main__':
    # In Python, every module (a .py file) has a special built-in variable called __name__.
    # If the file is being run directly, __name__ is set to '__main__'.
    # If the file is being imported as a module into another file, __name__ is set to the module’s name (e.g., 'game', 'utils', etc.)
    # game = Game()
    # game.run()
    Game_Manager()
