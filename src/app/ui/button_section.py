import pygame
import os
from src.app.config import AppConfig, Colors

class ButtonSection: 
    def __init__(self, screen, camera, action_section):
        self.screen = screen
        self.camera = camera
        self.font = pygame.font.Font(None, 18)
        self.buttons_rect = []
        self.action_section = action_section #Referenciamos al otro section

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


    def draw_button_section(self, position):
        button_section_width = self.screen.get_width()  
        button_section_height = 100  
        button_section_x, button_section_y = position

        #Creamos un frame/rectangulo para guardar el contenido #(x,y,width,height)
        button_section_rect = pygame.Rect(button_section_x, button_section_y, button_section_width, button_section_height)  
        
        self.draw_buttons(len(AppConfig.GESTURE_FOLDERS), button_section_rect)

    def handle_click(self, pos):
        print("Botones activos:", len(self.buttons_rect))
        for i,button in enumerate(self.buttons_rect):
            if button.collidepoint(pos):
                self.action_section.start_action_sequence()

                folder_path = os.path.join(AppConfig.DATA_FOLDER, AppConfig.GESTURE_FOLDERS[i])
                self.camera.start_recording(6, folder_path, AppConfig.GESTURE_FOLDERS[i])
                return True
        return False