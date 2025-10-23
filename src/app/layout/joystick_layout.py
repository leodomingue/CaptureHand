import pygame
from src.app.config import Colors
from src.app.ui.title_section import TitleSection
from src.app.ui.instruction_section import InstructionSection
from src.app.ui.camera_section import CameraSection
from src.app.ui.buttons.button_section_for_joystick import ButtonSectionForJoystick
from src.app.ui.action_section import ActionSection
from src.app.layout.base_layout import BaseLayout
from src.app.ui.back_button import BackButton
from src.utils.event_recorder import EventRecorder
from src.utils.recorder.indefinite_recording import IndefiniteRecording


class JoystickLayout(BaseLayout):

    def __init__(self, app):
        super().__init__(app)
        
        self.screen = app.screen
        self.camera = app.camera
        self.recorder = None

        self.background_image = pygame.image.load("src/app/ui/fondo.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, 
                                                         (self.screen.get_width(), 
                                                          self.screen.get_height()))
        
        self.current_state = None
        self.is_recording_mode = False
        self.active_button = None
        self.is_recording_clips = False
        
        self.key_mapping = {
            pygame.K_1: '1', pygame.K_2: '2', pygame.K_3: '3', pygame.K_4: '4',
            pygame.K_5: '5', pygame.K_6: '6', pygame.K_7: '7', pygame.K_8: '8',
            pygame.K_9: '9', pygame.K_0: '0',
            pygame.K_KP1: '1', pygame.K_KP2: '2', pygame.K_KP3: '3', pygame.K_KP4: '4',
            pygame.K_KP5: '5', pygame.K_KP6: '6', pygame.K_KP7: '7', pygame.K_KP8: '8',
            pygame.K_KP9: '9', pygame.K_KP0: '0'
        }
        
        # Creamos cada seccion por separado
        self.back_button = BackButton(app, "main")
        self.title_section = TitleSection(self.screen)
        self.instructions_section = InstructionSection(self.screen)
        self.camera_section = CameraSection(self.screen, self.camera, 375, 175, 15, 15)
        self.action_section = ActionSection(self.screen, self.camera)
        self.button_section = ButtonSectionForJoystick(self.screen, recording_strategy=IndefiniteRecording(self.camera))

    def handle_events(self, events):
        #Manejamos cada evento de esta ventana
        
        def process_single_event(event):
            #Procesa cada evento por separado
            if event.type == pygame.QUIT:
                return False
            
            #Si se realiza un click en la pantalla
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.handle_click(event.pos):
                    return True
                handle_mouse_click(event)
            #Si se toca un tecla
            elif event.type == pygame.KEYDOWN:
                handle_key_press(event)
            #Si se deja de presionar una tecla
            elif event.type == pygame.KEYUP:
                handle_key_release(event)
            
            return True

        def handle_mouse_click(event):
            if event.button == 1:
                button_name = self.button_section.handle_click(event.pos)
                if not button_name:
                    return
            
            button_name = self.button_section.handle_click(event.pos)
            if not button_name:
                return
            #Si se toca un boton de la pantalla comenzamos a grabar con el EventRecorder
            start_new_recorder(button_name)

        def start_new_recorder(button_name):
            #inicializamo un eventRecorder y que empiece a grabar indefinidamente
            if self.recorder:
                print(f"Terminando recorder anterior para botón {self.active_button}")
                self._cleanup_recording()
                    
            # Inicializamos nuevo EventRecorder
            print(f"Inicializando EventRecorder para botón {button_name}")
            self.recorder = EventRecorder(pre_buffer_seconds=4, fps=int(self.camera.real_fps))
            self.active_button = button_name
            self.is_recording_clips = False
            self.button_section.recording_strategy.recorder = self.recorder
            print(f"EventRecorder listo. Presiona la tecla '{button_name}' para empezar a grabar clips")

        def switch_to_released_clip(key_name):
            #Cambiamos estado de presioando a soltado
            #Terminamos el clip actual
            self.button_section.recording_strategy.stop()
            
            #inciamos nuevo clip
            self.button_section.recording_strategy.start(f"{key_name}_soltado")


        def handle_key_press(event):
            #Si se toca una tecla, obtenemos su matching de la key bindeada y vemos como la manejamos
            key_name = self._get_key_name(event.key)
            print(f"Tecla presionada: '{key_name}', Botón activo: '{self.active_button}'")
            
            if not self.recorder:
                return
            
            if key_name == self.active_button:
                start_pressed_clip(key_name)
            else:
                self._cleanup_recording()

        def start_pressed_clip(key_name):
            #Empezamos a tomar clips con nuestra estrategia
            # Terminamos el clip anterior
            if self.is_recording_clips:
                self.button_section.recording_strategy.stop()
            
            # Iniciamos nuevo clip
            self.button_section.recording_strategy.start(f"{key_name}_presionado")
            self.is_recording_clips = True

        def handle_key_release(event):
            #Si se deja de presionar la tecla
            key_name = self._get_key_name(event.key)

            if not (self.recorder and (key_name == self.active_button) and self.is_recording_clips):
                return
            
            switch_to_released_clip(key_name)


        def switch_to_released_clip(key_name):
            #Cambia de clip presionado a soltado
            # terminamos el clip anterior
            self.button_section.recording_strategy.stop()
            
            #Empezamos a grabar clips con el nuevo estado
            self.button_section.recording_strategy.start(f"{key_name}_soltado")


        for event in events:
            if not process_single_event(event):
                return False
        return True


    def _get_key_name(self, event_key):
        #buscamos la tecla de pygame y la pasamos a string desde neustro diccionario
        for key, index in self.button_section.key_bindings.items():
            if key == event_key:
                return self.button_section.index_to_string[index]

        #Si no esta, devolvemos lo que diga pygame
        return pygame.key.name(event_key)

    def _cleanup_recording(self):
        #Limpiamos la grabacion
        if self.button_section.recording_strategy:
            self.button_section.recording_strategy.stop()
        
        if self.recorder:
            self.recorder.end_state()
            self.recorder = None
        
        self.active_button = None
        self.is_recording_clips = False
        print("EventRecorder terminado completamente")

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.action_section.update()

        self.back_button.draw((0,0))
        title_section_rect = self.title_section.draw_title_section((0,0), "Visualizacion Joystick")
        instructions_rect = self.instructions_section.draw_instructions_section((0, title_section_rect.height))
        camera_one_rect = self.camera_section.draw_camera((instructions_rect.width,title_section_rect.height))
        camera_two_rect = self.camera_section.draw_camera((instructions_rect.width,camera_one_rect.bottom+10))
        self.action_section.draw_action_section((0,instructions_rect.height))
        self.button_section.draw_button_section((0,self.screen.get_height()-100))

        # Obtenemos el frame de la camra de la pantalla
        frame = self.camera.get_preview_frame()
        
        #Agregamos los frames a la grabadora (todos los frames) y lo colocamos en el buffer
        if frame is not None and self.recorder is not None:
            self.recorder.add_frame(frame)
            
            # y decidimso si se sigue grabando o tenemos que parar (nos fijamos el tiempo)
            if self.is_recording_clips and self.button_section.recording_strategy is not None:
                self.button_section.recording_strategy.update()


        if self.recorder:
            status_text = f"EventRecorder activo - Botón: {self.active_button} - Grabando clips: {self.is_recording_clips}"
            font = pygame.font.Font(None, 30)
            text_surface = font.render(status_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (120, self.screen.get_height() - 130))