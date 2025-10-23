import pygame
from src.app.config import Colors
from src.app.ui.title_section import TitleSection
from src.app.ui.instruction_section import InstructionSection
from src.app.ui.camera_section import CameraSection
from src.app.ui.buttons.button_section_for_hands import ButtonSectionForHands
from src.app.ui.action_section import ActionSection
from src.app.layout.base_layout import BaseLayout
from src.app.ui.back_button import BackButton
from src.utils.recorder.fixed_recording import FixedRecording

class RightHandLayout(BaseLayout):

    def __init__(self, app):
        super().__init__(app)
        self.screen = app.screen
        self.camera = app.camera

        self.background_image = pygame.image.load("src/app/ui/fondo.png").convert_alpha()

        self.background_image = pygame.transform.scale(self.background_image, 
                                                         (self.screen.get_width(), 
                                                          self.screen.get_height()))
        
        # Creamos cada seccion por separado
        self.back_button = BackButton(app, "main")
        self.title_section = TitleSection(self.screen)
        self.instructions_section = InstructionSection(self.screen)
        self.camera_section = CameraSection(self.screen, self.camera, 375, 175, 15, 15)
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

        self.action_section.update()

        self.back_button.draw((0,0))
        title_section_rect = self.title_section.draw_title_section((0,0), "Visualizacion solo mano derecha")
        instructions_rect = self.instructions_section.draw_instructions_section((0, title_section_rect.height))
        camera_one_rect = self.camera_section.draw_camera((instructions_rect.width,title_section_rect.height))
        camera_two_rect = self.camera_section.draw_camera((instructions_rect.width,camera_one_rect.bottom+10))
        self.action_section.draw_action_section((0,instructions_rect.height))
        self.button_section.draw_button_section((0,self.screen.get_height()-100))
