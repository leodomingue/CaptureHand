import pygame
import sys
import time
import os
import cv2
from datetime import datetime
from src.camera.camera import Camera
from ..app.config import Colors, AppConfig

class GestureRecorderApp:
    def __init__(self):
        pygame.init()
        self.screen_width = AppConfig.SCREEN_WIDTH
        self.screen_height = AppConfig.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tomador de Datos de Gestos de La Mano")
        
        self.camera = Camera()
        self.camera.initialize_camera()
        
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 18)
        
        

        os.makedirs(AppConfig.DATA_FOLDER, exist_ok=True)

        for folder in AppConfig.GESTURE_FOLDERS:
            folder_path = os.path.join(AppConfig.DATA_FOLDER, folder)
            os.makedirs(folder_path, exist_ok=True)

        self.button_rects = []


    def handle_button_click(self, pos):
        for i, button_rect in enumerate(self.button_rects):
            if button_rect.collidepoint(pos):
                gesture_folder = AppConfig.GESTURE_FOLDERS[i]
                folder_path = os.path.join(AppConfig.DATA_FOLDER, gesture_folder)

                self.camera.start_recording(5, folder_path, gesture_folder)

        return False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.handle_button_click(event.pos):
                        print("pulsado")
            
        return True
                

    def draw_camera(self,position):
        if self.camera:
            frame = self.camera.get_preview_frame()
            if frame is not None:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Cambiamos a RGB

                #Pygame espera ancho y alto
                frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1)) #Cambiamos de lugar ancho y alto de la camra
                
                # Creamos superficie donde colocar la imagen
                frame_surface = pygame.transform.scale(frame_surface, (self.screen.get_width()//2, 400))
                self.screen.blit(frame_surface, position) #Y la pegamos



    def draw_buttons(self, num_buttons, button_section_rect):
        current_button_rects = []
        #Tamaño del contenedor
        button_section_width = button_section_rect.width
        button_section_height = button_section_rect.height
        button_section_x, button_section_y = button_section_rect.topleft
        
        #Tamaño de los botones y margen
        button_witdth = 120  
        button_height = 90
        button_margin = 50  
        #Tamaño que ocupan los botones botonoes + margen
        total_buttons_width = num_buttons * button_witdth + (num_buttons - 1) * button_margin 
        
        #Centramos para 1era posicion
        start_x = button_section_x + (button_section_width - total_buttons_width) // 2
        start_y = button_section_y + (button_section_height - button_height) // 2


        for i in range(num_buttons):
            button_rect = pygame.Rect(start_x + i * (button_witdth + button_margin), start_y, button_witdth, button_height)
            pygame.draw.rect(self.screen, AppConfig.BUTTON_COLORS[i], button_rect)

            current_button_rects.append(button_rect)

            button_text = self.font_small.render(f"{AppConfig.GESTURE_NAMES[i]}", True, (0, 0, 0))
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)

        self.button_rects = current_button_rects


    def draw_button_section(self, position):
        button_section_width = self.screen.get_width()  
        button_section_height = 150  
        button_section_x, button_section_y = position

        #Creamos un frame/rectangulo para guardar el contenido #(x,y,width,height)
        button_section_rect = pygame.Rect(button_section_x, button_section_y, button_section_width, button_section_height) 
        
        pygame.draw.rect(self.screen, Colors.BUTTON_SECTION, button_section_rect) 

        pygame.draw.rect(self.screen, Colors.BUTTON_SECTION_BORDER, button_section_rect, 2)
        
        self.draw_buttons(4, button_section_rect)

    def draw_title_section(self, position, title_text="Título"):
        title_section_width = self.screen.get_width()
        title_section_height = 50

        title_section_x, title_section_y = position

        title_section_rect = pygame.Rect(title_section_x, title_section_y, title_section_width, title_section_height) 

        pygame.draw.rect(self.screen, Colors.BUTTON_SECTION, title_section_rect)

        #creamos superficie del texto (es otro "rectangulo" dentro del anterior)
        text_surface = self.font_large.render(title_text, True, Colors.TEXT) #El true es de antiliasing

        #centramos
        text_rect = text_surface.get_rect(center=title_section_rect.center)

        #PEGAMOS
        self.screen.blit(text_surface, text_rect)

        return title_section_rect


    def draw_instructions_section(self, position):
        instructions_section_width = self.screen.get_width()//2
        instructions_section_height = 400

        instructions_section_x, instructions_section_y = position

        instructions_rect = pygame.Rect(instructions_section_x, instructions_section_y, instructions_section_width, instructions_section_height)

        pygame.draw.rect(self.screen, Colors.BUTTON_SECTION, instructions_rect)


        instructions = [
        "Toca un botón para capturar ese gesto",
        "Mantene la mano abierta hasta que te digan que realices el gesto",
        "Mantene el gesto hasta que te digan lo contrario",
        "Volvé a tener la mano abierta hasta que termine la grabación",
        "Repetir paso 1"
        ]

        header_text = "Instrucciones:"
        header_surface = self.font_medium.render(header_text, True, Colors.TEXT)
        header_rect = header_surface.get_rect(center=(instructions_rect.centerx, instructions_rect.top + 10))
        self.screen.blit(header_surface, header_rect)

        line_height = 60
        start_y = header_rect.bottom + 20

        for i, instruction in enumerate(instructions):
        
            numbered_text = f"{i+1}- {instruction}"
            instruction_surface = self.font_small.render(numbered_text, True, Colors.TEXT)
            
            instruction_rect = instruction_surface.get_rect(left=instructions_rect.left, top=start_y + (i * line_height))
            
            self.screen.blit(instruction_surface, instruction_rect)

        return instructions_rect



    def draw(self):
        #DEBEMOS SIEMPRE POR CADA TICK RELLENAR EL FONDO DE NEGRO PARA "LIMPIAR LA IAMGEN"
        #Pensa que por cada tick se "suponerpone" la imagen anterior para generar sensacion de movimiento en la app
        self.screen.fill(Colors.BACKGROUND)

        title_section_rect = self.draw_title_section((0,0), "Visualizacion solo manos")
        instructions_rect = self.draw_instructions_section((0, title_section_rect.height))
        self.draw_camera((instructions_rect.width,title_section_rect.height))

        self.draw_button_section((0,self.screen.get_height()-150))




    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_events()

            self.draw()

            pygame.display.flip()

            clock.tick(30) 
        
        pygame.quit()
        sys.exit()