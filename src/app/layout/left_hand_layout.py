import pygame
from src.app.config import Colors
from src.app.ui.title_section import TitleSection
from src.app.ui.instruction_section import InstructionSection
from src.app.ui.camera_section import CameraSection
from src.app.ui.button_section import ButtonSection
from src.app.ui.action_section import ActionSection
from src.app.layout.base_layout import BaseLayout


class LeftHandLayout(BaseLayout):

    def __init__(self, app):
        super().__init__(app)
        self.screen = app.screen
        self.camera = app.camera
        
        # Creamos cada seccion por separado
        self.title_section = TitleSection(self.screen)
        self.instructions_section = InstructionSection(self.screen)
        self.camera_section = CameraSection(self.screen, self.camera)
        self.action_section = ActionSection(self.screen, self.camera)
        self.button_section = ButtonSection(self.screen, self.camera, self.action_section)


    def handle_events(self,events): 
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.button_section.handle_click(event.pos)
        return True
    
    def draw(self):
        #DEBEMOS SIEMPRE POR CADA TICK RELLENAR EL FONDO DE NEGRO PARA "LIMPIAR LA IAMGEN"
        #Pensa que por cada tick se "suponerpone" la imagen anterior para generar sensacion de movimiento en la app
        self.screen.fill(Colors.BACKGROUND)

        self.action_section.update()

        title_section_rect = self.title_section.draw_title_section((0,0), "Visualizacion solo mano izquierda")
        instructions_rect = self.instructions_section.draw_instructions_section((0, title_section_rect.height))
        self.camera_section.draw_camera((instructions_rect.width,title_section_rect.height))
        self.action_section.draw_action_section((0,instructions_rect.height))
        self.button_section.draw_button_section((0,self.screen.get_height()-150))