import math
# game settings
# global variables, signed as constants, but remember that technically they can be changed (as in Python doesn't stop you)
RES = WIDTH, HEIGHT = 1600, 900  # RES is a tuple now
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 120

PLAYER_POS = 1, 1  # on the mini_map
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002  # rotation speed

FOV = math.pi / 3
HALF_FOV = FOV / 2  # float division
NUM_RAYS = WIDTH // 2  # integer division
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20  # draw distance

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
# to mantain better performance, because number of rays is less than screen resolution
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2
