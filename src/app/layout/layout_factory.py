from src.app.layout.right_hand_layout import RightHandLayout
from src.app.layout.left_hand_layout import LeftHandLayout

class LayoutFactory:
    @staticmethod #permite no recibir parametros, pertenece a la clase y no a una instancia
    def create_layout(name, app):
        if name == "right_hand":
            return RightHandLayout(app)
        elif name == "left_hand":
            return LeftHandLayout(app)
        else:
            raise ValueError(f"Layout Error: {name}")