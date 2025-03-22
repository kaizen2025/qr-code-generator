#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Générateur de styles QR avancés - Module pour générer des QR codes
avec différents styles semblables à QR Code Monkey
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
from PIL import Image, ImageDraw, ImageFilter

class QRStyleGenerator:
    """Classe pour générer des QR codes avec différents styles"""
    
    def __init__(self, output_dir=None):
        """Initialisation du générateur de styles"""
        self.output_dir = output_dir or "static/img/styles"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Définition des styles avec les noms de paramètres corrects
        self.styles = {
            # Styles de base
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
                    bottom_color=(0, 51, 153),  # Attention: top/bottom sont inversés dans certaines versions
                    top_color=(0, 102, 204),
                    back_color=(255, 255, 255)
                ),
                'description': 'Style moderne avec dégradé bleu'
            },
            'sunset': {
                'drawer': CircleModuleDrawer(),
                'mask': HorizontalGradiantColorMask(
                    left_color=(255, 102, 0),   # Attention: left/right au lieu de top/bottom
                    right_color=(204, 0, 0),
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
            
            try:
                # Application du style
                img = qr.make_image(
                    image_factory=StyledPilImage,
                    module_drawer=style_config['drawer'],
                    color_mask=style_config['mask']
                )
                
                # Sauvegarde
                img.save(output_path)
                
                # Ajouter un texte descriptif (comme référence visuelle)
                self._add_label_to_image(output_path, style_name)
                
                generated_files[style_name] = output_path
                
            except Exception as e:
                print(f"Erreur lors de la génération du style {style_name}: {e}")
                # Fallback - créer un QR code basique si le style échoue
                fallback = qr.make_image(fill_color="black", back_color="white")
                fallback.save(output_path)
                generated_files[style_name] = output_path
            
        return generated_files
    
    def _add_label_to_image(self, image_path, label):
        """Ajoute un texte de label en bas de l'image pour l'identification visuelle"""
        try:
            # Ouvrir l'image
            img = Image.open(image_path)
            width, height = img.size
            
            # Créer une nouvelle image avec espace pour le texte
            new_img = Image.new('RGB', (width, height + 20), color=(255, 255, 255))
            new_img.paste(img, (0, 0))
            
            # Dessiner le texte
            draw = ImageDraw.Draw(new_img)
            text_width = len(label) * 6  # Estimation de la largeur du texte
            draw.text(((width - text_width) // 2, height + 5), label, fill=(0, 0, 0))
            
            # Sauvegarder l'image modifiée
            new_img.save(image_path)
        except Exception as e:
            print(f"Erreur lors de l'ajout du label à l'image: {e}")
    
    def create_mini_qr_collection(self):
        """Crée une image unique avec tous les styles pour prévisualisation"""
        # Générer d'abord les exemples
        self.generate_style_samples()
        
        styles_count = len(self.styles)
        cols = 3
        rows = (styles_count + cols - 1) // cols
        
        # Taille de chaque vignette
        thumb_size = 100
        padding = 10
        
        # Taille totale de l'image collection
        total_width = cols * (thumb_size + padding) + padding
        total_height = rows * (thumb_size + padding) + padding
        
        # Création de l'image collection
        collection = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))
        
        # Placement des vignettes
        col, row = 0, 0
        for style_name in self.styles.keys():
            # Charger l'image de style
            style_path = os.path.join(self.output_dir, f"{style_name}.png")
            if os.path.exists(style_path):
                try:
                    style_img = Image.open(style_path)
                    # Redimensionner pour la vignette
                    style_img = style_img.resize((thumb_size, thumb_size), Image.LANCZOS)
                    
                    # Calculer la position
                    x = padding + col * (thumb_size + padding)
                    y = padding + row * (thumb_size + padding)
                    
                    # Coller la vignette
                    collection.paste(style_img, (x, y))
                    
                    # Texte du style
                    draw = ImageDraw.Draw(collection)
                    text_x = x + thumb_size // 2
                    text_y = y + thumb_size + 2
                    draw.text((text_x, text_y), style_name, fill=(0, 0, 0))
                    
                except Exception as e:
                    print(f"Erreur lors de l'ajout de {style_name} à la collection: {e}")
            
            # Passer à la colonne/ligne suivante
            col += 1
            if col >= cols:
                col = 0
                row += 1
        
        # Sauvegarder la collection
        collection_path = os.path.join(self.output_dir, "collection.png")
        collection.save(collection_path)
        return collection_path

# Fonction principale pour l'utilisation en script autonome
def main():
    # Détermination du chemin de sortie
    if os.environ.get('RENDER'):
        output_dir = '/tmp/static/img/styles'
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(base_dir, 'src', 'frontend', 'static', 'img', 'styles')
    
    print(f"Génération des styles QR dans: {output_dir}")
    
    # Création du générateur
    generator = QRStyleGenerator(output_dir)
    
    # Génération des styles
    styles = generator.generate_style_samples()
    print(f"Styles générés: {len(styles)}")
    
    # Création de la collection
    collection_path = generator.create_mini_qr_collection()
    print(f"Collection créée: {collection_path}")

if __name__ == "__main__":
    main()
