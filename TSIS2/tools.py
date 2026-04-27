import pygame
import datetime
from collections import deque


#Draw line between two points
def draw_line(surf, color, start, end, width):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    if iterations == 0:
        pygame.draw.circle(surf, color, start, width)
        return
    
    for i in range(iterations + 1):
        progress = i / iterations if iterations else 0
        x = int(start[0] * (1 - progress) + end[0] * progress)
        y = int(start[1] * (1 - progress) + end[1] * progress)
        pygame.draw.circle(surf, color, (x, y), width)


#Flood fill algorithm using queue (BFS)
def flood_fill(surface, start_pos, new_color):
    w, h = surface.get_size()
    x0, y0 = start_pos

    if not (0 <= x0 < w and 0 <= y0 < h):
        return
    target = surface.get_at((x0, y0))
    new_col = pygame.Color(*new_color)

    if target == new_col:
        return
    q = deque()
    q.append((x0, y0))

    while q:
        x, y = q.popleft()

        try:
            if surface.get_at((x, y)) != target:
                continue
        except IndexError:
            continue

        surface.set_at((x, y), new_col)


        if x > 0:
            q.append((x-1, y))
        if x < w-1:
            q.append((x+1, y))
        if y > 0:
            q.append((x, y-1))
        if y < h-1:
            q.append((x, y+1))



#Save canvas with timestamp
def save_canvas(surface):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"paint_{ts}.png"
    pygame.image.save(surface, filename)
    return filename