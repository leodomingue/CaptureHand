import pygame
import sys
from src.camera.camera import Camera
from src.app.config import AppConfig
from src.app.layout.layout_factory import LayoutFactory

class GestureRecorderApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((AppConfig.SCREEN_WIDTH, AppConfig.SCREEN_HEIGHT))
        pygame.display.set_caption("Tomador de Datos de Gestos de la Mano")

        AppConfig.ensure_gesture_folders_exist()

        self.camera = Camera()
        self.camera.initialize_camera()

        #Si alguien quiere, puede crear su layout, agregarlo al facotry ya estaria
        self.current_layout = LayoutFactory.create_layout("right_hand", self)

    def change_layout(self, name):
        self.current_layout.on_exit()
        self.current_layout = LayoutFactory.create_layout(name, self)
        self.current_layout.on_enter()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            events = pygame.event.get()
            running = self.current_layout.handle_events(events)
            self.current_layout.draw()
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()