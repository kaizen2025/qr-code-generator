#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module de génération de QR codes basique.
Ce module fournit les fonctionnalités de base pour générer des QR codes.
"""

import os
import qrcode
from PIL import Image
import uuid
from datetime import datetime


class QRCodeGenerator:
    """
    Classe principale pour la génération de QR codes.
    Fournit les méthodes de base pour créer des QR codes avec différentes options.
    """

    def __init__(self, output_dir=None):
        """
        Initialise le générateur de QR codes.
        
        Args:
            output_dir (str, optional): Répertoire de sortie pour les QR codes générés.
                Si non spécifié, utilise le répertoire courant.
        """
        self.output_dir = output_dir or os.path.join(os.getcwd(), 'generated_qrcodes')
        
        # Création du répertoire de sortie s'il n'existe pas
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_basic_qrcode(self, data, filename=None, box_size=10, border=4):
        """
        Génère un QR code basique avec les paramètres par défaut.
        
        Args:
            data (str): Données à encoder dans le QR code (URL, texte, etc.)
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            box_size (int, optional): Taille de chaque "boîte" du QR code en pixels.
            border (int, optional): Taille de la bordure en nombre de boîtes.
            
        Returns:
            str: Chemin du fichier QR code généré.
        """
        if not filename:
            filename = f"qrcode_{uuid.uuid4().hex[:8]}.png"
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Génération du QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Création de l'image
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_path)
        
        # Enregistrement des métadonnées
        self._save_metadata(data, output_path)
        
        return output_path
    
    def generate_qrcode_with_options(self, data, filename=None, **options):
        """
        Génère un QR code avec des options personnalisées.
        
        Args:
            data (str): Données à encoder dans le QR code (URL, texte, etc.)
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour la personnalisation du QR code.
                - version (int): Version du QR code (1-40)
                - error_correction (int): Niveau de correction d'erreur
                - box_size (int): Taille de chaque "boîte" du QR code en pixels
                - border (int): Taille de la bordure en nombre de boîtes
                - fill_color (str): Couleur de remplissage des modules
                - back_color (str): Couleur d'arrière-plan
            
        Returns:
            str: Chemin du fichier QR code généré.
        """
        if not filename:
            filename = f"qrcode_{uuid.uuid4().hex[:8]}.png"
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Paramètres par défaut
        version = options.get('version', 1)
        error_correction = options.get('error_correction', qrcode.constants.ERROR_CORRECT_L)
        box_size = options.get('box_size', 10)
        border = options.get('border', 4)
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
        
        # Création de l'image
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(output_path)
        
        # Enregistrement des métadonnées
        self._save_metadata(data, output_path, options)
        
        return output_path
    
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
                - fill_color (str): Couleur de remplissage des modules
                - back_color (str): Couleur d'arrière-plan
                - logo_size (float): Taille du logo en pourcentage du QR code (0.0-1.0)
            
        Returns:
            str: Chemin du fichier QR code généré.
        """
        if not filename:
            filename = f"qrcode_logo_{uuid.uuid4().hex[:8]}.png"
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Paramètres par défaut
        version = options.get('version', 1)
        # Utiliser un niveau de correction d'erreur élevé pour compenser le logo
        error_correction = options.get('error_correction', qrcode.constants.ERROR_CORRECT_H)
        box_size = options.get('box_size', 10)
        border = options.get('border', 4)
        fill_color = options.get('fill_color', "black")
        back_color = options.get('back_color', "white")
        logo_size = options.get('logo_size', 0.2)  # 20% par défaut
        
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
        
        # Ouverture et redimensionnement du logo
        try:
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


# Exemple d'utilisation si exécuté directement
if __name__ == "__main__":
    generator = QRCodeGenerator()
    
    # Exemple 1: QR code basique
    basic_qr = generator.generate_basic_qrcode("https://www.example.com", "example_basic.png")
    print(f"QR code basique généré: {basic_qr}")
    
    # Exemple 2: QR code avec options personnalisées
    custom_qr = generator.generate_qrcode_with_options(
        "https://www.example.com",
        "example_custom.png",
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=15,
        border=2,
        fill_color="blue",
        back_color="yellow"
    )
    print(f"QR code personnalisé généré: {custom_qr}")
    
    # Exemple 3: QR code avec logo (nécessite un fichier logo.png)
    # Décommentez les lignes suivantes et remplacez le chemin du logo
    # logo_path = "path/to/logo.png"
    # logo_qr = generator.generate_qrcode_with_logo(
    #     "https://www.example.com",
    #     logo_path,
    #     "example_logo.png",
    #     logo_size=0.3
    # )
    # print(f"QR code avec logo généré: {logo_qr}")
