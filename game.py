import pygame as pg

# The sys module controls:
# program input, output, and error streams, enabling precise data handling beyond standard input and print functions,
# Command-line arguments
# also gives us paths
import sys
from settings import *  # inluding a file from our project
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from AI_model import *


class Game:
    # constructor of the class, self is like this from c++
    def __init__(self, _level, _game_mode):
        pg.init()
        # now we set the resolution of our screen
        self.running = True
        self.screen = pg.display.set_mode(RES, pg.FULLSCREEN)
        self.clock = pg.time.Clock()  # we initialise our clock
        pg.mouse.set_visible(False)
        self.delta_time = 1

        self.check_map = False
        self.map_background = pg.image.load(
            "resources/textures/Sphinx_map_back.png").convert_alpha()
        self.map_background = pg.transform.scale(
            self.map_background, (WIDTH, HEIGHT))
        self.help_screen = False
        self.help_screen_image = pg.image.load(
            "resources/textures/Sphinx_jak_grac.png").convert_alpha()
        self.help_screen_image = pg.transform.scale(
            self.help_screen_image, (WIDTH, HEIGHT))

        pg.display.set_caption("Labirynt Sfinksa")

        # self.font_size = int(HEIGHT * 0.028)
        self.font_size = int(WIDTH * 0.018)
        self.font_colour = "#fcefc9"
        self.font = pg.font.SysFont('georgia', self.font_size)

        self.quick_game_switch = False if _game_mode == "normal" else True
        self.level = _level
        self.new_game()
        self.Sphinx_room = False
        self.finished_riddles = False
        self.run()

    def new_game(self):  # initialise some stuff
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)

        self.object_handler = ObjectHandler(self)
        self.map = Map(self)  # because map takes this Game as an argument

        self.raycasting = RayCasting(self)

        self.AI_Sphinx = AI_Sphinx(self)
        # self.static_sprite = SpriteObject(w
        #     self, path="resources/textures/DOOM_bush.png", pos=(1.5, 1.5))
        # self.animated_sprite = AnimatedSprite(
        #     self, path="resources/textures/animated_lamp.png", pos=(5, 1.5), no_of_rows=1, no_of_cols=6)

    def update(self):
        if self.finished_riddles == True:
            self.Sphinx_room = False
            self.running = False
            return

        if self.Sphinx_room == False:
            self.player.update()

        self.raycasting.update()

        if self.Sphinx_room:
            # update all objects that are in the sphinx roomsssss
            self.object_handler.updateSphinx()
            self.AI_Sphinx.update()
        else:
            self.object_handler.update()

        # update the clock once per framerate aka 60 fps given
        # update the delta_time, it is a float
        self.delta_time = self.clock.tick(FPS)
        # # display the information behind fps on our screen
        # pg.display.set_caption(f'{self.clock.get_fps(): .1f}')

        # or self.switch:
        if (self.player.get_map_pos == (self.map.goal_x + 1, self.map.goal_y+1)) or self.quick_game_switch == True:
            print("You got there!")
            self.map.teleport_to_sphinx()
            self.player.set_map_pos(2.5, 2.5)
            self.player.rel = 0
            self.player.set_angle(0)  # reset
            self.AI_Sphinx.start_riddles()
            self.Sphinx_room = True
            self.quick_game_switch = False

    def draw(self):  # render
        self.screen.fill('black')  # clear the window
        # if self.finished_riddles == True:
        #     reading_text = self.font.render(
        #         str(self.AI_Sphinx.all_points)+"/3", True, self.font_colour)
        #     self.screen.blit(reading_text, (WIDTH//2, HEIGHT//2))
        #     self.AI_Sphinx.draw()
        # else:
        if self.check_map:
            self.screen.blit(self.map_background, (0, 0))
            self.map.draw()
            self.player.draw()
            # self.object_handler.draw()
            # self.object_handler.list_all_sprites()
        elif self.help_screen:
            self.screen.blit(self.help_screen_image, (0, 0))
        else:
            self.object_renderer.draw()

        if self.Sphinx_room:
            self.AI_Sphinx.draw()

        # self.map.draw()
        pg.display.flip()  # Update the full display Surface to the screen

        # self.player.draw()

    def check_events(self):
        self.events = pg.event.get()
        for event in self.events:  # basically event polling
            # if key is pressed and it is escape button
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False
                # pg.quit()  # uninitialize all pygame modules

                # Raise a SystemExit exception, signaling an intention to exit the interpreter.
                # sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_m and self.Sphinx_room == False:
                self.check_map = not self.check_map

            if event.type == pg.KEYDOWN and event.key == pg.K_h and self.Sphinx_room == False:
                self.help_screen = not self.help_screen

    def run(self):  # to be changed, because what do you mean while True
        self.running = True
        while self.running:
            self.check_events()
            self.update()
            self.draw()
        pg.quit()
