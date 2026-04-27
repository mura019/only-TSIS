import pygame
import random



#Game constants
LANES = [200, 300, 400] 
SPEED_BASE = 5

#Player class
class Player(pygame.sprite.Sprite):
    #Initialize player with image, position, speed, and power-up states
    def __init__(self, color_name):
        super().__init__()
        self.image = pygame.image.load(f"Racer/assets/images/Player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(300, 500))
        self.speed = 6
        self.shield_active = False
        self.nitro_active = False
        self.powerup_timer = 0
        self.crashes_allowed = 0

    #Update player position based on input and manage power-up timers
    def update(self):
        keys = pygame.key.get_pressed()
        current_speed = self.speed * 1.5 if self.nitro_active else self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 150:
            self.rect.x -= current_speed
        if keys[pygame.K_RIGHT] and self.rect.right < 450:
            self.rect.x += current_speed

        #Deactivate power-ups after their duration ends
        if (self.nitro_active or self.shield_active) and pygame.time.get_ticks() > self.powerup_timer:
            self.nitro_active = False
            self.shield_active = False



#Enemy, Obstacle, and PowerUp classes with movement logic
class Enemy(pygame.sprite.Sprite):
    def __init__(self, difficulty):
        #Initialize enemy with image, position, and speed based on difficulty
        super().__init__()
        self.image = pygame.image.load("Racer/assets/images/enemy.png").convert_alpha()
        self.rect = self.image.get_rect(center=(random.choice(LANES), -100))
        self.speed = SPEED_BASE + (2 if difficulty == "hard" else 0)

    def update(self):
        #Move enemy down the screen and remove it if it goes off-screen
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        #Initialize obstacle with image and position
        super().__init__()
        self.image = pygame.image.load("Racer/assets/images/obstacle.png").convert_alpha()
        self.rect = self.image.get_rect(center=(random.choice(LANES), -50))

    def update(self):
        #Move obstacle down the screen and remove it if it goes off-screen
        self.rect.y += SPEED_BASE
        if self.rect.top > 600:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        #Initialize power-up with random type, corresponding image, and position
        super().__init__()
        self.type = random.choice(["Nitro", "Shield", "Repair"])
        img_name = self.type.lower() + ".png"
        self.image = pygame.image.load(f"Racer/assets/images/{img_name}").convert_alpha()
        self.rect = self.image.get_rect(center=(random.choice(LANES), -50))

    def update(self):
        #Move power-up down the screen and remove it if it goes off-screen
        self.rect.y += SPEED_BASE
        if self.rect.top > 600:
            self.kill()