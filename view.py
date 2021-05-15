# this class functions as the camera, placed on the main plane
from gameObject import GameObj
import pygame


def image_scale(image, scale):
    if scale > 1:
        return pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
    else:
        return image


def rect_scale(rect, x, y, scale):
    x = x * scale
    y = y * scale
    width = rect.width * scale
    height = rect.height * scale
    return pygame.Rect(x, y, width, height)


# def draw_objects(backgrounds, objects, rectangles, view, scale):
    # for background in backgrounds:

    #WIN.blit(image_scale(SPACE, settings.SCALE), (0, 0))


class GameView(GameObj):
    # an extension of game object, adding a display to blit to and some scale params
    def __init__(self, shape, gamebounds, scale, max_scale):
        super().__init__(0, 0, shape, gamebounds)
        self.display = pygame.display.set_mode((
            shape.width * scale, shape.height * scale
        ))
        self.scale = scale
        self.max_scale = max_scale

    def get_display(self):
        return self.display

    def get_window_width(self):
        return self.get_width() * self.scale

    def get_window_height(self):
        return self.get_height() * self.scale

    # given a position, return the relative position of the object in relation to the camera
    def relativePosition(self, x, y):
        return x - self.get_x(), y - self.get_y()

    def increaseScale(self):
        self.scale = (self.scale % self.max_scale) + 1
        pygame.display.set_mode((
            self.get_width() * self.scale,
            self.get_height() * self.scale
        ))

    def display_rectangle(self, rectangle, colour):
        x, y = self.relativePosition(rectangle.x, rectangle.y)
        pygame.draw.rect(self.display, colour,
                         rect_scale(rectangle, x, y, self.scale))

    def display_object(self, object):
        x, y = self.relativePosition(object.get_x(), object.get_y())
        self.display.blit(
            image_scale(object.get_image(), self.scale),
            (x * self.scale, y * self.scale)
        )

    def display_background(self, image):
        x, y = self.relativePosition(0, 0)
        print(x, y)
        self.display.blit(
            image_scale(image, self.scale),
            (x * self.scale, y * self.scale)
        )
