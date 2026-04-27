import pygame
import sys
import datetime
from collections import deque
from tools import draw_line, flood_fill, save_canvas



#Init pyfame and font
pygame.init()
pygame.font.init()

#Constants
WIDTH, HEIGHT = 900, 600
UI_HEIGHT = 60
CANVAS_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT - UI_HEIGHT)
FPS = 60

#Default Colors
BLACK = (0, 0, 0)
UI_BG = (50, 50, 50)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
ACTIVE_BTN = (150, 150, 150)

#State variables
current_color = (0, 0, 255)
brush_sizes = {'small': 2, 'medium': 5, 'large': 10}
brush_size_keys = [2, 5, 10]
brush_index = 1 #start with medium brush
radius = brush_size_keys[brush_index]



mode = 'pencil'   #Pencil, line, rect, circle, square, eraser, rtriangle, etriangle, rhombus, fill, text
start_pos = None
points = []
drawings = []     #Saved shapes on canvas
preview = None    #Preview shapes
text_input = ""   #Current typing text
text_pos = None   #Where text is being typed
text_active = False    #Whether currently typing text


#UI buttons
buttons = [
    ("Pencil", 'pencil', 10),
    ("Line", 'line', 90),
    ("Rect", 'rect', 170),
    ("Circle", 'circle', 250),
    ("Square", 'square', 330),
    ("Eraser", 'eraser', 410),
    ("Fill", 'fill', 490),
    ("Text", 'text', 570),
    ("rTri", 'rtriangle', 650),
    ("eTri", 'etriangle', 730),
    ("Rhombus", 'rhombus', 810),
]


#Color palette
colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,165,0), BLACK, WHITE]


#Create main window and canvas surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")
canvas = pygame.Surface((CANVAS_RECT.width, CANVAS_RECT.height))
canvas.fill(WHITE)

#Set up clock and fonts
clock = pygame.time.Clock()
font_small = pygame.font.SysFont("Verdana", 14)
font_mid = pygame.font.SysFont("Verdana", 18)


#Draw UI
def draw_ui():
    #UI background
    pygame.draw.rect(screen, UI_BG, (0, HEIGHT - UI_HEIGHT, WIDTH, UI_HEIGHT))
    pygame.draw.rect(screen, UI_BG, (480, 0, WIDTH - 480, UI_HEIGHT - 10))


    #Mode buttons
    for label, key, bx in buttons:
        rect = pygame.Rect(bx, HEIGHT - 45, 70, 30)
        color_btn = ACTIVE_BTN if mode == key else GRAY
        pygame.draw.rect(screen, color_btn, rect)
        txt = font_small.render(label, True, BLACK)
        screen.blit(txt, (bx + 6, HEIGHT - 40))


    #Color buttons
    for i, col in enumerate(colors):
        rect = pygame.Rect(490 + i * 35, 5, 30, 30)
        pygame.draw.rect(screen, col, rect)
        if col == current_color:
            pygame.draw.rect(screen, BLACK, rect, 2)


    #Brush size buttons
    sizes = [("1", 2), ("2", 5), ("3", 10)]
    for i, (label, sz) in enumerate(sizes):
        bx = 10 + i * 30
        rect = pygame.Rect(bx, 5, 26, 26)
        pygame.draw.rect(screen, GRAY if radius != sz else ACTIVE_BTN, rect)
        txt = font_small.render(label, True, BLACK)
        screen.blit(txt, (bx + 8, 8))


    #Current mode and brush info
    info = font_mid.render(f"Mode: {mode}   Brush: {radius}px   Color: {current_color}", True, WHITE)
    screen.blit(info, (10, HEIGHT - UI_HEIGHT + 5))

    #Save hint
    hint = font_small.render("Ctrl+S to save canvas", True, WHITE)
    screen.blit(hint, (WIDTH - 180, HEIGHT - UI_HEIGHT + 8))


