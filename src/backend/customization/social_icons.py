#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module d'intégration d'icônes de réseaux sociaux dans les QR codes.
Ce module fournit des fonctionnalités pour ajouter des icônes de réseaux sociaux
aux QR codes générés.
"""

import os
import uuid
from PIL import Image, ImageDraw, ImageFont
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
            'facebook': os.path.join(self.icons_dir, 'facebook.png'),
            'twitter': os.path.join(self.icons_dir, 'twitter.png'),
            'instagram': os.path.join(self.icons_dir, 'instagram.png'),
            'linkedin': os.path.join(self.icons_dir, 'linkedin.png'),
            'youtube': os.path.join(self.icons_dir, 'youtube.png'),
            'tiktok': os.path.join(self.icons_dir, 'tiktok.png'),
            'snapchat': os.path.join(self.icons_dir, 'snapchat.png'),
            'pinterest': os.path.join(self.icons_dir, 'pinterest.png'),
            'whatsapp': os.path.join(self.icons_dir, 'whatsapp.png'),
            'telegram': os.path.join(self.icons_dir, 'telegram.png'),
            'website': os.path.join(self.icons_dir, 'website.png'),
            'email': os.path.join(self.icons_dir, 'email.png'),
            'phone': os.path.join(self.icons_dir, 'phone.png')
        }
    
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
        
        icon_path = self.social_icons[social_platform]
        if not os.path.exists(icon_path):
            raise FileNotFoundError(f"Icône non trouvée: {icon_path}")
        
        # Paramètres par défaut
        version = options.get('version', 1)
        error_correction = options.get('error_correction', qrcode.constants.ERROR_CORRECT_H)
        box_size = options.get('box_size', 10)
        border = options.get('border', 4)
        fill_color = options.get('fill_color', "black")
        back_color = options.get('back_color', "white")
        icon_size = options.get('icon_size', 0.2)  # 20% par défaut
        icon_position = options.get('icon_position', 'center')
        
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
        
        # Ouverture et redimensionnement de l'icône
        try:
            icon = Image.open(icon_path).convert('RGBA')
            
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
            
            icon_path = self.social_icons[platform]
            if not os.path.exists(icon_path):
                raise FileNotFoundError(f"Icône non trouvée: {icon_path}")
        
        # Paramètres par défaut
        version = options.get('version', 1)
        error_correction = options.get('error_correction', qrcode.constants.ERROR_CORRECT_H)
        box_size = options.get('box_size', 10)
        border = options.get('border', 4)
        fill_color = options.get('fill_color', "black")
        back_color = options.get('back_color', "white")
        icon_size = options.get('icon_size', 0.15)  # 15% par défaut pour les multi-icônes
        layout = options.get('layout', 'circle')
        
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
            
            # Disposition des icônes
            if layout == 'circle':
                # Disposition en cercle autour du centre
                import math
                
                # Rayon du cercle
                radius = min(qr_width, qr_height) * 0.3
                
                # Angle entre chaque icône
                angle_step = 2 * math.pi / num_icons
                
                # Centre du QR code
                center_x = qr_width // 2
                center_y = qr_height // 2
                
                for i, platform in enumerate(social_platforms):
                    # Calcul de la position de l'icône
                    angle = i * angle_step
                    x = center_x + int(radius * math.cos(angle)) - icon_max_size // 2
                    y = center_y + int(radius * math.sin(angle)) - icon_max_size // 2
                    
                    # Ouverture et redimensionnement de l'icône
                    icon = Image.open(self.social_icons[platform]).convert('RGBA')
                    icon_width, icon_height = icon.size
                    ratio = min(icon_max_size / icon_width, icon_max_size / icon_height)
                    new_icon_width = int(icon_width * ratio)
                    new_icon_height = int(icon_height * ratio)
                    icon = icon.resize((new_icon_width, new_icon_height), Image.LANCZOS)
                    
                    # Ajout de l'icône
                    result.paste(icon, (x, y), icon)
                
            elif layout == 'row':
                # Disposition en ligne horizontale en bas du QR code
                total_width = num_icons * icon_max_size
                start_x = (qr_width - total_width) // 2
                y = qr_height - icon_max_size - border * box_size
                
                for i, platform in enumerate(social_platforms):
                    # Calcul de la position de l'icône
                    x = start_x + i * icon_max_size
                    
                    # Ouverture et redimensionnement de l'icône
                    icon = Image.open(self.social_icons[platform]).convert('RGBA')
                    icon_width, icon_height = icon.size
                    ratio = min(icon_max_size / icon_width, icon_max_size / icon_height)
                    new_icon_width = int(icon_width * ratio)
                    new_icon_height = int(icon_height * ratio)
                    icon = icon.resize((new_icon_width, new_icon_height), Image.LANCZOS)
                    
                    # Ajout de l'icône
                    result.paste(icon, (x, y), icon)
                
            elif layout == 'column':
                # Disposition en colonne verticale à droite du QR code
                total_height = num_icons * icon_max_size
                x = qr_width - icon_max_size - border * box_size
                start_y = (qr_height - total_height) // 2
                
                for i, platform in enumerate(social_platforms):
                    # Calcul de la position de l'icône
                    y = start_y + i * icon_max_size
                    
                    # Ouverture et redimensionnement de l'icône
                    icon = Image.open(self.social_icons[platform]).convert('RGBA')
                    icon_width, icon_height = icon.size
                    ratio = min(icon_max_size / icon_width, icon_max_size / icon_height)
                    new_icon_width = int(icon_width * ratio)
                    new_icon_height = int(icon_height * ratio)
                    icon = icon.resize((new_icon_width, new_icon_height), Image.LANCZOS)
                    
                    # Ajout de l'icône
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
    # social_qr = generator.generate_social_qrcode(
    #     "https://www.facebook.com/example",
    #     "facebook",
    #     "example_facebook.png"
    # )
    # print(f"QR code avec icône Facebook généré: {social_qr}")
    
    # Exemple 2: QR code avec plusieurs icônes de réseaux sociaux
    # multi_social_qr = generator.generate_multi_social_qrcode(
    #     "https://www.example.com",
    #     ["facebook", "twitter", "instagram", "linkedin"],
    #     "example_multi_social.png",
    #     layout="circle"
    # )
    # print(f"QR code avec plusieurs icônes généré: {multi_social_qr}")
