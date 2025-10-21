import pygame

class BackButton:
    def __init__(self, app, previous_layout_name):
        self.previous_layout_name = previous_layout_name
        self.app = app
        self.size = 40

        self.image = pygame.image.load("src/app/ui/back_button.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
    
    def draw(self,pos):
        self.rect = pygame.Rect(pos[0], pos[1], self.size, self.size)
        self.app.screen.blit(self.image, self.rect)

    
    def handle_click(self, pos):
        if self.rect and self.rect.collidepoint(pos):
            self.app.change_layout(self.previous_layout_name)
            return True
        return False