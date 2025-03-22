#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module de personnalisation avancée pour les QR codes.
Ce module fournit des styles, formes et templates avancés pour 
personnaliser l'apparence des QR codes, similaire à QR Code Monkey.
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
from PIL import Image, ImageDraw, ImageColor, ImageFont, ImageFilter, ImageOps, ImageChops


class AdvancedQRStyleGenerator:
    """
    Générateur de styles avancés pour QR codes.
    Fournit des méthodes pour personnaliser l'apparence des QR codes avec des styles
    similaires à QR Code Monkey.
    """

    def __init__(self, output_dir=None, templates_dir=None):
        """
        Initialise le générateur de styles de QR codes.
        
        Args:
            output_dir (str, optional): Répertoire de sortie pour les QR codes générés.
                Si non spécifié, utilise le répertoire courant.
            templates_dir (str, optional): Répertoire contenant les templates de styles.
                Si non spécifié, utilise le sous-répertoire 'styles' du répertoire courant.
        """
        # Répertoire de sortie par défaut
        self.output_dir = output_dir or os.path.join(os.getcwd(), 'generated_qrcodes')
        
        # Répertoire des templates par défaut
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.templates_dir = templates_dir or os.path.join(current_dir, '..', '..', 'frontend', 'static', 'img', 'styles')
        
        # Création des répertoires s'ils n'existent pas
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Initialisation des dictionnaires de styles
        self._init_module_drawers()
        self._init_color_masks()
        self._init_eye_shapes()
        self._init_frame_shapes()
        self._init_predefined_styles()
    
    def _init_module_drawers(self):
        """
        Initialise le dictionnaire des styles de modules disponibles.
        """
        self.module_drawers = {
            'square': {
                'name': 'Carré',
                'description': 'Modules carrés classiques',
                'drawer': SquareModuleDrawer(),
                'preview': os.path.join(self.templates_dir, 'module_shapes', 'square.png')
            },
            'rounded_square': {
                'name': 'Carré arrondi',
                'description': 'Modules carrés aux coins arrondis',
                'drawer': RoundedModuleDrawer(),
                'preview': os.path.join(self.templates_dir, 'module_shapes', 'rounded_square.png')
            },
            'circle': {
                'name': 'Cercle',
                'description': 'Modules en forme de cercles',
                'drawer': CircleModuleDrawer(),
                'preview': os.path.join(self.templates_dir, 'module_shapes', 'circle.png')
            },
            'dot': {
                'name': 'Point',
                'description': 'Modules en forme de petits points',
                'drawer': CircleModuleDrawer(radius_ratio=0.6),
                'preview': os.path.join(self.templates_dir, 'module_shapes', 'dot.png')
            },
            'vertical_bars': {
                'name': 'Barres verticales',
                'description': 'Modules en forme de barres verticales',
                'drawer': VerticalBarsDrawer(),
                'preview': os.path.join(self.templates_dir, 'module_shapes', 'vertical_bars.png')
            },
            'horizontal_bars': {
                'name': 'Barres horizontales',
                'description': 'Modules en forme de barres horizontales',
                'drawer': HorizontalBarsDrawer(),
                'preview': os.path.join(self.templates_dir, 'module_shapes', 'horizontal_bars.png')
            },
            'gapped_square': {
                'name': 'Carré espacé',
                'description': 'Modules carrés avec espacement',
                'drawer': GappedSquareDrawer(gap_width=0.15),
                'preview': os.path.join(self.templates_dir, 'module_shapes', 'gapped_square.png')
            },
            'mini_square': {
                'name': 'Mini carré',
                'description': 'Modules carrés de taille réduite',
                'drawer': SquareModuleDrawer(module_scale=0.8),
                'preview': os.path.join(self.templates_dir, 'module_shapes', 'mini_square.png')
            },
            'rounded_vertical_bars': {
                'name': 'Barres verticales arrondies',
                'description': 'Modules en forme de barres verticales aux extrémités arrondies',
                'drawer': RoundedVerticalBarsDrawer(),
                'preview': os.path.join(self.templates_dir, 'module_shapes', 'rounded_vertical_bars.png')
            },
            'rounded_horizontal_bars': {
                'name': 'Barres horizontales arrondies',
                'description': 'Modules en forme de barres horizontales aux extrémités arrondies',
                'drawer': RoundedHorizontalBarsDrawer(),
                'preview': os.path.join(self.templates_dir, 'module_shapes', 'rounded_horizontal_bars.png')
            },
            'diamond': {
                'name': 'Losange',
                'description': 'Modules en forme de losange',
                'drawer': DiamondModuleDrawer(),
                'preview': os.path.join(self.templates_dir, 'module_shapes', 'diamond.png')
            },
            'pixel': {
                'name': 'Pixel',
                'description': 'Style pixelisé',
                'drawer': PixelModuleDrawer(),
                'preview': os.path.join(self.templates_dir, 'module_shapes', 'pixel.png')
            }
        }
        
        # Création des prévisualisations manquantes
        for style_id, style_info in self.module_drawers.items():
            if not os.path.exists(style_info['preview']):
                os.makedirs(os.path.dirname(style_info['preview']), exist_ok=True)
                self._generate_module_preview(style_id)
    
    def _init_color_masks(self):
        """
        Initialise le dictionnaire des masques de couleur disponibles.
        """
        self.color_masks = {
            'solid': {
                'name': 'Couleur unie',
                'description': 'Couleur de remplissage unique',
                'class': SolidFillColorMask,
                'preview': os.path.join(self.templates_dir, 'color_masks', 'solid.png')
            },
            'radial_gradient': {
                'name': 'Dégradé radial',
                'description': 'Dégradé circulaire du centre vers l\'extérieur',
                'class': RadialGradiantColorMask,
                'preview': os.path.join(self.templates_dir, 'color_masks', 'radial_gradient.png')
            },
            'square_gradient': {
                'name': 'Dégradé carré',
                'description': 'Dégradé carré du centre vers l\'extérieur',
                'class': SquareGradiantColorMask,
                'preview': os.path.join(self.templates_dir, 'color_masks', 'square_gradient.png')
            },
            'horizontal_gradient': {
                'name': 'Dégradé horizontal',
                'description': 'Dégradé de gauche à droite',
                'class': HorizontalGradiantColorMask,
                'preview': os.path.join(self.templates_dir, 'color_masks', 'horizontal_gradient.png')
            },
            'vertical_gradient': {
                'name': 'Dégradé vertical',
                'description': 'Dégradé de haut en bas',
                'class': VerticalGradiantColorMask,
                'preview': os.path.join(self.templates_dir, 'color_masks', 'vertical_gradient.png')
            },
            'diagonal_gradient': {
                'name': 'Dégradé diagonal',
                'description': 'Dégradé du coin supérieur gauche au coin inférieur droit',
                'class': DiagonalGradiantColorMask,
                'preview': os.path.join(self.templates_dir, 'color_masks', 'diagonal_gradient.png')
            },
            'rainbow': {
                'name': 'Arc-en-ciel',
                'description': 'Dégradé multicolore',
                'class': RainbowColorMask,
                'preview': os.path.join(self.templates_dir, 'color_masks', 'rainbow.png')
            }
        }
        
        # Création des prévisualisations manquantes
        for mask_id, mask_info in self.color_masks.items():
            if not os.path.exists(mask_info['preview']):
                os.makedirs(os.path.dirname(mask_info['preview']), exist_ok=True)
                self._generate_color_mask_preview(mask_id)
    
    def _init_eye_shapes(self):
        """
        Initialise le dictionnaire des formes d'yeux disponibles.
        """
        self.eye_shapes = {
            'square': {
                'name': 'Carré',
                'description': 'Yeux carrés classiques',
                'preview': os.path.join(self.templates_dir, 'eye_shapes', 'square.png')
            },
            'circle': {
                'name': 'Cercle',
                'description': 'Yeux en forme de cercles',
                'preview': os.path.join(self.templates_dir, 'eye_shapes', 'circle.png')
            },
            'rounded': {
                'name': 'Arrondi',
                'description': 'Yeux arrondis',
                'preview': os.path.join(self.templates_dir, 'eye_shapes', 'rounded.png')
            },
            'diamond': {
                'name': 'Losange',
                'description': 'Yeux en forme de losange',
                'preview': os.path.join(self.templates_dir, 'eye_shapes', 'diamond.png')
            },
            'cushion': {
                'name': 'Coussin',
                'description': 'Yeux en forme de coussin',
                'preview': os.path.join(self.templates_dir, 'eye_shapes', 'cushion.png')
            },
            'star': {
                'name': 'Étoile',
                'description': 'Yeux en forme d\'étoile',
                'preview': os.path.join(self.templates_dir, 'eye_shapes', 'star.png')
            },
            'dots': {
                'name': 'Points',
                'description': 'Yeux composés de points',
                'preview': os.path.join(self.templates_dir, 'eye_shapes', 'dots.png')
            },
            'rounded_rect': {
                'name': 'Rectangle arrondi',
                'description': 'Yeux en forme de rectangle aux coins arrondis',
                'preview': os.path.join(self.templates_dir, 'eye_shapes', 'rounded_rect.png')
            },
            'flower': {
                'name': 'Fleur',
                'description': 'Yeux en forme de fleur',
                'preview': os.path.join(self.templates_dir, 'eye_shapes', 'flower.png')
            },
            'leaf': {
                'name': 'Feuille',
                'description': 'Yeux en forme de feuille',
                'preview': os.path.join(self.templates_dir, 'eye_shapes', 'leaf.png')
            }
        }
        
        # Création des prévisualisations manquantes
        for shape_id, shape_info in self.eye_shapes.items():
            if not os.path.exists(shape_info['preview']):
                os.makedirs(os.path.dirname(shape_info['preview']), exist_ok=True)
                self._generate_eye_preview(shape_id)
    
    def _init_frame_shapes(self):
        """
        Initialise le dictionnaire des formes de contour des marqueurs disponibles.
        """
        self.frame_shapes = {
            'square': {
                'name': 'Carré',
                'description': 'Contour carré classique',
                'preview': os.path.join(self.templates_dir, 'frame_shapes', 'square.png')
            },
            'rounded_square': {
                'name': 'Carré arrondi',
                'description': 'Contour carré aux coins légèrement arrondis',
                'preview': os.path.join(self.templates_dir, 'frame_shapes', 'rounded_square.png')
            },
            'circle': {
                'name': 'Cercle',
                'description': 'Contour circulaire',
                'preview': os.path.join(self.templates_dir, 'frame_shapes', 'circle.png')
            },
            'rounded': {
                'name': 'Arrondi',
                'description': 'Contour fortement arrondi',
                'preview': os.path.join(self.templates_dir, 'frame_shapes', 'rounded.png')
            },
            'diamond': {
                'name': 'Losange',
                'description': 'Contour en forme de losange',
                'preview': os.path.join(self.templates_dir, 'frame_shapes', 'diamond.png')
            },
            'corner_cut': {
                'name': 'Coins coupés',
                'description': 'Contour aux coins coupés',
                'preview': os.path.join(self.templates_dir, 'frame_shapes', 'corner_cut.png')
            },
            'jagged': {
                'name': 'Dentelé',
                'description': 'Contour aux bords dentelés',
                'preview': os.path.join(self.templates_dir, 'frame_shapes', 'jagged.png')
            },
            'dots': {
                'name': 'Points',
                'description': 'Contour composé de points',
                'preview': os.path.join(self.templates_dir, 'frame_shapes', 'dots.png')
            },
            'pointed': {
                'name': 'Pointu',
                'description': 'Contour aux coins pointus',
                'preview': os.path.join(self.templates_dir, 'frame_shapes', 'pointed.png')
            },
            'pixel': {
                'name': 'Pixel',
                'description': 'Contour pixelisé',
                'preview': os.path.join(self.templates_dir, 'frame_shapes', 'pixel.png')
            }
        }
        
        # Création des prévisualisations manquantes
        for shape_id, shape_info in self.frame_shapes.items():
            if not os.path.exists(shape_info['preview']):
                os.makedirs(os.path.dirname(shape_info['preview']), exist_ok=True)
                self._generate_frame_preview(shape_id)
    
    def _init_predefined_styles(self):
        """
        Initialise le dictionnaire des styles prédéfinis.
        """
        self.predefined_styles = {
            'classic': {
                'name': 'Classique',
                'description': 'Style noir et blanc classique',
                'module_drawer': 'square',
                'color_mask': 'solid',
                'front_color': (0, 0, 0),
                'back_color': (255, 255, 255),
                'eye_shape': 'square',
                'frame_shape': 'square',
                'preview': os.path.join(self.templates_dir, 'classic.png')
            },
            'rounded': {
                'name': 'Arrondi',
                'description': 'Style avec coins arrondis',
                'module_drawer': 'rounded_square',
                'color_mask': 'solid',
                'front_color': (0, 0, 0),
                'back_color': (255, 255, 255),
                'eye_shape': 'rounded',
                'frame_shape': 'rounded_square',
                'preview': os.path.join(self.templates_dir, 'rounded.png')
            },
            'dots': {
                'name': 'Points',
                'description': 'Style avec modules en points',
                'module_drawer': 'circle',
                'color_mask': 'solid',
                'front_color': (0, 0, 0),
                'back_color': (255, 255, 255),
                'eye_shape': 'circle',
                'frame_shape': 'circle',
                'preview': os.path.join(self.templates_dir, 'dots.png')
            },
            'modern_blue': {
                'name': 'Bleu Moderne',
                'description': 'Style moderne avec dégradé bleu',
                'module_drawer': 'rounded_square',
                'color_mask': 'vertical_gradient',
                'front_color': (0, 102, 204),
                'edge_color': (0, 51, 153),
                'back_color': (255, 255, 255),
                'eye_shape': 'rounded',
                'frame_shape': 'rounded_square',
                'preview': os.path.join(self.templates_dir, 'modern_blue.png')
            },
            'sunset': {
                'name': 'Coucher de Soleil',
                'description': 'Style avec dégradé orange-rouge',
                'module_drawer': 'circle',
                'color_mask': 'horizontal_gradient',
                'front_color': (255, 102, 0),
                'edge_color': (204, 0, 0),
                'back_color': (255, 255, 255),
                'eye_shape': 'circle',
                'frame_shape': 'circle',
                'preview': os.path.join(self.templates_dir, 'sunset.png')
            },
            'forest': {
                'name': 'Forêt',
                'description': 'Style avec dégradé vert',
                'module_drawer': 'square',
                'color_mask': 'radial_gradient',
                'front_color': (0, 102, 0),
                'edge_color': (0, 51, 0),
                'back_color': (255, 255, 255),
                'eye_shape': 'square',
                'frame_shape': 'square',
                'preview': os.path.join(self.templates_dir, 'forest.png')
            },
            'ocean': {
                'name': 'Océan',
                'description': 'Style avec dégradé bleu océan',
                'module_drawer': 'rounded_square',
                'color_mask': 'radial_gradient',
                'front_color': (0, 153, 204),
                'edge_color': (0, 51, 102),
                'gradient_center': (0.5, 0.5),
                'back_color': (255, 255, 255),
                'eye_shape': 'rounded',
                'frame_shape': 'rounded_square',
                'preview': os.path.join(self.templates_dir, 'ocean.png')
            },
            'barcode': {
                'name': 'Code-barres',
                'description': 'Style similaire aux codes-barres',
                'module_drawer': 'vertical_bars',
                'color_mask': 'solid',
                'front_color': (0, 0, 0),
                'back_color': (255, 255, 255),
                'eye_shape': 'square',
                'frame_shape': 'square',
                'preview': os.path.join(self.templates_dir, 'barcode.png')
            },
            'elegant': {
                'name': 'Élégant',
                'description': 'Style minimaliste élégant',
                'module_drawer': 'gapped_square',
                'color_mask': 'solid',
                'front_color': (51, 51, 51),
                'back_color': (245, 245, 245),
                'eye_shape': 'square',
                'frame_shape': 'square',
                'preview': os.path.join(self.templates_dir, 'elegant.png')
            },
            'colorful': {
                'name': 'Coloré',
                'description': 'Style multicolore vif',
                'module_drawer': 'circle',
                'color_mask': 'rainbow',
                'back_color': (255, 255, 255),
                'eye_shape': 'circle',
                'frame_shape': 'circle',
                'preview': os.path.join(self.templates_dir, 'colorful.png')
            },
            'night': {
                'name': 'Nuit',
                'description': 'Style sombre avec dégradé bleu nuit',
                'module_drawer': 'square',
                'color_mask': 'radial_gradient',
                'front_color': (30, 30, 70),
                'edge_color': (5, 5, 20),
                'back_color': (0, 0, 0),
                'eye_shape': 'square',
                'frame_shape': 'square',
                'preview': os.path.join(self.templates_dir, 'night.png')
            },
            'tech': {
                'name': 'Technologie',
                'description': 'Style futuriste avec dégradé cyan',
                'module_drawer': 'gapped_square',
                'color_mask': 'diagonal_gradient',
                'front_color': (0, 255, 255),
                'edge_color': (0, 150, 200),
                'back_color': (0, 0, 30),
                'eye_shape': 'diamond',
                'frame_shape': 'corner_cut',
                'preview': os.path.join(self.templates_dir, 'tech.png')
            },
            'urban': {
                'name': 'Urbain',
                'description': 'Style urbain avec dégradé gris',
                'module_drawer': 'square',
                'color_mask': 'vertical_gradient',
                'front_color': (150, 150, 150),
                'edge_color': (30, 30, 30),
                'back_color': (255, 255, 255),
                'eye_shape': 'square',
                'frame_shape': 'pixel',
                'preview': os.path.join(self.templates_dir, 'urban.png')
            },
            'vintage': {
                'name': 'Vintage',
                'description': 'Style vintage avec teintes sépia',
                'module_drawer': 'rounded_square',
                'color_mask': 'solid',
                'front_color': (112, 66, 20),
                'back_color': (255, 242, 212),
                'eye_shape': 'rounded',
                'frame_shape': 'rounded_square',
                'preview': os.path.join(self.templates_dir, 'vintage.png')
            }
        }
        
        # Création des prévisualisations manquantes
        for style_id, style_info in self.predefined_styles.items():
            if not os.path.exists(style_info['preview']):
                os.makedirs(os.path.dirname(style_info['preview']), exist_ok=True)
                self._generate_style_preview(style_id)
    
    def _generate_module_preview(self, module_style_id):
        """
        Génère une prévisualisation pour un style de module.
        
        Args:
            module_style_id (str): Identifiant du style de module
        """
        if module_style_id not in self.module_drawers:
            return
        
        # Récupération du drawer
        drawer_info = self.module_drawers[module_style_id]
        drawer = drawer_info['drawer']
        
        # Génération d'un QR code simple
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data("PREVIEW")
        qr.make(fit=True)
        
        # Création de l'image avec le style spécifié
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=drawer,
            color_mask=SolidFillColorMask(front_color=(0, 0, 0), back_color=(255, 255, 255))
        )
        
        # Redimensionnement pour la prévisualisation
        img = img.resize((100, 100), Image.LANCZOS)
        
        # Sauvegarde de l'image
        img.save(drawer_info['preview'])
    
    def _generate_color_mask_preview(self, mask_id):
        """
        Génère une prévisualisation pour un masque de couleur.
        
        Args:
            mask_id (str): Identifiant du masque de couleur
        """
        if mask_id not in self.color_masks:
            return
        
        # Récupération du masque
        mask_info = self.color_masks[mask_id]
        mask_class = mask_info['class']
        
        # Configuration des couleurs pour la prévisualisation
        if mask_id == 'solid':
            mask = mask_class(front_color=(0, 0, 0), back_color=(255, 255, 255))
        elif mask_id == 'rainbow':
            mask = mask_class(back_color=(255, 255, 255))
        elif mask_id in ['radial_gradient', 'square_gradient', 'diagonal_gradient']:
            mask = mask_class(center_color=(0, 102, 204), edge_color=(0, 51, 153), back_color=(255, 255, 255))
        elif mask_id == 'horizontal_gradient':
            mask = mask_class(left_color=(255, 102, 0), right_color=(204, 0, 0), back_color=(255, 255, 255))
        elif mask_id == 'vertical_gradient':
            mask = mask_class(top_color=(0, 153, 0), bottom_color=(0, 51, 0), back_color=(255, 255, 255))
        else:
            # Masque par défaut
            mask = SolidFillColorMask(front_color=(0, 0, 0), back_color=(255, 255, 255))
        
        # Génération d'un QR code simple
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data("PREVIEW")
        qr.make(fit=True)
        
        # Création de l'image avec le masque spécifié
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=SquareModuleDrawer(),
            color_mask=mask
        )
        
        # Redimensionnement pour la prévisualisation
        img = img.resize((100, 100), Image.LANCZOS)
        
        # Sauvegarde de l'image
        img.save(mask_info['preview'])
    
    def _generate_eye_preview(self, eye_shape_id):
        """
        Génère une prévisualisation pour une forme d'œil.
        
        Args:
            eye_shape_id (str): Identifiant de la forme d'œil
        """
        if eye_shape_id not in self.eye_shapes:
            return
        
        # Récupération des informations de la forme
        shape_info = self.eye_shapes[eye_shape_id]
        
        # Création d'une image vide
        img = Image.new('RGB', (100, 100), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Dessin d'un exemple d'œil de QR code avec la forme spécifiée
        self._draw_eye_shape(draw, eye_shape_id, 10, 10, 80, (0, 0, 0))
        
        # Sauvegarde de l'image
        img.save(shape_info['preview'])
    
    def _generate_frame_preview(self, frame_shape_id):
        """
        Génère une prévisualisation pour une forme de contour.
        
        Args:
            frame_shape_id (str): Identifiant de la forme de contour
        """
        if frame_shape_id not in self.frame_shapes:
            return
        
        # Récupération des informations de la forme
        shape_info = self.frame_shapes[frame_shape_id]
        
        # Création d'une image vide
        img = Image.new('RGB', (100, 100), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Dessin d'un exemple de contour de marqueur avec la forme spécifiée
        self._draw_frame_shape(draw, frame_shape_id, 10, 10, 80, (0, 0, 0))
        
        # Sauvegarde de l'image
        img.save(shape_info['preview'])
    
    def _generate_style_preview(self, style_id):
        """
        Génère une prévisualisation pour un style prédéfini.
        
        Args:
            style_id (str): Identifiant du style prédéfini
        """
        if style_id not in self.predefined_styles:
            return
        
        # Récupération des informations du style
        style_info = self.predefined_styles[style_id]
        
        # Génération d'un QR code avec le style spécifié
        qr_code = self.apply_predefined_style(
            "PREVIEW",
            style_id,
            None,
            save_to_file=True,
            output_path=style_info['preview']
        )
    
    def _draw_eye_shape(self, draw, shape_id, x, y, size, color):
        """
        Dessine un œil de QR code avec une forme spécifique.
        
        Args:
            draw: Objet ImageDraw
            shape_id (str): Identifiant de la forme
            x, y: Coordonnées du coin supérieur gauche
            size: Taille de l'œil
            color: Couleur de l'œil
        """
        # Point central
        cx, cy = x + size // 2, y + size // 2
        
        if shape_id == 'square':
            # Carré extérieur
            draw.rectangle([x, y, x + size, y + size], fill=color)
            # Carré intérieur (vide)
            inner_size = size * 3 // 5
            inner_x = x + (size - inner_size) // 2
            inner_y = y + (size - inner_size) // 2
            draw.rectangle([inner_x, inner_y, inner_x + inner_size, inner_y + inner_size], fill='white')
            # Carré central
            center_size = size // 5
            center_x = x + (size - center_size) // 2
            center_y = y + (size - center_size) // 2
            draw.rectangle([center_x, center_y, center_x + center_size, center_y + center_size], fill=color)
            
        elif shape_id == 'circle':
            # Cercle extérieur
            draw.ellipse([x, y, x + size, y + size], fill=color)
            # Cercle intérieur (vide)
            inner_size = size * 3 // 5
            inner_x = x + (size - inner_size) // 2
            inner_y = y + (size - inner_size) // 2
            draw.ellipse([inner_x, inner_y, inner_x + inner_size, inner_y + inner_size], fill='white')
            # Cercle central
            center_size = size // 5
            center_x = x + (size - center_size) // 2
            center_y = y + (size - center_size) // 2
            draw.ellipse([center_x, center_y, center_x + center_size, center_y + center_size], fill=color)
            
        elif shape_id == 'rounded':
            # Rectangle arrondi
            radius = size // 5
            # Dessiner un rectangle
            draw.rectangle([x + radius, y, x + size - radius, y + size], fill=color)
            draw.rectangle([x, y + radius, x + size, y + size - radius], fill=color)
            # Ajouter les coins arrondis
            draw.pieslice([x, y, x + radius * 2, y + radius * 2], 180, 270, fill=color)
            draw.pieslice([x + size - radius * 2, y, x + size, y + radius * 2], 270, 0, fill=color)
            draw.pieslice([x, y + size - radius * 2, x + radius * 2, y + size], 90, 180, fill=color)
            draw.pieslice([x + size - radius * 2, y + size - radius * 2, x + size, y + size], 0, 90, fill=color)
            # Intérieur (vide)
            inner_size = size * 3 // 5
            inner_x = x + (size - inner_size) // 2
            inner_y = y + (size - inner_size) // 2
            inner_radius = inner_size // 5
            # Rectangle intérieur
            draw.rectangle([inner_x + inner_radius, inner_y, inner_x + inner_size - inner_radius, inner_y + inner_size], fill='white')
            draw.rectangle([inner_x, inner_y + inner_radius, inner_x + inner_size, inner_y + inner_size - inner_radius], fill='white')
            # Coins arrondis intérieurs
            draw.pieslice([inner_x, inner_y, inner_x + inner_radius * 2, inner_y + inner_radius * 2], 180, 270, fill='white')
            draw.pieslice([inner_x + inner_size - inner_radius * 2, inner_y, inner_x + inner_size, inner_y + inner_radius * 2], 270, 0, fill='white')
            draw.pieslice([inner_x, inner_y + inner_size - inner_radius * 2, inner_x + inner_radius * 2, inner_y + inner_size], 90, 180, fill='white')
            draw.pieslice([inner_x + inner_size - inner_radius * 2, inner_y + inner_size - inner_radius * 2, inner_x + inner_size, inner_y + inner_size], 0, 90, fill='white')
            # Centre
            center_size = size // 5
            center_x = x + (size - center_size) // 2
            center_y = y + (size - center_size) // 2
            center_radius = center_size // 5
            # Rectangle central
            draw.rectangle([center_x + center_radius, center_y, center_x + center_size - center_radius, center_y + center_size], fill=color)
            draw.rectangle([center_x, center_y + center_radius, center_x + center_size, center_y + center_size - center_radius], fill=color)
            # Coins arrondis centraux
            draw.pieslice([center_x, center_y, center_x + center_radius * 2, center_y + center_radius * 2], 180, 270, fill=color)
            draw.pieslice([center_x + center_size - center_radius * 2, center_y, center_x + center_size, center_y + center_radius * 2], 270, 0, fill=color)
            draw.pieslice([center_x, center_y + center_size - center_radius * 2, center_x + center_radius * 2, center_y + center_size], 90, 180, fill=color)
            draw.pieslice([center_x + center_size - center_radius * 2, center_y + center_size - center_radius * 2, center_x + center_size, center_y + center_size], 0, 90, fill=color)
            
        elif shape_id == 'diamond':
            # Points du losange extérieur
            points = [
                (x + size // 2, y),  # haut
                (x + size, y + size // 2),  # droite
                (x + size // 2, y + size),  # bas
                (x, y + size // 2)  # gauche
            ]
            draw.polygon(points, fill=color)
            
            # Points du losange intérieur (vide)
            inner_size = size * 3 // 5
            inner_offset = (size - inner_size) // 2
            inner_points = [
                (x + size // 2, y + inner_offset),  # haut
                (x + size - inner_offset, y + size // 2),  # droite
                (x + size // 2, y + size - inner_offset),  # bas
                (x + inner_offset, y + size // 2)  # gauche
            ]
            draw.polygon(inner_points, fill='white')
            
            # Points du losange central
            center_size = size // 5
            center_offset = (size - center_size) // 2
            center_points = [
                (x + size // 2, y + center_offset),  # haut
                (x + size - center_offset, y + size // 2),  # droite
                (x + size // 2, y + size - center_offset),  # bas
                (x + center_offset, y + size // 2)  # gauche
            ]
            draw.polygon(center_points, fill=color)
            
        elif shape_id == 'cushion':
            # Forme de coussin
            draw.rectangle([x, y, x + size, y + size], fill=color)
            # Arrondir les coins
            radius = size // 3
            # Créer un effet de "coussin" en arrondissant les coins
            draw.pieslice([x - radius, y - radius, x + radius, y + radius], 0, 90, fill='white')
            draw.pieslice([x + size - radius, y - radius, x + size + radius, y + radius], 90, 180, fill='white')
            draw.pieslice([x - radius, y + size - radius, x + radius, y + size + radius], 270, 360, fill='white')
            draw.pieslice([x + size - radius, y + size - radius, x + size + radius, y + size + radius], 180, 270, fill='white')
            
            # Intérieur (vide)
            inner_size = size * 3 // 5
            inner_x = x + (size - inner_size) // 2
            inner_y = y + (size - inner_size) // 2
            draw.rectangle([inner_x, inner_y, inner_x + inner_size, inner_y + inner_size], fill='white')
            
            # Centre
            center_size = size // 5
            center_x = x + (size - center_size) // 2
            center_y = y + (size - center_size) // 2
            draw.rectangle([center_x, center_y, center_x + center_size, center_y + center_size], fill=color)
            
        elif shape_id == 'star':
            # Étoile à 4 branches
            # Centre de l'étoile
            cx, cy = x + size // 2, y + size // 2
            outer_radius = size // 2
            inner_radius = size // 4
            
            # Points de l'étoile
            points = []
            for i in range(8):
                angle = i * 45  # 45 degrés entre chaque point
                radius = outer_radius if i % 2 == 0 else inner_radius
                px = cx + int(radius * (i % 2 == 0))  # points externes
                py = cy + int(radius * (i % 2 == 1))  # points internes
                if i % 4 == 0:  # haut
                    px = cx
                    py = cy - radius
                elif i % 4 == 1:  # diagonale
                    px = cx + radius // 2
                    py = cy - radius // 2
                elif i % 4 == 2:  # droite
                    px = cx + radius
                    py = cy
                elif i % 4 == 3:  # diagonale
                    px = cx + radius // 2
                    py = cy + radius // 2
                points.append((px, py))
            
            # Dessiner l'étoile
            draw.polygon(points, fill=color)
            
            # Centre vide
            inner_size = size // 3
            draw.ellipse([cx - inner_size//2, cy - inner_size//2, cx + inner_size//2, cy + inner_size//2], fill='white')
            
            # Point central
            center_size = size // 10
            draw.ellipse([cx - center_size//2, cy - center_size//2, cx + center_size//2, cy + center_size//2], fill=color)
            
        elif shape_id == 'dots':
            # Coordonnées du centre
            cx, cy = x + size // 2, y + size // 2
            radius = size // 2
            small_radius = size // 8
            
            # Dessiner le cercle extérieur
            draw.ellipse([x, y, x + size, y + size], fill=color)
            
            # Dessiner le cercle intérieur (vide)
            inner_size = size * 3 // 5
            inner_x = x + (size - inner_size) // 2
            inner_y = y + (size - inner_size) // 2
            draw.ellipse([inner_x, inner_y, inner_x + inner_size, inner_y + inner_size], fill='white')
            
            # Dessiner les points autour du cercle
            num_dots = 8
            dot_radius = size // 16
            for i in range(num_dots):
                angle = i * (360 / num_dots)
                dot_x = cx + int(radius * 0.6 * cos(angle * pi / 180))
                dot_y = cy + int(radius * 0.6 * sin(angle * pi / 180))
                draw.ellipse([dot_x - dot_radius, dot_y - dot_radius, dot_x + dot_radius, dot_y + dot_radius], fill=color)
            
            # Dessiner le point central
            draw.ellipse([cx - small_radius, cy - small_radius, cx + small_radius, cy + small_radius], fill=color)
            
        elif shape_id == 'rounded_rect':
            # Rectangle aux coins arrondis
            radius = size // 8
            
            # Rectangle principal
            draw.rectangle([x + radius, y, x + size - radius, y + size], fill=color)
            draw.rectangle([x, y + radius, x + size, y + size - radius], fill=color)
            
            # Coins arrondis
            draw.pieslice([x, y, x + radius * 2, y + radius * 2], 180, 270, fill=color)
            draw.pieslice([x + size - radius * 2, y, x + size, y + radius * 2], 270, 0, fill=color)
            draw.pieslice([x, y + size - radius * 2, x + radius * 2, y + size], 90, 180, fill=color)
            draw.pieslice([x + size - radius * 2, y + size - radius * 2, x + size, y + size], 0, 90, fill=color)
            
            # Rectangle intérieur (vide)
            inner_size = size * 3 // 5
            inner_x = x + (size - inner_size) // 2
            inner_y = y + (size - inner_size) // 2
            inner_radius = inner_size // 8
            
            # Rectangle intérieur
            draw.rectangle([inner_x + inner_radius, inner_y, inner_x + inner_size - inner_radius, inner_y + inner_size], fill='white')
            draw.rectangle([inner_x, inner_y + inner_radius, inner_x + inner_size, inner_y + inner_size - inner_radius], fill='white')
            
            # Coins arrondis intérieurs
            draw.pieslice([inner_x, inner_y, inner_x + inner_radius * 2, inner_y + inner_radius * 2], 180, 270, fill='white')
            draw.pieslice([inner_x + inner_size - inner_radius * 2, inner_y, inner_x + inner_size, inner_y + inner_radius * 2], 270, 0, fill='white')
            draw.pieslice([inner_x, inner_y + inner_size - inner_radius * 2, inner_x + inner_radius * 2, inner_y + inner_size], 90, 180, fill='white')
            draw.pieslice([inner_x + inner_size - inner_radius * 2, inner_y + inner_size - inner_radius * 2, inner_x + inner_size, inner_y + inner_size], 0, 90, fill='white')
            
            # Rectangle central
            center_size = size // 5
            center_x = x + (size - center_size) // 2
            center_y = y + (size - center_size) // 2
            draw.rectangle([center_x, center_y, center_x + center_size, center_y + center_size], fill=color)
            
        elif shape_id == 'flower':
            # Coordonnées du centre
            cx, cy = x + size // 2, y + size // 2
            radius = size // 2
            
            # Dessiner le cercle central
            center_radius = radius // 2
            draw.ellipse([cx - center_radius, cy - center_radius, cx + center_radius, cy + center_radius], fill=color)
            
            # Dessiner les pétales (4 cercles autour du centre)
            petal_radius = radius // 2
            positions = [
                (cx, cy - radius),  # haut
                (cx + radius, cy),  # droite
                (cx, cy + radius),  # bas
                (cx - radius, cy)   # gauche
            ]
            for px, py in positions:
                draw.ellipse([px - petal_radius, py - petal_radius, px + petal_radius, py + petal_radius], fill=color)
            
            # Centre vide
            inner_radius = radius // 3
            draw.ellipse([cx - inner_radius, cy - inner_radius, cx + inner_radius, cy + inner_radius], fill='white')
            
            # Point central
            dot_radius = radius // 6
            draw.ellipse([cx - dot_radius, cy - dot_radius, cx + dot_radius, cy + dot_radius], fill=color)
            
        elif shape_id == 'leaf':
            # Forme de feuille
            # Triangle principal
            points = [
                (x + size // 2, y),  # sommet
                (x + size, y + size),  # coin inférieur droit
                (x, y + size)  # coin inférieur gauche
            ]
            draw.polygon(points, fill=color)
            
            # Triangle intérieur (vide)
            inner_size = size * 3 // 5
            inner_offset = (size - inner_size) // 2
            inner_points = [
                (x + size // 2, y + inner_offset),  # sommet
                (x + size - inner_offset, y + size - inner_offset),  # coin inférieur droit
                (x + inner_offset, y + size - inner_offset)  # coin inférieur gauche
            ]
            draw.polygon(inner_points, fill='white')
            
            # Triangle central
            center_size = size // 5
            center_offset = size // 2
            center_points = [
                (x + size // 2, y + center_offset),  # sommet
                (x + size // 2 + center_size // 2, y + center_offset + center_size),  # coin inférieur droit
                (x + size // 2 - center_size // 2, y + center_offset + center_size)  # coin inférieur gauche
            ]
            draw.polygon(center_points, fill=color)
            
        else:
            # Forme par défaut (carré)
            draw.rectangle([x, y, x + size, y + size], fill=color)
            # Carré intérieur (vide)
            inner_size = size * 3 // 5
            inner_x = x + (size - inner_size) // 2
            inner_y = y + (size - inner_size) // 2
            draw.rectangle([inner_x, inner_y, inner_x + inner_size, inner_y + inner_size], fill='white')
            # Carré central
            center_size = size // 5
            center_x = x + (size - center_size) // 2
            center_y = y + (size - center_size) // 2
            draw.rectangle([center_x, center_y, center_x + center_size, center_y + center_size], fill=color)
    
    def _draw_frame_shape(self, draw, shape_id, x, y, size, color):
        """
        Dessine un contour de marqueur avec une forme spécifique.
        
        Args:
            draw: Objet ImageDraw
            shape_id (str): Identifiant de la forme
            x, y: Coordonnées du coin supérieur gauche
            size: Taille du contour
            color: Couleur du contour
        """
        # Épaisseur du contour
        thickness = size // 7
        
        if shape_id == 'square':
            # Contour carré
            draw.rectangle([x, y, x + size, y + size], fill=color)
            draw.rectangle([x + thickness, y + thickness, x + size - thickness, y + size - thickness], fill='white')
            
        elif shape_id == 'rounded_square':
            # Carré aux coins légèrement arrondis
            radius = size // 10
            
            # Rectangle extérieur
            draw.rectangle([x + radius, y, x + size - radius, y + size], fill=color)
            draw.rectangle([x, y + radius, x + size, y + size - radius], fill=color)
            
            # Coins arrondis
            draw.pieslice([x, y, x + radius * 2, y + radius * 2], 180, 270, fill=color)
            draw.pieslice([x + size - radius * 2, y, x + size, y + radius * 2], 270, 0, fill=color)
            draw.pieslice([x, y + size - radius * 2, x + radius * 2, y + size], 90, 180, fill=color)
            draw.pieslice([x + size - radius * 2, y + size - radius * 2, x + size, y + size], 0, 90, fill=color)
            
            # Rectangle intérieur (vide)
            inner_radius = max(1, (radius - thickness))
            draw.rectangle([x + thickness + inner_radius, y + thickness, x + size - thickness - inner_radius, y + size - thickness], fill='white')
            draw.rectangle([x + thickness, y + thickness + inner_radius, x + size - thickness, y + size - thickness - inner_radius], fill='white')
            
            # Coins arrondis intérieurs
            draw.pieslice([x + thickness, y + thickness, x + thickness + inner_radius * 2, y + thickness + inner_radius * 2], 180, 270, fill='white')
            draw.pieslice([x + size - thickness - inner_radius * 2, y + thickness, x + size - thickness, y + thickness + inner_radius * 2], 270, 0, fill='white')
            draw.pieslice([x + thickness, y + size - thickness - inner_radius * 2, x + thickness + inner_radius * 2, y + size - thickness], 90, 180, fill='white')
            draw.pieslice([x + size - thickness - inner_radius * 2, y + size - thickness - inner_radius * 2, x + size - thickness, y + size - thickness], 0, 90, fill='white')
            
        elif shape_id == 'circle':
            # Contour circulaire
            draw.ellipse([x, y, x + size, y + size], fill=color)
            draw.ellipse([x + thickness, y + thickness, x + size - thickness, y + size - thickness], fill='white')
            
        elif shape_id == 'rounded':
            # Contour fortement arrondi (presque circulaire)
            radius = size // 3
            
            # Rectangle extérieur avec coins très arrondis
            draw.rectangle([x + radius, y, x + size - radius, y + size], fill=color)
            draw.rectangle([x, y + radius, x + size, y + size - radius], fill=color)
            
            # Coins arrondis
            draw.pieslice([x, y, x + radius * 2, y + radius * 2], 180, 270, fill=color)
            draw.pieslice([x + size - radius * 2, y, x + size, y + radius * 2], 270, 0, fill=color)
            draw.pieslice([x, y + size - radius * 2, x + radius * 2, y + size], 90, 180, fill=color)
            draw.pieslice([x + size - radius * 2, y + size - radius * 2, x + size, y + size], 0, 90, fill=color)
            
            # Intérieur (vide)
            inner_radius = max(1, (radius - thickness))
            draw.rectangle([x + thickness + inner_radius, y + thickness, x + size - thickness - inner_radius, y + size - thickness], fill='white')
            draw.rectangle([x + thickness, y + thickness + inner_radius, x + size - thickness, y + size - thickness - inner_radius], fill='white')
            
            # Coins arrondis intérieurs
            draw.pieslice([x + thickness, y + thickness, x + thickness + inner_radius * 2, y + thickness + inner_radius * 2], 180, 270, fill='white')
            draw.pieslice([x + size - thickness - inner_radius * 2, y + thickness, x + size - thickness, y + thickness + inner_radius * 2], 270, 0, fill='white')
            draw.pieslice([x + thickness, y + size - thickness - inner_radius * 2, x + thickness + inner_radius * 2, y + size - thickness], 90, 180, fill='white')
            draw.pieslice([x + size - thickness - inner_radius * 2, y + size - thickness - inner_radius * 2, x + size - thickness, y + size - thickness], 0, 90, fill='white')
            
        elif shape_id == 'diamond':
            # Points du losange extérieur
            points = [
                (x + size // 2, y),  # haut
                (x + size, y + size // 2),  # droite
                (x + size // 2, y + size),  # bas
                (x, y + size // 2)  # gauche
            ]
            draw.polygon(points, fill=color)
            
            # Points du losange intérieur (vide)
            inner_offset = thickness
            inner_points = [
                (x + size // 2, y + inner_offset),  # haut
                (x + size - inner_offset, y + size // 2),  # droite
                (x + size // 2, y + size - inner_offset),  # bas
                (x + inner_offset, y + size // 2)  # gauche
            ]
            draw.polygon(inner_points, fill='white')
            
        elif shape_id == 'corner_cut':
            # Contour aux coins coupés
            # Points du polygone
            cut_size = size // 5
            points = [
                (x + cut_size, y),  # haut gauche
                (x + size - cut_size, y),  # haut droite
                (x + size, y + cut_size),  # droite haut
                (x + size, y + size - cut_size),  # droite bas
                (x + size - cut_size, y + size),  # bas droite
                (x + cut_size, y + size),  # bas gauche
                (x, y + size - cut_size),  # gauche bas
                (x, y + cut_size)  # gauche haut
            ]
            draw.polygon(points, fill=color)
            
            # Points du polygone intérieur (vide)
            inner_cut_size = max(1, cut_size - thickness)
            inner_points = [
                (x + cut_size + thickness, y + thickness),  # haut gauche
                (x + size - cut_size - thickness, y + thickness),  # haut droite
                (x + size - thickness, y + cut_size + thickness),  # droite haut
                (x + size - thickness, y + size - cut_size - thickness),  # droite bas
                (x + size - cut_size - thickness, y + size - thickness),  # bas droite
                (x + cut_size + thickness, y + size - thickness),  # bas gauche
                (x + thickness, y + size - cut_size - thickness),  # gauche bas
                (x + thickness, y + cut_size + thickness)  # gauche haut
            ]
            draw.polygon(inner_points, fill='white')
            
        elif shape_id == 'jagged':
            # Contour dentelé
            # Nombre de dents par côté
            teeth = 3
            teeth_depth = size // 10
            
            # Points du polygone dentelé
            points = []
            
            # Côté supérieur
            for i in range(teeth + 1):
                x_pos = x + i * (size / teeth)
                y_pos = y + (teeth_depth if i % 2 else 0)
                points.append((x_pos, y_pos))
            
            # Côté droit
            for i in range(1, teeth + 1):
                x_pos = x + size - (teeth_depth if i % 2 else 0)
                y_pos = y + i * (size / teeth)
                points.append((x_pos, y_pos))
            
            # Côté inférieur
            for i in range(teeth, -1, -1):
                x_pos = x + i * (size / teeth)
                y_pos = y + size - (teeth_depth if i % 2 else 0)
                points.append((x_pos, y_pos))
            
            # Côté gauche
            for i in range(teeth, 0, -1):
                x_pos = x + (teeth_depth if i % 2 else 0)
                y_pos = y + i * (size / teeth)
                points.append((x_pos, y_pos))
            
            draw.polygon(points, fill=color)
            
            # Points du polygone intérieur (vide)
            inner_teeth_depth = max(1, teeth_depth - thickness // 2)
            inner_size = size - 2 * thickness
            inner_teeth = teeth
            inner_points = []
            
            # Côté supérieur
            for i in range(inner_teeth + 1):
                x_pos = x + thickness + i * (inner_size / inner_teeth)
                y_pos = y + thickness + (inner_teeth_depth if i % 2 else 0)
                inner_points.append((x_pos, y_pos))
            
            # Côté droit
            for i in range(1, inner_teeth + 1):
                x_pos = x + thickness + inner_size - (inner_teeth_depth if i % 2 else 0)
                y_pos = y + thickness + i * (inner_size / inner_teeth)
                inner_points.append((x_pos, y_pos))
            
            # Côté inférieur
            for i in range(inner_teeth, -1, -1):
                x_pos = x + thickness + i * (inner_size / inner_teeth)
                y_pos = y + thickness + inner_size - (inner_teeth_depth if i % 2 else 0)
                inner_points.append((x_pos, y_pos))
            
            # Côté gauche
            for i in range(inner_teeth, 0, -1):
                x_pos = x + thickness + (inner_teeth_depth if i % 2 else 0)
                y_pos = y + thickness + i * (inner_size / inner_teeth)
                inner_points.append((x_pos, y_pos))
            
            draw.polygon(inner_points, fill='white')
            
        elif shape_id == 'dots':
            # Contour composé de points
            # Nombre de points par côté
            num_dots = 8
            dot_radius = size // 20
            dots_positions = []
            
            # Calculer les positions des points
            for i in range(num_dots):
                # Côté supérieur
                dots_positions.append((x + i * size / (num_dots - 1), y))
                # Côté droit
                dots_positions.append((x + size, y + i * size / (num_dots - 1)))
                # Côté inférieur
                dots_positions.append((x + size - i * size / (num_dots - 1), y + size))
                # Côté gauche
                dots_positions.append((x, y + size - i * size / (num_dots - 1)))
            
            # Dessiner les points
            for px, py in dots_positions:
                draw.ellipse([px - dot_radius, py - dot_radius, px + dot_radius, py + dot_radius], fill=color)
            
            # Rectangle intérieur (vide)
            inner_offset = thickness
            draw.rectangle([x + inner_offset, y + inner_offset, x + size - inner_offset, y + size - inner_offset], fill='white')
            
        elif shape_id == 'pointed':
            # Contour aux coins pointus
            # Points du polygone
            point_size = size // 4
            points = [
                (x, y + point_size),  # haut gauche
                (x + point_size, y),  # coin pointu haut gauche
                (x + size - point_size, y),  # haut droite
                (x + size, y + point_size),  # coin pointu haut droite
                (x + size, y + size - point_size),  # droite bas
                (x + size - point_size, y + size),  # coin pointu bas droite
                (x + point_size, y + size),  # bas gauche
                (x, y + size - point_size)  # coin pointu bas gauche
            ]
            draw.polygon(points, fill=color)
            
            # Points du polygone intérieur (vide)
            inner_point_size = max(1, point_size - thickness)
            inner_points = [
                (x + thickness, y + point_size),  # haut gauche
                (x + point_size, y + thickness),  # coin pointu haut gauche
                (x + size - point_size, y + thickness),  # haut droite
                (x + size - thickness, y + point_size),  # coin pointu haut droite
                (x + size - thickness, y + size - point_size),  # droite bas
                (x + size - point_size, y + size - thickness),  # coin pointu bas droite
                (x + point_size, y + size - thickness),  # bas gauche
                (x + thickness, y + size - point_size)  # coin pointu bas gauche
            ]
            draw.polygon(inner_points, fill='white')
            
        elif shape_id == 'pixel':
            # Contour pixelisé
            # Taille des pixels
            pixel_size = size // 10
            
            # Dessiner le contour extérieur pixelisé
            for i in range(0, size + 1, pixel_size):
                for j in range(0, size + 1, pixel_size):
                    # Dessiner seulement les pixels du contour
                    if (i < thickness or i >= size - thickness or 
                        j < thickness or j >= size - thickness):
                        draw.rectangle([x + i, y + j, x + i + pixel_size - 1, y + j + pixel_size - 1], fill=color)
            
            # Rectangle intérieur (vide)
            draw.rectangle([x + thickness, y + thickness, x + size - thickness, y + size - thickness], fill='white')
            
        else:
            # Contour carré par défaut
            draw.rectangle([x, y, x + size, y + size], fill=color)
            draw.rectangle([x + thickness, y + thickness, x + size - thickness, y + size - thickness], fill='white')
    
    def generate_styled_qrcode(self, data, module_drawer_id, color_mask_id, filename=None, **options):
        """
        Génère un QR code avec un style personnalisé.
        
        Args:
            data (str): Données à encoder dans le QR code (URL, texte, etc.)
            module_drawer_id (str): Identifiant du style de module ('square', 'circle', etc.)
            color_mask_id (str): Identifiant du masque de couleur ('solid', 'radial_gradient', etc.)
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour la personnalisation du QR code.
            
        Returns:
            str: Chemin du fichier QR code généré.
        """
        if not filename:
            filename = f"styled_qrcode_{uuid.uuid4().hex[:8]}.png"
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Vérification des identifiants de style
        if module_drawer_id not in self.module_drawers:
            module_drawer_id = 'square'  # Style par défaut
        
        if color_mask_id not in self.color_masks:
            color_mask_id = 'solid'  # Masque par défaut
        
        # Récupération du module drawer
        module_drawer = self.module_drawers[module_drawer_id]['drawer']
        
        # Récupération du masque de couleur
        color_mask_class = self.color_masks[color_mask_id]['class']
        
        # Paramètres du QR code
        version = options.get('version', 1)
        error_correction = options.get('error_correction', qrcode.constants.ERROR_CORRECT_M)
        box_size = options.get('box_size', 10)
        border = options.get('border', 4)
        
        # Options pour le masque de couleur
        color_mask_kwargs = {}
        
        if color_mask_id == 'solid':
            # Couleur unie
            color_mask_kwargs = {
                'front_color': options.get('front_color', (0, 0, 0)),
                'back_color': options.get('back_color', (255, 255, 255))
            }
        elif color_mask_id in ['radial_gradient', 'square_gradient']:
            # Dégradés radial ou carré
            color_mask_kwargs = {
                'center_color': options.get('front_color', (0, 102, 204)),
                'edge_color': options.get('edge_color', (0, 51, 153)),
                'back_color': options.get('back_color', (255, 255, 255))
            }
            
            if 'gradient_center' in options:
                color_mask_kwargs['center'] = options.get('gradient_center')
        elif color_mask_id == 'horizontal_gradient':
            # Dégradé horizontal
            color_mask_kwargs = {
                'left_color': options.get('front_color', (255, 102, 0)),
                'right_color': options.get('edge_color', (204, 0, 0)),
                'back_color': options.get('back_color', (255, 255, 255))
            }
        elif color_mask_id == 'vertical_gradient':
            # Dégradé vertical
            color_mask_kwargs = {
                'top_color': options.get('front_color', (0, 153, 0)),
                'bottom_color': options.get('edge_color', (0, 51, 0)),
                'back_color': options.get('back_color', (255, 255, 255))
            }
        elif color_mask_id == 'diagonal_gradient':
            # Dégradé diagonal
            color_mask_kwargs = {
                'top_left_color': options.get('front_color', (0, 102, 204)),
                'bottom_right_color': options.get('edge_color', (0, 51, 153)),
                'back_color': options.get('back_color', (255, 255, 255))
            }
        elif color_mask_id == 'rainbow':
            # Dégradé arc-en-ciel
            color_mask_kwargs = {
                'back_color': options.get('back_color', (255, 255, 255))
            }
            
            if 'colors' in options:
                color_mask_kwargs['colors'] = options.get('colors')
        
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
        img_pil = img.get_image() if hasattr(img, 'get_image') else img
        
        eye_shape = options.get('eye_shape')
        frame_shape = options.get('frame_shape')
        
        if eye_shape or frame_shape:
            if not eye_shape:
                eye_shape = 'square'
            if not frame_shape:
                frame_shape = 'square'
            
            # Personnalisation des yeux et contours
            img_pil = self._customize_markers(img_pil, qr, frame_shape, eye_shape, options)
        
        # Sauvegarde de l'image
        img_pil.save(output_path)
        
        # Enregistrement des métadonnées
        self._save_metadata(data, output_path, options)
        
        return output_path
    
    def _customize_markers(self, qr_image, qr_code, frame_shape, eye_shape, options):
        """
        Personnalise les marqueurs d'un QR code (yeux et contours).
        
        Args:
            qr_image: Image PIL du QR code
            qr_code: Objet QRCode
            frame_shape (str): Forme du contour des marqueurs
            eye_shape (str): Forme du centre des marqueurs
            options (dict): Options supplémentaires pour la personnalisation
        
        Returns:
            Image: Image PIL modifiée
        """
        # Copie de l'image pour éviter de modifier l'original
        enhanced_img = qr_image.copy().convert('RGBA')
        
        # Configuration des marqueurs
        # Calcul de la taille des modules (pixels par module)
        box_size = qr_code.box_size
        border = qr_code.border
        
        # Positions des trois yeux de détection (haut-gauche, haut-droit, bas-gauche)
        positions = [
            (border, border),  # Haut-gauche
            (border, qr_code.modules_count - 7 - border + 1),  # Bas-gauche
            (qr_code.modules_count - 7 - border + 1, border)  # Haut-droit
        ]
        
        # Taille de l'œil de détection (7 modules)
        eye_size = 7 * box_size
        
        # Création d'un calque pour les yeux personnalisés
        eye_layer = Image.new('RGBA', enhanced_img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(eye_layer)
        
        # Couleur pour les yeux (par défaut, noir)
        eye_color = options.get('front_color', (0, 0, 0))
        if isinstance(eye_color, str):
            eye_color = ImageColor.getrgb(eye_color)
        
        # Dessiner les yeux personnalisés
        for pos_x, pos_y in positions:
            x = pos_x * box_size
            y = pos_y * box_size
            
            # Dessiner le contour
            self._draw_frame_shape(draw, frame_shape, x, y, eye_size, eye_color)
            
            # Dessiner le centre de l'œil (à l'intérieur du contour)
            center_x = x + eye_size // 3
            center_y = y + eye_size // 3
            center_size = eye_size // 3
            self._draw_eye_shape(draw, eye_shape, center_x, center_y, center_size, eye_color)
        
        # Fusion du calque des yeux avec l'image d'origine
        enhanced_img = Image.alpha_composite(enhanced_img, eye_layer)
        
        return enhanced_img.convert('RGB')
    
    def apply_predefined_style(self, data, style_id, filename=None, save_to_file=True, output_path=None, **custom_options):
        """
        Applique un style prédéfini à un QR code.
        
        Args:
            data (str): Données à encoder dans le QR code (URL, texte, etc.)
            style_id (str): Identifiant du style prédéfini
            filename (str, optional): Nom du fichier de sortie.
            save_to_file (bool): Indique si le QR code doit être sauvegardé sur disque
            output_path (str, optional): Chemin de sortie spécifique (ignore filename si spécifié)
            **custom_options: Options personnalisées qui remplaceront celles du style prédéfini
            
        Returns:
            str: Chemin du fichier QR code généré ou Image PIL si save_to_file=False
        """
        # Vérification du style
        if style_id not in self.predefined_styles:
            style_id = 'classic'  # Style par défaut
        
        # Récupération des options du style
        style_info = self.predefined_styles[style_id]
        
        # Création d'un dictionnaire d'options à partir du style
        options = {
            'module_drawer': style_info.get('module_drawer', 'square'),
            'color_mask': style_info.get('color_mask', 'solid'),
            'front_color': style_info.get('front_color', (0, 0, 0)),
            'back_color': style_info.get('back_color', (255, 255, 255)),
            'eye_shape': style_info.get('eye_shape', 'square'),
            'frame_shape': style_info.get('frame_shape', 'square')
        }
        
        # Ajout des options spécifiques au masque de couleur
        if 'edge_color' in style_info:
            options['edge_color'] = style_info['edge_color']
        if 'gradient_center' in style_info:
            options['gradient_center'] = style_info['gradient_center']
        
        # Fusion avec les options personnalisées
        options.update(custom_options)
        
        # Détermination du nom de fichier
        if output_path:
            final_path = output_path
        elif not filename:
            filename = f"{style_id}_qrcode_{uuid.uuid4().hex[:8]}.png"
            final_path = os.path.join(self.output_dir, filename)
        else:
            final_path = os.path.join(self.output_dir, filename)
        
        if save_to_file:
            # Génération du QR code avec le style spécifié
            return self.generate_styled_qrcode(
                data,
                options['module_drawer'],
                options['color_mask'],
                final_path,
                **options
            )
        else:
            # Génération sans sauvegarde sur disque
            # Récupération du module drawer et du color mask
            module_drawer_id = options['module_drawer']
            color_mask_id = options['color_mask']
            
            module_drawer = self.module_drawers[module_drawer_id]['drawer']
            color_mask_class = self.color_masks[color_mask_id]['class']
            
            # Options pour le masque de couleur
            color_mask_kwargs = {}
            
            if color_mask_id == 'solid':
                color_mask_kwargs = {
                    'front_color': options.get('front_color', (0, 0, 0)),
                    'back_color': options.get('back_color', (255, 255, 255))
                }
            elif color_mask_id in ['radial_gradient', 'square_gradient']:
                color_mask_kwargs = {
                    'center_color': options.get('front_color', (0, 102, 204)),
                    'edge_color': options.get('edge_color', (0, 51, 153)),
                    'back_color': options.get('back_color', (255, 255, 255))
                }
                
                if 'gradient_center' in options:
                    color_mask_kwargs['center'] = options.get('gradient_center')
            elif color_mask_id == 'horizontal_gradient':
                color_mask_kwargs = {
                    'left_color': options.get('front_color', (255, 102, 0)),
                    'right_color': options.get('edge_color', (204, 0, 0)),
                    'back_color': options.get('back_color', (255, 255, 255))
                }
            elif color_mask_id == 'vertical_gradient':
                color_mask_kwargs = {
                    'top_color': options.get('front_color', (0, 153, 0)),
                    'bottom_color': options.get('edge_color', (0, 51, 0)),
                    'back_color': options.get('back_color', (255, 255, 255))
                }
            elif color_mask_id == 'diagonal_gradient':
                color_mask_kwargs = {
                    'top_left_color': options.get('front_color', (0, 102, 204)),
                    'bottom_right_color': options.get('edge_color', (0, 51, 153)),
                    'back_color': options.get('back_color', (255, 255, 255))
                }
            elif color_mask_id == 'rainbow':
                color_mask_kwargs = {
                    'back_color': options.get('back_color', (255, 255, 255))
                }
                
                if 'colors' in options:
                    color_mask_kwargs['colors'] = options.get('colors')
            
            # Création du masque de couleur
            color_mask = color_mask_class(**color_mask_kwargs)
            
            # Paramètres du QR code
            version = options.get('version', 1)
            error_correction = options.get('error_correction', qrcode.constants.ERROR_CORRECT_M)
            box_size = options.get('box_size', 10)
            border = options.get('border', 4)
            
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
            img_pil = img.get_image() if hasattr(img, 'get_image') else img
            
            eye_shape = options.get('eye_shape')
            frame_shape = options.get('frame_shape')
            
            if eye_shape or frame_shape:
                if not eye_shape:
                    eye_shape = 'square'
                if not frame_shape:
                    frame_shape = 'square'
                
                # Personnalisation des yeux et contours
                img_pil = self._customize_markers(img_pil, qr, frame_shape, eye_shape, options)
            
            return img_pil
    
    def generate_qrcode_with_logo(self, data, logo_path, filename=None, **options):
        """
        Génère un QR code avec un logo au centre.
        
        Args:
            data (str): Données à encoder dans le QR code (URL, texte, etc.)
            logo_path (str): Chemin vers le fichier logo à insérer
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour la personnalisation du QR code.
                - version (int): Version du QR code (1-40)
                - error_correction (int): Niveau de correction d'erreur
                - box_size (int): Taille de chaque "boîte" du QR code en pixels
                - border (int): Taille de la bordure en nombre de boîtes
                - module_drawer (str): Style des modules ('square', 'circle', etc.)
                - color_mask (str): Type de masque de couleur ('solid', 'radial_gradient', etc.)
                - front_color (tuple/str): Couleur de premier plan (RGB ou nom)
                - back_color (tuple/str): Couleur d'arrière-plan (RGB ou nom)
                - logo_size (float): Taille du logo en pourcentage du QR code (0.0-1.0)
                - logo_border (bool): Ajouter une bordure blanche autour du logo
                - logo_border_width (int): Largeur de la bordure du logo en pixels
            
        Returns:
            str: Chemin du fichier QR code généré.
        """
        if not filename:
            filename = f"logo_qrcode_{uuid.uuid4().hex[:8]}.png"
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Options par défaut avec niveau de correction d'erreur élevé pour compenser le logo
        version = options.get('version', 1)
        error_correction = options.get('error_correction', qrcode.constants.ERROR_CORRECT_H)
        box_size = options.get('box_size', 10)
        border = options.get('border', 4)
        
        # Style et couleurs
        module_drawer_id = options.get('module_drawer', 'square')
        color_mask_id = options.get('color_mask', 'solid')
        logo_size = options.get('logo_size', 0.2)  # 20% par défaut
        logo_border = options.get('logo_border', True)
        logo_border_width = options.get('logo_border_width', 2)
        
        # Génération du QR code avec le style spécifié
        if module_drawer_id in self.module_drawers and color_mask_id in self.color_masks:
            # Génération avec style personnalisé
            qr_img = self.generate_styled_qrcode(
                data,
                module_drawer_id,
                color_mask_id,
                None,  # Ne pas sauvegarder le fichier
                version=version,
                error_correction=error_correction,
                box_size=box_size,
                border=border,
                **options
            )
            
            # Conversion en image PIL
            if not isinstance(qr_img, Image.Image):
                qr_img = Image.open(qr_img)
        else:
            # Génération avec style par défaut
            qr = qrcode.QRCode(
                version=version,
                error_correction=error_correction,
                box_size=box_size,
                border=border,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            fill_color = options.get('front_color', "black")
            back_color = options.get('back_color', "white")
            
            qr_img = qr.make_image(fill_color=fill_color, back_color=back_color)
            qr_img = qr_img.get_image() if hasattr(qr_img, 'get_image') else qr_img
        
        # Conversion en mode RGBA pour la transparence
        qr_img = qr_img.convert('RGBA')
        
        try:
            # Ouverture et redimensionnement du logo
            logo = Image.open(logo_path).convert('RGBA')
            
            # Calcul de la taille du logo
            qr_width, qr_height = qr_img.size
            logo_max_size = int(min(qr_width, qr_height) * logo_size)
            
            # Redimensionnement du logo tout en conservant le ratio
            logo_width, logo_height = logo.size
            ratio = min(logo_max_size / logo_width, logo_max_size / logo_height)
            new_logo_width = int(logo_width * ratio)
            new_logo_height = int(logo_height * ratio)
            logo = logo.resize((new_logo_width, new_logo_height), Image.LANCZOS)
            
            # Ajout d'une bordure blanche autour du logo si demandé
            if logo_border:
                # Création d'une image légèrement plus grande pour la bordure
                border_size = logo_border_width
                bordered_logo = Image.new('RGBA', 
                                         (new_logo_width + 2 * border_size, 
                                          new_logo_height + 2 * border_size), 
                                         (255, 255, 255, 255))
                # Placement du logo au centre
                bordered_logo.paste(logo, (border_size, border_size), logo)
                logo = bordered_logo
                new_logo_width += 2 * border_size
                new_logo_height += 2 * border_size
            
            # Calcul de la position du logo (centre)
            position = ((qr_width - new_logo_width) // 2, (qr_height - new_logo_height) // 2)
            
            # Création d'une nouvelle image pour le résultat final
            result = Image.new('RGBA', (qr_width, qr_height), (0, 0, 0, 0))
            
            # Copie du QR code sur l'image résultat
            result.paste(qr_img, (0, 0))
            
            # Ajout du logo
            result.paste(logo, position, logo)
            
            # Sauvegarde de l'image finale
            result.save(output_path)
            
            # Enregistrement des métadonnées
            options['logo_path'] = logo_path
            self._save_metadata(data, output_path, options)
            
            return output_path
            
        except Exception as e:
            print(f"Erreur lors de l'ajout du logo: {e}")
            # En cas d'erreur, générer un QR code sans logo
            qr_img.save(output_path)
            return output_path
    
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
    
    def get_all_module_styles(self):
        """
        Obtient la liste de tous les styles de modules disponibles.
        
        Returns:
            list: Liste des styles de modules avec leurs informations
        """
        styles = []
        for style_id, style_info in self.module_drawers.items():
            styles.append({
                'id': style_id,
                'name': style_info['name'],
                'description': style_info['description'],
                'preview_url': os.path.relpath(style_info['preview'], self.templates_dir)
            })
        
        return styles
    
    def get_all_color_masks(self):
        """
        Obtient la liste de tous les masques de couleur disponibles.
        
        Returns:
            list: Liste des masques de couleur avec leurs informations
        """
        masks = []
        for mask_id, mask_info in self.color_masks.items():
            masks.append({
                'id': mask_id,
                'name': mask_info['name'],
                'description': mask_info['description'],
                'preview_url': os.path.relpath(mask_info['preview'], self.templates_dir)
            })
        
        return masks
    
    def get_all_eye_shapes(self):
        """
        Obtient la liste de toutes les formes d'yeux disponibles.
        
        Returns:
            list: Liste des formes d'yeux avec leurs informations
        """
        shapes = []
        for shape_id, shape_info in self.eye_shapes.items():
            shapes.append({
                'id': shape_id,
                'name': shape_info['name'],
                'description': shape_info['description'],
                'preview_url': os.path.relpath(shape_info['preview'], self.templates_dir)
            })
        
        return shapes
    
    def get_all_frame_shapes(self):
        """
        Obtient la liste de toutes les formes de contours disponibles.
        
        Returns:
            list: Liste des formes de contours avec leurs informations
        """
        shapes = []
        for shape_id, shape_info in self.frame_shapes.items():
            shapes.append({
                'id': shape_id,
                'name': shape_info['name'],
                'description': shape_info['description'],
                'preview_url': os.path.relpath(shape_info['preview'], self.templates_dir)
            })
        
        return shapes
    
    def get_all_predefined_styles(self):
        """
        Obtient la liste de tous les styles prédéfinis disponibles.
        
        Returns:
            list: Liste des styles prédéfinis avec leurs informations
        """
        styles = []
        for style_id, style_info in self.predefined_styles.items():
            styles.append({
                'id': style_id,
                'name': style_info['name'],
                'description': style_info['description'],
                'preview_url': os.path.relpath(style_info['preview'], self.templates_dir)
            })
        
        return styles
    
    def generate_preview_base64(self, data, style_id=None, module_shape=None, color_mask=None, **options):
        """
        Génère une prévisualisation d'un QR code en base64.
        
        Args:
            data (str): Données à encoder
            style_id (str, optional): ID d'un style prédéfini
            module_shape (str, optional): ID de forme de module
            color_mask (str, optional): ID de masque de couleur
            **options: Options supplémentaires
            
        Returns:
            str: Image base64 du QR code
        """
        import base64
        from io import BytesIO
        
        # Génération de l'image
        if style_id and style_id in self.predefined_styles:
            # Utiliser un style prédéfini
            img = self.apply_predefined_style(data, style_id, save_to_file=False, **options)
        elif module_shape and color_mask:
            # Générer avec module et masque spécifiés
            options['module_drawer'] = module_shape
            options['color_mask'] = color_mask
            
            # Version simplifiée pour prévisualisation
            version = options.get('version', 1)
            error_correction = options.get('error_correction', qrcode.constants.ERROR_CORRECT_M)
            box_size = options.get('box_size', 10)
            border = options.get('border', 4)
            
            # Génération du QR code
            qr = qrcode.QRCode(
                version=version,
                error_correction=error_correction,
                box_size=box_size,
                border=border,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            module_drawer = self.module_drawers.get(module_shape, {'drawer': SquareModuleDrawer()})['drawer']
            color_mask_class = self.color_masks.get(color_mask, {'class': SolidFillColorMask})['class']
            
            # Options du masque de couleur
            color_mask_kwargs = {}
            if color_mask == 'solid':
                color_mask_kwargs = {
                    'front_color': options.get('front_color', (0, 0, 0)),
                    'back_color': options.get('back_color', (255, 255, 255))
                }
            elif color_mask in ['radial_gradient', 'square_gradient']:
                color_mask_kwargs = {
                    'center_color': options.get('front_color', (0, 102, 204)),
                    'edge_color': options.get('edge_color', (0, 51, 153)),
                    'back_color': options.get('back_color', (255, 255, 255))
                }
            elif color_mask == 'horizontal_gradient':
                color_mask_kwargs = {
                    'left_color': options.get('front_color', (255, 102, 0)),
                    'right_color': options.get('edge_color', (204, 0, 0)),
                    'back_color': options.get('back_color', (255, 255, 255))
                }
            elif color_mask == 'vertical_gradient':
                color_mask_kwargs = {
                    'top_color': options.get('front_color', (0, 153, 0)),
                    'bottom_color': options.get('edge_color', (0, 51, 0)),
                    'back_color': options.get('back_color', (255, 255, 255))
                }
            else:
                color_mask_kwargs = {
                    'front_color': options.get('front_color', (0, 0, 0)),
                    'back_color': options.get('back_color', (255, 255, 255))
                }
            
            # Création du masque de couleur
            color_mask = color_mask_class(**color_mask_kwargs)
            
            # Création de l'image
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=module_drawer,
                color_mask=color_mask
            )
            
            # Personnalisation des yeux si demandé
            if 'eye_shape' in options or 'frame_shape' in options:
                eye_shape = options.get('eye_shape', 'square')
                frame_shape = options.get('frame_shape', 'square')
                
                img_pil = img.get_image() if hasattr(img, 'get_image') else img
                img = self._customize_markers(img_pil, qr, frame_shape, eye_shape, options)
        else:
            # Style par défaut si aucun style n'est spécifié
            qr = qrcode.QRCode(
                version=options.get('version', 1),
                error_correction=options.get('error_correction', qrcode.constants.ERROR_CORRECT_M),
                box_size=options.get('box_size', 10),
                border=options.get('border', 4),
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(
                fill_color=options.get('front_color', 'black'),
                back_color=options.get('back_color', 'white')
            )
        
        # Conversion en base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"


# Classes personnalisées pour les formes de modules


class GappedSquareDrawer(SquareModuleDrawer):
    """Drawer qui dessine des carrés avec un espacement."""
    
    def __init__(self, gap_width=0.1):
        super().__init__()
        self.gap_width = gap_width
    
    def drawrect(self, box, is_active, context):
        if not is_active:
            return
        
        # Calcul des dimensions avec l'espacement
        gap = self.gap_width * box[2]  # largeur de l'espace basée sur la largeur du carré
        x, y, w, h = box
        
        # Dessiner un carré légèrement plus petit
        x += gap / 2
        y += gap / 2
        w -= gap
        h -= gap
        
        # Dessiner le carré avec les dimensions réduites
        context.rectangle((x, y, w, h))


class DiamondModuleDrawer:
    """Drawer qui dessine des modules en forme de losange."""
    
    def __init__(self, module_scale=1.0):
        self.module_scale = module_scale
    
    def drawrect(self, box, is_active, context):
        if not is_active:
            return
        
        x, y, w, h = box
        
        # Points du losange
        cx, cy = x + w/2, y + h/2
        size = min(w, h) * self.module_scale
        
        points = [
            (cx, cy - size/2),  # haut
            (cx + size/2, cy),  # droite
            (cx, cy + size/2),  # bas
            (cx - size/2, cy)   # gauche
        ]
        
        # Dessiner le losange
        context.polygon(points)


class PixelModuleDrawer:
    """Drawer qui dessine des modules avec un effet pixelisé."""
    
    def __init__(self, pixel_scale=0.2):
        self.pixel_scale = pixel_scale
    
    def drawrect(self, box, is_active, context):
        if not is_active:
            return
        
        x, y, w, h = box
        
        # Taille des pixels
        pixel_size = min(w, h) * self.pixel_scale
        
        # Dessiner une grille de petits carrés
        for i in range(int(x), int(x + w), int(pixel_size)):
            for j in range(int(y), int(y + h), int(pixel_size)):
                context.rectangle((i, j, pixel_size, pixel_size))


class RoundedVerticalBarsDrawer(VerticalBarsDrawer):
    """Drawer qui dessine des barres verticales aux extrémités arrondies."""
    
    def drawrect(self, box, is_active, context):
        if not is_active:
            return
        
        x, y, w, h = box
        
        # Dessiner une barre verticale
        bar_width = w * 0.8
        bar_x = x + (w - bar_width) / 2
        
        # Rectangle principal de la barre
        context.rectangle((bar_x, y, bar_width, h))
        
        # Demi-cercles aux extrémités
        radius = bar_width / 2
        context.arc((bar_x + radius, y + radius), radius, 180, 0)
        context.arc((bar_x + radius, y + h - radius), radius, 0, 180)


class RoundedHorizontalBarsDrawer(HorizontalBarsDrawer):
    """Drawer qui dessine des barres horizontales aux extrémités arrondies."""
    
    def drawrect(self, box, is_active, context):
        if not is_active:
            return
        
        x, y, w, h = box
        
        # Dessiner une barre horizontale
        bar_height = h * 0.8
        bar_y = y + (h - bar_height) / 2
        
        # Rectangle principal de la barre
        context.rectangle((x, bar_y, w, bar_height))
        
        # Demi-cercles aux extrémités
        radius = bar_height / 2
        context.arc((x + radius, bar_y + radius), radius, 90, 270)
        context.arc((x + w - radius, bar_y + radius), radius, 270, 90)


# Classes personnalisées pour les masques de couleur


class DiagonalGradiantColorMask(SquareGradiantColorMask):
    """Masque avec un dégradé diagonal."""
    
    def __init__(self, top_left_color=(0, 0, 0), bottom_right_color=(100, 100, 100), back_color=(255, 255, 255)):
        super().__init__(center_color=top_left_color, edge_color=bottom_right_color, back_color=back_color)
        self.top_left_color = top_left_color
        self.bottom_right_color = bottom_right_color
    
    def get_fg_pixel(self, image, x, y):
        """Return the foreground pixel."""
        image_width, image_height = image.size
        
        # Position normalisée (0-1)
        nx = x / image_width
        ny = y / image_height
        
        # Calcul de la position diagonale (0-1)
        diagonal_pos = (nx + ny) / 2
        
        # Interpolation linéaire entre les couleurs
        r = int(self.top_left_color[0] + (self.bottom_right_color[0] - self.top_left_color[0]) * diagonal_pos)
        g = int(self.top_left_color[1] + (self.bottom_right_color[1] - self.top_left_color[1]) * diagonal_pos)
        b = int(self.top_left_color[2] + (self.bottom_right_color[2] - self.top_left_color[2]) * diagonal_pos)
        
        return (r, g, b)


class RainbowColorMask:
    """Masque avec un dégradé arc-en-ciel."""
    
    def __init__(self, back_color=(255, 255, 255), colors=None):
        self.back_color = back_color
        if colors is None:
            self.colors = [
                (255, 0, 0),    # Rouge
                (255, 165, 0),  # Orange
                (255, 255, 0),  # Jaune
                (0, 255, 0),    # Vert
                (0, 0, 255),    # Bleu
                (75, 0, 130),   # Indigo
                (238, 130, 238) # Violet
            ]
        else:
            self.colors = colors
    
    def get_fg_pixel(self, image, x, y):
        """Return the foreground pixel with a rainbow pattern."""
        image_width, image_height = image.size
        
        # Position normalisée (0-1)
        ny = y / image_height
        
        # Sélectionner la couleur en fonction de la position verticale
        num_colors = len(self.colors)
        color_index = int(ny * num_colors)
        color_index = max(0, min(color_index, num_colors - 2))  # Garantir un indice valide pour l'interpolation
        
        # Position exacte entre les deux couleurs
        color_frac = (ny * num_colors) - color_index
        
        # Interpolation entre les deux couleurs
        color1 = self.colors[color_index]
        color2 = self.colors[color_index + 1]
        
        r = int(color1[0] + (color2[0] - color1[0]) * color_frac)
        g = int(color1[1] + (color2[1] - color1[1]) * color_frac)
        b = int(color1[2] + (color2[2] - color1[2]) * color_frac)
        
        return (r, g, b)
    
    def get_bg_pixel(self, image, x, y):
        """Return the background pixel."""
        return self.back_color


# Fonction d'importation de la bibliothèque math (pour cos, sin, pi)
from math import cos, sin, pi
