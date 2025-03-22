#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module de gestion des QR codes avec intégration d'icônes de réseaux sociaux.
Ce module fournit des fonctionnalités pour créer des QR codes thématiques 
pour les réseaux sociaux et ajouter des icônes sociales aux QR codes générés.
"""

import os
import uuid
import math
import requests
import base64
from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageEnhance
import qrcode
from qrcode.image.styledpil import StyledPilImage


class SocialIconLibrary:
    """
    Bibliothèque d'icônes de réseaux sociaux prédéfinies.
    Fournit des méthodes pour récupérer et manipuler des icônes de réseaux sociaux.
    """

    def __init__(self, icons_dir=None, download_if_missing=True):
        """
        Initialise la bibliothèque d'icônes de réseaux sociaux.
        
        Args:
            icons_dir (str, optional): Répertoire de stockage des icônes.
                Si non spécifié, utilise le sous-répertoire 'social_icons' du répertoire courant.
            download_if_missing (bool): Télécharge automatiquement les icônes manquantes
        """
        # Répertoire par défaut des icônes
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.icons_dir = icons_dir or os.path.join(current_dir, '..', '..', 'frontend', 'static', 'img', 'social_icons')
        
        # Création du répertoire s'il n'existe pas
        os.makedirs(self.icons_dir, exist_ok=True)
        
        # Configuration des icônes
        self.icons_config = {
            'facebook': {
                'name': 'Facebook',
                'color': '#1877F2',
                'filename': 'facebook.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/facebook.svg',
                'formats': ['png', 'svg']
            },
            'twitter': {
                'name': 'Twitter',
                'color': '#1DA1F2',
                'filename': 'twitter.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/twitter.svg',
                'formats': ['png', 'svg']
            },
            'instagram': {
                'name': 'Instagram',
                'color': '#E4405F',
                'filename': 'instagram.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/instagram.svg',
                'formats': ['png', 'svg']
            },
            'linkedin': {
                'name': 'LinkedIn',
                'color': '#0A66C2',
                'filename': 'linkedin.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/linkedin.svg',
                'formats': ['png', 'svg']
            },
            'youtube': {
                'name': 'YouTube',
                'color': '#FF0000',
                'filename': 'youtube.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/youtube.svg',
                'formats': ['png', 'svg']
            },
            'tiktok': {
                'name': 'TikTok',
                'color': '#000000',
                'filename': 'tiktok.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/tiktok.svg',
                'formats': ['png', 'svg']
            },
            'snapchat': {
                'name': 'Snapchat',
                'color': '#FFFC00',
                'filename': 'snapchat.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/snapchat.svg',
                'formats': ['png', 'svg']
            },
            'pinterest': {
                'name': 'Pinterest',
                'color': '#E60023',
                'filename': 'pinterest.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/pinterest.svg',
                'formats': ['png', 'svg']
            },
            'whatsapp': {
                'name': 'WhatsApp',
                'color': '#25D366',
                'filename': 'whatsapp.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/whatsapp.svg',
                'formats': ['png', 'svg']
            },
            'telegram': {
                'name': 'Telegram',
                'color': '#26A5E4',
                'filename': 'telegram.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/telegram.svg',
                'formats': ['png', 'svg']
            },
            'reddit': {
                'name': 'Reddit',
                'color': '#FF4500',
                'filename': 'reddit.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/reddit.svg',
                'formats': ['png', 'svg']
            },
            'github': {
                'name': 'GitHub',
                'color': '#181717',
                'filename': 'github.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/github.svg',
                'formats': ['png', 'svg']
            },
            'discord': {
                'name': 'Discord',
                'color': '#5865F2',
                'filename': 'discord.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/discord.svg',
                'formats': ['png', 'svg']
            },
            'twitch': {
                'name': 'Twitch',
                'color': '#9146FF',
                'filename': 'twitch.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/twitch.svg',
                'formats': ['png', 'svg']
            },
            'vimeo': {
                'name': 'Vimeo',
                'color': '#1AB7EA',
                'filename': 'vimeo.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/vimeo.svg',
                'formats': ['png', 'svg']
            },
            'email': {
                'name': 'Email',
                'color': '#EA4335',
                'filename': 'email.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/gmail.svg',
                'formats': ['png', 'svg']
            },
            'website': {
                'name': 'Site Web',
                'color': '#4285F4',
                'filename': 'website.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/googlechrome.svg',
                'formats': ['png', 'svg']
            },
            'phone': {
                'name': 'Téléphone',
                'color': '#0F9D58',
                'filename': 'phone.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/phone.svg',
                'formats': ['png', 'svg']
            },
            'spotify': {
                'name': 'Spotify',
                'color': '#1DB954',
                'filename': 'spotify.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/spotify.svg',
                'formats': ['png', 'svg']
            },
            'apple': {
                'name': 'Apple',
                'color': '#000000',
                'filename': 'apple.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/apple.svg',
                'formats': ['png', 'svg']
            },
            'google': {
                'name': 'Google',
                'color': '#4285F4',
                'filename': 'google.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v7/icons/google.svg',
                'formats': ['png', 'svg']
            }
        }
        
        # Vérification et téléchargement des icônes manquantes
        if download_if_missing:
            self.check_and_download_icons()
    
    def check_and_download_icons(self):
        """
        Vérifie la présence des icônes et télécharge celles qui sont manquantes.
        """
        for platform, config in self.icons_config.items():
            # Vérification du fichier PNG
            png_path = os.path.join(self.icons_dir, config['filename'])
            if not os.path.exists(png_path):
                self._download_icon(platform)
            
            # Vérification du fichier SVG
            svg_filename = f"{os.path.splitext(config['filename'])[0]}.svg"
            svg_path = os.path.join(self.icons_dir, svg_filename)
            if not os.path.exists(svg_path) and 'svg' in config.get('formats', []):
                self._download_icon(platform, 'svg')
    
    def _download_icon(self, platform, format_type='png'):
        """
        Télécharge l'icône d'une plateforme spécifique.
        
        Args:
            platform (str): Nom de la plateforme
            format_type (str): Format de l'icône ('png' ou 'svg')
        
        Returns:
            bool: True si le téléchargement réussit, False sinon
        """
        if platform not in self.icons_config:
            return False
        
        config = self.icons_config[platform]
        url = config['url']
        
        try:
            # Téléchargement de l'icône
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            if format_type == 'svg':
                # Sauvegarde directe du SVG
                svg_filename = f"{os.path.splitext(config['filename'])[0]}.svg"
                svg_path = os.path.join(self.icons_dir, svg_filename)
                with open(svg_path, 'wb') as f:
                    f.write(response.content)
            else:
                # Conversion du SVG en PNG coloré
                try:
                    from cairosvg import svg2png
                    
                    # Modifier la couleur du SVG
                    svg_content = response.text
                    svg_content = svg_content.replace('fill="currentColor"', f'fill="{config["color"]}"')
                    
                    # Convertir en PNG
                    png_path = os.path.join(self.icons_dir, config['filename'])
                    svg2png(bytestring=svg_content.encode('utf-8'), write_to=png_path, output_width=200, output_height=200)
                except ImportError:
                    # Si cairosvg n'est pas disponible, créer une icône de secours
                    self._create_fallback_icon(platform)
            
            return True
            
        except Exception as e:
            print(f"Erreur lors du téléchargement de l'icône {platform}: {e}")
            
            # Création d'une icône de secours
            if format_type == 'png':
                self._create_fallback_icon(platform)
            
            return False
    
    def _create_fallback_icon(self, platform):
        """
        Crée une icône de secours pour une plateforme.
        
        Args:
            platform (str): Nom de la plateforme
        """
        if platform not in self.icons_config:
            return
        
        config = self.icons_config[platform]
        
        # Création d'une image avec la première lettre
        size = 200
        img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Dessin du cercle de fond
        color = config.get('color', '#000000')
        if color.startswith('#'):
            # Conversion hex en RGB
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            color_rgb = (r, g, b, 255)
        else:
            color_rgb = (0, 0, 0, 255)
        
        # Dessiner le cercle
        draw.ellipse((0, 0, size, size), fill=color_rgb)
        
        # Ajouter la lettre
        letter = config.get('name', platform)[0].upper()
        
        # Utiliser une police par défaut
        font_size = size // 2
        try:
            # Essayer de charger une police
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # Sinon utiliser la police par défaut
            font = ImageFont.load_default()
        
        # Calculer la position du texte pour le centrer
        text_width, text_height = draw.textsize(letter, font=font) if hasattr(draw, 'textsize') else font.getsize(letter)
        position = ((size - text_width) // 2, (size - text_height) // 2)
        
        # Dessiner le texte
        draw.text(position, letter, fill=(255, 255, 255, 255), font=font)
        
        # Sauvegarder l'image
        png_path = os.path.join(self.icons_dir, config['filename'])
        img.save(png_path)
    
    def get_icon_path(self, platform, format_type='png'):
        """
        Obtient le chemin d'une icône de réseau social.
        
        Args:
            platform (str): Nom de la plateforme ('facebook', 'twitter', etc.)
            format_type (str): Format de l'icône ('png' ou 'svg')
        
        Returns:
            str: Chemin de l'icône, ou None si la plateforme n'existe pas
        """
        if platform not in self.icons_config:
            return None
        
        config = self.icons_config[platform]
        
        if format_type == 'svg':
            filename = f"{os.path.splitext(config['filename'])[0]}.svg"
        else:
            filename = config['filename']
        
        icon_path = os.path.join(self.icons_dir, filename)
        
        # Vérifier si l'icône existe
        if not os.path.exists(icon_path):
            if self._download_icon(platform, format_type):
                return icon_path
            else:
                return None
        
        return icon_path
    
    def get_icon_color(self, platform):
        """
        Obtient la couleur officielle d'une plateforme sociale.
        
        Args:
            platform (str): Nom de la plateforme ('facebook', 'twitter', etc.)
        
        Returns:
            str: Code hexadécimal de la couleur, ou noir par défaut
        """
        if platform in self.icons_config:
            return self.icons_config[platform].get('color', '#000000')
        return '#000000'
    
    def get_platform_name(self, platform):
        """
        Obtient le nom complet d'une plateforme sociale.
        
        Args:
            platform (str): Identifiant de la plateforme ('facebook', 'twitter', etc.)
        
        Returns:
            str: Nom complet de la plateforme, ou l'identifiant si non trouvé
        """
        if platform in self.icons_config:
            return self.icons_config[platform].get('name', platform)
        return platform
    
    def get_all_platforms(self):
        """
        Obtient la liste de toutes les plateformes disponibles.
        
        Returns:
            list: Liste des plateformes avec leurs informations
        """
        platforms = []
        for platform, config in self.icons_config.items():
            icon_url = f"/static/img/social_icons/{config['filename']}"
            platforms.append({
                'id': platform,
                'name': config['name'],
                'color': config['color'],
                'icon_url': icon_url
            })
        
        return platforms
    
    def resize_icon(self, platform, size=(64, 64)):
        """
        Redimensionne une icône à la taille spécifiée.
        
        Args:
            platform (str): Nom de la plateforme
            size (tuple): Dimensions (largeur, hauteur)
        
        Returns:
            Image: Objet PIL Image contenant l'icône redimensionnée
        """
        icon_path = self.get_icon_path(platform)
        if not icon_path:
            return None
        
        try:
            img = Image.open(icon_path)
            return img.resize(size, Image.LANCZOS)
        except Exception as e:
            print(f"Erreur lors du redimensionnement de l'icône {platform}: {e}")
            return None


class SocialQRGenerator:
    """
    Générateur de QR codes avec intégration d'icônes de réseaux sociaux.
    Fournit des méthodes pour créer des QR codes thématiques et multi-sociaux.
    """

    def __init__(self, output_dir=None, icon_library=None):
        """
        Initialise le générateur de QR codes social.
        
        Args:
            output_dir (str, optional): Répertoire de sortie pour les QR codes générés.
                Si non spécifié, utilise le répertoire courant.
            icon_library (SocialIconLibrary, optional): Bibliothèque d'icônes à utiliser.
                Si non spécifiée, crée une nouvelle instance.
        """
        self.output_dir = output_dir or os.path.join(os.getcwd(), 'generated_qrcodes')
        
        # Création du répertoire de sortie s'il n'existe pas
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialisation de la bibliothèque d'icônes
        self.icon_library = icon_library or SocialIconLibrary()
        
        # Création du répertoire de métadonnées
        self.metadata_dir = os.path.join(self.output_dir, 'metadata')
        os.makedirs(self.metadata_dir, exist_ok=True)
    
    def generate_social_qrcode(self, data, platform, filename=None, **options):
        """
        Génère un QR code aux couleurs d'une plateforme sociale spécifique.
        
        Args:
            data (str): Données à encoder dans le QR code (URL, texte, etc.)
            platform (str): Plateforme sociale ('facebook', 'twitter', etc.)
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour la génération du QR code.
                - version (int): Version du QR code
                - error_correction (int): Niveau de correction d'erreur
                - box_size (int): Taille de chaque "boîte" du QR code en pixels
                - border (int): Taille de la bordure en nombre de boîtes
                - fill_color (str/tuple): Couleur de remplissage (remplace la couleur de la plateforme)
                - back_color (str/tuple): Couleur d'arrière-plan du QR code
                - add_icon (bool): Ajouter l'icône de la plateforme au centre du QR code
                - icon_size (float): Taille de l'icône en pourcentage du QR code (0.0-1.0)
            
        Returns:
            str: Chemin du fichier QR code généré.
        """
        if not filename:
            filename = f"social_qrcode_{platform}_{uuid.uuid4().hex}.png"
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Options par défaut
        version = int(options.get('version', 1))
        
        # Niveau de correction d'erreur (0=L, 1=M, 2=Q, 3=H)
        error_level = int(options.get('error_correction', 1))
        error_correction_map = {
            0: qrcode.constants.ERROR_CORRECT_L,
            1: qrcode.constants.ERROR_CORRECT_M,
            2: qrcode.constants.ERROR_CORRECT_Q,
            3: qrcode.constants.ERROR_CORRECT_H
        }
        error_correction = error_correction_map.get(error_level, qrcode.constants.ERROR_CORRECT_M)
        
        box_size = int(options.get('box_size', 10))
        border = int(options.get('border', 4))
        
        # Couleurs
        # Si une couleur de remplissage est spécifiée, l'utiliser, sinon utiliser la couleur de la plateforme
        if 'fill_color' in options:
            fill_color = options['fill_color']
        else:
            fill_color = self.icon_library.get_icon_color(platform)
        
        back_color = options.get('back_color', "white")
        
        # Génération du QR code
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Génération de l'image QR code
        qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGBA')
        
        # Ajout de l'icône de la plateforme si demandé
        if options.get('add_icon', True):
            # Récupération de l'icône
            icon_size_percent = float(options.get('icon_size', 0.2))  # 20% par défaut
            qr_width, qr_height = qr_img.size
            icon_size = int(min(qr_width, qr_height) * icon_size_percent)
            
            # Redimensionnement de l'icône
            icon = self.icon_library.resize_icon(platform, (icon_size, icon_size))
            
            if icon:
                # Position de l'icône (centre)
                icon_pos = ((qr_width - icon_size) // 2, (qr_height - icon_size) // 2)
                
                # Création d'un cercle blanc pour le fond de l'icône
                circle = Image.new('RGBA', (icon_size + 20, icon_size + 20), (255, 255, 255, 255))
                
                # Dessiner un cercle blanc parfait
                circle_draw = ImageDraw.Draw(circle)
                circle_draw.ellipse((0, 0, icon_size + 19, icon_size + 19), fill=(255, 255, 255, 255))
                
                # Placer l'icône au centre du cercle
                circle.paste(icon, (10, 10), icon)
                
                # Position du cercle (centre)
                circle_pos = ((qr_width - icon_size - 20) // 2, (qr_height - icon_size - 20) // 2)
                
                # Superposition du cercle sur le QR code
                qr_img.paste(circle, circle_pos, circle)
        
        # Sauvegarde de l'image finale
        qr_img.save(output_path)
        
        # Enregistrement des métadonnées
        metadata = {
            'data': data,
            'platform': platform,
            'platform_name': self.icon_library.get_platform_name(platform),
            'platform_color': fill_color,
            **options
        }
        self._save_metadata(metadata, output_path)
        
        return output_path
    
    def generate_multi_social_qrcode(self, data, platforms, filename=None, **options):
        """
        Génère un QR code avec plusieurs icônes sociales.
        
        Args:
            data (str): Données à encoder dans le QR code (URL, texte, etc.)
            platforms (list): Liste des plateformes sociales à inclure
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour la génération du QR code.
                - version (int): Version du QR code
                - error_correction (int): Niveau de correction d'erreur
                - box_size (int): Taille de chaque "boîte" du QR code en pixels
                - border (int): Taille de la bordure en nombre de boîtes
                - fill_color (str/tuple): Couleur de remplissage du QR code
                - back_color (str/tuple): Couleur d'arrière-plan du QR code
                - layout (str): Disposition des icônes ('circle', 'line', 'grid')
                - icon_size (float): Taille des icônes en pourcentage du QR code
            
        Returns:
            str: Chemin du fichier QR code généré.
        """
        if not filename:
            filename = f"multi_social_qrcode_{uuid.uuid4().hex}.png"
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Vérification des plateformes
        if not platforms:
            raise ValueError("Aucune plateforme spécifiée")
        
        # Filtrage des plateformes valides
        valid_platforms = [p for p in platforms if p in self.icon_library.icons_config]
        
        if not valid_platforms:
            raise ValueError("Aucune plateforme valide spécifiée")
        
        # Options par défaut
        version = int(options.get('version', 1))
        
        # Niveau de correction d'erreur (0=L, 1=M, 2=Q, 3=H)
        error_level = int(options.get('error_correction', 3))  # H par défaut pour les multi-icônes
        error_correction_map = {
            0: qrcode.constants.ERROR_CORRECT_L,
            1: qrcode.constants.ERROR_CORRECT_M,
            2: qrcode.constants.ERROR_CORRECT_Q,
            3: qrcode.constants.ERROR_CORRECT_H
        }
        error_correction = error_correction_map.get(error_level, qrcode.constants.ERROR_CORRECT_H)
        
        box_size = int(options.get('box_size', 10))
        border = int(options.get('border', 4))
        
        # Couleurs
        fill_color = options.get('fill_color', "black")
        back_color = options.get('back_color', "white")
        
        # Génération du QR code
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Génération de l'image QR code
        qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGBA')
        qr_width, qr_height = qr_img.size
        
        # Disposition des icônes
        layout = options.get('layout', 'circle').lower()
        
        # Taille des icônes individuelles
        icon_size_percent = float(options.get('icon_size', 0.15))  # 15% par défaut pour plusieurs icônes
        base_icon_size = int(min(qr_width, qr_height) * icon_size_percent)
        
        # Nombre d'icônes
        num_icons = len(valid_platforms)
        
        # Création d'un masque blanc au centre du QR code
        mask_size = int(min(qr_width, qr_height) * 0.4)  # Taille du masque central
        mask = Image.new('RGBA', (mask_size, mask_size), (255, 255, 255, 255))
        
        # Création d'un masque circulaire
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, mask_size - 1, mask_size - 1), fill=(255, 255, 255, 255))
        
        # Position du masque (centre)
        mask_pos = ((qr_width - mask_size) // 2, (qr_height - mask_size) // 2)
        
        # Superposition du masque sur le QR code
        qr_img.paste(mask, mask_pos, mask)
        
        # Positions des icônes selon la disposition
        icon_positions = []
        
        if layout == 'circle':
            # Disposition en cercle
            radius = mask_size // 3
            center_x = qr_width // 2
            center_y = qr_height // 2
            
            for i in range(num_icons):
                angle = 2 * math.pi * i / num_icons
                x = center_x + int(radius * math.cos(angle)) - base_icon_size // 2
                y = center_y + int(radius * math.sin(angle)) - base_icon_size // 2
                icon_positions.append((x, y))
                
        elif layout == 'line':
            # Disposition en ligne horizontale
            total_width = num_icons * base_icon_size
            start_x = (qr_width - total_width) // 2
            y = qr_height // 2 - base_icon_size // 2
            
            for i in range(num_icons):
                x = start_x + i * base_icon_size
                icon_positions.append((x, y))
                
        elif layout == 'grid':
            # Disposition en grille
            # Calculer le nombre de lignes et de colonnes
            cols = int(math.ceil(math.sqrt(num_icons)))
            rows = int(math.ceil(num_icons / cols))
            
            # Taille totale de la grille
            grid_width = cols * base_icon_size
            grid_height = rows * base_icon_size
            
            # Position de départ (centre)
            start_x = (qr_width - grid_width) // 2
            start_y = (qr_height - grid_height) // 2
            
            for i in range(num_icons):
                col = i % cols
                row = i // cols
                x = start_x + col * base_icon_size
                y = start_y + row * base_icon_size
                icon_positions.append((x, y))
        
        else:
            # Disposition par défaut (une seule icône au centre)
            icon_positions = [((qr_width - base_icon_size) // 2, (qr_height - base_icon_size) // 2)]
        
        # Ajout des icônes
        for i, platform in enumerate(valid_platforms):
            if i >= len(icon_positions):
                break
                
            # Récupération de l'icône
            icon = self.icon_library.resize_icon(platform, (base_icon_size, base_icon_size))
            
            if icon:
                # Position de l'icône
                icon_pos = icon_positions[i]
                
                # Superposition de l'icône sur le QR code
                qr_img.paste(icon, icon_pos, icon)
        
        # Sauvegarde de l'image finale
        qr_img.save(output_path)
        
        # Enregistrement des métadonnées
        metadata = {
            'data': data,
            'platforms': valid_platforms,
            'layout': layout,
            **options
        }
        self._save_metadata(metadata, output_path)
        
        return output_path
    
    def _save_metadata(self, metadata, output_path):
        """
        Enregistre les métadonnées du QR code généré.
        
        Args:
            metadata (dict): Métadonnées du QR code
            output_path (str): Chemin du fichier QR code généré
        """
        # Nom du fichier de métadonnées basé sur le nom du QR code
        qr_filename = os.path.basename(output_path)
        metadata_filename = f"{os.path.splitext(qr_filename)[0]}.txt"
        metadata_path = os.path.join(self.metadata_dir, metadata_filename)
        
        # Création du contenu des métadonnées
        metadata_content = [
            f"Date de création: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Fichier: {qr_filename}",
        ]
        
        # Ajout des métadonnées
        for key, value in metadata.items():
            metadata_content.append(f"{key}: {value}")
        
        # Écriture des métadonnées dans le fichier
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(metadata_content))
