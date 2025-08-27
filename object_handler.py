from sprite_object import *


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []

        # self.add_sprite(SpriteObject(
        #    self.game, path="resources/textures/DOOM_bush.png", pos=(1.5, 1.5)))
        self.add_sprite(AnimatedSprite(
            self.game, path="resources/textures/Sphinx_lamp.png", pos=(1.5, 1.5), no_of_rows=1, no_of_cols=5, Sphinx=True, animation_time=230))
        self.add_sprite(AnimatedSprite(
            self.game, path="resources/textures/Sphinx_lamp.png", pos=(1.5, 3.5), no_of_rows=1, no_of_cols=5, Sphinx=True, animation_time=230))
        self.add_sprite(AnimatedSprite(
            self.game, path="resources/textures/Sphinx_lamp.png", pos=(4.5, 1.5), no_of_rows=1, no_of_cols=5, Sphinx=True, animation_time=230))
        self.add_sprite(AnimatedSprite(
            self.game, path="resources/textures/Sphinx_lamp.png", pos=(4.5, 3.5), no_of_rows=1, no_of_cols=5, Sphinx=True, animation_time=230))
        # self.add_sprite(AnimatedSprite(
        #     self.game, path="resources/textures/Sphinx_sprite.png", pos=(6, 2.0), no_of_rows=1, no_of_cols=18, scale=1.80, Sphinx=True))
        self.add_sprite(AnimatedSprite(
            self.game, path="resources/textures/Sphinx_sprite.png", pos=(5.5, 2.5), no_of_rows=1, no_of_cols=1, scale=2.0, Sphinx=True))

    def update(self):
        # calling the update function for all sprites in the sprite list
        for sprite in self.sprite_list:
            if sprite.is_at_Sphinx == False:
                sprite.update()

    def updateSphinx(self):
        for sprite in self.sprite_list:
            if sprite.is_at_Sphinx:
                sprite.update()

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def list_all_sprites(self):
        print([sprite.path for sprite in self.sprite_list])

    def draw(self):
        for sprite in self.sprite_list:
            if sprite.is_at_Sphinx == False:
                sprite.draw()
