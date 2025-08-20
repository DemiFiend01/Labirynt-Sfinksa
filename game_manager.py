import tkinter as tk
from tkinter import ttk
from game import *
from settings import *
from PIL import Image, ImageTk


class Game_Manager:
    def __init__(self):
        # self.game = Game()
        self.start()
        pass

    def create_new_window(self, restart=False):
        self.window = tk.Tk()
        self.window.title = "Main Menu"
        self.running = True
        self.all_backgrounds = ["resources/textures/Sphinx_main_menu.png",
                                "resources/textures/Sphinx_jak_grac.png", "resources/textures/Sphinx_intro.png",
                                "resources/textures/Sphinx_jak_grac_szybka_gra.png", "resources/textures/Sphinx_intro_szybka_gra.png"]
        self.background = self.resize_background(0)
        self.width_of_button = 20 * self.scale
        self.height_of_button = 10 * self.scale

        self.window.protocol("WM_DELETE_WINDOW", self.quit)
        self.window.geometry(f'{WIDTH}x{HEIGHT}')

        self.frame = tk.Frame(self.window)
        self.frame.pack(fill="both", expand=True)

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=0)
        self.window.grid_columnconfigure(2, weight=5)
        self.window.grid_rowconfigure(0, weight=5)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_rowconfigure(3, weight=1)
        self.window.grid_rowconfigure(4, weight=2)
        # self.frame.grid_columnconfigure(0, weight=1)
        # self.frame.grid_columnconfigure(1, weight=0)
        # self.frame.grid_columnconfigure(2, weight=5)
        # self.frame.grid_rowconfigure(0, weight=5)
        # self.frame.grid_rowconfigure(1, weight=1)
        # self.frame.grid_rowconfigure(2, weight=1)
        # self.frame.grid_rowconfigure(3, weight=1)
        # self.frame.grid_rowconfigure(4, weight=2)

        try:
            self.window.state('fullscreen')  # for windows
        except tk.TclError:
            # for laptop and Fedora
            self.window.attributes('-fullscreen', True)

        # self.window.attributes('-transparentcolor', '#ab23ff')

        # self.Label_background = tk.Label(self.window, image=self.background)
        # no need to create a new label
        self.Label_background = tk.Label(self.window, image=self.background)
        self.Label_background.place(x=0, y=0, relwidth=1, relheight=1)
        self.Label_background.lower()

        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.font = ("Georgia", round(20 * self.scale), "bold")
        self.style.configure("TButton", font=self.font,
                             foreground="#452a1b", background="#f8c53a", padding=2)

        self.window.bind("<Escape>", lambda e: self.main_menu())

        if restart:
            self.main_menu()
        else:
            self.results()

    def resize_background(self, _choice):
        image = Image.open(self.all_backgrounds[_choice])
        self.scale = max(WIDTH / image.width, HEIGHT / image.height)
        image = image.resize(
            (int(image.width * self.scale), int(image.height * self.scale)), Image.LANCZOS)

        left = (image.width - WIDTH) // 2
        top = (image.height - HEIGHT) // 2
        return ImageTk.PhotoImage(image.crop((left, top, left + WIDTH, top + HEIGHT)))

    def clear_screen(self):
        for widget in self.window.winfo_children():
            if widget != self.Label_background:  # to avoid flashing
                widget.destroy()

    def main_menu(self):
        self.clear_screen()
        self.background = self.resize_background(0)
        # self.Label_background = tk.Label(
        #     self.window, image=self.background)
        self.Label_background.configure(image=self.background)
        self.Label_background.place(x=0, y=0, relwidth=1, relheight=1)

        self.game_button = ttk.Button(
            self.window,
            text="Pełna gra",
            command=lambda: self.game_select_menu("normal")
            # width=self.padding
        )

        self.game_button.grid(row=1, column=1, pady=10,
                              ipadx=self.width_of_button, ipady=self.height_of_button)
        self.game_quick_button = ttk.Button(
            self.window,
            text="Szybka gra",
            command=lambda: self.game_select_menu("quick"),
            # padding=self.padding
        )

        self.game_quick_button.grid(row=2, column=1, pady=10,
                                    ipadx=self.width_of_button, ipady=self.height_of_button)
        self.game_info_button = ttk.Button(
            self.window,
            text="Jak grać?",
            command=lambda: self.info(self.main_menu, "normal"),
            # padding=self.padding
        )

        self.game_info_button.grid(row=3, column=1, pady=10,
                                   ipadx=self.width_of_button, ipady=self.height_of_button)

        self.game_quit_button = ttk.Button(
            self.window,
            text="Wyjdź",
            command=lambda: self.quit(),
            # padding=self.padding
        )

        self.game_quit_button.grid(row=4, column=1, pady=10,
                                   ipadx=self.width_of_button, ipady=self.height_of_button)

    def game_select_menu(self, _game_mode):
        self.game_mode = _game_mode
        self.clear_screen()
        self.background = self.resize_background(0)
        # self.Label_background = tk.Label(self.window, image=self.background)
        self.Label_background.configure(image=self.background)
        self.Label_background.place(x=0, y=0, relwidth=1, relheight=1)

        self.game_easy_button = ttk.Button(
            self.window,
            text="Uczeń",
            command=lambda: self.intro('easy'),
            # padding=self.padding
        )

        self.game_easy_button.grid(row=1, column=1, pady=10,
                                   ipadx=self.width_of_button, ipady=self.height_of_button)
        self.game_hard_button = ttk.Button(
            self.window,
            text="Mistrz",
            command=lambda: self.intro('hard'),
            # padding=self.padding
        )

        self.game_hard_button.grid(row=2, column=1, pady=10,
                                   ipadx=self.width_of_button, ipady=self.height_of_button)
        self.game_go_back_button = ttk.Button(
            self.window,
            text="Wróć",
            command=lambda: self.main_menu(),
            # padding=self.padding
        )

        self.game_go_back_button.grid(row=3, column=1, pady=10,
                                      ipadx=self.width_of_button, ipady=self.height_of_button)

    def info(self, func, _type):
        self.clear_screen()
        self.background = self.resize_background(1 if _type == "normal" else 3)
        # self.Label_background = tk.Label(self.window, image=self.background)
        self.Label_background.configure(image=self.background)
        self.Label_background.place(x=0, y=0, relwidth=1, relheight=1)

        self.game_go_back_button = ttk.Button(
            self.window,
            text="Wróć",
            command=lambda: func(),
        )

        self.game_go_back_button.grid(row=4, column=1, pady=10,
                                      ipadx=self.width_of_button, ipady=self.height_of_button)

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

    def intro(self, _level):
        self.clear_screen()
        self.background = self.resize_background(
            2 if self.game_mode == "normal" else 4)
        # self.Label_background = tk.Label(self.window, image=self.background)
        self.Label_background.configure(image=self.background)
        self.Label_background.place(x=0, y=0, relwidth=1, relheight=1)

        self.game_continue_button = ttk.Button(
            self.window,
            text="Kontynuuj",
            command=lambda: self.run_game(_level),
        )

        self.game_continue_button.grid(row=4, column=1, pady=10,
                                       ipadx=self.width_of_button, ipady=self.height_of_button)
        self.game_info_button = ttk.Button(
            self.window,
            text="Jak grać?",
            command=lambda: self.info(
                lambda: self.intro(_level), self.game_mode),
        )

        self.game_info_button.grid(row=4, column=0, pady=10,
                                   ipadx=self.width_of_button, ipady=self.height_of_button)

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
