import pygame, sys, time
from pygame.locals import *
import random
 
pygame.init()
 
FPS = 60
FramePerSec = pygame.time.Clock()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 700

 
DISPLAYSURF = pygame.display.set_mode((400,700))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Racer/images/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0) 
 
      def move(self):
        self.rect.move_ip(0,6)
        if (self.rect.bottom > 700):
            self.rect.top = 0
            self.rect.center = random.choice([(70, 0), (200, 0), (330, 0)])
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Racer/images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 600)
 
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-7, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(7, 0)    

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Racer/images/Coin.png")
        self.rect = self.image.get_rect()
        self.rect.center= (160, 660) 
 
    def move(self):
        self.rect.move_ip(0,6)
        if (self.rect.bottom > 700):
            self.rect.top = 0
            self.rect.center = random.choice([(70, 0), (200, 0), (330, 0)]) 
 

P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)


def game_loop():
    enemies = pygame.sprite.Group()
    enemies.add(E1)
    coins = pygame.sprite.Group()
    coins.add(C1)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)
    all_sprites.add(C1)
    SUM = 0
    while True:
        SPEED = 5 
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                SPEED += 2
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    
    
        DISPLAYSURF.fill(WHITE)

        if pygame.sprite.spritecollideany(P1, coins):
            SUM += 1
            C1.rect.top = 0
            C1.rect.center = random.choice([(70, 0), (200, 0), (330, 0)])

        if pygame.sprite.spritecollideany(E1, coins):
            SUM += 1
            C1.rect.top = 0
            C1.rect.center = random.choice([(70, 0), (200, 0), (330, 0)])

        font = pygame.font.SysFont("Elephent", 32)
        text = font.render("Coins Collected: " + str(SUM), True, BLACK)
        DISPLAYSURF.blit(text, (50, 50))
        pygame.display.update()
    
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()
    
        if pygame.sprite.spritecollideany(P1, enemies):
            waiting = True
            while waiting:
                font = pygame.font.SysFont("Elephent", 58)
                font2 = pygame.font.SysFont("Calibri", 32)

                text = font.render("GAME OVER", True, WHITE)
                text1 = font2.render("Coins Collected: " + str(SUM), True, (211, 211, 211))
                text2 = font2.render("Press R to Restart", True, (211, 211, 211))
                text3 = font2.render("Press Q to Quit", True, (211, 211, 211))

                DISPLAYSURF.fill(RED)
                DISPLAYSURF.blit(text, (75, 150))
                DISPLAYSURF.blit(text1, (75, 220))
                DISPLAYSURF.blit(text2, (75, 300))
                DISPLAYSURF.blit(text3, (75, 330))

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            for entity in all_sprites:
                                entity.kill()
                            waiting = False
                            game_loop()
                        elif event.key == pygame.K_q:
                            for entity in all_sprites:
                                entity.kill()
                            return False
            
                


        pygame.display.update()
        FramePerSec.tick(FPS)




restart = True
while restart:
    restart = game_loop()


