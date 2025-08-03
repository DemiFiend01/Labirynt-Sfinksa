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


class Game:
    def __init__(self):  # constructor of the class, self is like this from c++
        # pg.init()
        # now we set the resolution of our screen
        self.screen = pg.display.set_mode(RES, pg.RESIZABLE)
        self.clock = pg.time.Clock()  # we initialise our clock
        pg.mouse.set_visible(False)
        self.delta_time = 1
        self.check_map = False
        self.new_game()
        self.Sphinx_room = False
        # self.switch = True

    def new_game(self):  # initialise some stuff
        self.map = Map(self)  # because map takes this Game as an argument
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        # self.static_sprite = SpriteObject(w
        #     self, path="resources/textures/DOOM_bush.png", pos=(1.5, 1.5))
        # self.animated_sprite = AnimatedSprite(
        #     self, path="resources/textures/animated_lamp.png", pos=(5, 1.5), no_of_rows=1, no_of_cols=6)

    def update(self):
        self.player.update()
        self.raycasting.update()
        if self.Sphinx_room:
            self.object_handler.update()  # update all objects that are in the sphinx roomsssss
        # update the clock once per framerate aka 60 fps given
        # update the delta_time, it is a float
        self.delta_time = self.clock.tick(FPS)
        # display the information behind fps on our screen
        pg.display.set_caption(f'{self.clock.get_fps(): .1f}')

        # or self.switch:
        if (self.player.get_map_pos == (self.map.goal_x + 1, self.map.goal_y+1)):
            print("You got there!")
            self.map.teleport_to_sphinx()
            self.player.set_map_pos(2.5, 2.5)
            self.player.set_angle(0)  # reset
            self.Sphinx_room = True
            # self.switch = False

    def draw(self):  # render
        self.screen.fill('black')  # clear the window
        if self.check_map:
            self.map.draw()
            self.player.draw()
        else:
            self.object_renderer.draw()

        # self.map.draw()
        pg.display.flip()  # Update the full display Surface to the screen

        # self.player.draw()

    def check_events(self):
        for event in pg.event.get():  # basically event polling
            # if key is pressed and it is escape button
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()  # uninitialize all pygame modules

                # Raise a SystemExit exception, signaling an intention to exit the interpreter.
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_m:
                self.check_map = not self.check_map

    def run(self):  # to be changed, because what do you mean while True
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    # In Python, every module (a .py file) has a special built-in variable called __name__.
    # If the file is being run directly, __name__ is set to '__main__'.
    # If the file is being imported as a module into another file, __name__ is set to the module’s name (e.g., 'game', 'utils', etc.)
    game = Game()
    game.run()
