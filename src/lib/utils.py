import pygame
import math

class Ball():
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 100
        self.vector = pygame.math.Vector2.from_polar((self.speed, angle))
        self.radius = 10
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)
        self.rect.centerx = x
        self.rect.centery = y
    
    def update_pos(self, screen, dt):
        (speed, angle) = pygame.math.Vector2.as_polar(self.vector)
        self.x += dt * speed * math.cos(math.radians(angle))
        self.y += dt * speed * math.sin(math.radians(angle))
        self.rect.update(self.x, self.y, self.radius * 2, self.radius * 2)
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def check_collision(self, screen, paddles):
        (width, height) = screen.get_size()
        horizontal = pygame.math.Vector2((1, 0))
        vertical = pygame.math.Vector2((0, 1))

        if (self.x <= self.radius):
            return 1
        if (self.x >= width - self.radius):
            return 2
        if (self.y <= self.radius) or (self.y > height - self.radius):
            self.speed *= 1.05
            self.vector = self.vector.reflect(vertical)
            self.vector.scale_to_length(self.speed)
            return 0
        if (self.rect.collideobjects(paddles)):
            self.speed *= 1.05
            self.vector = self.vector.reflect(horizontal)
            self.vector.scale_to_length(self.speed)
            return 0
        return -1


    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.radius)

class Paddle():
    def __init__(self, screen):
        self.rect = pygame.Rect(0, 0, 10, 150)
        self.pos = screen.get_height() / 2
        self.rect.centery = self.pos

    def move_paddle(self, screen, dt, direction):
        (width, height) = screen.get_size()
        if (direction == "up") and (self.rect.top > 0):
            self.pos -= 300 * dt
        elif (direction == "down") and (self.rect.bottom < height):
            self.pos += 300 * dt
        self.rect.centery = self.pos