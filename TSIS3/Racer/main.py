import pygame
import sys


from persistence import load_settings, load_leaderboard, save_score, save_settings
from ui import Button, TextInput
from racer import Player, Enemy, Obstacle, PowerUp


#init
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 600

#Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3: Racer")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

#Load settings
settings = load_settings()

#Load sounds
def load_sound(name):
    path = "assets/sounds/" + name

    try:
        return pygame.mixer.Sound(path)
    except (FileNotFoundError, pygame.error) as e:
        print(f"Warning: Could not load {name}. Error: {e}")
        return None


#Load music and sounds
snd_crash = load_sound('Racer/assets/sounds/crash.wav')
snd_powerup = load_sound('Racer/assets/sounds/powerup.wav')
music_loaded = False


#Attempt to load background music
try:
    pygame.mixer.music.load("Racer/assets/sounds/bg_music.mp3")
    music_loaded = True
except:
    print("Warning: bg_music.mp3 not found.")



#Game variables
state = "MENU"
player_name = "Player"
score = 0
distance = 0


#Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = None


#Reset game function
def reset_game():
    #Reset game state and variables
    global player, score, distance, all_sprites, enemies, obstacles, powerups
    all_sprites.empty()
    enemies.empty()
    obstacles.empty()
    powerups.empty()
    player = Player(settings["car_color"])
    all_sprites.add(player)
    score = 0
    distance = 0
    if music_loaded and settings["sound"]:
        pygame.mixer.music.play(-1)


#Draw HUD function
def draw_hud():
    #Draw score, distance, and powerup timers
    screen.blit(font.render(f"Score: {int(score)}", True, (255,255,255)), (10, 10))
    screen.blit(font.render(f"Dist: {int(distance)}m", True, (255,255,255)), (10, 40))

    time_left = (player.powerup_timer - pygame.time.get_ticks()) // 1000

    #Powerup timers
    if player and player.nitro_active:
        screen.blit(font.render(f"NITRO: {max(0, time_left)}s", True, (0, 255, 255)), (10, 80))
    if player and player.shield_active:
        screen.blit(font.render(f"SHIELD ACTIVE: {max(0, time_left)}s", True, (255, 215, 0)), (10, 80))


#UI Elements
btn_play = Button(200, 150, 200, 50, "Play")
btn_board = Button(200, 220, 200, 50, "Leaderboard")
btn_settings = Button(200, 290, 200, 50, "Settings")
btn_quit = Button(200, 360, 200, 50, "Quit")
btn_back = Button(200, 500, 200, 50, "Back")
btn_retry = Button(200, 350, 200, 50, "Retry")
btn_menu = Button(200, 420, 200, 50, "Main Menu")
name_input = TextInput(200, 250, 200, 40)


#Spawn timers
SPAWN_ENEMY = pygame.USEREVENT + 1
SPAWN_OBSTACLE = pygame.USEREVENT + 2
SPAWN_POWERUP = pygame.USEREVENT + 3
pygame.time.set_timer(SPAWN_ENEMY, 1500)
pygame.time.set_timer(SPAWN_OBSTACLE, 2500)
pygame.time.set_timer(SPAWN_POWERUP, 6000)


#Skip the menu
if state == "PLAY":
    reset_game()


