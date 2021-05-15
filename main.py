import pygame
import os
import settings
from gameObject import GameObj
from view import GameView
pygame.mixer.init()

field = pygame.Rect(0, 0, settings.WIDTH, settings.HEIGHT)
camera = pygame.Rect(0, 0, settings.WIDTH, settings.HEIGHT)
view = GameView(camera, field, settings.SCALE, settings.MAXSCALE)

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


def draw_window(red, yellow, bullets, red_health, yellow_health):
    # draw the background and border
    view.display_background(SPACE)
    view.display_rectangle(BORDER, settings.BLACK)

    view.display_object(red)
    view.display_object(yellow)
    # spaceships

    # any bullets
    for bullet in bullets:
        view.display_rectangle(bullet, settings.WHITE)

    # text
    red_health_text = settings.HEALTH_FONT.render(
        "Health: " + str(red_health), 1, settings.WHITE)
    yellow_health_text = settings.HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, settings.WHITE)
    view.get_display().blit(red_health_text, (view.get_window_width() - red_health_text.get_width() -
                                              10, view.get_window_height() - red_health_text.get_height() - 10))
    view.get_display().blit(yellow_health_text, (10, view.get_window_height() -
                                                 yellow_health_text.get_height() - 10))
    pygame.display.update()


def draw_winner(text):
    text = settings.WINNER_FONT.render(text, 1, settings.WHITE)
    view.get_display().blit(text, (view.get_window_width() // 2 - text.get_width() //
                                   2, view.get_window_height() // 2 - text.get_height() // 2))
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
                        yellow.get_y() + yellow.get_height() // 2 - settings.BULLET_HEIGHT // 2,
                        settings.BULLET_WIDTH, settings.BULLET_HEIGHT
                    ))

                if event.key == settings.REDCONTROLS["shoot"] and len(red_bullets) < settings.AMMO:
                    # make a red bullet
                    red_bullets.append(pygame.Rect(
                        red.get_x(), red.get_y() + red.get_height() // 2 - settings.BULLET_HEIGHT // 2,
                        settings.BULLET_WIDTH, settings.BULLET_HEIGHT
                    ))

                if event.key == pygame.K_COMMA:
                    # scale everything up
                    view.increaseScale()

            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1

        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, yellow, settings.YELLOWCONTROLS)
        handle_movement(keys_pressed, red, settings.REDCONTROLS)
        view.move(view.get_x() + 1, view.get_y())
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
