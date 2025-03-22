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
from PIL import Image, ImageDraw
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
            preview_type (str): Type de prévisualisation ('basic', 'custom', 'styled', 'logo', 'social', 'custom_shape')
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
        
        elif preview_type == 'custom_shape':
            module_shape = options.get('module_shape', 'square')
            frame_shape = options.get('frame_shape', 'square')
            eye_shape = options.get('eye_shape', 'square')
            fill_color = options.get('fill_color', "black")
            back_color = options.get('back_color', "white")
            img = self._generate_custom_shape_preview(data, version, error_correction, box_size, border, 
                                                    module_shape, frame_shape, eye_shape, fill_color, back_color)
        
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
        elif color_mask_name == 'horizontal_gradient':
            color_mask_kwargs = {
                'left_color': options.get('front_color', (0, 0, 0)),
                'right_color': options.get('edge_color', (100, 100, 100)),
                'back_color': options.get('back_color', (255, 255, 255))
            }
        elif color_mask_name == 'vertical_gradient':
            color_mask_kwargs = {
                'top_color': options.get('front_color', (0, 0, 0)),
                'bottom_color': options.get('edge_color', (100, 100, 100)),
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
        
        # Création d'une image QR code simple
        # Dans une implémentation réelle, nous ajouterions l'icône sociale
        qr_img = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        # Simuler l'ajout d'une icône sociale (simplifié pour la prévisualisation)
        qr_pil = qr_img.get_image() if hasattr(qr_img, 'get_image') else qr_img
        
        # Dessiner un cercle central ou un carré pour simuler l'icône
        draw = ImageDraw.Draw(qr_pil)
        width, height = qr_pil.size
        center_size = min(width, height) // 5
        position = ((width - center_size) // 2, (height - center_size) // 2)
        
        if social_platform in ['facebook', 'twitter', 'linkedin']:
            # Cercle bleu pour certains réseaux
            draw.ellipse([position, (position[0] + center_size, position[1] + center_size)], fill=(59, 89, 152))
        elif social_platform in ['instagram', 'youtube']:
            # Carré rouge/rose pour d'autres
            draw.rectangle([position, (position[0] + center_size, position[1] + center_size)], fill=(225, 48, 108))
        else:
            # Rectangle vert pour les autres
            draw.rectangle([position, (position[0] + center_size, position[1] + center_size)], fill=(37, 211, 102))
        
        return qr_pil
    
    def _generate_custom_shape_preview(self, data, version, error_correction, box_size, border, 
                                    module_shape, frame_shape, eye_shape, fill_color, back_color):
        """
        Génère une prévisualisation de QR code avec des formes personnalisées.
        
        Args:
            data (str): Données à encoder dans le QR code
            version (int): Version du QR code
            error_correction: Niveau de correction d'erreur
            box_size (int): Taille de chaque "boîte" du QR code en pixels
            border (int): Taille de la bordure en nombre de boîtes
            module_shape (str): Forme des modules
            frame_shape (str): Forme des contours des yeux
            eye_shape (str): Forme des centres des yeux
            fill_color: Couleur de remplissage
            back_color: Couleur d'arrière-plan
            
        Returns:
            PIL.Image: Image QR code générée
        """
        # Génération du QR code avec le style de module personnalisé
        module_drawer = self.module_drawers.get(module_shape, SquareModuleDrawer())
        
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Création de l'image QR code
        qr_img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=SolidFillColorMask(front_color=fill_color, back_color=back_color)
        )
        
        # Conversion en mode PIL Image pour traitement avancé
        pil_img = qr_img.get_image() if hasattr(qr_img, 'get_image') else qr_img
        
        # Application des formes personnalisées pour les yeux (simplifié pour la prévisualisation)
        if frame_shape != 'square' or eye_shape != 'square':
            # Dimensions de l'image
            width, height = pil_img.size
            
            # Estimation de la taille d'un module
            module_size = min(width, height) // 25
            
            # Positions approximatives des trois yeux de détection
            eye_positions = [
                (border * box_size, border * box_size),  # Haut-gauche
                (width - 7 * module_size, border * box_size),  # Haut-droit
                (border * box_size, height - 7 * module_size)  # Bas-gauche
            ]
            
            # Taille approximative des yeux
            eye_size = 7 * module_size
            
            # Création d'une copie de l'image pour les modifications
            enhanced_img = pil_img.copy()
            draw = ImageDraw.Draw(enhanced_img)
            
            # Dessiner les formes des yeux personnalisés
            for x, y in eye_positions:
                # Contour extérieur
                if frame_shape == 'circle':
                    draw.ellipse([(x, y), (x + eye_size, y + eye_size)], fill=fill_color)
                    # Cercle intérieur (vide)
                    inner_size = eye_size * 5/7
                    inner_x = x + (eye_size - inner_size) / 2
                    inner_y = y + (eye_size - inner_size) / 2
                    draw.ellipse([(inner_x, inner_y), (inner_x + inner_size, inner_y + inner_size)], fill=back_color)
                elif frame_shape == 'rounded_square':
                    # Simuler un carré arrondi (simplifié)
                    draw.rectangle([(x, y), (x + eye_size, y + eye_size)], fill=fill_color)
                    # Carré intérieur (vide)
                    inner_size = eye_size * 5/7
                    inner_x = x + (eye_size - inner_size) / 2
                    inner_y = y + (eye_size - inner_size) / 2
                    draw.rectangle([(inner_x, inner_y), (inner_x + inner_size, inner_y + inner_size)], fill=back_color)
                
                # Centre de l'œil
                center_size = eye_size * 3/7
                center_x = x + 2 * module_size
                center_y = y + 2 * module_size
                
                if eye_shape == 'circle':
                    draw.ellipse([(center_x, center_y), (center_x + center_size, center_y + center_size)], fill=fill_color)
                elif eye_shape == 'diamond':
                    # Points du diamant
                    points = [
                        (center_x + center_size/2, center_y),  # haut
                        (center_x + center_size, center_y + center_size/2),  # droite
                        (center_x + center_size/2, center_y + center_size),  # bas
                        (center_x, center_y + center_size/2)  # gauche
                    ]
                    draw.polygon(points, fill=fill_color)
                else:
                    draw.rectangle([(center_x, center_y), (center_x + center_size, center_y + center_size)], fill=fill_color)
            
            return enhanced_img
        
        return pil_img


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
    def _parse_color(self, color):
        """
        Convertit une couleur de différents formats (hex, nom, rgb) en tuple RGB.
        
        Args:
            color: Couleur à convertir (str ou tuple)
            
        Returns:
            tuple: Tuple RGB (r, g, b)
        """
        if isinstance(color, tuple):
            return color
        
        if isinstance(color, str):
            # Conversion des codes hexadécimaux
            if color.startswith('#'):
                color = color.lstrip('#')
                if len(color) == 3:  # Format court #RGB
                    return tuple(int(c + c, 16) for c in color)
                elif len(color) == 6:  # Format long #RRGGBB
                    return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            
            # Couleurs nommées courantes
            color_map = {
                'black': (0, 0, 0),
                'white': (255, 255, 255),
                'red': (255, 0, 0),
                'green': (0, 255, 0),
                'blue': (0, 0, 255),
                'yellow': (255, 255, 0),
                'cyan': (0, 255, 255),
                'magenta': (255, 0, 255),
                'gray': (128, 128, 128),
                'orange': (255, 165, 0),
                'purple': (128, 0, 128)
            }
            if color.lower() in color_map:
                return color_map[color.lower()]
        
        # Valeur par défaut si la conversion échoue
        return (0, 0, 0)
    
    def generate_all_style_previews(self, data="https://example.com", size=150):
        """
        Génère des prévisualisations pour tous les styles prédéfinis.
        
        Args:
            data (str): Données à encoder dans les QR codes
            size (int): Taille des prévisualisations en pixels
            
        Returns:
            dict: Dictionnaire des images base64 par nom de style
        """
        previews = {}
        
        for style_name in self.predefined_styles:
            try:
                base64_img = self.generate_preview_base64(
                    data,
                    preview_type='predefined',
                    style_name=style_name
                )
                previews[style_name] = base64_img
            except Exception as e:
                print(f"Erreur lors de la génération de la prévisualisation pour le style {style_name}: {e}")
                # En cas d'erreur, générer une image vide
                img = Image.new('RGB', (size, size), (240, 240, 240))
                draw = ImageDraw.Draw(img)
                draw.text((size//2-30, size//2-10), f"Erreur: {style_name}", fill=(200, 0, 0))
                
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                previews[style_name] = f"data:image/png;base64,{img_str}"
        
        return previews
    
    def generate_all_module_shape_previews(self, size=100):
        """
        Génère des prévisualisations pour toutes les formes de modules disponibles.
        
        Args:
            size (int): Taille des prévisualisations en pixels
            
        Returns:
            dict: Dictionnaire des images base64 par nom de forme
        """
        previews = {}
        sample_data = "SHAPE"
        
        for shape_name in self.module_drawers.keys():
            try:
                base64_img = self.generate_preview_base64(
                    sample_data,
                    preview_type='custom_shape',
                    module_shape=shape_name,
                    frame_shape='square',
                    eye_shape='square',
                    box_size=5,
                    border=2
                )
                previews[shape_name] = base64_img
            except Exception as e:
                print(f"Erreur lors de la génération de la prévisualisation pour la forme {shape_name}: {e}")
                # En cas d'erreur, générer une image vide
                img = Image.new('RGB', (size, size), (240, 240, 240))
                draw = ImageDraw.Draw(img)
                draw.text((size//2-30, size//2-10), f"Erreur: {shape_name}", fill=(200, 0, 0))
                
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                previews[shape_name] = f"data:image/png;base64,{img_str}"
        
        return previews
    
    def generate_error_correction_preview(self, data, error_levels=None):
        """
        Génère des prévisualisations pour différents niveaux de correction d'erreur.
        
        Args:
            data (str): Données à encoder dans les QR codes
            error_levels (list, optional): Liste des niveaux à prévisualiser
            
        Returns:
            dict: Dictionnaire des images base64 par niveau de correction
        """
        if error_levels is None:
            error_levels = [
                (qrcode.constants.ERROR_CORRECT_L, "L - 7%"),
                (qrcode.constants.ERROR_CORRECT_M, "M - 15%"),
                (qrcode.constants.ERROR_CORRECT_Q, "Q - 25%"),
                (qrcode.constants.ERROR_CORRECT_H, "H - 30%")
            ]
        
        previews = {}
        
        for level, name in error_levels:
            try:
                base64_img = self.generate_preview_base64(
                    data,
                    preview_type='basic',
                    error_correction=level
                )
                previews[name] = base64_img
            except Exception as e:
                print(f"Erreur lors de la génération de la prévisualisation pour le niveau {name}: {e}")
                # En cas d'erreur, on ignore cette prévisualisation
                continue
        
        return previews
    
    def add_overlay_text(self, img, text, position=None, font_size=12, color=(0, 0, 0)):
        """
        Ajoute un texte superposé à une image.
        
        Args:
            img: Image PIL sur laquelle ajouter le texte
            text (str): Texte à ajouter
            position (tuple, optional): Position (x, y) du texte. Si None, centré en bas
            font_size (int): Taille de la police
            color (tuple): Couleur RGB du texte
            
        Returns:
            PIL.Image: Image avec le texte ajouté
        """
        img_copy = img.copy()
        draw = ImageDraw.Draw(img_copy)
        
        width, height = img_copy.size
        
        if position is None:
            # Position par défaut: centré en bas
            position = (width // 2 - len(text) * font_size // 4, height - font_size * 2)
        
        # Ajout du texte
        draw.text(position, text, fill=color)
        
        return img_copy
    
    def batch_preview_generation(self, data_list, preview_type='basic', **options):
        """
        Génère des prévisualisations en lot pour plusieurs données.
        
        Args:
            data_list (list): Liste des données à encoder
            preview_type (str): Type de prévisualisation
            **options: Options supplémentaires pour la personnalisation
            
        Returns:
            list: Liste des images base64 générées
        """
        previews = []
        
        for data in data_list:
            try:
                base64_img = self.generate_preview_base64(data, preview_type, **options)
                previews.append({
                    'data': data,
                    'image': base64_img,
                    'success': True
                })
            except Exception as e:
                # En cas d'erreur, on ajoute un objet avec l'erreur
                previews.append({
                    'data': data,
                    'error': str(e),
                    'success': False
                })
        
        return previews


def hex_to_rgb(hex_color):
    """
    Convertit une couleur hexadécimale en tuple RGB.
    
    Args:
        hex_color (str): Code hexadécimal de la couleur (#RRGGBB ou #RGB)
        
    Returns:
        tuple: Tuple RGB (r, g, b)
    """
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        return tuple(int(c + c, 16) for c in hex_color)
    elif len(hex_color) == 6:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    else:
        raise ValueError(f"Format hexadécimal invalide: {hex_color}")

def rgb_to_hex(rgb_color):
    """
    Convertit un tuple RGB en couleur hexadécimale.
    
    Args:
        rgb_color (tuple): Tuple RGB (r, g, b)
        
    Returns:
        str: Code hexadécimal de la couleur (#RRGGBB)
    """
    return "#{:02x}{:02x}{:02x}".format(*rgb_color)
