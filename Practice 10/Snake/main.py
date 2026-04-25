import pygame, sys
import random


pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

#Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)

#Resolution
w = 600
h = 400
SEG = 10

#Variables
SPEED = 10
SCORE = 0
LEVEL = 1

#Fonts
font = pygame.font.SysFont("Calibri", 60)
font_small = pygame.font.SysFont("Calibri", 20)
game_over_text = font.render("Game Over", True, BLACK)

#Display
display = pygame.display.set_mode((w, h))
pygame.display.set_caption("Snake")

#Load and scale the food image
food_img = pygame.image.load("Practice 10/Snake/images/Coin.png")
food_img = pygame.transform.scale(food_img, (SEG, SEG))



#Logic for spawning food
def spawn_food(snake):
    #Spawn food in random location that is not taken by the snake
    while True:
        fx = random.randint(0, (w // SEG) - 1) * SEG
        fy = random.randint(0, (h // SEG) - 1) * SEG
        if (fx, fy) not in snake:
            return fx, fy


#Starting position of the snake
snake = [(w//2, h//2), (w//2 - SEG, h//2), (w//2 - SEG*2, h//2)]
Direction = "RIGHT"

#First food spawn
food_x, food_y = spawn_food(snake)
food_rect = food_img.get_rect()
food_rect.topleft = (food_x, food_y)

#Game loop
while True:

    for event in pygame.event.get():
        #Check for quitting the game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            #Movement controls for the snake, and preventing the snake from 180 turn
            if (event.key == pygame.K_w or event.key == pygame.K_UP) and Direction != "DOWN":
                Direction = "UP"
            elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and Direction != "UP":
                Direction = "DOWN"
            elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and Direction != "RIGHT":
                Direction = "LEFT"
            elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and Direction != "LEFT":
                Direction = "RIGHT"


    #Calculate new head position based on the current direction
    head_x, head_y = snake[0]

    #Move the head in the current direction
    if Direction == "UP":
        head_y -= SEG
    elif Direction == "DOWN":
        head_y += SEG
    elif Direction == "LEFT":
        head_x -= SEG
    elif Direction == "RIGHT":
        head_x += SEG

    new_head = (head_x, head_y)

    #Check for collision with walls
    if head_x < 0 or head_x >= w or head_y < 0 or head_y >= h:
        display.fill(RED)
        display.blit(game_over_text, (w//2 - 150, h//2 - 50))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    #Check for collision with itself
    if new_head in snake:
        display.fill(RED)
        display.blit(game_over_text, (w//2 - 150, h//2 - 50))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    #Add the new head to the snake
    snake.insert(0, new_head)

    #Check if the snake has eaten the food
    if new_head == (food_x, food_y):
        SCORE += 1
        #Every 3 points, increase the level and speed of the snake
        if SCORE % 3 == 0:
            LEVEL += 1
            SPEED += 1
        food_x, food_y = spawn_food(snake)
        food_rect.topleft = (food_x, food_y)
    else:
        #Remove the tail segment if no food was eaten
        snake.pop()

    #Draw everything
    display.fill(BLACK)

    #Draw the snake segments
    for segment in snake:
        pygame.draw.rect(display, GREEN, [segment[0], segment[1], SEG, SEG])

    display.blit(food_img, food_rect)

    #Show the score and level on the screen
    score_text = font_small.render(f"Score: {SCORE}  Level: {LEVEL}", True, WHITE)
    display.blit(score_text, (10, 10))

    #Update the display and set the frame rate based on the current speed
    pygame.display.update()
    FramePerSec.tick(SPEED)