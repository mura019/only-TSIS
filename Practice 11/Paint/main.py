import pygame



def main():
    #Initialize Pygame and set up the screen and clock
    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    clock = pygame.time.Clock()

    radius = 15
    mode = 'draw'        #Current mode: draw; rect, circle, eraser
    points = []          #List of points for freehand drawing
    start_pos = None     #Starting position for shapes
    drawings = []        #List of all drawings

    current_color = (0, 0, 255)
    colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,165,0)]

    WHITE = (255, 255, 255)

    #Buttons for modes
    buttons = [
        ("Draw",   'draw',   10),
        ("Rect",   'rect',   100),
        ("Circle", 'circle', 190),
        ("Eraser", 'eraser', 280),
        ("Square", 'square', 370),
        ("rTriangle", 'rtriangle', 460),
        ("eTriangle", 'etriangle', 550),
        ("Rhombus", 'rhombus', 640)
    ]


    #Game loop
    while True:
        #Get the current position of the mouse
        mouse_pos = pygame.mouse.get_pos()


        #Check for events
        for event in pygame.event.get():
            #Check for QUIT event
            if event.type == pygame.QUIT:
                return

            #Check for mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    #Check if the click was on one of the mode buttons
                    for (label, btn_mode, bx) in buttons:
                        btn_rect = pygame.Rect(bx, 445, 80, 30)
                        #If the click was on a button, change the mode
                        if btn_rect.collidepoint(event.pos):
                            mode = btn_mode
                            break

                    #Check if the click was on one of the color buttons
                    for i, color in enumerate(colors):
                        color_rect = pygame.Rect(490 + i * 35, 0, 30, 30)
                        #If the click was on a color button, change the current color
                        if color_rect.collidepoint(event.pos):
                            current_color = color
                            break

                    #If the click was not on a button, start drawing
                    start_pos = event.pos
                    points = []

                #Check for right mouse button down to decrease the radius of the brush
                elif event.button == 3:
                    radius = max(1, radius - 1)

            #Check for mouse motion
            if event.type == pygame.MOUSEMOTION:
                if mode == 'draw':
                    #Add the current mouse position to the list of points and draw a line between the last two points
                    points = points + [event.pos]
                    if len(points) >= 2:
                        drawings.append(('line', current_color, points[-2], points[-1], radius))
                
                #If the mode is eraser, add an eraser circle at the current mouse position
                elif mode == 'eraser':
                    drawings.append(('eraser', (0,0,0), event.pos, radius * 2))

            #Check for mouse button up
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and start_pos:
                    #If the mode is rect, circle, square, triangle, or rhombus, add the final shape to the list of drawings
                    if mode == 'rect':
                        x = min(start_pos[0], event.pos[0])
                        y = min(start_pos[1], event.pos[1])
                        w = abs(event.pos[0] - start_pos[0])
                        h = abs(event.pos[1] - start_pos[1])
                        drawings.append(('rect', current_color, (x, y, w, h)))
                    elif mode == 'circle':
                        dx = event.pos[0] - start_pos[0]
                        dy = event.pos[1] - start_pos[1]
                        r = int((dx**2 + dy**2) ** 0.5)
                        drawings.append(('circle', current_color, start_pos, r))
                    elif mode == 'square':
                        x = min(start_pos[0], event.pos[0])
                        y = min(start_pos[1], event.pos[1])
                        w = h = min(abs(event.pos[0] - start_pos[0]), abs(event.pos[1] - start_pos[1]))
                        drawings.append(('square', current_color, (x, y, w, h)))
                    elif mode == 'etriangle':
                        drawings.append(('etriangle', current_color, [start_pos, event.pos, ((start_pos[0] + event.pos[0]) // 2, start_pos[1] + int(abs(event.pos[0] - start_pos[0]) * 0.866))]))
                    elif mode == 'rhombus':
                        x = (start_pos[0] + event.pos[0]) // 2
                        y = (start_pos[1] + event.pos[1]) // 2
                        top    = (x, start_pos[1]) 
                        right  = (event.pos[0], y) 
                        bottom = (x, event.pos[1])  
                        left   = (start_pos[0], y)
                        drawings.append(('rhombus', current_color, [top, right, bottom, left]))
                    elif mode == 'rtriangle':
                        drawings.append(('rtriangle', current_color, [start_pos, (start_pos[0], event.pos[1]), event.pos]))
                    start_pos = None
                    points = []

        #Draw the background
        screen.fill((0, 0, 0))

        #Draw all saved shapes in order
        for drawing in drawings:
            if drawing[0] == 'line':
                drawLineBetween(screen, 0, drawing[2], drawing[3], drawing[4], drawing[1])
            elif drawing[0] == 'rect':
                pygame.draw.rect(screen, drawing[1], drawing[2], 2)
            elif drawing[0] == 'square':
                pygame.draw.rect(screen, drawing[1], drawing[2], 2)
            elif drawing[0] == 'etriangle':
                pygame.draw.polygon(screen, drawing[1], drawing[2], 2)
            elif drawing[0] == 'circle':
                pygame.draw.circle(screen, drawing[1], drawing[2], drawing[3], 2)
            elif drawing[0] == 'eraser':
                pygame.draw.circle(screen, drawing[1], drawing[2], drawing[3])
            elif drawing[0] == 'rhombus':
                pygame.draw.polygon(screen, drawing[1], drawing[2], 2)
            elif drawing[0] == 'rtriangle':
                pygame.draw.polygon(screen, drawing[1], drawing[2], 2)


        #Draw the current shape being drawn
        if start_pos and mode == 'rect':
            x = min(start_pos[0], mouse_pos[0])
            y = min(start_pos[1], mouse_pos[1])
            w = abs(mouse_pos[0] - start_pos[0])
            h = abs(mouse_pos[1] - start_pos[1])
            pygame.draw.rect(screen, current_color, (x, y, w, h), 2)
        elif start_pos and mode == 'circle':
            dx = mouse_pos[0] - start_pos[0]
            dy = mouse_pos[1] - start_pos[1]
            r = int((dx**2 + dy**2) ** 0.5)
            pygame.draw.circle(screen, current_color, start_pos, r, 2)
        elif start_pos and mode == 'square':
            x = min(start_pos[0], mouse_pos[0])
            y = min(start_pos[1], mouse_pos[1])
            w = h = min(abs(mouse_pos[0] - start_pos[0]), abs(mouse_pos[1] - start_pos[1]))
            pygame.draw.rect(screen, current_color, (x, y, w, h), 2)
        elif start_pos and mode == 'etriangle':
            pygame.draw.polygon(screen, current_color, [start_pos, mouse_pos, ((start_pos[0] + mouse_pos[0]) // 2, start_pos[1] + int(abs(mouse_pos[0] - start_pos[0]) * 0.866))], 2)
        elif start_pos and mode == 'rhombus':
            x = (start_pos[0] + mouse_pos[0]) // 2
            y = (start_pos[1] + mouse_pos[1]) // 2
            top    = (x, start_pos[1]) 
            right  = (mouse_pos[0], y) 
            bottom = (x, mouse_pos[1])  
            left   = (start_pos[0], y)
            pygame.draw.polygon(screen, current_color, [top, right, bottom, left], 2)
        elif start_pos and mode == 'rtriangle':
            pygame.draw.polygon(screen, current_color, [start_pos, (start_pos[0], event.pos[1]), event.pos], 2)

        #Draw the User Interface (UI) elements
        pygame.draw.rect(screen, (50, 50, 50), (0, 440, 700, 60))
        pygame.draw.rect(screen, (50, 50, 50), (480, 0, 225, 50))

        #Buttons for modes
        for (label, btn_mode, bx) in buttons:
            color = (150, 150, 150) if mode == btn_mode else (100, 100, 100)
            pygame.draw.rect(screen, color, (bx, 445, 80, 30))
            txt = pygame.font.SysFont("Verdana", 12).render(label, True, (0,0,0))
            screen.blit(txt, (bx + 5, 452))

        #Buttons for colors
        for i, color in enumerate(colors):
            pygame.draw.rect(screen, color, (490 + i * 35, 0, 30, 30))
            if color == current_color:
                pygame.draw.rect(screen, (0, 0, 0), (490 + i * 35, 0, 30, 30), 2)


        #Update the display and set the frame rate
        pygame.display.flip()
        clock.tick(60)


def drawLineBetween(screen, index, start, end, width, current_color):
    #Draw a line between the start and end points
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    #If there are no iterations, return
    if iterations == 0:
        return

    #Draw a circle at each point along the line to create a thick line effect
    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, current_color, (x, y), width)


main()