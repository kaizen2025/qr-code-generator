#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module de prévisualisation en temps réel pour les QR codes.
Ce module fournit des fonctionnalités pour générer des prévisualisations
de QR codes en temps réel sans sauvegarder les fichiers.
"""

import io
import base64
import qrcode
from PIL import Image
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


class QRCodePreviewGenerator:
    """
    Classe pour la génération de prévisualisations de QR codes en temps réel.
    Fournit des méthodes pour générer des prévisualisations sans sauvegarder les fichiers.
    """

    def __init__(self):
        """
        Initialise le générateur de prévisualisations de QR codes.
        """
        # Dictionnaire des styles de modules disponibles
        self.module_drawers = {
            'square': SquareModuleDrawer(),
            'gapped_square': GappedSquareModuleDrawer(),
            'circle': CircleModuleDrawer(),
            'rounded': RoundedModuleDrawer(),
            'vertical_bars': VerticalBarsDrawer(),
            'horizontal_bars': HorizontalBarsDrawer()
        }
        
        # Dictionnaire des masques de couleur disponibles
        self.color_masks = {
            'solid': SolidFillColorMask,
            'radial_gradient': RadialGradiantColorMask,
            'square_gradient': SquareGradiantColorMask,
            'horizontal_gradient': HorizontalGradiantColorMask,
            'vertical_gradient': VerticalGradiantColorMask
        }
        
        # Dictionnaire des styles prédéfinis
        self.predefined_styles = {
            'classic': {
                'module_drawer': 'square',
                'color_mask': 'solid',
                'front_color': (0, 0, 0),
                'back_color': (255, 255, 255)
            },
            'rounded': {
                'module_drawer': 'rounded',
                'color_mask': 'solid',
                'front_color': (0, 0, 0),
                'back_color': (255, 255, 255)
            },
            'dots': {
                'module_drawer': 'circle',
                'color_mask': 'solid',
                'front_color': (0, 0, 0),
                'back_color': (255, 255, 255)
            },
            'modern_blue': {
                'module_drawer': 'rounded',
                'color_mask': 'vertical_gradient',
                'front_color': (0, 102, 204),
                'bottom_color': (0, 51, 153),
                'back_color': (255, 255, 255)
            },
            'sunset': {
                'module_drawer': 'circle',
                'color_mask': 'horizontal_gradient',
                'front_color': (255, 102, 0),
                'bottom_color': (204, 0, 0),
                'back_color': (255, 255, 255)
            },
            'forest': {
                'module_drawer': 'square',
                'color_mask': 'radial_gradient',
                'front_color': (0, 102, 0),
                'edge_color': (0, 51, 0),
                'gradient_center': (0.5, 0.5),
                'back_color': (255, 255, 255)
            },
            'ocean': {
                'module_drawer': 'rounded',
                'color_mask': 'radial_gradient',
                'front_color': (0, 153, 204),
                'edge_color': (0, 51, 102),
                'gradient_center': (0.5, 0.5),
                'back_color': (255, 255, 255)
            },
            'barcode': {
                'module_drawer': 'vertical_bars',
                'color_mask': 'solid',
                'front_color': (0, 0, 0),
                'back_color': (255, 255, 255)
            },
            'elegant': {
                'module_drawer': 'gapped_square',
                'color_mask': 'solid',
                'front_color': (51, 51, 51),
                'back_color': (245, 245, 245)
            }
        }
    
    def generate_preview_base64(self, data, preview_type='basic', **options):
        """
        Génère une prévisualisation de QR code et la retourne en base64.
        
        Args:
            data (str): Données à encoder dans le QR code (URL, texte, etc.)
            preview_type (str): Type de prévisualisation ('basic', 'custom', 'styled', 'logo', 'social')
            **options: Options supplémentaires pour la personnalisation du QR code.
            
        Returns:
            str: Image QR code encodée en base64.
        """
        # Paramètres par défaut
        version = options.get('version', 1)
        error_correction = options.get('error_correction', qrcode.constants.ERROR_CORRECT_M)
        box_size = options.get('box_size', 10)
        border = options.get('border', 4)
        
        # Génération du QR code selon le type de prévisualisation
        if preview_type == 'basic':
            img = self._generate_basic_preview(data, version, error_correction, box_size, border)
        
        elif preview_type == 'custom':
            fill_color = options.get('fill_color', "black")
            back_color = options.get('back_color', "white")
            img = self._generate_custom_preview(data, version, error_correction, box_size, border, fill_color, back_color)
        
        elif preview_type == 'styled':
            module_drawer_name = options.get('module_drawer', 'square')
            color_mask_name = options.get('color_mask', 'solid')
            img = self._generate_styled_preview(data, version, error_correction, box_size, border, module_drawer_name, color_mask_name, **options)
        
        elif preview_type == 'predefined':
            style_name = options.get('style_name', 'classic')
            img = self._generate_predefined_preview(data, version, error_correction, box_size, border, style_name)
        
        elif preview_type == 'logo':
            logo_data = options.get('logo_data')
            if not logo_data:
                raise ValueError("Données du logo manquantes pour la prévisualisation avec logo")
            
            fill_color = options.get('fill_color', "black")
            back_color = options.get('back_color', "white")
            logo_size = options.get('logo_size', 0.2)
            img = self._generate_logo_preview(data, version, error_correction, box_size, border, fill_color, back_color, logo_data, logo_size)
        
        elif preview_type == 'social':
            social_platform = options.get('social_platform')
            if not social_platform:
                raise ValueError("Plateforme sociale manquante pour la prévisualisation avec icône")
            
            fill_color = options.get('fill_color', "black")
            back_color = options.get('back_color', "white")
            img = self._generate_social_preview(data, version, error_correction, box_size, border, fill_color, back_color, social_platform)
        
        else:
            raise ValueError(f"Type de prévisualisation non reconnu: {preview_type}")
        
        # Conversion de l'image en base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    def _generate_basic_preview(self, data, version, error_correction, box_size, border):
        """
        Génère une prévisualisation de QR code basique.
        
        Args:
            data (str): Données à encoder dans le QR code
            version (int): Version du QR code
            error_correction: Niveau de correction d'erreur
            box_size (int): Taille de chaque "boîte" du QR code en pixels
            border (int): Taille de la bordure en nombre de boîtes
            
        Returns:
            PIL.Image: Image QR code générée.
        """
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        return qr.make_image(fill_color="black", back_color="white")
    
    def _generate_custom_preview(self, data, version, error_correction, box_size, border, fill_color, back_color):
        """
        Génère une prévisualisation de QR code personnalisé.
        
        Args:
            data (str): Données à encoder dans le QR code
            version (int): Version du QR code
            error_correction: Niveau de correction d'erreur
            box_size (int): Taille de chaque "boîte" du QR code en pixels
            border (int): Taille de la bordure en nombre de boîtes
            fill_color: Couleur de remplissage des modules
            back_color: Couleur d'arrière-plan
            
        Returns:
            PIL.Image: Image QR code générée.
        """
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        return qr.make_image(fill_color=fill_color, back_color=back_color)
    
    def _generate_styled_preview(self, data, version, error_correction, box_size, border, module_drawer_name, color_mask_name, **options):
        """
        Génère une prévisualisation de QR code stylisé.
        
        Args:
            data (str): Données à encoder dans le QR code
            version (int): Version du QR code
            error_correction: Niveau de correction d'erreur
            box_size (int): Taille de chaque "boîte" du QR code en pixels
            border (int): Taille de la bordure en nombre de boîtes
            module_drawer_name (str): Nom du style de module
            color_mask_name (str): Nom du masque de couleur
            **options: Options supplémentaires pour la personnalisation
            
        Returns:
            PIL.Image: Image QR code générée.
        """
        # Récupération du module drawer
        module_drawer = self.module_drawers.get(module_drawer_name, SquareModuleDrawer())
        
        # Récupération du masque de couleur
        color_mask_class = self.color_masks.get(color_mask_name, SolidFillColorMask)
        
        # Options pour le masque de couleur
        color_mask_kwargs = {}
        if color_mask_name == 'solid':
            color_mask_kwargs = {
                'front_color': options.get('front_color', (0, 0, 0)),
                'back_color': options.get('back_color', (255, 255, 255))
            }
        elif color_mask_name == 'radial_gradient' or color_mask_name == 'square_gradient':
            color_mask_kwargs = {
                'center_color': options.get('front_color', (0, 0, 0)),
                'edge_color': options.get('edge_color', (100, 100, 100)),
                'back_color': options.get('back_color', (255, 255, 255))
            }
            if 'gradient_center' in options:
                color_mask_kwargs['center'] = options.get('gradient_center')
        else:  # horizontal or vertical gradient
            color_mask_kwargs = {
                'top_color': options.get('front_color', (0, 0, 0)),
                'bottom_color': options.get('bottom_color', (100, 100, 100)),
                'back_color': options.get('back_color', (255, 255, 255))
            }
        
        # Création du masque de couleur
        color_mask = color_mask_class(**color_mask_kwargs)
        
        # Génération du QR code
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Création de l'image avec le style personnalisé
        return qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=color_mask
        )
    
    def _generate_predefined_preview(self, data, version, error_correction, box_size, border, style_name):
        """
        Génère une prévisualisation de QR code avec un style prédéfini.
        
        Args:
            data (str): Données à encoder dans le QR code
            version (int): Version du QR code
            error_correction: Niveau de correction d'erreur
            box_size (int): Taille de chaque "boîte" du QR code en pixels
            border (int): Taille de la bordure en nombre de boîtes
            style_name (str): Nom du style prédéfini
            
        Returns:
            PIL.Image: Image QR code générée.
        """
        # Vérification que le style existe
        if style_name not in self.predefined_styles:
            raise ValueError(f"Style '{style_name}' non reconnu. Styles disponibles: {', '.join(self.predefined_styles.keys())}")
        
        # Récupération des options du style prédéfini
        style_options = self.predefined_styles[style_name].copy()
        
        # Ajout des options de base
        style_options['version'] = version
        style_options['error_correction'] = error_correction
        style_options['box_size'] = box_size
        style_options['border'] = border
        
        # Génération de la prévisualisation stylisée
        return self._generate_styled_preview(data, version, error_correction, box_size, border, 
                                            style_options['module_drawer'], 
                                            style_options['color_mask'], 
                                            **style_options)
    
    def _generate_logo_preview(self, data, version, error_correction, box_size, border, fill_color, back_color, logo_data, logo_size):
        """
        Génère une prévisualisation de QR code avec un logo.
        
        Args:
            data (str): Données à encoder dans le QR code
            version (int): Version du QR code
            error_correction: Niveau de correction d'erreur
            box_size (int): Taille de chaque "boîte" du QR code en pixels
            border (int): Taille de la bordure en nombre de boîtes
            fill_color: Couleur de remplissage des modules
            back_color: Couleur d'arrière-plan
            logo_data (str): Données du logo en base64
            logo_size (float): Taille du logo en pourcentage du QR code
            
        Returns:
            PIL.Image: Image QR code générée.
        """
        # Génération du QR code
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Création de l'image QR code
        qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGBA')
        
        try:
            # Décodage du logo en base64
            logo_data = logo_data.split(',')[1] if ',' in logo_data else logo_data
            logo_binary = base64.b64decode(logo_data)
            logo = Image.open(io.BytesIO(logo_binary)).convert('RGBA')
            
            # Calcul de la taille du logo
            qr_width, qr_height = qr_img.size
            logo_max_size = int(min(qr_width, qr_height) * logo_size)
            
            # Redimensionnement du logo tout en conservant le ratio
            logo_width, logo_height = logo.size
            ratio = min(logo_max_size / logo_width, logo_max_size / logo_height)
            new_logo_width = int(logo_width * ratio)
            new_logo_height = int(logo_height * ratio)
            logo = logo.resize((new_logo_width, new_logo_height), Image.LANCZOS)
            
            # Calcul de la position du logo (centre)
            position = ((qr_width - new_logo_width) // 2, (qr_height - new_logo_height) // 2)
            
            # Création d'une nouvelle image pour le résultat final
            result = Image.new('RGBA', (qr_width, qr_height), (0, 0, 0, 0))
            
            # Copie du QR code sur l'image résultat
            result.paste(qr_img, (0, 0))
            
            # Ajout du logo
            result.paste(logo, position, logo)
            
            return result
            
        except Exception as e:
            print(f"Erreur lors de l'ajout du logo: {e}")
            # En cas d'erreur, retourner le QR code sans logo
            return qr_img
    
    def _generate_social_preview(self, data, version, error_correction, box_size, border, fill_color, back_color, social_platform):
        """
        Génère une prévisualisation de QR code avec une icône de réseau social.
        
        Args:
            data (str): Données à encoder dans le QR code
            version (int): Version du QR code
            error_correction: Niveau de correction d'erreur
            box_size (int): Taille de chaque "boîte" du QR code en pixels
            border (int): Taille de la bordure en nombre de boîtes
            fill_color: Couleur de remplissage des modules
            back_color: Couleur d'arrière-plan
            social_platform (str): Nom de la plateforme sociale
            
        Returns:
            PIL.Image: Image QR code générée.
        """
        # Pour la prévisualisation, nous utilisons simplement un QR code personnalisé
        # L'intégration réelle des icônes sociales se fait dans le module social_icons.py
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        return qr.make_image(fill_color=fill_color, back_color=back_color)


# Exemple d'utilisation si exécuté directement
if __name__ == "__main__":
    preview_generator = QRCodePreviewGenerator()
    
    # Exemple de génération de prévisualisation basique
    base64_img = preview_generator.generate_preview_base64(
        "https://www.example.com",
        preview_type='basic'
    )
    print(f"Prévisualisation basique générée: {base64_img[:50]}...")
    
    # Exemple de génération de prévisualisation avec style prédéfini
    base64_img = preview_generator.generate_preview_base64(
        "https://www.example.com",
        preview_type='predefined',
        style_name='ocean'
    )
    print(f"Prévisualisation avec style prédéfini générée: {base64_img[:50]}...")
