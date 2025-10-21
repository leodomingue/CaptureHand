import pygame
from src.app.layout.base_layout import BaseLayout

class MainLayout(BaseLayout):
    def __init__(self, app):
        super().__init__(app)
        self.font = pygame.font.SysFont("Arial", 40)
        self.screen = app.screen

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        button_width = 250
        button_height = 80
        padding = 30

        total_height = (button_height * 3) + (padding * 2)
        start_y = (screen_height - total_height) // 2

        pos_x_center = (screen_width - button_width) // 2

        self.buttons = {
        "right": pygame.Rect(pos_x_center, start_y, button_width, button_height),
        "left": pygame.Rect(pos_x_center, start_y + button_height + padding, button_width, button_height),
        "exit": pygame.Rect(pos_x_center, start_y + (button_height + padding) * 2, button_width, button_height)
        }

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.buttons["right"].collidepoint(x, y):
                    self.app.change_layout("right_hand")
                elif self.buttons["left"].collidepoint(x, y):
                    self.app.change_layout("left_hand")
                elif self.buttons["exit"].collidepoint(x, y):
                    return False
        return True

    def draw(self):
        self.app.screen.fill((0, 0, 0))
        self.draw_button(self.buttons["right"], "Mano Derecha", (70, 130, 250))
        self.draw_button(self.buttons["left"], "Mano Izquierda", (70, 250, 130))
        self.draw_button(self.buttons["exit"], "Salir", (250, 70, 70))

    def draw_button(self, rect, text, color):
        pygame.draw.rect(self.app.screen, color, rect)
        label = self.font.render(text, True, (255, 255, 255))

        text_rect = label.get_rect()
        text_rect.center = rect.center

        self.app.screen.blit(label, text_rect)
