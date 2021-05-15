import pygame
import os
pygame.font.init()

# dimensions of objects
WIDTH, HEIGHT = 320, 180
SCALE = 1
MAXSCALE = 5
BORDER_WIDTH = 2
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 20, 15
BULLET_WIDTH, BULLET_HEIGHT = 4, 2


# fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 15)
WINNER_FONT = pygame.font.SysFont('comicsans', 25)

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# game settings
FPS = 60
MOVE_SPEED = 3
BULLET_VEL = 5
AMMO = 3

# controls

REDCONTROLS = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT,
               "up": pygame.K_UP, "down": pygame.K_DOWN, "shoot": pygame.K_RCTRL}

YELLOWCONTROLS = {"left": pygame.K_a, "right": pygame.K_d,
                  "up": pygame.K_w, "down": pygame.K_s, "shoot": pygame.K_LCTRL}

# images

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)


RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# events

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