#Game loop
def main():
    global mode, start_pos, points, preview, current_color, radius, brush_index, text_input, text_pos, text_active
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()   #Current mouse position

        #Event: Quit, mouse clicks, motion, keyboard
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #Keyboard
            if event.type == pygame.KEYDOWN:
                # brush sizes 1/2/3
                if event.key == pygame.K_1:
                    radius = 2
                elif event.key == pygame.K_2:
                    radius = 5
                elif event.key == pygame.K_3:
                    radius = 10

                #Save with Ctrl+S
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    print("Saved:", save_canvas(canvas))

                #Text input handling
                if mode == 'text' and text_active:
                    #Commit text with Enter
                    if event.key == pygame.K_RETURN:
                        if text_input and text_pos:
                            txt_surf = font_mid.render(text_input, True, current_color)
                            canvas.blit(txt_surf, text_pos)
                        text_input = ""
                        text_pos = None
                        text_active = False

                    #Cancel text input with Escape
                    elif event.key == pygame.K_ESCAPE:
                        text_input = ""
                        text_pos = None
                        text_active = False

                    #Delete last character with backspace
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]

                    else:
                        #Only add printable characters to text input
                        if event.unicode:
                            text_input += event.unicode

            #Mouse down
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Left click
                if event.button == 1:
                    clicked_ui = False

                    #Check mode buttons
                    for label, key, bx in buttons:
                        btn_rect = pygame.Rect(bx, HEIGHT - 45, 70, 30)

                        #If click on button, change mode and cancel drawing
                        if btn_rect.collidepoint(event.pos):
                            mode = key
                            clicked_ui = True

                            #Cancel any preview/text
                            start_pos = None
                            preview = None
                            text_active = False
                            break


                    #Check color buttons
                    for i, col in enumerate(colors):
                        color_rect = pygame.Rect(490 + i * 35, 5, 30, 30)

                        if color_rect.collidepoint(event.pos):
                            current_color = col
                            clicked_ui = True
                            break

                    #Brush size buttons
                    for i, sz in enumerate([2,5,10]):
                        rect = pygame.Rect(10 + i * 30, 5, 26, 26)

                        if rect.collidepoint(event.pos):
                            radius = sz
                            clicked_ui = True
                            break

                    if clicked_ui:
                        continue  #Don't start drawing when clicking UI

                    #If click on canvas area
                    if CANVAS_RECT.collidepoint(event.pos):
                        start_pos = event.pos
                        points = [event.pos]
                        preview = None

                        if mode == 'fill':
                            #Flood fill at clicked position, convert to canvas coords
                            x, y = event.pos
                            flood_fill(canvas, (x, y), current_color)
                            start_pos = None

                        elif mode == 'text':
                            #Start text input
                            text_active = True
                            text_input = ""
                            text_pos = event.pos

                        elif mode == 'eraser':
                            #Start erasing
                            draw_line(canvas, WHITE, event.pos, event.pos, radius*2)

                elif event.button == 3:
                    #Right click decreases brush size
                    radius = max(1, radius - 1)

                elif event.button == 4:  #Wheel up
                    radius = min(100, radius + 1)
                elif event.button == 5:  #Wheel down
                    radius = max(1, radius - 1)


            #Mouse motion
            if event.type == pygame.MOUSEMOTION:
                #If left button is held and we have a start position
                if pygame.mouse.get_pressed()[0] and start_pos and CANVAS_RECT.collidepoint(mouse_pos):
                    #For pencil and eraser, we draw directly on canvas as we move
                    if mode == 'pencil':
                        last = points[-1]
                        cur = event.pos
                        draw_line(canvas, current_color, last, cur, radius)
                        points.append(cur)
                    elif mode == 'eraser':
                        last = points[-1] if points else event.pos
                        cur = event.pos
                        draw_line(canvas, WHITE, last, cur, radius*2)
                        points.append(cur)
                    else:
                        #For shapes, to preview the shape as we draw
                        preview = (start_pos, event.pos)


            #Mouse up
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and start_pos and CANVAS_RECT.collidepoint(event.pos):
                    end = event.pos

                    #Commit the shape to canvas
                    if mode == 'line':
                        draw_line(canvas, current_color, start_pos, end, radius)
                    elif mode == 'rect':
                        x = min(start_pos[0], end[0])
                        y = min(start_pos[1], end[1])
                        w = abs(end[0] - start_pos[0])
                        h = abs(end[1] - start_pos[1])
                        pygame.draw.rect(canvas, current_color, (x, y, w, h), max(1, radius//2))
                    elif mode == 'circle':
                        dx = end[0] - start_pos[0]
                        dy = end[1] - start_pos[1]
                        r = int((dx*dx + dy*dy) ** 0.5)
                        pygame.draw.circle(canvas, current_color, start_pos, r, max(1, radius//2))
                    elif mode == 'square':
                        x = min(start_pos[0], end[0])
                        y = min(start_pos[1], end[1])
                        side = min(abs(end[0] - start_pos[0]), abs(end[1] - start_pos[1]))
                        pygame.draw.rect(canvas, current_color, (x, y, side, side), max(1, radius//2))
                    elif mode == 'rtriangle':
                        tri = [start_pos, (start_pos[0], end[1]), end]
                        pygame.draw.polygon(canvas, current_color, tri, max(1, radius//2))
                    elif mode == 'etriangle':
                        tri = [start_pos, end, ((start_pos[0] + end[0]) // 2, start_pos[1] + int(abs(end[0] - start_pos[0]) * 0.866))]
                        pygame.draw.polygon(canvas, current_color, tri, max(1, radius//2))
                    elif mode == 'rhombus':
                        x = (start_pos[0] + end[0]) // 2
                        y = (start_pos[1] + end[1]) // 2
                        top = (x, start_pos[1])
                        right = (end[0], y)
                        bottom = (x, end[1])
                        left = (start_pos[0], y)
                        pygame.draw.polygon(canvas, current_color, [top, right, bottom, left], max(1, radius//2))
                    
                    #Reset
                    start_pos = None
                    preview = None
                    points = []

        #Draw everything
        screen.fill(GRAY)
        #Draw canvas
        screen.blit(canvas, (0, 0))

        #Review (draw, but not commit)
        if preview and CANVAS_RECT.collidepoint(pygame.mouse.get_pos()):
            s, e = preview

            #Draw the preview shape on top of canvas
            if mode == 'line':
                draw_line(screen, current_color, s, e, radius)
            elif mode == 'rect':
                x = min(s[0], e[0]); y = min(s[1], e[1])
                w = abs(e[0] - s[0]); h = abs(e[1] - s[1])
                pygame.draw.rect(screen, current_color, (x, y, w, h), max(1, radius//2))
            elif mode == 'circle':
                dx = e[0] - s[0]; dy = e[1] - s[1]
                r = int((dx*dx + dy*dy) ** 0.5)
                pygame.draw.circle(screen, current_color, s, r, max(1, radius//2))
            elif mode == 'square':
                x = min(s[0], e[0]); y = min(s[1], e[1])
                side = min(abs(e[0] - s[0]), abs(e[1] - s[1]))
                pygame.draw.rect(screen, current_color, (x, y, side, side), max(1, radius//2))
            elif mode == 'rtriangle':
                pygame.draw.polygon(screen, current_color, [s, (s[0], e[1]), e], max(1, radius//2))
            elif mode == 'etriangle':
                pygame.draw.polygon(screen, current_color, [s, e, ((s[0] + e[0]) // 2, s[1] + int(abs(e[0] - s[0]) * 0.866))], max(1, radius//2))
            elif mode == 'rhombus':
                x = (s[0] + e[0]) // 2; y = (s[1] + e[1]) // 2
                top = (x, s[1]); right = (e[0], y); bottom = (x, e[1]); left = (s[0], y)
                pygame.draw.polygon(screen, current_color, [top, right, bottom, left], max(1, radius//2))

        #Text typing preview (not committed)
        if text_active and text_pos:
            txt_surf = font_mid.render(text_input, True, current_color)
            screen.blit(txt_surf, text_pos)

        #UI overlay
        draw_ui()

        #Update display and FPS
        pygame.display.flip()
        clock.tick(FPS)

    #Quit
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
