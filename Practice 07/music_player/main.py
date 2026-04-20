import pygame
import sys
from player import MusicPlayer

pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music Player")

font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()

player = MusicPlayer()

TICK_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TICK_EVENT, 1000)
current_track = player.get_current_track()
current_pos = player.get_position()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.prev()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

        if event.type == TICK_EVENT:
            current_track = player.get_current_track()
            current_pos = player.get_position()

        screen.fill((30, 30, 30))

        track_text = font.render(
            f"Track: {player.get_current_track()}", 
            True,
            (255, 255, 255)
        )

        screen.blit(track_text, (50, 100))

        time_text = font.render(
            f"Time: {player.get_position()} sec",
            True,
            (200, 200, 200)
        )

        screen.blit(time_text, (50, 150))

        controls = [
            "P - Play",
            "S - Stop",
            "N - Next",
            "B - Back",
            "Q - Quit"
        ]

        for i, text in enumerate(controls):
            ctrl_text = font.render(text, True, (150, 150, 150))
            screen.blit(ctrl_text, (50, 220 + i * 30))

        pygame.display.flip()
        clock.tick(30)