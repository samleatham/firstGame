import pygame


def bound(i, minimum, maximum):
    if i < minimum:
        return minimum
    elif i > maximum:
        return maximum
    else:
        return i


class GameObj:

    def __init__(self, image, image_angle, shape, boundaries):
        self.image = image
        self.image_angle = image_angle
        self.shape = shape
        self.boundaries = boundaries

    def get_x(self):
        return self.shape.x

    def get_y(self):
        return self.shape.y

    def get_width(self):
        return self.shape.width

    def get_height(self):
        return self.shape.height

    def checkcollision(self, other):
        return self.shape.colliderect(other)

    def get_image(self):
        if self.image:
            return pygame.transform.scale(pygame.transform.rotate(
                self.image, self.image_angle), (self.get_width(), self.get_height()))
        else:
            return 0

    def move(self, x, y):
        self.shape.x = bound(x, self.boundaries.x,
                             self.boundaries.x + self.boundaries.width - self.get_width())
        self.shape.y = bound(y, self.boundaries.y,
                             self.boundaries.y + self.boundaries.height - self.get_height())
