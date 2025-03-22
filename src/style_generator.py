#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Générateur de styles QR simplifié - Corrigé pour Render
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
from PIL import Image

class QRStyleGenerator:
    """Classe pour générer des QR codes avec différents styles"""
    
    def __init__(self, output_dir=None):
        """Initialisation du générateur de styles"""
        self.output_dir = output_dir or "static/img/styles"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Définition des styles - avec les paramètres corrects
        self.styles = {
            # Styles de base
            'classic': {
                'drawer': SquareModuleDrawer(),
                'mask': SolidFillColorMask(front_color=(0, 0, 0), back_color=(255, 255, 255))
            },
            'rounded': {
                'drawer': RoundedModuleDrawer(),
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
    
    def generate_style_samples(self, sample_data="https://example.com"):
        """Génère des exemples de tous les styles disponibles"""
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
            
            # Application du style
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=style_config['drawer'],
                color_mask=style_config['mask']
            )
            
            # Sauvegarde
            img.save(output_path)
            generated_files[style_name] = output_path
            
        return generated_files

# Fonction principale pour l'utilisation en script
def main():
    if os.environ.get('RENDER'):
        output_dir = '/tmp/static/img/styles'
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(base_dir, 'src', 'frontend', 'static', 'img', 'styles')
    
    generator = QRStyleGenerator(output_dir)
    styles = generator.generate_style_samples()
    print(f"Styles générés: {len(styles)}")

if __name__ == "__main__":
    main()
