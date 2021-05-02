import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")
BORDER_WIDTH = 10
BORDER = pygame.Rect((WIDTH // 2) - (BORDER_WIDTH // 2),
                     0, BORDER_WIDTH, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
MOVE_SPEED = 5
BULLET_VEL = 7
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
AMMO = 5

SPACE_IMAGE = pygame.image.load(os.path.join("Assets", "space.png"))
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)


RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


def draw_window(red, yellow, bullets, red_health, yellow_health):
	WIN.blit(SPACE, (0, 0))
	pygame.draw.rect(WIN, BLACK, BORDER)
	WIN.blit(RED_SPACESHIP, (red.x, red.y))
	WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
	for bullet in bullets:
		pygame.draw.rect(WIN, WHITE, bullet)
	red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
	yellow_health_text = HEALTH_FONT.render(
            "Health: " + str(yellow_health), 1, WHITE)
	WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() -
                            10, HEIGHT - red_health_text.get_height() - 10))
	WIN.blit(yellow_health_text, (10, HEIGHT -
                               yellow_health_text.get_height() - 10))
	pygame.display.update()


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
	for bullet in red_bullets:
		bullet.x -= BULLET_VEL
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(YELLOW_HIT))
			red_bullets.remove(bullet)
		elif bullet.x < 0:
			red_bullets.remove(bullet)

	for bullet in yellow_bullets:
		bullet.x += BULLET_VEL
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RED_HIT))
			yellow_bullets.remove(bullet)
		elif bullet.y > WIDTH:
			yellow_bullets.remove(bullet)


def draw_winner(text):
	text = WINNER_FONT.render(text, 1, WHITE)
	WIN.blit(text, (WIDTH // 2 - text.get_width() //
                 2, HEIGHT // 2 - text.get_height() // 2))
	pygame.display.update()
	pygame.time.delay(5000)


def handle_yellow_movement(keys, yellow):
	if keys[pygame.K_a] and (yellow.x - MOVE_SPEED > 0):  # left
		yellow.x -= MOVE_SPEED

	if keys[pygame.K_d] and (yellow.x + yellow.width + MOVE_SPEED < BORDER.x):  # right
		yellow.x += MOVE_SPEED

	if keys[pygame.K_w] and (yellow.y - MOVE_SPEED > 0):  # up
		yellow.y -= MOVE_SPEED

	if keys[pygame.K_s] and (yellow.y + MOVE_SPEED + yellow.height < HEIGHT):  # down
		yellow.y += MOVE_SPEED


def handle_red_movement(keys, red):
	if keys[pygame.K_LEFT] and (red.x - MOVE_SPEED > BORDER.x + BORDER.width):  # left
		red.x -= MOVE_SPEED

	if keys[pygame.K_RIGHT] and (red.x + red.width + MOVE_SPEED < WIDTH):  # right
		red.x += MOVE_SPEED

	if keys[pygame.K_UP] and (red.y - MOVE_SPEED > 0):  # up
		red.y -= MOVE_SPEED

	if keys[pygame.K_DOWN] and (red.y + MOVE_SPEED + red.height < HEIGHT):  # down
		red.y += MOVE_SPEED


def main():
	red = pygame.Rect(700, 200, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
	yellow = pygame.Rect(100, 200, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
	red_bullets = []
	yellow_bullets = []
	red_health = 10
	yellow_health = 10
	clock = pygame.time.Clock()
	running = True
	while running:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LCTRL and len(yellow_bullets) < AMMO:
					# make a yellow bullet
					yellow_bullets.append(pygame.Rect(
                                            yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5))
				if event.key == pygame.K_RCTRL and len(red_bullets) < AMMO:
					# make a red bullet
					red_bullets.append(pygame.Rect(red.x, red.y + red.width // 2 - 2, 10, 5))

			if event.type == RED_HIT:
				red_health -= 1
			if event.type == YELLOW_HIT:
				yellow_health -= 1

		keys_pressed = pygame.key.get_pressed()
		handle_yellow_movement(keys_pressed, yellow)
		handle_red_movement(keys_pressed, red)

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


if __name__ == "__main__":
	main()
