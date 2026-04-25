import pygame, sys, time, random
from pygame.locals import *
import random
 
#Initalize  pygame
pygame.init()

#Frame per second controller
FPS = 60
FramePerSec = pygame.time.Clock()

#Basic colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Resolution of the window
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 700

#Create a white screen
DISPLAYSURF = pygame.display.set_mode((400,700))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 

#Setting up Sprites, Enemy
class Enemy(pygame.sprite.Sprite):
    #Insert the image of Enemy, and set its location
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Practice 10/Racer/images/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0) 

    #Logic for the movement of Enemy
    def move(self):
        global SPEED
        #Speed of the Enemy
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 700):
            self.rect.top = 0
            #Three strips where the Enemy can appear, and it will appear randomly in one of the three strips
            self.rect.center = random.choice([(70, 0), (200, 0), (330, 0)])
 

#Setting up Sprites, Player
class Player(pygame.sprite.Sprite):
    #Insert the image of Player, and set its location
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Practice 10/Racer/images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 600)
    
    #Logic for the movement of Player
    def move(self):
        global SPEED
        #Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                    #Move left if the left arrow key is pressed
                    self.rect.move_ip(-SPEED, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                    #Move right if the right arrow key is pressed
                    self.rect.move_ip(SPEED, 0)    


#Setting up Sprites, Coin
class Coin(pygame.sprite.Sprite):
    #Insert the image of Coin, and set its location
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Practice 10/Racer/images/Coin.png")
        self.rect = self.image.get_rect()
        self.rect.center= (160, 660) 
 
    #Logic for the movement of Coin
    def move(self):
        global SPEED
        self.rect.move_ip(0, SPEED)
        #Randomly appear in one of the three strips when it goes out of the screen
        if (self.rect.bottom > 700):
            self.rect.top = 0
            self.rect.center = random.choice([(70, 0), (200, 0), (330, 0)]) 
 

#Setting up Sprites, Enemy, Player and Coin
P1 = Player()
E1 = Enemy()
C1 = Coin()


#Event for increasing speed of Enemy and Coin
INC_SPEED = pygame.USEREVENT + 1

#Counter for the coins collected
SUM = 0
SPEED = 5
prev_coins_for_speed = 0


def game_loop():
    #Creating Sprites Groups
    enemies = pygame.sprite.Group()
    enemies.add(E1)
    coins = pygame.sprite.Group()
    coins.add(C1)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)
    all_sprites.add(C1)


    global INC_SPEED
    global SUM
    global SPEED
    global prev_coins_for_speed

    #Game Loop
    while True: 

        #
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                SPEED += 20
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    
    
        DISPLAYSURF.fill(WHITE)


        #Check if the Player has collected the Coin, and count it
        if pygame.sprite.spritecollideany(P1, coins):
            SUM += 1
            C1.rect.top = 0
            C1.rect.center = random.choice([(70, 0), (200, 0), (330, 0)])

            coins_for_speed = SUM // 5  #How many times the player has collected 5 coins

            if coins_for_speed > prev_coins_for_speed:
                SPEED += 1
                prev_coins_for_speed = coins_for_speed


            #update to show the new score after collecting the coin
            pygame.display.update()

        #If enemy intersects with the coin, then dont show the coin
        if pygame.sprite.spritecollideany(E1, coins):
            C1.rect.top = 0
            C1.rect.center = random.choice([(70, 0), (200, 0), (330, 0)])

        #Display the score of coins collected
        font = pygame.font.SysFont("Elephent", 32)
        text = font.render("Coins Collected: " + str(SUM), True, BLACK)
        tex2 = font.render("Speed: " + str(SPEED), True, BLACK)
        DISPLAYSURF.blit(tex2, (30, 70))
        DISPLAYSURF.blit(text, (30, 30))


        #Move each sprite
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()


        #Check if any of the enemies have collided with the Player
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
            
                
        #Update the display and set the frame rate
        pygame.display.update()
        FramePerSec.tick(FPS)



#Start the game loop
restart = True
while restart:
    restart = game_loop()