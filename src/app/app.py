import pygame
import sys
from src.camera.camera import Camera
from src.app.config import AppConfig
from src.app.layout.main_layout import MainLayout

class GestureRecorderApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((AppConfig.SCREEN_WIDTH, AppConfig.SCREEN_HEIGHT))
        pygame.display.set_caption("Tomador de Datos de Gestos de la Mano")

        AppConfig.ensure_gesture_folders_exist()

        self.camera = Camera()
        self.camera.initialize_camera()
        self.layout = MainLayout(self.screen, self.camera)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        self.layout.draw()
        pygame.display.flip()

        while running:
            running = self.layout.handle_events()
            self.layout.draw()
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        sys.exit()