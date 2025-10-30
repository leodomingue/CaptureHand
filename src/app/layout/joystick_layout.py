import pygame
import time
from src.app.ui import (BackButton, TitleSection, InstructionSection, CameraSection, ActionSection)
from src.app.layout.base_layout import BaseLayout
from src.app.ui.buttons import ButtonSectionForJoystick
from src.utils import EventRecorder
from src.utils.recorder import IndefiniteRecording


class JoystickLayout(BaseLayout):

    def __init__(self, app):
        super().__init__(app)
        
        self.screen = app.screen
        self.local_camera = app.local_camera
        self.remote_camera = app.remote_camera
        self.local_recorder = None
        self.remote_recorder = None

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

        self.joystick_mapping = {
            0: 'A',      # Botón A (Xbox) / X (PS)
            1: 'B',      # Botón B (Xbox) / Círculo (PS)
            2: 'X',      # Botón X (Xbox) / Cuadrado (PS)
            3: 'Y',      # Botón Y (Xbox) / Triángulo (PS)
            4: 'LB',     # Botón izquierdo superior
            5: 'RB',     # Botón derecho superior
            6: 'Back',   # Botón back/select
            7: 'Start',  # Botón start
            8: 'LS',     # Click stick izquierdo
            9: 'RS',     # Click stick derecho
        }

        self.joystick_to_ui_equivalence = {
            'A': '1',
            'B': '2',
            'X': '3',
            'Y': '4',
            'LB': '5',
            'RB': '6',
            'Back': '7',
            'Start': '8'
        }

        self.ui_to_joystick_equivalence = {v: k for k, v in self.joystick_to_ui_equivalence.items()}


        self.joystick = None
        self.init_joystick()

        
        # Creamos cada seccion por separado
        self.back_button = BackButton(app, "main")
        self.title_section = TitleSection(self.screen)
        self.instructions_section = InstructionSection(self.screen)
        self.local_camera_section = CameraSection(self.screen, self.local_camera, 375, 175, 15, 15)
        self.remote_camera_section = CameraSection(self.screen, self.remote_camera, 375, 175, 15, 15)
        self.local_action_section = ActionSection(self.screen, self.local_camera)
        self.remote_action_section = ActionSection(self.screen, self.remote_camera)

        recorders = []
        if self.local_camera:
            self.local_recorder = EventRecorder(
                pre_buffer_seconds=4,
                fps=int(self.local_camera.real_fps),
                camera_type="local"
            )
            recorders.append(self.local_recorder)

        if self.remote_camera:
            self.remote_recorder = EventRecorder(
                pre_buffer_seconds=4,
                fps=int(self.remote_camera.real_fps),
                camera_type="remote"
            )
            recorders.append(self.remote_recorder)

        self.button_section = ButtonSectionForJoystick(
            self.screen, 
            recording_strategy=IndefiniteRecording(recorders)
        )
        

        self.is_recording = None
        self.current_clip_type = None
        self.message = '-'
        self.last_clip_end_time = None


    def init_joystick(self):
        pygame.joystick.init()
        if pygame.joystick.get_count()> 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        else:
            print("No se encontró ningún joystick")
            self.joystick = None

    

    def handle_events(self, events):
        #Manejamos cada evento de esta ventana
        
        def process_single_event(event):
            #Procesa cada evento por separado
            if event.type == pygame.QUIT:
                return False
            
            #Eventos con JOystick
            if event.type == pygame.JOYBUTTONDOWN:
                handle_joystick_button_press(event)
            elif event.type == pygame.JOYBUTTONUP:
                handle_joystick_button_release(event)
            
            #Eventos con mouse y teclado
            #Si se realiza un click en la pantalla
            elif event.type == pygame.MOUSEBUTTONDOWN:
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
        

        def handle_joystick_button_press(event):
            if event.button in self.joystick_mapping:
                button_name = self.joystick_mapping[event.button]
                ui_equiv = self.joystick_to_ui_equivalence.get(button_name, button_name)


                if not (self.local_recorder or self.remote_recorder):
                    print("No hay EventRecorder activo — primero hacé clic en un botón en pantalla.")
                    return
                
                if ui_equiv == self.active_button:
                    start_pressed_clip(button_name)
                else:
                    print(f"Botón '{button_name}' != activo '{self.active_button}' → cancelando grabación.")
                    self._cleanup_recording()

        def handle_joystick_button_release(event):
            if event.button in self.joystick_mapping:
                button_name = self.joystick_mapping[event.button]
                ui_equiv = self.joystick_to_ui_equivalence.get(button_name, button_name)

              

                if (self.active_button and ui_equiv == self.active_button and self.is_recording_clips):
                    switch_to_released_clip(button_name)


        def handle_mouse_click(event):
            if event.button == 1:
                button_name = self.button_section.handle_click(event.pos)
                if button_name:
                    #Si se toca un boton de la pantalla comenzamos a grabar con el EventRecorder
                    start_new_recorder(button_name)

        def start_new_recorder(button_name):
            # Limpiamos recorders anteriores si existen
            if self.local_recorder:
                print(f"Terminando recorder local anterior para botón {self.active_button}")
                self.local_recorder.end_state()
                self.local_recorder = None
            if self.remote_recorder:
                print(f"Terminando recorder remota anterior para botón {self.active_button}")
                self.remote_recorder.end_state()
                self.remote_recorder = None

            self.active_button = button_name
            self.is_recording_clips = False

            # Inicializamos nuevos EventRecorder diferenciando local y remota
            recorders = []
            if self.local_camera:
                self.local_recorder = EventRecorder(
                    pre_buffer_seconds=4,
                    fps=int(self.local_camera.real_fps),
                    camera_type="local"
                )
                recorders.append(self.local_recorder)
            if self.remote_camera:
                self.remote_recorder = EventRecorder(
                    pre_buffer_seconds=4,
                    fps=int(self.remote_camera.real_fps),
                    camera_type="remote"
                )
                recorders.append(self.remote_recorder)
            

            self.button_section.recording_strategy = IndefiniteRecording(recorders)


            print(f"EventRecorder inicializado para botón '{button_name}'.")
            if self.local_recorder:
                print("Recorder local listo.")
            if self.remote_recorder:
                print("Recorder remota listo.")
            joystick_name = self.ui_to_joystick_equivalence.get(button_name, button_name)
            print(f"Presiona la tecla '{joystick_name}' para empezar a grabar clips")
            

        def switch_to_released_clip(key_name):
            #Cambiamos estado de presioando a soltado
            #Terminamos el clip actual
            self.button_section.recording_strategy.stop()
            
            #inciamos nuevo clip
            self.button_section.recording_strategy.start(f"{key_name}_soltado")
            self.current_clip_type = "soltado"


        def handle_key_press(event):
            #Si se toca una tecla, obtenemos su matching de la key bindeada y vemos como la manejamos
            key_name = self._get_key_name(event.key)
            print(f"Tecla presionada: '{key_name}', Botón activo: '{self.active_button}'")
            
            if not (self.local_recorder or self.remote_recorder):
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
            self.current_clip_type = "presionado"


        def handle_key_release(event):
            #Si se deja de presionar la tecla
            key_name = self._get_key_name(event.key)

            if not ((self.local_recorder or self.remote_recorder) and (key_name == self.active_button) and self.is_recording_clips):
                return
            
            switch_to_released_clip(key_name)



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
        
        if self.local_recorder:
            self.local_recorder.end_state()
            self.local_recorder = None
        if self.remote_recorder:
            self.remote_recorder.end_state()
            self.remote_recorder = None
        
        self.active_button = None
        self.is_recording_clips = False
        print("EventRecorder terminado completamente")

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))

        if self.local_camera is None and self.remote_camera is None:
            self.draw_no_camera_message()
            self.back_button.draw((0, 0))
            pygame.display.flip()
            return
        
        if self.local_camera:
            self.local_action_section.update()
        if self.remote_camera:
            self.remote_action_section.update()

        self.back_button.draw((0,0))
        title_section_rect = self.title_section.draw_title_section((0,0), "Visualizacion Joystick")
        instructions_rect = self.instructions_section.draw_instructions_section((0, title_section_rect.height))
        camera_one_rect = self.local_camera_section.draw_camera((instructions_rect.width,title_section_rect.height))
        camera_two_rect = self.remote_camera_section.draw_camera((instructions_rect.width,camera_one_rect.bottom+10))
        self.button_section.draw_button_section((0,self.screen.get_height()-100))

        # Obtenemos el frame de la camra de la pantalla
        if self.local_camera and self.local_recorder:
            frame_local = self.local_camera.get_preview_frame()
            if frame_local is not None:
                self.local_recorder.add_frame(frame_local)

        if self.remote_camera and self.remote_recorder:
            frame_remote = self.remote_camera.get_preview_frame()
            if frame_remote is not None:
                self.remote_recorder.add_frame(frame_remote)

        if self.is_recording_clips:
            if self.button_section.recording_strategy:
                still_recording = self.button_section.recording_strategy.update()
                self.is_recording = still_recording
            
            # y decidimso si se sigue grabando o tenemos que parar (nos fijamos el tiempo)


            if self.is_recording:
                if self.current_clip_type == "presionado":
                    self.message = f"Grabando clip: mantiene presionada la tecla {self.active_button}"
                elif self.current_clip_type == "soltado":
                    self.message = f"Grabando clip: soltando la tecla {self.active_button}"

                # Reinicimiaos temporizador
                self.last_clip_end_time = None


            #--------------Refactorizar------------
            #Si el clip terminó
            else:
                current_time = time.time()

                # Si el clip acaba de terminar, guardamos el momento de fin
                if self.last_clip_end_time is None:
                    self.last_clip_end_time = current_time

                elapsed_since_end = current_time - self.last_clip_end_time

                # Si aún no pasó 1 segundo desde el final, mantenemos el mensaje anterior
                if elapsed_since_end < 1.0:
                    if self.current_clip_type == "presionado":
                        self.message = f"Grabando clip: mantené presionada la tecla {self.active_button}"
                    elif self.current_clip_type == "soltado":
                        self.message = f"Grabando clip: tocá pero no presiones la tecla {self.active_button}"
                else:
                    # Luego del 1 segundo, mostramos el mensaje de siguiente acción
                    if self.current_clip_type == "presionado":
                        self.message = f"Finalizado el clip de presión {self.active_button}. Soltá la tecla."
                    elif self.current_clip_type == "soltado":
                        self.message = f"Finalizado el clip de soltar {self.active_button}. Toca la tecla {self.active_button}."
                    else:
                        self.message = "-"
        else:
            self.message = "-"

                   


        if self.local_recorder or self.remote_recorder:
            status_text = self.message
            font = pygame.font.Font(None, 30)
            text_surface = font.render(status_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (120, self.screen.get_height() - 130))



    def draw_no_camera_message(self):
        font = pygame.font.SysFont("Arial", 28)
        msg = "No hay cámara Local y/o remota inicializada. Volvé al menú principal."
        text_surface = font.render(msg, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(text_surface, text_rect)
