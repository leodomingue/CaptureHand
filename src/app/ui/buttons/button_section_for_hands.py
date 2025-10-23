import pygame
import os
from src.app.config import AppConfig, Colors
from .button_base import ButtonSection


class ButtonSectionForHands(ButtonSection): 
    def __init__(self, screen, recording_strategy):
        super().__init__(screen, recording_strategy)

    def draw_buttons(self, num_buttons, button_section_rect):
        current_button_rects = []

        #Tamaño del contenedor
        button_section_width = button_section_rect.width
        button_section_height = button_section_rect.height
        button_section_x, button_section_y = button_section_rect.topleft
        
        #Tamaño de los botones y margen
        button_witdth = 120  
        button_height = 60
        button_margin = 50  
        
        #Tamaño que ocupan los botones botonoes + margen
        total_buttons_width = num_buttons * button_witdth + (num_buttons - 1) * button_margin 
        
        #Centramos para 1era posicion
        start_x = button_section_x + (button_section_width - total_buttons_width) // 2
        start_y = button_section_y + (button_section_height - button_height) // 2


        for i in range(num_buttons):
            button_rect = pygame.Rect(start_x + i * (button_witdth + button_margin), start_y, button_witdth, button_height)
            pygame.draw.rect(self.screen, AppConfig.BUTTON_COLORS[i], button_rect)

            current_button_rects.append(button_rect)

            button_text = self.font.render(f"{AppConfig.GESTURE_NAMES[i]}", True, (0, 0, 0))
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)

        self.buttons_rect = current_button_rects

    def get_button_count(self):
        return len(AppConfig.GESTURE_FOLDERS)
    
    def get_action_for_button(self, button_index):
        return AppConfig.GESTURE_FOLDERS[button_index]

    def get_button_text(self, index):
        key_name = self.get_key_name_for_button(index)
        return f"{AppConfig.GESTURE_NAMES[index]} ({key_name})"

