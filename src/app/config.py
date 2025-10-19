import os
class Colors:
    BACKGROUND = (30, 30, 30)
    BUTTON_READY = (0, 150, 0)
    BUTTON_SECTION = (50, 50, 50)
    BUTTON_SECTION_BORDER = (100, 100, 100)
    TEXT_COUNTDOWN = (255, 165, 0)
    SIGNAL_RECORDING = (255, 0, 0)
    TEXT = (255, 255, 255)

class AppConfig:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    DATA_FOLDER = "gesture_data"
    GESTURE_FOLDERS = ["Derecha-Pulgar-indice","Derecha-Pulgar-Medio", "Derecha-Pulgar-Anular", "Derecha-Pulgar-Meñique", "Derecha-No Accion"]
    BUTTON_COLORS = ["red", "green", "yellow", "blue", "purple"]
    GESTURE_NAMES = ["Pulgar-Indice", "Pulgar-Medio", "Pulgar-Anular", "Pulgar-Meñique", "No Accion"]

    BASE_GESTURE_PATH = "gesture_data"

    def ensure_gesture_folders_exist():
        os.makedirs(AppConfig.BASE_GESTURE_PATH, exist_ok=True)

        for folder_name in AppConfig.GESTURE_FOLDERS:
            path = os.path.join(AppConfig.BASE_GESTURE_PATH, folder_name)
            os.makedirs(path, exist_ok=True)