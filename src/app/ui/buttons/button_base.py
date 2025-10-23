from abc import ABC, abstractmethod
import pygame

class ButtonSection(ABC):
    def __init__(self, screen, recording_strategy):
        self.screen = screen
        self.font = pygame.font.Font(None, 18)
        self.buttons_rect = []
        self.recording_strategy = recording_strategy

    @abstractmethod
    def draw_buttons(self, num_buttons, button_section_rect):
        pass

    @abstractmethod
    def get_button_text(self, index):
        pass

    def handle_click(self, pos):
        for i, button in enumerate(self.buttons_rect):
            if button.collidepoint(pos):
                self.activate_button(i)
                return i
        return None
    
    def activate_button(self, button_index):
        action = self.get_action_for_button(button_index)
        
        if hasattr(self.recording_strategy, "is_recording") and self.recording_strategy.is_recording:
            self.recording_strategy.stop()
        else:
            self.recording_strategy.start(action)


    @abstractmethod
    def get_action_for_button(self, button_index):
        pass


    def draw_button_section(self, position, section_height=100):
        button_section_width = self.screen.get_width()  
        button_section_height = section_height  
        button_section_x, button_section_y = position

         #Creamos un frame/rectangulo para guardar el contenido #(x,y,width,height)
        button_section_rect = pygame.Rect(button_section_x, button_section_y, button_section_width, button_section_height)  
        

        self.draw_buttons(self.get_button_count(), button_section_rect)

    @abstractmethod
    def get_button_count(self):
        pass

    def get_key_name_for_button(self, button_index):
        for key, button_idx in self.key_bindings.items():
            if button_idx == button_index:
                return pygame.key.name(key)
        return ""