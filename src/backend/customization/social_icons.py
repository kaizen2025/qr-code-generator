#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module d'intégration d'icônes de réseaux sociaux dans les QR codes.
Ce module fournit des fonctionnalités pour ajouter des icônes de réseaux sociaux
aux QR codes générés.
"""

import os
import uuid
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import qrcode
from datetime import datetime


class SocialQRGenerator:
    """
    Classe pour l'intégration d'icônes de réseaux sociaux dans les QR codes.
    Fournit des méthodes pour ajouter des icônes de réseaux sociaux aux QR codes.
    """

    def __init__(self, output_dir=None, icons_dir=None):
        """
        Initialise le générateur de QR codes avec icônes de réseaux sociaux.
        
        Args:
            output_dir (str, optional): Répertoire de sortie pour les QR codes générés.
                Si non spécifié, utilise le répertoire courant.
            icons_dir (str, optional): Répertoire contenant les icônes de réseaux sociaux.
                Si non spécifié, utilise le sous-répertoire 'icons' du répertoire courant.
        """
        self.output_dir = output_dir or os.path.join(os.getcwd(), 'generated_qrcodes')
        self.icons_dir = icons_dir or os.path.join(os.getcwd(), 'src/frontend/static/img/social_icons')
        
        # Création des répertoires s'ils n'existent pas
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        if not os.path.exists(self.icons_dir):
            os.makedirs(self.icons_dir)
        
        # Dictionnaire des icônes de réseaux sociaux disponibles
        self.social_icons = {
            'facebook': {
                'path': os.path.join(self.icons_dir, 'facebook.png'),
                'color': (59, 89, 152)  # Bleu Facebook
            },
            'twitter': {
                'path': os.path.join(self.icons_dir, 'twitter.png'),
                'color': (29, 161, 242)  # Bleu Twitter
            },
            'instagram': {
                'path': os.path.join(self.icons_dir, 'instagram.png'),
                'color': (225, 48, 108)  # Rose Instagram
            },
            'linkedin': {
                'path': os.path.join(self.icons_dir, 'linkedin.png'),
                'color': (0, 119, 181)  # Bleu LinkedIn
            },
            'youtube': {
                'path': os.path.join(self.icons_dir, 'youtube.png'),
                'color': (255, 0, 0)  # Rouge YouTube
            },
            'tiktok': {
                'path': os.path.join(self.icons_dir, 'tiktok.png'),
                'color': (0, 0, 0)  # Noir TikTok
            },
            'snapchat': {
                'path': os.path.join(self.icons_dir, 'snapchat.png'),
                'color': (255, 252, 0)  # Jaune Snapchat
            },
            'pinterest': {
                'path': os.path.join(self.icons_dir, 'pinterest.png'),
                'color': (230, 0, 35)  # Rouge Pinterest
            },
            'whatsapp': {
                'path': os.path.join(self.icons_dir, 'whatsapp.png'),
                'color': (37, 211, 102)  # Vert WhatsApp
            },
            'telegram': {
                'path': os.path.join(self.icons_dir, 'telegram.png'),
                'color': (0, 136, 204)  # Bleu Telegram
            },
            'website': {
                'path': os.path.join(self.icons_dir, 'website.png'),
                'color': (51, 51, 51)  # Gris foncé
            },
            'email': {
                'path': os.path.join(self.icons_dir, 'email.png'),
                'color': (66, 133, 244)  # Bleu Gmail
            },
            'phone': {
                'path': os.path.join(self.icons_dir, 'phone.png'),
                'color': (76, 175, 80)  # Vert
            }
        }
    
    def _create_placeholder_icon(self, platform, size=100):
        """
        Crée une icône de substitution si l'icône demandée n'existe pas.
        
        Args:
            platform (str): Nom de la plateforme
            size (int): Taille de l'icône en pixels
            
        Returns:
            PIL.Image: Image de l'icône de substitution
        """
        # Création d'une image vide
        img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Couleur de fond en fonction de la plateforme
        bg_color = self.social_icons.get(platform, {}).get('color', (100, 100, 100))
        
        # Dessin d'un cercle de fond
        draw.ellipse([(0, 0), (size, size)], fill=bg_color)
        
        # Ajout du texte (première lettre de la plateforme)
        letter = platform[0].upper() if platform else "?"
        text_size = draw.textlength(letter, font=None)
        text_position = ((size - text_size) // 2, (size - text_size) // 2)
        draw.text(text_position, letter, fill=(255, 255, 255))
        
        return img
    
    def generate_social_qrcode(self, data, social_platform, filename=None, **options):
        """
        Génère un QR code avec une icône de réseau social.
        
        Args:
            data (str): Données à encoder dans le QR code (URL, texte, etc.)
            social_platform (str): Nom du réseau social ('facebook', 'twitter', etc.)
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour la personnalisation du QR code.
                - version (int): Version du QR code (1-40)
                - error_correction (int): Niveau de correction d'erreur
                - box_size (int): Taille de chaque "boîte" du QR code en pixels
                - border (int): Taille de la bordure en nombre de boîtes
                - fill_color (str/tuple): Couleur de remplissage des modules
                - back_color (str/tuple): Couleur d'arrière-plan
                - icon_size (float): Taille de l'icône en pourcentage du QR code (0.0-1.0)
                - icon_position (str): Position de l'icône ('center', 'top_left', etc.)
                - use_branded_colors (bool): Utiliser la couleur de la marque pour le QR code
            
        Returns:
            str: Chemin du fichier QR code généré.
        """
        if not filename:
            filename = f"social_qrcode_{uuid.uuid4().hex[:8]}.png"
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Vérification que l'icône existe
        if social_platform not in self.social_icons:
            raise ValueError(f"Plateforme sociale '{social_platform}' non reconnue. Options disponibles: {', '.join(self.social_icons.keys())}")
        
        icon_info = self.social_icons[social_platform]
        icon_path = icon_info['path']
        
        # Paramètres par défaut
        version = options.get('version', 1)
        error_correction = options.get('error_correction', qrcode.constants.ERROR_CORRECT_H)
        box_size = options.get('box_size', 10)
        border = options.get('border', 4)
        fill_color = options.get('fill_color', "black")
        back_color = options.get('back_color', "white")
        icon_size = options.get('icon_size', 0.2)  # 20% par défaut
        icon_position = options.get('icon_position', 'center')
        use_branded_colors = options.get('use_branded_colors', False)
        
        # Utiliser la couleur de la marque si demandé
        if use_branded_colors:
            fill_color = icon_info['color']
        
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
        
        # Chargement de l'icône
        try:
            if os.path.exists(icon_path):
                icon = Image.open(icon_path).convert('RGBA')
            else:
                # Utiliser une icône de substitution si le fichier n'existe pas
                icon = self._create_placeholder_icon(social_platform)
            
            # Calcul de la taille de l'icône
            qr_width, qr_height = qr_img.size
            icon_max_size = int(min(qr_width, qr_height) * icon_size)
            
            # Redimensionnement de l'icône tout en conservant le ratio
            icon_width, icon_height = icon.size
            ratio = min(icon_max_size / icon_width, icon_max_size / icon_height)
            new_icon_width = int(icon_width * ratio)
            new_icon_height = int(icon_height * ratio)
            icon = icon.resize((new_icon_width, new_icon_height), Image.LANCZOS)
            
            # Calcul de la position de l'icône
            if icon_position == 'center':
                position = ((qr_width - new_icon_width) // 2, (qr_height - new_icon_height) // 2)
            elif icon_position == 'top_left':
                position = (border * box_size, border * box_size)
            elif icon_position == 'top_right':
                position = (qr_width - new_icon_width - border * box_size, border * box_size)
            elif icon_position == 'bottom_left':
                position = (border * box_size, qr_height - new_icon_height - border * box_size)
            elif icon_position == 'bottom_right':
                position = (qr_width - new_icon_width - border * box_size, qr_height - new_icon_height - border * box_size)
            else:
                position = ((qr_width - new_icon_width) // 2, (qr_height - new_icon_height) // 2)
            
            # Option pour ajouter un cercle blanc derrière l'icône
            add_background = options.get('add_background', True)
            if add_background:
                # Création d'un masque circulaire blanc
                bg_size = max(new_icon_width, new_icon_height) + 20  # Légèrement plus grand que l'icône
                background = Image.new('RGBA', (bg_size, bg_size), (0, 0, 0, 0))
                draw = ImageDraw.Draw(background)
                draw.ellipse([(0, 0), (bg_size, bg_size)], fill=(255, 255, 255, 225))  # Blanc semi-transparent
                
                # Positionnement du fond
                bg_position = (
                    position[0] - (bg_size - new_icon_width) // 2,
                    position[1] - (bg_size - new_icon_height) // 2
                )
                
                # Application du fond blanc
                qr_img.paste(background, bg_position, background)
            
            # Création d'une nouvelle image pour le résultat final
            result = Image.new('RGBA', (qr_width, qr_height), (0, 0, 0, 0))
            
            # Copie du QR code sur l'image résultat
            result.paste(qr_img, (0, 0))
            
            # Ajout de l'icône
            result.paste(icon, position, icon)
            
            # Sauvegarde de l'image finale
            result.save(output_path)
            
            # Enregistrement des métadonnées
            options['social_platform'] = social_platform
            options['icon_path'] = icon_path
            self._save_metadata(data, output_path, options)
            
            return output_path
            
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'icône: {e}")
            # En cas d'erreur, générer un QR code sans icône
            qr_img.save(output_path)
            return output_path
    
    def generate_multi_social_qrcode(self, data, social_platforms, filename=None, **options):
        """
        Génère un QR code avec plusieurs icônes de réseaux sociaux.
        
        Args:
            data (str): Données à encoder dans le QR code (URL, texte, etc.)
            social_platforms (list): Liste des noms de réseaux sociaux
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour la personnalisation du QR code.
                - version (int): Version du QR code (1-40)
                - error_correction (int): Niveau de correction d'erreur
                - box_size (int): Taille de chaque "boîte" du QR code en pixels
                - border (int): Taille de la bordure en nombre de boîtes
                - fill_color (str/tuple): Couleur de remplissage des modules
                - back_color (str/tuple): Couleur d'arrière-plan
                - icon_size (float): Taille des icônes en pourcentage du QR code (0.0-1.0)
                - layout (str): Disposition des icônes ('circle', 'row', 'column')
                - layout_padding (int): Espacement entre les icônes
            
        Returns:
            str: Chemin du fichier QR code généré.
        """
        if not filename:
            filename = f"multi_social_qrcode_{uuid.uuid4().hex[:8]}.png"
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Vérification que les icônes existent
        for platform in social_platforms:
            if platform not in self.social_icons:
                raise ValueError(f"Plateforme sociale '{platform}' non reconnue. Options disponibles: {', '.join(self.social_icons.keys())}")
        
        # Paramètres par défaut
        version = options.get('version', 1)
        error_correction = options.get('error_correction', qrcode.constants.ERROR_CORRECT_H)
        box_size = options.get('box_size', 10)
        border = options.get('border', 4)
        fill_color = options.get('fill_color', "black")
        back_color = options.get('back_color', "white")
        icon_size = options.get('icon_size', 0.15)  # 15% par défaut pour les multi-icônes
        layout = options.get('layout', 'circle')
        layout_padding = options.get('layout_padding', 5)  # Espacement entre les icônes
        
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
        qr_width, qr_height = qr_img.size
        
        # Création d'une nouvelle image pour le résultat final
        result = Image.new('RGBA', (qr_width, qr_height), (0, 0, 0, 0))
        
        # Copie du QR code sur l'image résultat
        result.paste(qr_img, (0, 0))
        
        try:
            # Calcul de la taille des icônes
            icon_max_size = int(min(qr_width, qr_height) * icon_size)
            
            # Nombre d'icônes
            num_icons = len(social_platforms)
            
            # Chargement des icônes
            icons = []
            for platform in social_platforms:
                icon_path = self.social_icons[platform]['path']
                if os.path.exists(icon_path):
                    icon = Image.open(icon_path).convert('RGBA')
                else:
                    # Utiliser une icône de substitution
                    icon = self._create_placeholder_icon(platform, size=icon_max_size)
                
                # Redimensionnement de l'icône
                icon_width, icon_height = icon.size
                ratio = min(icon_max_size / icon_width, icon_max_size / icon_height)
                new_icon_width = int(icon_width * ratio)
                new_icon_height = int(icon_height * ratio)
                icon = icon.resize((new_icon_width, new_icon_height), Image.LANCZOS)
                
                # Ajouter l'icône redimensionnée à la liste
                icons.append(icon)
            
            # Disposition des icônes
            if layout == 'circle':
                # Disposition en cercle autour du centre
                import math
                
                # Rayon du cercle (30% de la taille du QR code)
                radius = min(qr_width, qr_height) * 0.3
                
                # Centre du QR code
                center_x = qr_width // 2
                center_y = qr_height // 2
                
                # Création d'un masque circulaire blanc pour le fond
                background_size = int(radius * 1.5)
                background = Image.new('RGBA', (background_size, background_size), (0, 0, 0, 0))
                draw = ImageDraw.Draw(background)
                draw.ellipse([(0, 0), (background_size, background_size)], fill=(255, 255, 255, 225))
                
                # Positionnement du fond
                bg_position = (center_x - background_size // 2, center_y - background_size // 2)
                result.paste(background, bg_position, background)
                
                # Placement des icônes en cercle
                for i, icon in enumerate(icons):
                    # Angle entre chaque icône
                    angle = i * (2 * math.pi / num_icons)
                    
                    # Position de l'icône
                    x = center_x + int(radius * math.cos(angle)) - icon.width // 2
                    y = center_y + int(radius * math.sin(angle)) - icon.height // 2
                    
                    # Ajout de l'icône
                    result.paste(icon, (x, y), icon)
                
            elif layout == 'row':
                # Disposition en ligne horizontale en bas du QR code
                total_width = sum(icon.width for icon in icons) + layout_padding * (num_icons - 1)
                start_x = (qr_width - total_width) // 2
                y = qr_height - icon_max_size - border * box_size
                
                # Fond blanc
                background = Image.new('RGBA', (total_width + layout_padding * 2, icon_max_size + layout_padding * 2), (255, 255, 255, 225))
                bg_position = (start_x - layout_padding, y - layout_padding)
                result.paste(background, bg_position, background)
                
                # Placement des icônes
                x = start_x
                for icon in icons:
                    # Ajout de l'icône
                    result.paste(icon, (x, y), icon)
                    x += icon.width + layout_padding
                
            elif layout == 'column':
                # Disposition en colonne verticale à droite du QR code
                total_height = sum(icon.height for icon in icons) + layout_padding * (num_icons - 1)
                x = qr_width - icon_max_size - border * box_size
                start_y = (qr_height - total_height) // 2
                
                # Fond blanc
                background = Image.new('RGBA', (icon_max_size + layout_padding * 2, total_height + layout_padding * 2), (255, 255, 255, 225))
                bg_position = (x - layout_padding, start_y - layout_padding)
                result.paste(background, bg_position, background)
                
                # Placement des icônes
                y = start_y
                for icon in icons:
                    # Ajout de l'icône
                    result.paste(icon, (x, y), icon)
                    y += icon.height + layout_padding
                
            elif layout == 'grid':
                # Disposition en grille
                cols = int(math.sqrt(num_icons))
                rows = (num_icons + cols - 1) // cols
                
                # Calcul de la taille totale de la grille
                grid_width = cols * icon_max_size + (cols - 1) * layout_padding
                grid_height = rows * icon_max_size + (rows - 1) * layout_padding
                
                # Position de départ (centré)
                start_x = (qr_width - grid_width) // 2
                start_y = (qr_height - grid_height) // 2
                
                # Fond blanc
                background = Image.new('RGBA', (grid_width + layout_padding * 2, grid_height + layout_padding * 2), (255, 255, 255, 225))
                bg_position = (start_x - layout_padding, start_y - layout_padding)
                result.paste(background, bg_position, background)
                
                # Placement des icônes
                for i, icon in enumerate(icons):
                    col = i % cols
                    row = i // cols
                    
                    x = start_x + col * (icon_max_size + layout_padding)
                    y = start_y + row * (icon_max_size + layout_padding)
                    
                    result.paste(icon, (x, y), icon)
            
            # Sauvegarde de l'image finale
            result.save(output_path)
            
            # Enregistrement des métadonnées
            options['social_platforms'] = social_platforms
            options['layout'] = layout
            self._save_metadata(data, output_path, options)
            
            return output_path
            
        except Exception as e:
            print(f"Erreur lors de l'ajout des icônes: {e}")
            # En cas d'erreur, générer un QR code sans icône
            qr_img.save(output_path)
            return output_path
    
    def generate_themed_social_qrcode(self, data, social_platform, filename=None, **options):
        """
        Génère un QR code thématique pour un réseau social spécifique.
        
        Args:
            data (str): Données à encoder dans le QR code (URL, texte, etc.)
            social_platform (str): Nom du réseau social
            filename (str, optional): Nom du fichier de sortie
            **options: Options supplémentaires pour la personnalisation
            
        Returns:
            str: Chemin du fichier QR code généré
        """
        if not filename:
            filename = f"themed_{social_platform}_qrcode_{uuid.uuid4().hex[:8]}.png"
        
        # Vérification que la plateforme existe
        if social_platform not in self.social_icons:
            raise ValueError(f"Plateforme sociale '{social_platform}' non reconnue. Options disponibles: {', '.join(self.social_icons.keys())}")
        
        # Récupération des informations de la plateforme
        platform_color = self.social_icons[social_platform]['color']
        
        # Options par défaut pour les QR codes thématiques
        theme_options = {
            'fill_color': platform_color,
            'back_color': "white",
            'icon_size': 0.25,
            'add_background': True,
            'error_correction': qrcode.constants.ERROR_CORRECT_H,
            'version': options.get('version', 1),
            'box_size': options.get('box_size', 10),
            'border': options.get('border', 4)
        }
        
        # Fusion avec les options fournies
        theme_options.update(options)
        
        # Génération du QR code thématique
        return self.generate_social_qrcode(data, social_platform, filename, **theme_options)
    
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
    generator = SocialQRGenerator()
    
    # Exemple 1: QR code avec une icône de réseau social
    social_qr = generator.generate_social_qrcode(
        "https://www.facebook.com/example",
        "facebook",
        "example_facebook.png"
    )
    print(f"QR code avec icône Facebook généré: {social_qr}")
    
    # Exemple 2: QR code avec plusieurs icônes de réseaux sociaux
    multi_social_qr = generator.generate_multi_social_qrcode(
        "https://www.example.com",
        ["facebook", "twitter", "instagram", "linkedin"],
        "example_multi_social.png",
        layout="circle"
    )
    print(f"QR code avec plusieurs icônes généré: {multi_social_qr}")
    
    # Exemple 3: QR code thématique
    themed_qr = generator.generate_themed_social_qrcode(
        "https://www.instagram.com/example",
        "instagram",
        "example_themed_instagram.png"
    )
    print(f"QR code thématique Instagram généré: {themed_qr}")
