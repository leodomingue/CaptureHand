import pygame
from src.app.config import Colors


class ActionSection:
    def __init__(self, screen, camera):
        self.screen = screen
        self.font = pygame.font.Font(None, 25)
        self.current_action_index = 0
        self.actions_sequence = []
        self.timer_start = 0
        self.is_active = False
        self.delays = [2.0, 2.0, 2.0]
        self.camera = camera

    def update(self):
        if not self.is_active:
            return
        
        recording_time = self.camera.get_recording_progress()
        
        if recording_time < self.delays[0]:
            self.current_action_index = 0
        elif recording_time < self.delays[0] + self.delays[1]:
            self.current_action_index = 1
        elif recording_time < self.delays[0] + self.delays[1] + self.delays[2]:
            self.current_action_index = 2
        else:
            self.is_active = False


    def start_action_sequence(self):
        self.current_action_index = 0
        self.timer_start = pygame.time.get_ticks()
        self.is_active = True
        self.actions_sequence = ["Mantene la mano abierta","Realiza el gesto","Mantene la mano abierta"]

    def draw_action_section(self, position):
        #Colocamos el tamaño
        action_section_width = self.screen.get_width()
        action_section_height = 50

        #Indicamos Posicion topLeft
        action_section_x, action_section_y = position

        #Creamos la superficie
        action_section_rect = pygame.Rect(action_section_x, action_section_y, action_section_width, action_section_height) 

        #Dibujamos/pegamos la superficie
        pygame.draw.rect(self.screen, (255,255,255), action_section_rect)


        if self.is_active and self.current_action_index < len(self.actions_sequence):
            current_action = self.actions_sequence[self.current_action_index]
            
            action_text_surface = self.font.render(current_action, True, (0,0,0))
            
            text_rect = action_text_surface.get_rect(center=action_section_rect.center)
            
            self.screen.blit(action_text_surface, text_rect)

        if not self.is_active:
            current_action = "-"
            
            action_text_surface = self.font.render(current_action, True, (0,0,0))
            
            text_rect = action_text_surface.get_rect(center=action_section_rect.center)
            
            self.screen.blit(action_text_surface, text_rect)