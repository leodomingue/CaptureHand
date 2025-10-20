import pygame

class BaseLayout:
    """Interfaz comun a todas las layouts"""

    def __init__(self, app):
        self.app = app  # referencia a GestureRecorderApp

    def handle_events(self, events):
        
        raise NotImplementedError

    def draw(self):
        
        raise NotImplementedError
