#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import qrcode
import math
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
from PIL import Image, ImageDraw, ImageFilter

class QRStyleGenerator:
    """Classe pour générer des QR codes avec différents styles"""
    
    def __init__(self, output_dir=None):
        """Initialisation du générateur de styles"""
        self.output_dir = output_dir or "static/img/styles"
        
        # Créer les sous-dossiers pour organiser les styles
        self.module_shapes_dir = os.path.join(self.output_dir, "module_shapes")
        self.frame_shapes_dir = os.path.join(self.output_dir, "frame_shapes")
        self.eye_shapes_dir = os.path.join(self.output_dir, "eye_shapes")
        
        # S'assurer que tous les dossiers existent
        for directory in [self.output_dir, self.module_shapes_dir, self.frame_shapes_dir, self.eye_shapes_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Définition des formes de modules disponibles (corps)
        self.module_shapes = {
            'square': SquareModuleDrawer(),
            'rounded': RoundedModuleDrawer(),
            'circle': CircleModuleDrawer(),
            'dot': CircleModuleDrawer(radius_ratio=0.6),
            'vertical_bars': VerticalBarsDrawer(),
            'horizontal_bars': HorizontalBarsDrawer(),
            'gapped_square': GappedSquareModuleDrawer(),
            'mini_square': SquareModuleDrawer(module_scale=0.8)
        }
        
        # Définition des styles complets
        self.styles = {
            'classic': {
                'drawer': SquareModuleDrawer(),
                'mask': SolidFillColorMask(front_color=(0, 0, 0), back_color=(255, 255, 255))
            },
            'rounded': {
                'drawer': RoundedModuleDrawer(radius_ratio=0.5),
                'mask': SolidFillColorMask(front_color=(0, 0, 0), back_color=(255, 255, 255))
            },
            'dots': {
                'drawer': CircleModuleDrawer(),
                'mask': SolidFillColorMask(front_color=(0, 0, 0), back_color=(255, 255, 255))
            },
            'modern_blue': {
                'drawer': RoundedModuleDrawer(),
                'mask': VerticalGradiantColorMask(
                    bottom_color=(0, 51, 153),
                    top_color=(0, 102, 204),
                    back_color=(255, 255, 255)
                )
            },
            'sunset': {
                'drawer': CircleModuleDrawer(),
                'mask': HorizontalGradiantColorMask(
                    left_color=(255, 102, 0),
                    right_color=(204, 0, 0),
                    back_color=(255, 255, 255)
                )
            },
            'forest': {
                'drawer': SquareModuleDrawer(),
                'mask': RadialGradiantColorMask(
                    center_color=(0, 102, 0), 
                    edge_color=(0, 51, 0),
                    back_color=(255, 255, 255)
                )
            },
            'ocean': {
                'drawer': RoundedModuleDrawer(),
                'mask': RadialGradiantColorMask(
                    center_color=(0, 153, 204), 
                    edge_color=(0, 51, 102),
                    back_color=(255, 255, 255)
                )
            },
            'barcode': {
                'drawer': VerticalBarsDrawer(),
                'mask': SolidFillColorMask(front_color=(0, 0, 0), back_color=(255, 255, 255))
            },
            'elegant': {
                'drawer': GappedSquareModuleDrawer(),
                'mask': SolidFillColorMask(front_color=(51, 51, 51), back_color=(245, 245, 245))
            }
        }
    
    def generate_module_shape_samples(self):
        """Génère des exemples pour toutes les formes de modules (corps)"""
        print("Génération des formes de modules...")
        shapes = [
            {'name': 'square', 'drawer': SquareModuleDrawer()},
            {'name': 'rounded', 'drawer': RoundedModuleDrawer(radius_ratio=0.5)},
            {'name': 'circle', 'drawer': CircleModuleDrawer()},
            {'name': 'dot', 'drawer': CircleModuleDrawer(radius_ratio=0.6)},
            {'name': 'vertical_bars', 'drawer': VerticalBarsDrawer()},
            {'name': 'horizontal_bars', 'drawer': HorizontalBarsDrawer()},
            {'name': 'gapped_square', 'drawer': GappedSquareModuleDrawer()},
            {'name': 'mini_square', 'drawer': SquareModuleDrawer(module_scale=0.8)},
        ]
        
        for shape in shapes:
            self._generate_shape_preview(shape['name'], shape['drawer'], self.module_shapes_dir)
    
    def generate_frame_shape_samples(self):
        """Génère des exemples pour toutes les formes de contour des marqueurs"""
        print("Génération des formes de contour des marqueurs...")
        
        # Liste des formes de contour
        frames = [
            'square', 'rounded_square', 'circle', 'rounded', 'dots', 
            'diamond', 'corner_cut', 'jagged', 'pointed', 'pixel'
        ]
        
        # Taille de chaque image
        size = 100
        
        for frame in frames:
            img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            # Dessiner différentes formes de contour
            if frame == 'square':
                draw.rectangle([5, 5, size-5, size-5], outline=(0, 0, 0), width=5)
            elif frame == 'rounded_square':
                # Simuler un rectangle arrondi
                draw.rounded_rectangle([5, 5, size-5, size-5], radius=10, outline=(0, 0, 0), width=5)
            elif frame == 'circle':
                draw.ellipse([5, 5, size-5, size-5], outline=(0, 0, 0), width=5)
            elif frame == 'rounded':
                # Rectangle avec coins très arrondis
                draw.rounded_rectangle([5, 5, size-5, size-5], radius=20, outline=(0, 0, 0), width=5)
            elif frame == 'dots':
                # Points pour former un cadre
                r = 4  # rayon des points
                spacing = 10  # espacement entre les points
                for x in range(10, size-10, spacing):
                    draw.ellipse([x-r, 10-r, x+r, 10+r], fill=(0, 0, 0))
                    draw.ellipse([x-r, size-10-r, x+r, size-10+r], fill=(0, 0, 0))
                for y in range(10, size-10, spacing):
                    draw.ellipse([10-r, y-r, 10+r, y+r], fill=(0, 0, 0))
                    draw.ellipse([size-10-r, y-r, size-10+r, y+r], fill=(0, 0, 0))
            elif frame == 'diamond':
                # Forme en diamant
                points = [(size//2, 5), (size-5, size//2), (size//2, size-5), (5, size//2)]
                draw.polygon(points, outline=(0, 0, 0), width=5)
            elif frame == 'corner_cut':
                # Rectangle avec coins coupés
                w = size - 10
                h = size - 10
                offset = 5
                corner_cut = 15
                points = [
                    (offset + corner_cut, offset), (offset + w - corner_cut, offset),
                    (offset + w, offset + corner_cut), (offset + w, offset + h - corner_cut),
                    (offset + w - corner_cut, offset + h), (offset + corner_cut, offset + h),
                    (offset, offset + h - corner_cut), (offset, offset + corner_cut)
                ]
                draw.polygon(points, outline=(0, 0, 0), width=5)
            elif frame == 'jagged':
                # Contour en zigzag
                points = []
                steps = 20
                for i in range(steps):
                    angle = 2 * math.pi * i / steps
                    radius = size//2 - 10
                    jag = 5 if i % 2 == 0 else 10
                    x = size//2 + int((radius - jag) * math.cos(angle))
                    y = size//2 + int((radius - jag) * math.sin(angle))
                    points.append((x, y))
                draw.polygon(points, outline=(0, 0, 0), width=3)
            elif frame == 'pointed':
                # Forme étoilée
                points = []
                steps = 8
                for i in range(steps * 2):
                    angle = math.pi * i / steps
                    radius = size//2 - 10
                    if i % 2 == 0:
                        r = radius
                    else:
                        r = radius - 15
                    x = size//2 + int(r * math.cos(angle))
                    y = size//2 + int(r * math.sin(angle))
                    points.append((x, y))
                draw.polygon(points, outline=(0, 0, 0), width=3)
            elif frame == 'pixel':
                # Style pixelisé
                pixel_size = 8
                for x in range(0, size, pixel_size):
                    if x < 15 or x > size - 15 - pixel_size:
                        for y in range(0, size, pixel_size):
                            draw.rectangle([x, y, x+pixel_size, y+pixel_size], outline=(0, 0, 0), width=1)
                    else:
                        draw.rectangle([x, 0, x+pixel_size, pixel_size], outline=(0, 0, 0), width=1)
                        draw.rectangle([x, size-pixel_size, x+pixel_size, size], outline=(0, 0, 0), width=1)
            
            # Ajouter le texte
            font_size = 12
            draw.text((size//2, size+5), frame, fill=(0, 0, 0), anchor="mt")
            
            # Sauvegarder l'image
            output_path = os.path.join(self.frame_shapes_dir, f"{frame}.png")
            img.save(output_path)
            print(f"  - {frame} créé: {output_path}")
    
    def generate_eye_shape_samples(self):
        """Génère des exemples pour toutes les formes du centre des marqueurs (yeux)"""
        print("Génération des formes de centre des marqueurs...")
        
        # Liste des formes d'yeux
        eyes = [
            'square', 'circle', 'rounded', 'cushion', 'diamond',
            'star', 'dots', 'rounded_rect', 'flower', 'leaf'
        ]
        
        # Taille de chaque image
        size = 100
        
        for eye in eyes:
            img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            # Dessiner la partie externe (grand carré)
            outer_offset = 5
            outer_size = size - 2 * outer_offset
            
            # Dessiner la partie interne (petit carré)
            inner_offset = size // 3
            inner_size = size // 3
            
            # Dessiner différentes formes d'yeux
            if eye == 'square':
                # Carré standard (externe + interne)
                draw.rectangle([outer_offset, outer_offset, outer_offset + outer_size, outer_offset + outer_size], fill=(0, 0, 0))
                draw.rectangle([inner_offset, inner_offset, inner_offset + inner_size, inner_offset + inner_size], fill=(255, 255, 255))
            elif eye == 'circle':
                # Cercle
                draw.ellipse([outer_offset, outer_offset, outer_offset + outer_size, outer_offset + outer_size], fill=(0, 0, 0))
                draw.ellipse([inner_offset, inner_offset, inner_offset + inner_size, inner_offset + inner_size], fill=(255, 255, 255))
            elif eye == 'rounded':
                # Carré arrondi
                draw.rounded_rectangle([outer_offset, outer_offset, outer_offset + outer_size, outer_offset + outer_size], radius=15, fill=(0, 0, 0))
                draw.rounded_rectangle([inner_offset, inner_offset, inner_offset + inner_size, inner_offset + inner_size], radius=5, fill=(255, 255, 255))
            elif eye == 'cushion':
                # Forme de coussin
                outer_points = [
                    (outer_offset + outer_size//2, outer_offset),
                    (outer_offset + outer_size, outer_offset + outer_size//2),
                    (outer_offset + outer_size//2, outer_offset + outer_size),
                    (outer_offset, outer_offset + outer_size//2)
                ]
                inner_points = [
                    (inner_offset + inner_size//2, inner_offset),
                    (inner_offset + inner_size, inner_offset + inner_size//2),
                    (inner_offset + inner_size//2, inner_offset + inner_size),
                    (inner_offset, inner_offset + inner_size//2)
                ]
                draw.polygon(outer_points, fill=(0, 0, 0))
                draw.polygon(inner_points, fill=(255, 255, 255))
            elif eye == 'diamond':
                # Diamant
                outer_points = [
                    (outer_offset + outer_size//2, outer_offset),
                    (outer_offset + outer_size, outer_offset + outer_size//2),
                    (outer_offset + outer_size//2, outer_offset + outer_size),
                    (outer_offset, outer_offset + outer_size//2)
                ]
                inner_points = [
                    (inner_offset + inner_size//2, inner_offset),
                    (inner_offset + inner_size, inner_offset + inner_size//2),
                    (inner_offset + inner_size//2, inner_offset + inner_size),
                    (inner_offset, inner_offset + inner_size//2)
                ]
                draw.polygon(outer_points, fill=(0, 0, 0))
                draw.polygon(inner_points, fill=(255, 255, 255))
            elif eye == 'star':
                # Étoile
                # Externe
                outer_points = []
                outer_steps = 10
                for i in range(outer_steps * 2):
                    angle = math.pi * i / outer_steps
                    radius = outer_size // 2
                    if i % 2 == 0:
                        r = radius
                    else:
                        r = radius * 0.6
                    x = size // 2 + int(r * math.cos(angle))
                    y = size // 2 + int(r * math.sin(angle))
                    outer_points.append((x, y))
                
                # Interne
                inner_points = []
                inner_steps = 8
                for i in range(inner_steps * 2):
                    angle = math.pi * i / inner_steps
                    radius = inner_size // 2
                    if i % 2 == 0:
                        r = radius
                    else:
                        r = radius * 0.6
                    x = size // 2 + int(r * math.cos(angle))
                    y = size // 2 + int(r * math.sin(angle))
                    inner_points.append((x, y))
                
                draw.polygon(outer_points, fill=(0, 0, 0))
                draw.polygon(inner_points, fill=(255, 255, 255))
            elif eye == 'dots':
                # Ensemble de points
                draw.rectangle([outer_offset, outer_offset, outer_offset + outer_size, outer_offset + outer_size], fill=(0, 0, 0))
                
                # Cercles pour le contour
                r = 5  # rayon
                spacing = 15  # espacement
                for x in range(outer_offset + spacing, outer_offset + outer_size, spacing):
                    draw.ellipse([x-r, outer_offset+spacing-r, x+r, outer_offset+spacing+r], fill=(255, 255, 255))
                    draw.ellipse([x-r, outer_offset+outer_size-spacing-r, x+r, outer_offset+outer_size-spacing+r], fill=(255, 255, 255))
                
                for y in range(outer_offset + spacing, outer_offset + outer_size, spacing):
                    draw.ellipse([outer_offset+spacing-r, y-r, outer_offset+spacing+r, y+r], fill=(255, 255, 255))
                    draw.ellipse([outer_offset+outer_size-spacing-r, y-r, outer_offset+outer_size-spacing+r, y+r], fill=(255, 255, 255))
                
                # Centre
                draw.ellipse([inner_offset, inner_offset, inner_offset + inner_size, inner_offset + inner_size], fill=(255, 255, 255))
            elif eye == 'rounded_rect':
                # Rectangle arrondi
                radius = min(outer_size, outer_size) // 4
                draw.rounded_rectangle([outer_offset, outer_offset, outer_offset + outer_size, outer_offset + outer_size], radius=radius, fill=(0, 0, 0))
                
                inner_radius = min(inner_size, inner_size) // 4
                draw.rounded_rectangle([inner_offset, inner_offset, inner_offset + inner_size, inner_offset + inner_size], radius=inner_radius, fill=(255, 255, 255))
            elif eye == 'flower':
                # Forme de fleur
                # Externe
                draw.ellipse([outer_offset, outer_offset, outer_offset + outer_size, outer_offset + outer_size], fill=(0, 0, 0))
                
                # Pétales
                petals = 6
                petal_size = outer_size // 3
                for i in range(petals):
                    angle = 2 * math.pi * i / petals
                    x = size // 2 + int((outer_size // 2) * math.cos(angle))
                    y = size // 2 + int((outer_size // 2) * math.sin(angle))
                    draw.ellipse([x - petal_size//2, y - petal_size//2, x + petal_size//2, y + petal_size//2], fill=(0, 0, 0))
                
                # Centre
                draw.ellipse([inner_offset, inner_offset, inner_offset + inner_size, inner_offset + inner_size], fill=(255, 255, 255))
            elif eye == 'leaf':
                # Forme de feuille
                draw.ellipse([outer_offset, outer_offset, outer_offset + outer_size, outer_offset + outer_size], fill=(0, 0, 0))
                
                # Dessins de feuilles
                for i in range(4):
                    angle = math.pi / 2 * i
                    x1 = size // 2 + int((outer_size // 2) * math.cos(angle))
                    y1 = size // 2 + int((outer_size // 2) * math.sin(angle))
                    x2 = size // 2 + int((outer_size // 2) * math.cos(angle + math.pi))
                    y2 = size // 2 + int((outer_size // 2) * math.sin(angle + math.pi))
                    draw.line([(x1, y1), (x2, y2)], fill=(0, 0, 0), width=5)
                
                # Centre
                draw.ellipse([inner_offset, inner_offset, inner_offset + inner_size, inner_offset + inner_size], fill=(255, 255, 255))
            
            # Ajouter le texte
            font_size = 12
            draw.text((size//2, size+5), eye, fill=(0, 0, 0), anchor="mt")
            
            # Sauvegarder l'image
            output_path = os.path.join(self.eye_shapes_dir, f"{eye}.png")
            img.save(output_path)
            print(f"  - {eye} créé: {output_path}")
    
    def _generate_shape_preview(self, name, drawer, output_dir):
        """Génère une prévisualisation pour une forme de module spécifique"""
        # Création du QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data("https://example.com")
        qr.make(fit=True)
        
        try:
            # Application du style
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=drawer,
                color_mask=SolidFillColorMask(front_color=(0, 0, 0), back_color=(255, 255, 255))
            )
            
            # Ajouter nom comme texte
            pil_img = img.get_image()
            draw = ImageDraw.Draw(pil_img)
            width, height = pil_img.size
            draw.text((width//2, height-10), name, fill=(0, 0, 0))
            
            # Sauvegarde
            output_path = os.path.join(output_dir, f"{name}.png")
            pil_img.save(output_path)
            print(f"  - {name} créé: {output_path}")
            
        except Exception as e:
            print(f"Erreur lors de la génération de {name}: {e}")
    
    def generate_style_samples(self, sample_data="https://example.com"):
        """Génère des exemples de tous les styles prédéfinis"""
        generated_files = {}
        
        for style_name, style_config in self.styles.items():
            output_path = os.path.join(self.output_dir, f"{style_name}.png")
            
            # Création du QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(sample_data)
            qr.make(fit=True)
            
            try:
                # Application du style
                img = qr.make_image(
                    image_factory=StyledPilImage,
                    module_drawer=style_config['drawer'],
                    color_mask=style_config['mask']
                )
                
                # Sauvegarde
                img.save(output_path)
                generated_files[style_name] = output_path
                
            except Exception as e:
                print(f"Erreur lors de la génération du style {style_name}: {e}")
                # Fallback
                fallback = qr.make_image(fill_color="black", back_color="white")
                fallback.save(output_path)
                generated_files[style_name] = output_path
            
        return generated_files
    
    def generate_all_samples(self):
        """Génère tous les exemples de styles et formes"""
        # Générer les styles complets
        self.generate_style_samples()
        
        # Générer les formes de modules
        self.generate_module_shape_samples()
        
        # Générer les formes de contour
        self.generate_frame_shape_samples()
        
        # Générer les formes d'yeux
        self.generate_eye_shape_samples()
        
        return {
            'styles': os.listdir(self.output_dir),
            'module_shapes': os.listdir(self.module_shapes_dir),
            'frame_shapes': os.listdir(self.frame_shapes_dir),
            'eye_shapes': os.listdir(self.eye_shapes_dir)
        }

# Fonction principale
def main():
    if os.environ.get('RENDER'):
        output_dir = '/tmp/static/img/styles'
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(base_dir, 'src', 'frontend', 'static', 'img', 'styles')
    
    print(f"Génération des styles QR dans: {output_dir}")
    
    # Création du générateur
    generator = QRStyleGenerator(output_dir)
    
    # Génération de tous les exemples
    results = generator.generate_all_samples()
    
    print("Génération terminée avec succès!")
    print(f"- Styles prédéfinis: {len(results['styles'])}")
    print(f"- Formes de modules: {len(results['module_shapes'])}")
    print(f"- Formes de contour: {len(results['frame_shapes'])}")
    print(f"- Formes d'yeux: {len(results['eye_shapes'])}")

if __name__ == "__main__":
    main()
