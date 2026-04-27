import pygame



#UI elements like buttons and text input fields
class Button:
    #Initialize button with position, size, text, and colors
    def __init__(self, x, y, w, h, text, color=(222, 200, 200), hover_color=(120, 120, 120)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font(None, 36)

    #Draw the button with hover effect and centered text
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, (0,0,0), self.rect, 2)
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    #Check if the button is clicked based on mouse events
    def is_clicked(self, event):
        #Check for left mouse button click within the button's area
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #If the click is within the button's rectangle, return True
            if self.rect.collidepoint(event.pos):
                return True
        return False

#Text input field for player name entry
class TextInput:
    #Initialize text input with position, size, and font
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.font = pygame.font.Font(None, 36)


    #Handle keyboard events to update the text input field
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isprintable() and len(self.text) < 15:
                self.text += event.unicode


    #Draw the text input box with current text
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))