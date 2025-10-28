import pygame
import cv2

class CameraSection:
    def __init__(self, screen, camera, width, height, margin_x, margin_y):
        self.screen = screen
        self.camera = camera
        self.width = width
        self.height = height
        self.margin_x = margin_x
        self.margin_y = margin_y


    def draw_camera(self, position):
        camera_rect = pygame.Rect(position[0] + self.margin_x, position[1] + self.margin_y, self.width, self.height)

        if self.camera is not None:
            frame = self.camera.get_preview_frame()
            if frame is not None:
                try:
                    # Si el frame viene en formato BGR, convertirlo
                    if len(frame.shape) == 3 and frame.shape[2] == 3:
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    else:
                        frame_rgb = frame

                    frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
                    frame_surface = pygame.transform.scale(frame_surface, (self.width, self.height))

                    final_position = (position[0] + self.margin_x, position[1] + self.margin_y)
                    self.screen.blit(frame_surface, final_position)
                except Exception as e:
                    print(f"Error mostrando cámara: {e}")
        else:
            # Dibujar fondo negro o gris para indicar que no hay cámara
            pygame.draw.rect(self.screen, (50, 50, 50), camera_rect)
            font = pygame.font.Font(None, 24)
            text_surface = font.render("Sin cámara", True, (200, 200, 200))
            text_rect = text_surface.get_rect(center=camera_rect.center)
            self.screen.blit(text_surface, text_rect)

        return camera_rect
        