import pygame
import sys
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()

ball = Ball(WIDTH, HEIGHT)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        ball.move(-20, 0)
    if keys[pygame.K_RIGHT]:
        ball.move(20, 0)
    if keys[pygame.K_UP]:
        ball.move(0, -20)
    if keys[pygame.K_DOWN]:
        ball.move(0, 20)

    screen.fill((255, 255, 255))  # белый фон
    ball.draw(screen)

    pygame.display.flip()
    clock.tick(30)