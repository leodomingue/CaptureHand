import pygame
import sys
from src.app.config import AppConfig
from src.app.layout.layout_factory import LayoutFactory

class GestureRecorderApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((AppConfig.SCREEN_WIDTH, AppConfig.SCREEN_HEIGHT))
        pygame.display.set_caption("Tomador de Datos de Gestos de la Mano")

        AppConfig.ensure_gesture_folders_exist()

        self.local_camera = None
        self.remote_camera = None
        self.active_cameras = []

        #Si alguien quiere, puede crear su layout, agregarlo al facotry ya estaria
        self.current_layout = LayoutFactory.create_layout("main", self)

    def activate_camera(self, camera_type):
        camera = None
        
        if camera_type == "local" and self.local_camera:
            camera = self.local_camera
        elif camera_type == "remote" and self.remote_camera:
            camera = self.remote_camera
        
        if camera and camera not in self.active_cameras:
            self.active_cameras.append(camera)
            print(f"Cámara {camera_type} activada")

    def change_layout(self, name):
        self.current_layout = LayoutFactory.create_layout(name, self)

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