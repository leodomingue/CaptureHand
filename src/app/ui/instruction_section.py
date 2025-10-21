import pygame
from src.app.config import Colors

class InstructionSection:
    def __init__(self, screen):
        self.screen = screen
        self.font_header = pygame.font.Font(None, 36)
        self.font_text = pygame.font.Font(None, 18)

    def draw_instructions_section(self, position):
        instructions_section_width = self.screen.get_width()//2
        instructions_section_height = 450

        instructions_section_x, instructions_section_y = position

        instructions_rect = pygame.Rect(instructions_section_x, instructions_section_y, instructions_section_width, instructions_section_height)


        instructions = [
        "Toca un botón para capturar ese gesto",
        "Mantene la mano abierta hasta que te digan que realices el gesto",
        "Mantene el gesto hasta que te digan lo contrario",
        "Volvé a tener la mano abierta hasta que termine la grabación",
        "Repetir paso 1"
        ]

        header_text = "Instrucciones:"
        header_surface = self.font_header.render(header_text, True, Colors.TEXT)
        header_rect = header_surface.get_rect(center=(instructions_rect.centerx, instructions_rect.top + 10))
        self.screen.blit(header_surface, header_rect)

        line_height = 60
        start_y = header_rect.bottom + 20

        for i, instruction in enumerate(instructions):
        
            numbered_text = f"{i+1}- {instruction}"
            instruction_surface = self.font_text.render(numbered_text, True, Colors.TEXT)
            
            instruction_rect = instruction_surface.get_rect(left=instructions_rect.left, top=start_y + (i * line_height))
            
            self.screen.blit(instruction_surface, instruction_rect)

        return instructions_rect