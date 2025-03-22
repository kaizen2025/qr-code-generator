#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module de gestion des icônes de réseaux sociaux.
Ce module fournit une bibliothèque d'icônes prêtes à l'emploi pour les réseaux sociaux.
"""

import os
import requests
import base64
from io import BytesIO
from PIL import Image

class SocialIconLibrary:
    """
    Bibliothèque d'icônes de réseaux sociaux prédéfinies.
    Fournit des icônes vectorielles et raster pour les principales plateformes.
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
        
        # Créer le répertoire s'il n'existe pas
        os.makedirs(self.icons_dir, exist_ok=True)
        
        # Configuration des icônes
        self.icons_config = {
            'facebook': {
                'name': 'Facebook',
                'color': '#1877F2',
                'filename': 'facebook.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/facebook.svg',
                'formats': ['png', 'svg']
            },
            'twitter': {
                'name': 'Twitter',
                'color': '#1DA1F2',
                'filename': 'twitter.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/twitter.svg',
                'formats': ['png', 'svg']
            },
            'instagram': {
                'name': 'Instagram',
                'color': '#E4405F',
                'filename': 'instagram.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/instagram.svg',
                'formats': ['png', 'svg']
            },
            'linkedin': {
                'name': 'LinkedIn',
                'color': '#0A66C2',
                'filename': 'linkedin.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/linkedin.svg',
                'formats': ['png', 'svg']
            },
            'youtube': {
                'name': 'YouTube',
                'color': '#FF0000',
                'filename': 'youtube.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/youtube.svg',
                'formats': ['png', 'svg']
            },
            'tiktok': {
                'name': 'TikTok',
                'color': '#000000',
                'filename': 'tiktok.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/tiktok.svg',
                'formats': ['png', 'svg']
            },
            'snapchat': {
                'name': 'Snapchat',
                'color': '#FFFC00',
                'filename': 'snapchat.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/snapchat.svg',
                'formats': ['png', 'svg']
            },
            'pinterest': {
                'name': 'Pinterest',
                'color': '#E60023',
                'filename': 'pinterest.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/pinterest.svg',
                'formats': ['png', 'svg']
            },
            'whatsapp': {
                'name': 'WhatsApp',
                'color': '#25D366',
                'filename': 'whatsapp.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/whatsapp.svg',
                'formats': ['png', 'svg']
            },
            'telegram': {
                'name': 'Telegram',
                'color': '#26A5E4',
                'filename': 'telegram.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/telegram.svg',
                'formats': ['png', 'svg']
            },
            'reddit': {
                'name': 'Reddit',
                'color': '#FF4500',
                'filename': 'reddit.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/reddit.svg',
                'formats': ['png', 'svg']
            },
            'github': {
                'name': 'GitHub',
                'color': '#181717',
                'filename': 'github.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/github.svg',
                'formats': ['png', 'svg']
            },
            'discord': {
                'name': 'Discord',
                'color': '#5865F2',
                'filename': 'discord.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/discord.svg',
                'formats': ['png', 'svg']
            },
            'twitch': {
                'name': 'Twitch',
                'color': '#9146FF',
                'filename': 'twitch.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/twitch.svg',
                'formats': ['png', 'svg']
            },
            'vimeo': {
                'name': 'Vimeo',
                'color': '#1AB7EA',
                'filename': 'vimeo.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/vimeo.svg',
                'formats': ['png', 'svg']
            },
            'email': {
                'name': 'Email',
                'color': '#EA4335',
                'filename': 'email.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/gmail.svg',
                'formats': ['png', 'svg']
            },
            'website': {
                'name': 'Site Web',
                'color': '#4285F4',
                'filename': 'website.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/googlechrome.svg',
                'formats': ['png', 'svg']
            },
            'phone': {
                'name': 'Téléphone',
                'color': '#0F9D58',
                'filename': 'phone.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/phone.svg',
                'formats': ['png', 'svg']
            },
            'spotify': {
                'name': 'Spotify',
                'color': '#1DB954',
                'filename': 'spotify.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/spotify.svg',
                'formats': ['png', 'svg']
            },
            'apple': {
                'name': 'Apple',
                'color': '#000000',
                'filename': 'apple.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/apple.svg',
                'formats': ['png', 'svg']
            },
            'google': {
                'name': 'Google',
                'color': '#4285F4',
                'filename': 'google.png',
                'url': 'https://cdn.jsdelivr.net/npm/simple-icons@v5/icons/google.svg',
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
                from cairosvg import svg2png
                
                # Modifier la couleur du SVG
                svg_content = response.text
                svg_content = svg_content.replace('fill="currentColor"', f'fill="{config["color"]}"')
                
                # Convertir en PNG
                png_path = os.path.join(self.icons_dir, config['filename'])
                svg2png(bytestring=svg_content.encode('utf-8'), write_to=png_path, output_width=200, output_height=200)
            
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
        from PIL import Image, ImageDraw, ImageFont
        
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
        try:
            # Essayer de charger une police
            font = ImageFont.truetype("arial.ttf", size // 2)
        except:
            # Sinon utiliser la police par défaut
            font = ImageFont.load_default()
        
        # Calculer la position du texte pour le centrer
        text_width, text_height = draw.textsize(letter, font=font)
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
    
    def get_icon_url(self, platform, format_type='png'):
        """
        Obtient l'URL relative d'une icône pour l'affichage dans le frontend.
        
        Args:
            platform (str): Nom de la plateforme ('facebook', 'twitter', etc.)
            format_type (str): Format de l'icône ('png' ou 'svg')
        
        Returns:
            str: URL relative de l'icône
        """
        if platform not in self.icons_config:
            return None
        
        config = self.icons_config[platform]
        
        if format_type == 'svg':
            filename = f"{os.path.splitext(config['filename'])[0]}.svg"
        else:
            filename = config['filename']
        
        # Vérifier si l'icône existe
        icon_path = os.path.join(self.icons_dir, filename)
        if not os.path.exists(icon_path):
            if not self._download_icon(platform, format_type):
                return None
        
        # Retourner l'URL relative
        return f"/static/img/social_icons/{filename}"
    
    def get_icon_base64(self, platform):
        """
        Obtient une icône encodée en base64 pour utilisation directe dans le HTML/CSS.
        
        Args:
            platform (str): Nom de la plateforme ('facebook', 'twitter', etc.)
        
        Returns:
            str: Icône encodée en base64 avec préfixe data:image
        """
        icon_path = self.get_icon_path(platform)
        if not icon_path:
            return None
        
        try:
            with open(icon_path, 'rb') as f:
                image_data = f.read()
            
            # Déterminer le type MIME
            mime_type = 'image/png'  # Par défaut
            if icon_path.lower().endswith('.svg'):
                mime_type = 'image/svg+xml'
            elif icon_path.lower().endswith('.jpg') or icon_path.lower().endswith('.jpeg'):
                mime_type = 'image/jpeg'
            
            # Encoder en base64
            encoded = base64.b64encode(image_data).decode('utf-8')
            return f"data:{mime_type};base64,{encoded}"
            
        except Exception as e:
            print(f"Erreur lors de l'encodage de l'icône {platform}: {e}")
            return None
    
    def get_all_platforms(self):
        """
        Obtient la liste de toutes les plateformes disponibles.
        
        Returns:
            list: Liste des plateformes avec leurs informations
        """
        platforms = []
        for platform, config in self.icons_config.items():
            icon_url = self.get_icon_url(platform)
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
            BytesIO: Objet contenant l'image redimensionnée
        """
        icon_path = self.get_icon_path(platform)
        if not icon_path:
            return None
        
        try:
            img = Image.open(icon_path)
            img = img.resize(size, Image.LANCZOS)
            
            # Conversion en BytesIO pour utilisation en mémoire
            output = BytesIO()
            img.save(output, format='PNG')
            output.seek(0)
            
            return output
            
        except Exception as e:
            print(f"Erreur lors du redimensionnement de l'icône {platform}: {e}")
            return None


# Exemple d'utilisation si exécuté directement
if __name__ == "__main__":
    icon_library = SocialIconLibrary()
    
    # Obtenir la liste des plateformes disponibles
    platforms = icon_library.get_all_platforms()
    print(f"Plateformes disponibles: {len(platforms)}")
    
    # Afficher le chemin d'une icône
    facebook_path = icon_library.get_icon_path('facebook')
    print(f"Chemin de l'icône Facebook: {facebook_path}")
    
    # Obtenir l'URL d'une icône
    twitter_url = icon_library.get_icon_url('twitter')
    print(f"URL de l'icône Twitter: {twitter_url}")
