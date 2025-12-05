# IA Usage
# fournis une palette de 20 couleurs au format "rgba(235,208,127,1)" pour réaliser des graphiques.

class Color:
    """
    Gestion des palettes de couleur
    """

    # -------------
    # Constructor
    # -------------
    def __init__(self):
        self.color_palette = [
            {'r': 46, 'g':204, 'b':113, 'rgb':'#2ECC71'},
            {'r':214, 'g':137, 'b': 16, 'rgb':'#D68910'},
            {'r': 52, 'g':152, 'b':219, 'rgb':'#3498DB'},
            {'r':231, 'g': 76, 'b': 60, 'rgb':'#E74C3C'},
            {'r':155, 'g': 89, 'b':182, 'rgb':'#9B59B6'},
            {'r':241, 'g':196, 'b': 15, 'rgb':'#F1C40F'},
            {'r':230, 'g':126, 'b': 34, 'rgb':'#E67E22'},
            {'r': 26, 'g':188, 'b':156, 'rgb':'#1ABC9C'},
            {'r':149, 'g':165, 'b':166, 'rgb':'#95A5A6'},
            {'r':243, 'g':156, 'b': 18, 'rgb':'#F39C12'},
            {'r': 52, 'g': 73, 'b': 94, 'rgb':'#34495E'},
            {'r':192, 'g': 57, 'b': 43, 'rgb':'#C0392B'},
            {'r': 41, 'g':128, 'b':185, 'rgb':"#2980B9"},
            {'r': 39, 'g':174, 'b': 96, 'rgb':'#27AE60'},
            {'r':127, 'g':140, 'b':141, 'rgb':'#7F8C8D'},
            {'r':142, 'g': 68, 'b':173, 'rgb':'#8E44AD'},
            {'r': 44, 'g': 62, 'b': 80, 'rgb':'#2C3E50'},
            {'r':236, 'g':112, 'b': 99, 'rgb':'#EC7063'},
            {'r': 22, 'g':160, 'b':133, 'rgb':'#16A085'},
            {'r':235, 'g':208, 'b':127, 'rgb':'#EBD07F'},
         ]   
    
    def get_color_palette(self):
        return  self.color_palette

    def get_rgba(self, no, alpha):
        return f'rgba({self.color_palette[no]['r']},{self.color_palette[no]['g']},{self.color_palette[no]['b']},{alpha})'

    def get_rgba_background(self, no):
        return  self.get_rgba(no, 0.7)
    
    def get_rgba_foreground(self, no):
        return  self.get_rgba(no, 1)

