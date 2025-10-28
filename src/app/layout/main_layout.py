import pygame
from src.app.layout.base_layout import BaseLayout
from src.camera import (LocalCamera, RemoteCamera)

class MainLayout(BaseLayout):
    def __init__(self, app):
        super().__init__(app)
        self.font = pygame.font.SysFont("Arial", 40)
        self.screen = app.screen

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        button_width = 300
        button_height = 70
        padding = 20

        total_height = (button_height * 6) + (padding * 5)
        start_y = (screen_height - total_height) // 2

        pos_x_center = (screen_width - button_width) // 2

        self.buttons = {
            "local_cam": pygame.Rect(pos_x_center, start_y, button_width, button_height),
            "remote_cam": pygame.Rect(pos_x_center, start_y + (button_height + padding), button_width, button_height),
            "right": pygame.Rect(pos_x_center, start_y + (button_height + padding) * 2, button_width, button_height),
            "left": pygame.Rect(pos_x_center, start_y + (button_height + padding) * 3, button_width, button_height),
            "joystick": pygame.Rect(pos_x_center, start_y + (button_height + padding) * 4, button_width, button_height),
            "exit": pygame.Rect(pos_x_center, start_y + (button_height + padding) * 5, button_width, button_height)
        }

        self.input_text = ""
        self.input_active = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.buttons["local_cam"].collidepoint(x, y):
                    self.init_local_camera()
                elif self.buttons["remote_cam"].collidepoint(x, y):
                    self.input_active = True

                elif self.buttons["right"].collidepoint(x, y):
                    self.app.change_layout("right_hand")
                elif self.buttons["left"].collidepoint(x, y):
                    self.app.change_layout("left_hand")
                elif self.buttons["joystick"].collidepoint(x, y):
                    self.app.change_layout("joystick")
                elif self.buttons["exit"].collidepoint(x, y):
                    return False
                
            elif event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_RETURN:
                    self.init_remote_camera(self.input_text.strip())
                    self.input_active = False
                    self.input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

        return True
    

    def init_local_camera(self):
        try:
            if self.app.local_camera is None:
                self.app.local_camera = LocalCamera()
                self.app.local_camera.initialize_camera()
                print("Cámara local inicializada correctamente")
            else:
                print("Cámara local ya estaba inicializada")
            
        except Exception as e:
            print(f"Error al inicializar la cámara local: {e}")

    def init_remote_camera(self, ip):
        try:
            url = f"http://{ip}:8080/video"
       
                
            self.app.remote_camera = RemoteCamera(url)
            self.app.remote_camera.initialize_camera()
            
            
            print(f"Cámara remota inicializada en {url}")
        except Exception as e:
            print(f"Error al conectar con cámara remota: {e}")


    

    def draw(self):
        self.app.screen.fill((0, 0, 0))
        self.draw_button(self.buttons["local_cam"], "Iniciar Cámara Local", (80, 200, 250))
        self.draw_button(self.buttons["remote_cam"], "Conectar Cámara Celular", (80, 250, 180))
        self.draw_button(self.buttons["right"], "Mano Derecha", (70, 130, 250))
        self.draw_button(self.buttons["left"], "Mano Izquierda", (70, 250, 130))
        self.draw_button(self.buttons["joystick"], "Joystick", (70, 250, 130))
        self.draw_button(self.buttons["exit"], "Salir", (250, 70, 70))

        if self.input_active:
            self.draw_input_box()

    def draw_button(self, rect, text, color):
        pygame.draw.rect(self.app.screen, color, rect)
        label = self.font.render(text, True, (255, 255, 255))

        text_rect = label.get_rect()
        text_rect.center = rect.center

        self.app.screen.blit(label, text_rect)


    def draw_input_box(self):
        box_width, box_height = 400, 60
        box_rect = pygame.Rect((self.screen.get_width() - box_width) // 2, (self.screen.get_height() - box_height) // 2,
            box_width,box_height)
        pygame.draw.rect(self.screen, (255, 255, 255), box_rect, border_radius=10)
        text_surface = self.font.render(self.input_text or "Ingresa tu IP + Enter", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=box_rect.center)
        self.screen.blit(text_surface, text_rect)
