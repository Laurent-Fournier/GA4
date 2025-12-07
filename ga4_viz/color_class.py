# IA Usage
# fournis une palette de 20 couleurs au format "rgba(235,208,127,1)" pour réaliser des graphiques.

class Color:
    """
    Gestion des palettes de couleur pour les graphiques.
    Fournit une palette de 20 couleurs au format RGBA.
    """

    # -------------
    # Constructor
    # -------------
    def __init__(self):
        self.color_palette = [
            {'r': 46, 'g':204, 'b':113, 'hex':'#2ECC71'},
            {'r':214, 'g':137, 'b': 16, 'hex':'#D68910'},
            {'r': 52, 'g':152, 'b':219, 'hex':'#3498DB'},
            {'r':231, 'g': 76, 'b': 60, 'hex':'#E74C3C'},
            {'r':155, 'g': 89, 'b':182, 'hex':'#9B59B6'},
            {'r':241, 'g':196, 'b': 15, 'hex':'#F1C40F'},
            {'r':230, 'g':126, 'b': 34, 'hex':'#E67E22'},
            {'r': 26, 'g':188, 'b':156, 'hex':'#1ABC9C'},
            {'r':149, 'g':165, 'b':166, 'hex':'#95A5A6'},
            {'r':243, 'g':156, 'b': 18, 'hex':'#F39C12'},
            {'r': 52, 'g': 73, 'b': 94, 'hex':'#34495E'},
            {'r':192, 'g': 57, 'b': 43, 'hex':'#C0392B'},
            {'r': 41, 'g':128, 'b':185, 'hex':"#2980B9"},
            {'r': 39, 'g':174, 'b': 96, 'hex':'#27AE60'},
            {'r':127, 'g':140, 'b':141, 'hex':'#7F8C8D'},
            {'r':142, 'g': 68, 'b':173, 'hex':'#8E44AD'},
            {'r': 44, 'g': 62, 'b': 80, 'hex':'#2C3E50'},
            {'r':236, 'g':112, 'b': 99, 'hex':'#EC7063'},
            {'r': 22, 'g':160, 'b':133, 'hex':'#16A085'},
            {'r':235, 'g':208, 'b':127, 'hex':'#EBD07F'},
         ]   
    
    def get_color_palette(self) -> list:
        """
        Retourne la palette de couleurs.
        """
        return  self.color_palette

    def get_rgba(self, index:int, alpha: float = 1.0) -> str :
        """
        Retourne une couleur au format RGBA.
        :param index: Index de la couleur dans la palette.
        :param alpha: Valeur d'opacité (0.0 à 1.0).
        :return: Couleur au format RGBA.
        """
        if index >= len(self.color_palette):
            index = index % len(self.color_palette)
        color = self.color_palette[index]       
        return f"rgba({color['r']},{color['g']},{color['b']},{alpha})"

    def get_rgba_background(self, index: int, alpha: float = 0.7) -> str:
        """
        Retourne une couleur au format RGBA pour l'arrière-plan.
        :param index: Index de la couleur dans la palette.
        :param alpha: Valeur d'opacité (par défaut 0.7).
        :return: Couleur au format RGBA.
        """        
        return  self.get_rgba(index, alpha)
    
    def get_rgba_foreground(self, index: int, alpha: float = 1.0) -> str:
        """
        Retourne une couleur au format RGBA pour le premier plan.
        :param index: Index de la couleur dans la palette.
        :param alpha: Valeur d'opacité (par défaut 1.0).
        :return: Couleur au format RGBA.
        """        
        return  self.get_rgba(index, alpha)

