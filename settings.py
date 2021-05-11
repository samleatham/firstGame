import pygame
import os
pygame.font.init()

# dimensions of objects
WIDTH, HEIGHT = 900, 500
BORDER_WIDTH = 10
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# game settings
FPS = 60
MOVE_SPEED = 5
BULLET_VEL = 7
AMMO = 5

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
