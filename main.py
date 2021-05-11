import pygame
import os
import settings
from gameObject import GameObj
pygame.mixer.init()

WIN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("First Game")

BORDER = pygame.Rect((settings.WIDTH // 2) - (settings.BORDER_WIDTH // 2),
                     0, settings.BORDER_WIDTH, settings.HEIGHT)


SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "space.png")), (settings.WIDTH, settings.HEIGHT))

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    settings.YELLOW_SPACESHIP_IMAGE,
    (settings.SPACESHIP_WIDTH, settings.SPACESHIP_HEIGHT)), 90)


RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    settings.RED_SPACESHIP_IMAGE,
    (settings.SPACESHIP_WIDTH, settings.SPACESHIP_HEIGHT)), 270)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


def image_scale(image, scale):
    if scale > 1:
        return pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
    else:
        return image


def rect_scale(rect, scale):
    if scale > 1:
        x = rect.x * scale
        y = rect.y * scale
        width = rect.width * scale
        height = rect.height * scale
        return pygame.Rect(x, y, width, height)
    else:
        return rect


def draw_window(red, yellow, bullets, red_health, yellow_health):
    # draw the background and border
    WIN.blit(image_scale(SPACE, settings.SCALE), (0, 0))
    pygame.draw.rect(WIN, settings.BLACK, rect_scale(BORDER, settings.SCALE))

    # spaceships
    WIN.blit(image_scale(red.get_image(), settings.SCALE),
             (red.get_x() * settings.SCALE, red.get_y() * settings.SCALE)
             )

    WIN.blit(image_scale(yellow.get_image(), settings.SCALE),
             (yellow.get_x() * settings.SCALE, yellow.get_y() * settings.SCALE)
             )

    # any bullets
    for bullet in bullets:
        pygame.draw.rect(WIN, settings.WHITE,
                         rect_scale(bullet, settings.SCALE)
                         )

    # text
    red_health_text = settings.HEALTH_FONT.render(
        "Health: " + str(red_health), 1, settings.WHITE)
    yellow_health_text = settings.HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, settings.WHITE)
    WIN.blit(red_health_text, (WIN.get_width() - red_health_text.get_width() -
                               10, WIN.get_height() - red_health_text.get_height() - 10))
    WIN.blit(yellow_health_text, (10, WIN.get_height() -
                                  yellow_health_text.get_height() - 10))
    pygame.display.update()


def draw_winner(text):
    text = settings.WINNER_FONT.render(text, 1, settings.WHITE)
    WIN.blit(text, (WIN.get_width() // 2 - text.get_width() //
                    2, WIN.get_height() // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in red_bullets:
        bullet.x -= settings.BULLET_VEL
        if yellow.checkcollision(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x += settings.BULLET_VEL
        if red.checkcollision(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.y > settings.WIDTH:
            yellow_bullets.remove(bullet)


def handle_movement(keys, player, controls):
    xmove = player.get_x() + \
        (keys[controls["right"]] - keys[controls["left"]]) * settings.MOVE_SPEED

    ymove = player.get_y() + \
        (keys[controls["down"]] - keys[controls["up"]]) * settings.MOVE_SPEED

    player.move(xmove, ymove)


def main():
    red_shape = pygame.Rect(700, 200, settings.SPACESHIP_HEIGHT,
                            settings.SPACESHIP_WIDTH)
    red_bounds = pygame.Rect(settings.WIDTH // 2, 0,
                             settings.WIDTH // 2, settings.HEIGHT)
    red = GameObj(settings.RED_SPACESHIP_IMAGE, 270, red_shape, red_bounds)

    yellow_shape = pygame.Rect(100, 200, settings.SPACESHIP_HEIGHT,
                               settings.SPACESHIP_WIDTH)
    yellow_bounds = pygame.Rect(0, 0,
                                settings.WIDTH // 2, settings.HEIGHT)
    yellow = GameObj(settings.YELLOW_SPACESHIP_IMAGE, 90,
                     yellow_shape, yellow_bounds)

    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(settings.FPS)
        keys_pressed = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == settings.YELLOWCONTROLS["shoot"] and len(yellow_bullets) < settings.AMMO:
                    # make a yellow bullet
                    yellow_bullets.append(pygame.Rect(
                        yellow.get_x() + yellow.get_width(),
                        yellow.get_y() + yellow.get_height() // 2 - 2, 10, 5)
                    )

                if event.key == settings.REDCONTROLS["shoot"] and len(red_bullets) < settings.AMMO:
                    # make a red bullet
                    red_bullets.append(pygame.Rect(
                        red.get_x(), red.get_y() + red.get_width() // 2 - 2, 10, 5)
                    )

                if event.key == pygame.K_COMMA:
                    # scale everything up
                    settings.SCALE = (settings.SCALE % settings.MAXSCALE) + 1
                    pygame.display.set_mode(
                        (settings.WIDTH * settings.SCALE, settings.HEIGHT * settings.SCALE))

            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1

        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, yellow, settings.YELLOWCONTROLS)
        handle_movement(keys_pressed, red, settings.REDCONTROLS)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets +
                    yellow_bullets, red_health, yellow_health)

        winner_text = ""
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if winner_text:
            draw_winner(winner_text)
            break
    main()


if __name__ == "__main__":
    main()
