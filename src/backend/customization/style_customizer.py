#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module de personnalisation avancée pour les QR codes.
Ce module fournit des fonctionnalités avancées pour personnaliser l'apparence des QR codes.
"""

import os
import uuid
from datetime import datetime
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
from PIL import Image, ImageDraw, ImageChops, ImageFilter


class QRCodeCustomizer:
    """
    Classe pour la personnalisation avancée des QR codes.
    Fournit des méthodes pour personnaliser l'apparence des QR codes avec différents styles.
    """

    def __init__(self, output_dir=None):
        """
        Initialise le personnalisateur de QR codes.
        
        Args:
            output_dir (str, optional): Répertoire de sortie pour les QR codes générés.
                Si non spécifié, utilise le répertoire courant.
        """
        self.output_dir = output_dir or os.path.join(os.getcwd(), 'generated_qrcodes')
        
        # Création du répertoire de sortie s'il n'existe pas
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Dictionnaire des styles de modules disponibles
        self.module_drawers = {
            'square': SquareModuleDrawer(),
            'gapped_square': GappedSquareModuleDrawer(),
            'circle': CircleModuleDrawer(),
            'rounded': RoundedModuleDrawer(),
            'vertical_bars': VerticalBarsDrawer(),
            'horizontal_bars': HorizontalBarsDrawer(),
            'dot': CircleModuleDrawer(radius_ratio=0.6),
            'mini_square': SquareModuleDrawer(module_scale=0.8)
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
                'left_color': (255, 102, 0),
                'right_color': (204, 0, 0),
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
    
    def generate_styled_qrcode(self, data, filename=None, **options):
        """
        Génère un QR code avec un style personnalisé.
        
        Args:
            data (str): Données à encoder dans le QR code (URL, texte, etc.)
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour la personnalisation du QR code.
                - version (int): Version du QR code (1-40)
                - error_correction (int): Niveau de correction d'erreur
                - box_size (int): Taille de chaque "boîte" du QR code en pixels
                - border (int): Taille de la bordure en nombre de boîtes
                - module_drawer (str): Style des modules ('square', 'gapped_square', 'circle', 'rounded', etc.)
                - color_mask (str): Type de masque de couleur ('solid', 'radial_gradient', etc.)
                - front_color (tuple/str): Couleur de premier plan (RGB ou nom)
                - back_color (tuple/str): Couleur d'arrière-plan (RGB ou nom)
                - gradient_center (tuple): Centre du gradient (x, y) entre 0 et 1
                - gradient_direction (tuple): Direction du gradient (x, y)
            
        Returns:
            str: Chemin du fichier QR code généré.
        """
        if not filename:
            filename = f"styled_qrcode_{uuid.uuid4().hex[:8]}.png"
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Paramètres par défaut
        version = options.get('version', 1)
        error_correction = options.get('error_correction', qrcode.constants.ERROR_CORRECT_M)
        box_size = options.get('box_size', 10)
        border = options.get('border', 4)
        
        # Style des modules
        module_drawer_name = options.get('module_drawer', 'square')
        module_drawer = self.module_drawers.get(module_drawer_name, SquareModuleDrawer())
        
        # Masque de couleur
        color_mask_name = options.get('color_mask', 'solid')
        color_mask_class = self.color_masks.get(color_mask_name, SolidFillColorMask)
        
        # Couleurs
        front_color = options.get('front_color', (0, 0, 0))
        back_color = options.get('back_color', (255, 255, 255))
        
        # Options spécifiques aux gradients
        color_mask_kwargs = {}
        if color_mask_name == 'solid':
            color_mask_kwargs = {
                'front_color': front_color,
                'back_color': back_color
            }
        elif color_mask_name == 'radial_gradient' or color_mask_name == 'square_gradient':
            color_mask_kwargs = {
                'center_color': front_color,
                'edge_color': options.get('edge_color', (100, 100, 100)),
                'back_color': back_color
            }
            if 'gradient_center' in options:
                color_mask_kwargs['center'] = options.get('gradient_center', (0.5, 0.5))
        elif color_mask_name == 'horizontal_gradient':
            color_mask_kwargs = {
                'left_color': front_color,
                'right_color': options.get('right_color', (100, 100, 100)),
                'back_color': back_color
            }
        elif color_mask_name == 'vertical_gradient':
            color_mask_kwargs = {
                'top_color': front_color,
                'bottom_color': options.get('bottom_color', (100, 100, 100)),
                'back_color': back_color
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
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=color_mask
        )
        
        # Personnalisation des yeux et des contours si spécifiée
        img_pil = img.get_image()
        if 'frame_shape' in options or 'eye_shape' in options:
            img_pil = self._customize_eyes_and_frames(img_pil, options)
        
        # Sauvegarde de l'image
        img_pil.save(output_path)
        
        # Enregistrement des métadonnées
        self._save_metadata(data, output_path, options)
        
        return output_path
    
    def _customize_eyes_and_frames(self, qr_image, options):
        """
        Personnalise les yeux et les contours du QR code.
        
        Args:
            qr_image: Image PIL du QR code
            options: Options de personnalisation
        
        Returns:
            Image: Image PIL modifiée
        """
        # Copie de l'image pour éviter de modifier l'original
        enhanced_img = qr_image.copy()
        
        # Paramètres
        frame_shape = options.get('frame_shape')
        eye_shape = options.get('eye_shape')
        
        if not frame_shape and not eye_shape:
            return qr_image
        
        # Obtenir les dimensions de l'image
        width, height = qr_image.size
        
        # Estimation de la taille d'un module
        module_size = min(width, height) // 25
        
        # Positions approximatives des trois yeux de détection
        # (haut-gauche, haut-droit, bas-gauche)
        eye_positions = [
            (0, 0),  # Haut-gauche
            (width - 7 * module_size, 0),  # Haut-droit
            (0, height - 7 * module_size)  # Bas-gauche
        ]
        
        # Taille approximative des yeux
        eye_size = 7 * module_size
        
        # On dessine sur l'image
        draw = ImageDraw.Draw(enhanced_img)
        
        # Couleur des yeux (par défaut, noir)
        eye_color = options.get('front_color', (0, 0, 0))
        if isinstance(eye_color, str):
            if eye_color.startswith('#'):
                eye_color = tuple(int(eye_color[i:i+2], 16) for i in (1, 3, 5))
        
        # Personnalisation des yeux
        for x, y in eye_positions:
            if frame_shape:
                # Contour extérieur
                self._draw_custom_eye_frame(draw, x, y, eye_size, frame_shape, eye_color)
            
            if eye_shape:
                # Centre de l'œil
                center_x = x + 2 * module_size
                center_y = y + 2 * module_size
                center_size = 3 * module_size
                self._draw_custom_eye_center(draw, center_x, center_y, center_size, eye_shape, eye_color)
        
        return enhanced_img
    
    def _draw_custom_eye_frame(self, draw, x, y, size, shape, color):
        """
        Dessine un contour personnalisé pour l'œil du QR code.
        
        Args:
            draw: Objet ImageDraw
            x, y: Coordonnées du coin supérieur gauche
            size: Taille du contour
            shape: Forme du contour
            color: Couleur du contour
        """
        if shape == 'circle':
            # Cercle complet
            draw.ellipse([(x, y), (x + size, y + size)], fill=color)
            # Cercle intérieur (vide)
            inner_size = size * 5/7
            inner_x = x + (size - inner_size) / 2
            inner_y = y + (size - inner_size) / 2
            draw.ellipse([(inner_x, inner_y), (inner_x + inner_size, inner_y + inner_size)], fill='white')
            
        elif shape == 'rounded_square':
            # Carré arrondi
            radius = size / 5
            # Dessiner un rectangle
            draw.rectangle([(x, y + radius), (x + size, y + size - radius)], fill=color)
            draw.rectangle([(x + radius, y), (x + size - radius, y + size)], fill=color)
            # Ajouter les coins arrondis
            draw.pieslice([(x, y), (x + radius * 2, y + radius * 2)], 180, 270, fill=color)
            draw.pieslice([(x + size - radius * 2, y), (x + size, y + radius * 2)], 270, 0, fill=color)
            draw.pieslice([(x, y + size - radius * 2), (x + radius * 2, y + size)], 90, 180, fill=color)
            draw.pieslice([(x + size - radius * 2, y + size - radius * 2), (x + size, y + size)], 0, 90, fill=color)
            # Carré intérieur (vide)
            inner_size = size * 5/7
            inner_x = x + (size - inner_size) / 2
            inner_y = y + (size - inner_size) / 2
            inner_radius = inner_size / 5
            # Dessiner un rectangle intérieur blanc
            draw.rectangle([(inner_x, inner_y + inner_radius), (inner_x + inner_size, inner_y + inner_size - inner_radius)], fill='white')
            draw.rectangle([(inner_x + inner_radius, inner_y), (inner_x + inner_size - inner_radius, inner_y + inner_size)], fill='white')
            # Ajouter les coins arrondis intérieurs
            draw.pieslice([(inner_x, inner_y), (inner_x + inner_radius * 2, inner_y + inner_radius * 2)], 180, 270, fill='white')
            draw.pieslice([(inner_x + inner_size - inner_radius * 2, inner_y), (inner_x + inner_size, inner_y + inner_radius * 2)], 270, 0, fill='white')
            draw.pieslice([(inner_x, inner_y + inner_size - inner_radius * 2), (inner_x + inner_radius * 2, inner_y + inner_size)], 90, 180, fill='white')
            draw.pieslice([(inner_x + inner_size - inner_radius * 2, inner_y + inner_size - inner_radius * 2), (inner_x + inner_size, inner_y + inner_size)], 0, 90, fill='white')
            
        elif shape == 'diamond':
            # Contour en losange
            points = [
                (x + size // 2, y),  # haut
                (x + size, y + size // 2),  # droite
                (x + size // 2, y + size),  # bas
                (x, y + size // 2)  # gauche
            ]
            draw.polygon(points, fill=color)
            # Losange intérieur (vide)
            inner_size = size * 5/7
            inner_offset = (size - inner_size) / 2
            inner_points = [
                (x + size // 2, y + inner_offset),  # haut
                (x + size - inner_offset, y + size // 2),  # droite
                (x + size // 2, y + size - inner_offset),  # bas
                (x + inner_offset, y + size // 2)  # gauche
            ]
            draw.polygon(inner_points, fill='white')
            
        elif shape == 'rounded':
            # Carré fortement arrondi
            radius = size / 3
            # Dessiner un rectangle
            draw.rectangle([(x, y + radius), (x + size, y + size - radius)], fill=color)
            draw.rectangle([(x + radius, y), (x + size - radius, y + size)], fill=color)
            # Ajouter les coins arrondis
            draw.pieslice([(x, y), (x + radius * 2, y + radius * 2)], 180, 270, fill=color)
            draw.pieslice([(x + size - radius * 2, y), (x + size, y + radius * 2)], 270, 0, fill=color)
            draw.pieslice([(x, y + size - radius * 2), (x + radius * 2, y + size)], 90, 180, fill=color)
            draw.pieslice([(x + size - radius * 2, y + size - radius * 2), (x + size, y + size)], 0, 90, fill=color)
            # Carré intérieur (vide)
            inner_size = size * 5/7
            inner_x = x + (size - inner_size) / 2
            inner_y = y + (size - inner_size) / 2
            inner_radius = inner_size / 3
            # Dessiner un rectangle intérieur blanc
            draw.rectangle([(inner_x, inner_y + inner_radius), (inner_x + inner_size, inner_y + inner_size - inner_radius)], fill='white')
            draw.rectangle([(inner_x + inner_radius, inner_y), (inner_x + inner_size - inner_radius, inner_y + inner_size)], fill='white')
            # Ajouter les coins arrondis intérieurs
            draw.pieslice([(inner_x, inner_y), (inner_x + inner_radius * 2, inner_y + inner_radius * 2)], 180, 270, fill='white')
            draw.pieslice([(inner_x + inner_size - inner_radius * 2, inner_y), (inner_x + inner_size, inner_y + inner_radius * 2)], 270, 0, fill='white')
            draw.pieslice([(inner_x, inner_y + inner_size - inner_radius * 2), (inner_x + inner_radius * 2, inner_y + inner_size)], 90, 180, fill='white')
            draw.pieslice([(inner_x + inner_size - inner_radius * 2, inner_y + inner_size - inner_radius * 2), (inner_x + inner_size, inner_y + inner_size)], 0, 90, fill='white')
            
        else:  # Default: square
            # Carré simple
            draw.rectangle([(x, y), (x + size, y + size)], fill=color)
            # Carré intérieur (vide)
            inner_size = size * 5/7
            inner_x = x + (size - inner_size) / 2
            inner_y = y + (size - inner_size) / 2
            draw.rectangle([(inner_x, inner_y), (inner_x + inner_size, inner_y + inner_size)], fill='white')
    
    def _draw_custom_eye_center(self, draw, x, y, size, shape, color):
        """
        Dessine un centre personnalisé pour l'œil du QR code.
        
        Args:
            draw: Objet ImageDraw
            x, y: Coordonnées du coin supérieur gauche
            size: Taille du centre
            shape: Forme du centre
            color: Couleur du centre
        """
        if shape == 'circle':
            draw.ellipse([(x, y), (x + size, y + size)], fill=color)
            
        elif shape == 'diamond':
            points = [
                (x + size // 2, y),  # haut
                (x + size, y + size // 2),  # droite
                (x + size // 2, y + size),  # bas
                (x, y + size // 2)  # gauche
            ]
            draw.polygon(points, fill=color)
            
        elif shape == 'rounded':
            radius = size / 4
            # Dessiner un rectangle
            draw.rectangle([(x, y + radius), (x + size, y + size - radius)], fill=color)
            draw.rectangle([(x + radius, y), (x + size - radius, y + size)], fill=color)
            # Ajouter les coins arrondis
            draw.pieslice([(x, y), (x + radius * 2, y + radius * 2)], 180, 270, fill=color)
            draw.pieslice([(x + size - radius * 2, y), (x + size, y + radius * 2)], 270, 0, fill=color)
            draw.pieslice([(x, y + size - radius * 2), (x + radius * 2, y + size)], 90, 180, fill=color)
            draw.pieslice([(x + size - radius * 2, y + size - radius * 2), (x + size, y + size)], 0, 90, fill=color)
            
        elif shape == 'cushion':
            # Forme de coussin (carré aux coins arrondis convexes)
            draw.rectangle([(x, y), (x + size, y + size)], fill=color)
            radius = size / 3
            # Créer un effet de "coussin" en arrondissant les coins
            draw.pieslice([(x - radius, y - radius), (x + radius, y + radius)], 0, 90, fill='white')
            draw.pieslice([(x + size - radius, y - radius), (x + size + radius, y + radius)], 90, 180, fill='white')
            draw.pieslice([(x - radius, y + size - radius), (x + radius, y + size + radius)], 270, 360, fill='white')
            draw.pieslice([(x + size - radius, y + size - radius), (x + size + radius, y + size + radius)], 180, 270, fill='white')
            
        elif shape == 'star':
            # Étoile à 4 branches
            # Centre de l'étoile
            center_x = x + size // 2
            center_y = y + size // 2
            # Points de l'étoile
            points = []
            for i in range(8):
                angle = i * 45  # 45 degrés entre chaque point
                radius = size // 2 if i % 2 == 0 else size // 4
                px = center_x + int(radius * (i % 2 == 0))  # points externes
                py = center_y + int(radius * (i % 2 == 1))  # points internes
                if i % 4 == 0:  # haut
                    px = center_x
                    py = center_y - radius
                elif i % 4 == 1:  # diagonale
                    px = center_x + radius // 2
                    py = center_y - radius // 2
                elif i % 4 == 2:  # droite
                    px = center_x + radius
                    py = center_y
                elif i % 4 == 3:  # diagonale
                    px = center_x + radius // 2
                    py = center_y + radius // 2
                points.append((px, py))
            draw.polygon(points, fill=color)
            
        elif shape == 'flower':
            # Centre de la fleur
            center_x = x + size // 2
            center_y = y + size // 2
            radius = size // 2
            # Dessiner le centre
            draw.ellipse([(center_x - radius//2, center_y - radius//2), 
                           (center_x + radius//2, center_y + radius//2)], fill=color)
            # Dessiner les pétales
            petal_radius = radius // 2
            positions = [
                (center_x, center_y - radius),  # haut
                (center_x + radius, center_y),  # droite
                (center_x, center_y + radius),  # bas
                (center_x - radius, center_y)   # gauche
            ]
            for px, py in positions:
                draw.ellipse([(px - petal_radius, py - petal_radius), 
                               (px + petal_radius, py + petal_radius)], fill=color)
            
        else:  # Default: square
            draw.rectangle([(x, y), (x + size, y + size)], fill=color)
    
    def generate_custom_shape_qrcode(self, data, module_shape, frame_shape, eye_shape, filename=None, **options):
        """
        Génère un QR code avec des formes personnalisées pour les modules, les contours et les yeux.
        
        Args:
            data (str): Données à encoder dans le QR code
            module_shape (str): Style des modules ('square', 'circle', 'rounded', etc.)
            frame_shape (str): Style des contours des marqueurs ('square', 'rounded_square', 'circle', etc.)
            eye_shape (str): Style du centre des marqueurs ('square', 'circle', 'rounded', etc.)
            filename (str, optional): Nom du fichier de sortie
            **options: Options supplémentaires
        
        Returns:
            str: Chemin du fichier QR code généré
        """
        if not filename:
            filename = f"custom_shape_qrcode_{uuid.uuid4().hex[:8]}.png"
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Paramètres par défaut
        version = options.get('version', 1)
        error_correction = options.get('error_correction', qrcode.constants.ERROR_CORRECT_M)
        box_size = options.get('box_size', 10)
        border = options.get('border', 4)
        
        # Couleurs
        fill_color = options.get('fill_color', "black")
        back_color = options.get('back_color', "white")
        
        # Sélection du module drawer en fonction du module_shape
        module_drawer = self.module_drawers.get(module_shape, SquareModuleDrawer())
        
        # Génération du QR code
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Création de l'image avec le style de module personnalisé
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=SolidFillColorMask(front_color=fill_color, back_color=back_color)
        )
        
        # Conversion en mode PIL Image pour traitement avancé
        pil_img = img.get_image()
        
        # Application des formes personnalisées pour les marqueurs d'alignement (yeux)
        if frame_shape != 'square' or eye_shape != 'square':
            # Options pour la personnalisation des yeux et contours
            eye_options = {
                'frame_shape': frame_shape,
                'eye_shape': eye_shape,
                'front_color': fill_color
            }
            pil_img = self._customize_eyes_and_frames(pil_img, eye_options)
        
        # Sauvegarde de l'image finale
        pil_img.save(output_path)
        
        # Enregistrement des métadonnées
        options['module_shape'] = module_shape
        options['frame_shape'] = frame_shape
        options['eye_shape'] = eye_shape
        self._save_metadata(data, output_path, options)
        
        return output_path
    
    def _get_eye_positions(self, qr, box_size, border):
        """
        Récupère les positions des yeux du QR code.
        
        Args:
            qr: QR code généré
            box_size: Taille des modules
            border: Taille de la bordure
        
        Returns:
            list: Liste des positions des yeux et leurs tailles
        """
        # Positions standard des yeux dans un QR code: haut gauche, haut droit, bas gauche
        # Tailles approximatives des yeux (7x7 modules)
        eye_size = 7 * box_size
        
        # Position des yeux en tenant compte de la bordure
        top_left = (border * box_size, border * box_size)
        top_right = (border * box_size + (qr.modules_count - 7) * box_size, border * box_size)
        bottom_left = (border * box_size, border * box_size + (qr.modules_count - 7) * box_size)
        
        return [
            (top_left, eye_size),
            (top_right, eye_size),
            (bottom_left, eye_size)
        ]
    
    def apply_predefined_style(self, data, style_name, filename=None, **custom_options):
        """
        Applique un style prédéfini au QR code.
        
        Args:
            data (str): Données à encoder dans le QR code (URL, texte, etc.)
            style_name (str): Nom du style prédéfini à appliquer
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **custom_options: Options personnalisées qui remplaceront celles du style prédéfini
            
        Returns:
            str: Chemin du fichier QR code généré.
        """
        # Vérification que le style existe
        if style_name not in self.predefined_styles:
            raise ValueError(f"Style '{style_name}' non reconnu. Styles disponibles: {', '.join(self.predefined_styles.keys())}")
        
        # Récupération des options du style prédéfini
        style_options = self.predefined_styles[style_name].copy()
        
        # Fusion avec les options personnalisées
        style_options.update(custom_options)
        
        # Génération du QR code avec le style
        if not filename:
            filename = f"{style_name}_qrcode_{uuid.uuid4().hex[:8]}.png"
        
        return self.generate_styled_qrcode(data, filename, **style_options)
    
    def _save_metadata(self, data, output_path, options=None):
        """
        Enregistre les métadonnées du QR code généré.
        
        Args:
            data (str): Données encodées dans le QR code
            output_path (str): Chemin du fichier QR code généré
            options (dict, optional): Options utilisées pour la génération
        """
        metadata_dir = os.path.join(self.output_dir, 'metadata')
        if not os.path.exists(metadata_dir):
            os.makedirs(metadata_dir)
        
        # Nom du fichier de métadonnées basé sur le nom du QR code
        qr_filename = os.path.basename(output_path)
        metadata_filename = f"{os.path.splitext(qr_filename)[0]}.txt"
        metadata_path = os.path.join(metadata_dir, metadata_filename)
        
        # Création du contenu des métadonnées
        metadata_content = [
            f"Date de création: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Données: {data}",
            f"Fichier: {qr_filename}",
        ]
        
        # Ajout des options si spécifiées
        if options:
            metadata_content.append("Options:")
            for key, value in options.items():
                metadata_content.append(f"  {key}: {value}")
        
        # Écriture des métadonnées dans le fichier
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(metadata_content))


# Exemple d'utilisation si exécuté directement
if __name__ == "__main__":
    customizer = QRCodeCustomizer()
    
    # Exemple 1: QR code avec style personnalisé
    styled_qr = customizer.generate_styled_qrcode(
        "https://www.example.com",
        "example_styled.png",
        module_drawer="circle",
        color_mask="radial_gradient",
        front_color=(0, 102, 204),
        edge_color=(0, 51, 153),
        gradient_center=(0.5, 0.5)
    )
    print(f"QR code stylisé généré: {styled_qr}")
    
    # Exemple 2: QR code avec style prédéfini
    predefined_qr = customizer.apply_predefined_style(
        "https://www.example.com",
        "ocean",
        "example_ocean.png"
    )
    print(f"QR code avec style prédéfini généré: {predefined_qr}")
