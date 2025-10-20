import pygame
from src.app.config import Colors

class TitleSection:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)

    def draw_title_section(self, position, title_text="Título"):
        #Colocamos el tamaño
        title_section_width = self.screen.get_width()
        title_section_height = 50

        #Indicamos Posicion topLeft
        title_section_x, title_section_y = position

        #Creamos la superficie
        title_section_rect = pygame.Rect(title_section_x, title_section_y, title_section_width, title_section_height) 

        #Dibujamos/pegamos la superficie
        pygame.draw.rect(self.screen, Colors.BUTTON_SECTION, title_section_rect)

        #creamos superficie del texto (es otro "rectangulo" dentro del anterior)
        text_surface = self.font.render(title_text, True, Colors.TEXT) #El true es de antiliasing

        #centramos
        text_rect = text_surface.get_rect(center=title_section_rect.center)

        #PEGAMOS
        self.screen.blit(text_surface, text_rect)

        return title_section_rect