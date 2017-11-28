import pygame
from pong.constants import *
from pygame.math import Vector2


class GameEntity(pygame.sprite.Sprite):
    world = None
    HEIGHT = 16
    WIDTH = 16

    def __init__(self, location=None):
        if self.world is None:
            super().__init__()
        else:
            super().__init__(GameEntity.world)    # Place this in the world automatically
        self.location = Vector2(location) if location is not None else Vector2()

    def update(self, seconds_passed):
        pass

    def get_rect(self):
        x, y = self.location
        return pygame.Rect(int(x), int(y), self.WIDTH, self.HEIGHT)

    def get_collision(self):
        """Gets the GameEntity object that this has collided with"""
        if self.world is None:
            return None

        for entity in self.world.sprites():
            if self is entity:
                continue
            if self.get_rect().colliderect(entity.get_rect()):
                return entity
        return None


class Ball(GameEntity):
    HEIGHT = 16
    WIDTH = 16
    SIZE = (WIDTH, HEIGHT)
    COLOR = WHITE
    SPEED = 200
    # WORLD = None

    # container = None

    def __init__(self, location=None):
        super().__init__(location=location)
        # GameEntity.__init__(self)
        # pygame.sprite.Sprite.__init__(self, self.world)
        self.image = pygame.Surface(self.SIZE)
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect()
        self.speed = self.SPEED
        self.heading = Vector2()

    def update(self, seconds_passed):
        self.location += seconds_passed * self.speed * self.heading

        if self.location.y < 0:
            self.location.y = 0
            self.heading = self.heading.reflect(Vector2(0, 1))

        elif self.location.y + self.HEIGHT > FIELD_HEIGHT:
            self.location.y = FIELD_HEIGHT - self.HEIGHT
            self.heading = self.heading.reflect(Vector2(0, 1))

        collision = self.get_collision()
        if collision is not None:
            if self.location.x < collision.location.x:
                # Ball is left of paddle when they collided...
                self.location.x = collision.location.x - self.WIDTH
            else:
                # Ball is right of paddle when they collided...
                self.location.x = collision.location.x + collision.WIDTH
            self.heading.reflect_ip(Vector2(1, 0))  # Flip horizontal movement
        # ball_rect = self.get_rect()

    def alive(self):
        if self.world is None:
            return False
        if not self.get_rect().colliderect(pygame.Rect(0, 0, self.world.WIDTH, self.world.HEIGHT)):
            return False
        return True

    def reset(self):
        if self.world is None:
            return
        # Put the ball in the middle of the field.
        # self.location = Vector2((self.world.WIDTH - self.WIDTH) / 2, (self.world.HEIGHT - self.HEIGHT) / 2)
        self.location = self.default_location()
        self.speed = self.SPEED

    def default_location(self):
        if self.world is None:
            return Vector2()
        return Vector2((self.world.WIDTH - self.WIDTH) / 2, (self.world.HEIGHT - self.HEIGHT) / 2)


class Paddle(GameEntity):
    WIDTH = 16
    HEIGHT = WIDTH * 5
    SIZE = (WIDTH, HEIGHT)
    COLOR = WHITE
    SPEED = 200

    def __init__(self, location=None):
        super().__init__(location=location)
        self.image = pygame.Surface(self.SIZE)
        self.image.fill(self.COLOR)
        self.speed = self.SPEED
        self.heading = Vector2()

    def update(self, seconds_passed):
        self.move(seconds_passed)

    def move(self, seconds_passed):
        self.location += self.speed * self.heading * seconds_passed

        if self.world is None:
            return

        # Clamp it's Y location in the field.
        if self.location.y + self.HEIGHT > self.world.HEIGHT:
            self.location.y = self.world.HEIGHT - self.HEIGHT
            self.heading = Vector2()

        elif self.location.y < 0:
            self.location.y = 0
            self.heading = Vector2()


class World(pygame.sprite.Group):
    WIDTH = FIELD_WIDTH
    HEIGHT = FIELD_HEIGHT
    COLOR = BLACK
    X = 0
    Y = 0

    def __init__(self):
        pygame.sprite.Group.__init__(self)