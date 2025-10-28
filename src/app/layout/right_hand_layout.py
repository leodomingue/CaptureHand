import pygame
from src.app.ui import (TitleSection, InstructionSection, CameraSection, ActionSection, BackButton)
from src.app.ui.buttons.button_section_for_hands import ButtonSectionForHands
from src.app.layout.base_layout import BaseLayout
from src.utils.recorder.fixed_recording import FixedRecording

class RightHandLayout(BaseLayout):

    def __init__(self, app):
        super().__init__(app)
        self.screen = app.screen
        self.camera = app.local_camera

        self.background_image = pygame.image.load("src/app/ui/fondo.png").convert_alpha()

        self.background_image = pygame.transform.scale(self.background_image, 
                                                         (self.screen.get_width(), 
                                                          self.screen.get_height()))
        
        # Creamos cada seccion por separado
        self.back_button = BackButton(app, "main")
        self.title_section = TitleSection(self.screen)
        self.instructions_section = InstructionSection(self.screen)
        self.camera_section = CameraSection(self.screen, self.camera, 400, 400, 0, 0)
        self.action_section = ActionSection(self.screen, self.camera)
        self.button_section = ButtonSectionForHands(self.screen, FixedRecording(camera=self.camera, action_section=self.action_section))


    def handle_events(self,events): 
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if self.back_button.handle_click(event.pos):
                    continue

                self.button_section.handle_click(event.pos)
        return True
    
    def draw(self):
        #DEBEMOS SIEMPRE POR CADA TICK RELLENAR EL FONDO DE NEGRO PARA "LIMPIAR LA IAMGEN"
        #Pensa que por cada tick se "suponerpone" la imagen anterior para generar sensacion de movimiento en la app
        self.screen.blit(self.background_image, (0, 0))

        if self.camera is None:
            self.draw_no_camera_message()
            self.back_button.draw((0, 0))
            pygame.display.flip()
            return

        self.action_section.update()

        self.back_button.draw((0,0))
        title_section_rect = self.title_section.draw_title_section((0,0), "Visualizacion solo mano derecha")
        instructions_rect = self.instructions_section.draw_instructions_section((0, title_section_rect.height))
        camera_one_rect = self.camera_section.draw_camera((instructions_rect.width,title_section_rect.height))
        self.action_section.draw_action_section((0,instructions_rect.height))
        self.button_section.draw_button_section((0,self.screen.get_height()-100))


    def draw_no_camera_message(self):
        font = pygame.font.SysFont("Arial", 28)
        msg = "No hay cámara Local inicializada. Volvé al menú principal."
        text_surface = font.render(msg, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(text_surface, text_rect)