running = True
#Game loop
while running:
    #Event handling
    screen.fill((50, 50, 50)) 
    pygame.draw.rect(screen, (20, 20, 20), (150, 0, 300, 600)) 
    
    #Draw lane markings
    for y in range(0, 600, 40):
        pygame.draw.rect(screen, (255, 255, 255), (245, (y + int(distance * 10)) % 600, 3, 20))
        pygame.draw.rect(screen, (255, 255, 255), (345, (y + int(distance * 10)) % 600, 3, 20))


    #Handle events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        

        #Menu buttons
        if state == "MENU":
            if btn_play.is_clicked(event): state = "NAME_INPUT"
            if btn_board.is_clicked(event): state = "LEADERBOARD"
            if btn_settings.is_clicked(event): state = "SETTINGS"
            if btn_quit.is_clicked(event): running = False
        
        #Name input handling
        elif state == "NAME_INPUT":
            name_input.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                player_name = name_input.text if name_input.text else "Player"
                reset_game()
                state = "PLAY"

        
        #Settings and leaderboard buttons
        elif state in ["LEADERBOARD", "SETTINGS"]:
            #Back button to return to menu
            if btn_back.is_clicked(event):
                state = "MENU"

            #Settings interaction: toggle sound, change car color, difficulty
            if state == "SETTINGS" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                #Button areas for settings options
                if 180 <= mx <= 500 and 180 <= my <= 210:
                    settings["sound"] = not settings.get("sound", True)
                    save_settings(settings)

                #Car color
                if 180 <= mx <= 500 and 230 <= my <= 260:
                    colors = ["blue", "green", "gray"]
                    cur = settings.get("car_color", "gray")
                    try:
                        idx = colors.index(cur)
                    except ValueError:
                        idx = 0
                    settings["car_color"] = colors[(idx + 1) % len(colors)]
                    save_settings(settings)

                #Difficulty
                if 180 <= mx <= 500 and 280 <= my <= 310:
                    diffs = ["easy", "normal", "hard"]
                    cur = settings.get("difficulty", "normal")
                    try:
                        idx = diffs.index(cur)
                    except ValueError:
                        idx = 1
                    settings["difficulty"] = diffs[(idx + 1) % len(diffs)]
                    save_settings(settings)


        #Gameplay events
        elif state == "PLAY":
            speed_boost = score // 500
            
            #Spawn enemies, obstacles, and powerups based on timers
            if event.type == SPAWN_ENEMY:
                e = Enemy(settings["difficulty"])
                e.speed += speed_boost
                if not pygame.sprite.spritecollideany(e, enemies) and not pygame.sprite.spritecollideany(e, obstacles):
                    all_sprites.add(e)
                    enemies.add(e)
            
            if event.type == SPAWN_OBSTACLE:
                o = Obstacle()
                if not pygame.sprite.spritecollideany(o, enemies) and not pygame.sprite.spritecollideany(o, obstacles):
                    all_sprites.add(o)
                    obstacles.add(o)
            
            if event.type == SPAWN_POWERUP:
                p = PowerUp()
                if not pygame.sprite.spritecollideany(p, enemies) and not pygame.sprite.spritecollideany(p, obstacles):
                    all_sprites.add(p)
                    powerups.add(p)

        #Back button for leaderboard and settings
        elif state in ["LEADERBOARD", "SETTINGS"]:
            if btn_back.is_clicked(event): state = "MENU"


        #Game over
        elif state == "GAMEOVER":
            if btn_retry.is_clicked(event):
                reset_game()
                state = "PLAY"
            if btn_menu.is_clicked(event): 
                state = "MENU"


    #Draw everything based on state
    if state == "MENU":
        btn_play.draw(screen)
        btn_board.draw(screen)
        btn_settings.draw(screen)
        btn_quit.draw(screen)
    #Name input
    elif state == "NAME_INPUT":
        screen.blit(font.render("Enter Name & Press Enter:", True, (255,255,255)), (150, 200))
        name_input.draw(screen)

    elif state == "SETTINGS":
        # фон
        screen.fill((30, 30, 30))
        # заголовок
        screen.blit(font.render("Settings", True, (255,255,255)), (240, 80))

        # Отображаем текущие настройки и кнопки переключения (простая реализация)
        # Sound
        sound_text = "On" if settings.get("sound", True) else "Off"
        screen.blit(font.render(f"Sound: {sound_text}", True, (255,255,255)), (180, 180))
        # Car color
        screen.blit(font.render(f"Car color: {settings.get('car_color','red')}", True, (255,255,255)), (180, 230))
        # Difficulty
        screen.blit(font.render(f"Difficulty: {settings.get('difficulty','normal')}", True, (255,255,255)), (180, 280))

        # Traffic density (если хотите)
        td = settings.get("traffic_density", None)
        if td is not None:
            screen.blit(font.render(f"Traffic density: {td}", True, (255,255,255)), (180, 330))

        # Рисуем кнопку Back (у вас уже есть btn_back)
        btn_back.draw(screen)

    #Gameplay
    elif state == "PLAY":
        all_sprites.update()
        speed_boost = score // 500
        distance += (0.1 + (speed_boost * 0.05)) * (1.5 if player.nitro_active else 1)
        score += 0.1 if not player.nitro_active else 0.5
        
        #Collision for enemies and obstacles with player
        if not player.shield_active:
            if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(player, obstacles):
                if settings["sound"] and snd_crash: snd_crash.play()
                if player.crashes_allowed > 0:
                    player.crashes_allowed -= 1
                    player.shield_active = True
                    player.powerup_timer = pygame.time.get_ticks() + 2000
                else:
                    pygame.mixer.music.stop()
                    save_score(player_name, int(score), int(distance))
                    state = "GAMEOVER"
        
        #Powerup collection
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if settings["sound"] and snd_powerup: snd_powerup.play()
            #Apply powerup effects
            if hit.type == "Nitro":
                player.nitro_active, player.shield_active = True, False
                player.powerup_timer = pygame.time.get_ticks() + 4000
            elif hit.type == "Shield":
                player.shield_active, player.nitro_active = True, False
                player.powerup_timer = pygame.time.get_ticks() + 4000
            elif hit.type == "Repair": 
                player.crashes_allowed = 1
        

        #Draw everything
        all_sprites.draw(screen)
        draw_hud()


    #Leaderboard screen
    elif state == "LEADERBOARD":
        screen.fill((30, 30, 30))
        board = load_leaderboard()
        for i, entry in enumerate(board):
            txt = f"{i+1}. {entry['name']} - {entry['score']} pts"
            screen.blit(font.render(txt, True, (255,255,255)), (150, 50 + i*35))
        btn_back.draw(screen)

    #Game over screen
    elif state == "GAMEOVER":
        screen.fill((0, 0, 0))
        screen.blit(font.render(f"GAME OVER! Score: {int(score)}", True, (255, 0, 0)), (180, 200))
        btn_retry.draw(screen)
        btn_menu.draw(screen)


    #Update display and tick clock
    pygame.display.flip()
    clock.tick(60)


#Exit cleanly
pygame.quit()
sys.exit()