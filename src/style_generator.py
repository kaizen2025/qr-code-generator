#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Générateur de styles QR avancés - Intègre plusieurs bibliothèques pour 
produire des QR codes aux styles variés comme QR Code Monkey
"""

import os
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer, 
    GappedSquareModuleDrawer,
    CircleModuleDrawer, 
    RoundedModuleDrawer,
    VerticalBarsDrawer, 
    HorizontalBarsDrawer
)
from qrcode.image.styles.colormasks import (
    SolidFillColorMask,
    RadialGradiantColorMask,
    SquareGradiantColorMask,
    HorizontalGradiantColorMask,
    VerticalGradiantColorMask
)
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import random

class QRStyleGenerator:
    """Classe pour générer des QR codes avec différents styles"""
    
    def __init__(self, output_dir=None):
        """Initialisation du générateur de styles"""
        self.output_dir = output_dir or "static/img/styles"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Définition des styles
        self.styles = {
            # Styles de base (comme QR Code Monkey)
            'classic': {
                'drawer': SquareModuleDrawer(),
                'mask': SolidFillColorMask(front_color=(0, 0, 0), back_color=(255, 255, 255)),
                'description': 'Style classique noir et blanc'
            },
            'rounded': {
                'drawer': RoundedModuleDrawer(),
                'mask': SolidFillColorMask(front_color=(0, 0, 0), back_color=(255, 255, 255)),
                'description': 'Modules arrondis noir et blanc'
            },
            'dots': {
                'drawer': CircleModuleDrawer(),
                'mask': SolidFillColorMask(front_color=(0, 0, 0), back_color=(255, 255, 255)),
                'description': 'Modules en forme de points'
            },
            'modern_blue': {
                'drawer': RoundedModuleDrawer(),
                'mask': VerticalGradiantColorMask(
                    top_color=(0, 102, 204), 
                    bottom_color=(0, 51, 153),
                    back_color=(255, 255, 255)
                ),
                'description': 'Style moderne avec dégradé bleu'
            },
            'sunset': {
                'drawer': CircleModuleDrawer(),
                'mask': HorizontalGradiantColorMask(
                    top_color=(255, 102, 0), 
                    bottom_color=(204, 0, 0),
                    back_color=(255, 255, 255)
                ),
                'description': 'Dégradé orange-rouge'
            },
            'forest': {
                'drawer': SquareModuleDrawer(),
                'mask': RadialGradiantColorMask(
                    center_color=(0, 102, 0), 
                    edge_color=(0, 51, 0),
                    back_color=(255, 255, 255)
                ),
                'description': 'Dégradé de verts'
            },
            'ocean': {
                'drawer': RoundedModuleDrawer(),
                'mask': RadialGradiantColorMask(
                    center_color=(0, 153, 204), 
                    edge_color=(0, 51, 102),
                    back_color=(255, 255, 255)
                ),
                'description': 'Dégradé de bleus'
            },
            'barcode': {
                'drawer': VerticalBarsDrawer(),
                'mask': SolidFillColorMask(front_color=(0, 0, 0), back_color=(255, 255, 255)),
                'description': 'Style code-barres vertical'
            },
            'elegant': {
                'drawer': GappedSquareModuleDrawer(),
                'mask': SolidFillColorMask(front_color=(51, 51, 51), back_color=(245, 245, 245)),
                'description': 'Style minimaliste avec espacement'
            },
            
            # Styles additionnels (plus avancés)
            'neon': {
                'drawer': RoundedModuleDrawer(),
                'mask': RadialGradiantColorMask(
                    center_color=(0, 255, 204), 
                    edge_color=(255, 0, 255),
                    back_color=(20, 20, 40)
                ),
                'description': 'Style néon brillant'
            },
            'vintage': {
                'drawer': SquareModuleDrawer(),
                'mask': SolidFillColorMask(front_color=(139, 69, 19), back_color=(255, 248, 220)),
                'description': 'Style vintage sépia'
            },
            'rainbow': {
                'drawer': CircleModuleDrawer(),
                'mask': HorizontalGradiantColorMask(
                    top_color=(255, 0, 0), 
                    bottom_color=(0, 0, 255),
                    back_color=(255, 255, 255)
                ),
                'description': 'Dégradé arc-en-ciel'
            },
            'pixelated': {
                'drawer': SquareModuleDrawer(),
                'mask': SquareGradiantColorMask(
                    center_color=(52, 152, 219), 
                    edge_color=(41, 128, 185),
                    back_color=(236, 240, 241)
                ),
                'description': 'Style pixelisé carré'
            },
            'industrial': {
                'drawer': HorizontalBarsDrawer(),
                'mask': SolidFillColorMask(front_color=(50, 50, 50), back_color=(180, 180, 180)),
                'description': 'Style industriel avec barres'
            }
        }
    
    def generate_style_samples(self, sample_data="https://example.com"):
        """Génère des exemples de tous les styles disponibles"""
        generated_files = {}
        
        for style_name, style_config in self.styles.items():
            output_path = os.path.join(self.output_dir, f"{style_name}.png")
            
            # Création du QR code de base
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(sample_data)
            qr.make(fit=True)
            
            # Application du style
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=style_config['drawer'],
                color_mask=style_config['mask']
            )
            
            # Sauvegarde de l'image
            img.save(output_path)
            generated_files[style_name] = output_path
            
        return generated_files
    
    def create_custom_shapes(self):
        """Crée des exemples de formes personnalisées pour les modules QR"""
        output_dir = os.path.join(self.output_dir, "shapes")
        os.makedirs(output_dir, exist_ok=True)
        
        shapes = [
            "circle", "square", "diamond", "hexagon", "rounded", 
            "dot", "mini_circle", "heart", "star", "cross"
        ]
        
        for shape in shapes:
            # Création d'une image 100x100
            img = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            if shape == "circle":
                draw.ellipse((10, 10, 90, 90), fill=(0, 0, 0))
            elif shape == "square":
                draw.rectangle((10, 10, 90, 90), fill=(0, 0, 0))
            elif shape == "diamond":
                draw.polygon([(50, 10), (90, 50), (50, 90), (10, 50)], fill=(0, 0, 0))
            elif shape == "hexagon":
                draw.polygon([(25, 10), (75, 10), (90, 50), (75, 90), (25, 90), (10, 50)], fill=(0, 0, 0))
            elif shape == "rounded":
                draw.rounded_rectangle((10, 10, 90, 90), radius=20, fill=(0, 0, 0))
            elif shape == "dot":
                draw.ellipse((30, 30, 70, 70), fill=(0, 0, 0))
            elif shape == "mini_circle":
                draw.ellipse((35, 35, 65, 65), fill=(0, 0, 0))
            elif shape == "heart":
                # Approximation simple d'un cœur avec des courbes
                draw.pieslice((20, 20, 60, 60), 0, 180, fill=(0, 0, 0))
                draw.pieslice((40, 20, 80, 60), 0, 180, fill=(0, 0, 0))
                draw.polygon([(20, 40), (80, 40), (50, 90)], fill=(0, 0, 0))
            elif shape == "star":
                # Étoile à 5 branches
                points = []
                for i in range(10):
                    angle = i * 36 * 3.14159 / 180
                    r = 40 if i % 2 == 0 else 20
                    points.append((50 + r * round(cos(angle)), 50 + r * round(sin(angle))))
                draw.polygon(points, fill=(0, 0, 0))
            elif shape == "cross":
                draw.rectangle((40, 10, 60, 90), fill=(0, 0, 0))
                draw.rectangle((10, 40, 90, 60), fill=(0, 0, 0))
                
            img.save(os.path.join(output_dir, f"{shape}.png"))
    
    def generate_style_gallery(self, columns=3, width=800):
        """Génère une galerie d'images avec tous les styles disponibles"""
        # D'abord, génère tous les exemples de style
        self.generate_style_samples()
        
        # Calcule les dimensions de la galerie
        style_count = len(self.styles)
        rows = (style_count + columns - 1) // columns
        
        # Taille de chaque cellule (image + titre)
        cell_width = width // columns
        cell_height = cell_width + 30  # Espace pour le texte
        
        # Création de l'image de la galerie
        gallery = Image.new('RGB', (width, rows * cell_height), color=(255, 255, 255))
        
        # Placement des images et des titres
        for i, (style_name, style_config) in enumerate(self.styles.items()):
            # Chargement de l'image de style
            style_path = os.path.join(self.output_dir, f"{style_name}.png")
            style_img = Image.open(style_path)
            
            # Redimensionnement pour s'adapter à la cellule
            thumb_size = cell_width - 20
            style_img = style_img.resize((thumb_size, thumb_size), Image.LANCZOS)
            
            # Calcul de la position
            row = i // columns
            col = i % columns
            x = col * cell_width + (cell_width - thumb_size) // 2
            y = row * cell_height + 10
            
            # Placement de l'image
            gallery.paste(style_img, (x, y))
            
            # Ajout du titre
            draw = ImageDraw.Draw(gallery)
            text_x = col * cell_width + cell_width // 2
            text_y = y + thumb_size + 10
            draw.text((text_x, text_y), style_name, fill=(0, 0, 0), anchor="mt")
        
        # Sauvegarde de la galerie
        gallery_path = os.path.join(os.path.dirname(self.output_dir), "style_gallery.png")
        gallery.save(gallery_path)
        return gallery_path

# Fonction principale pour l'utilisation en tant que script
def main():
    # Détermination du chemin de sortie basé sur l'environnement
    if os.environ.get('RENDER'):
        output_dir = '/tmp/static/img/styles'
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(base_dir, 'src', 'frontend', 'static', 'img', 'styles')
    
    # Création du générateur
    generator = QRStyleGenerator(output_dir)
    
    # Génération des exemples de style
    styles = generator.generate_style_samples()
    print(f"Styles générés: {len(styles)}")
    for style, path in styles.items():
        print(f"- {style}: {path}")
    
    # Création d'une galerie des styles
    gallery_path = generator.generate_style_gallery()
    print(f"Galerie des styles créée: {gallery_path}")

if __name__ == "__main__":
    main()
