import pygame
import os
from src.app.config import AppConfig, Colors
from .button_base import ButtonSection


class ButtonSectionForJoystick(ButtonSection):
    def __init__(self, screen, recording_strategy):
        super().__init__(screen, recording_strategy)
        # Mapeo de índices a strings
        self.index_to_string = {
            0: '1', 1: '2', 2: '3', 3: '4', 
            4: '5', 5: '6', 6: '7', 7: '8'
        }
        self.key_bindings = {
            pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3,
            pygame.K_5: 4, pygame.K_6: 5, pygame.K_7: 6, pygame.K_8: 7,
            pygame.K_KP1: 0, pygame.K_KP2: 1, pygame.K_KP3: 2, pygame.K_KP4: 3,
            pygame.K_KP5: 4, pygame.K_KP6: 5, pygame.K_KP7: 6, pygame.K_KP8: 7
        }

    def get_button_count(self):
        return 4

    def get_button_text(self, index):
        texts = ["Boton A(XBOX)/X(PS)", "Boton B(XBOX)/O(PS)", "Boton X(XBOX)/■(PS)", "Boton Y(XBOX)/▲(PS)"]
        return texts[index]

    def get_action_for_button(self, button_index):
        return self.index_to_string[button_index]

    def draw_buttons(self, num_buttons, button_section_rect):
        self.buttons_rect = []
        button_width = 120
        button_height = 60
        margin = 10
        start_x = button_section_rect.x + margin
        start_y = button_section_rect.y + margin

        total_width = (num_buttons * button_width) + ((num_buttons - 1) * margin)

        start_x = button_section_rect.x + (button_section_rect.width - total_width) // 2
        start_y = button_section_rect.y + margin

        for i in range(num_buttons):
            button_x = start_x + i * (button_width + margin)
            button_rect = pygame.Rect(button_x, start_y, button_width, button_height)
            self.buttons_rect.append(button_rect)
            
            # Dibujar botón
            pygame.draw.rect(self.screen, (200, 200, 200), button_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)  # Borde
            
            # Dibujar texto
            text_surface = self.font.render(self.get_button_text(i), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)

    def handle_click(self, pos):
        index = super().handle_click(pos)
        if index is not None:
            return self.index_to_string[index]
        return None

    def get_key_name_for_button(self, button_index):
        for key, idx in self.key_bindings.items():
            if idx == button_index:
                return self.index_to_string[idx]  
        return ""
    
    

