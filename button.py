import pygame

class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = (200, 200, 200)
        self.text_color = (0, 0, 0)

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text_surface = font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.x + 5, self.y + 5))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False