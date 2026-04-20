import pygame

class Ball:
    def __init__(self, width, height):
        self.radius = 25
        self.x = width // 2
        self.y = height // 2

        self.screen_wigth = width
        self.screen_height = height

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if self.radius <= new_x <= self.screen_wigth - self.radius:
            self.x = new_x

        if self.radius <= new_y <= self.screen_height - self.radius:
            self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)

        