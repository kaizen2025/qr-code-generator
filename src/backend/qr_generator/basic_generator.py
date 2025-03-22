#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module de base pour la génération de QR codes.
Ce module fournit les fonctionnalités fondamentales pour générer des QR codes simples,
qui peuvent ensuite être personnalisés avec les modules de personnalisation.
"""

import os
import uuid
from datetime import datetime
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageChops


class QRCodeGenerator:
    """
    Classe pour la génération de QR codes de base.
    Fournit des méthodes pour créer des QR codes simples ou avec des options basiques.
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
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Création du répertoire de métadonnées
        self.metadata_dir = os.path.join(self.output_dir, 'metadata')
        os.makedirs(self.metadata_dir, exist_ok=True)
        
        # Mappings pour les niveaux de correction d'erreur
        self.error_correction_levels = {
            0: ERROR_CORRECT_L,  # 7% de correction
            1: ERROR_CORRECT_M,  # 15% de correction
            2: ERROR_CORRECT_Q,  # 25% de correction
            3: ERROR_CORRECT_H   # 30% de correction
        }
        
    def generate_basic_qrcode(self, data, filename=None):
        """
        Génère un QR code basique avec les paramètres par défaut.
        
        Args:
            data (str): Données à encoder dans le QR code (URL, texte, etc.)
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            
        Returns:
            str: Chemin du fichier QR code généré.
        """
        if not filename:
            filename = f"qrcode_{uuid.uuid4().hex}.png"
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Génération du QR code avec les paramètres par défaut
        qr = qrcode.QRCode(
            version=1,
            error_correction=ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Génération de l'image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Sauvegarde de l'image
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
            **options: Options supplémentaires pour la génération du QR code.
                - version (int): Version du QR code (1-40, taille de la matrice)
                - error_correction (int): Niveau de correction d'erreur (0-3)
                - box_size (int): Taille de chaque "boîte" du QR code en pixels
                - border (int): Taille de la bordure en nombre de boîtes
                - fill_color (str/tuple): Couleur de remplissage du QR code
                - back_color (str/tuple): Couleur d'arrière-plan du QR code
            
        Returns:
            str: Chemin du fichier QR code généré.
        """
        if not filename:
            filename = f"qrcode_{uuid.uuid4().hex}.png"
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Options par défaut
        version = options.get('version', 1)
        
        # Conversion du niveau de correction d'erreur
        error_correction_index = options.get('error_correction', 1)  # 1 = M par défaut
        error_correction = self.error_correction_levels.get(error_correction_index, ERROR_CORRECT_M)
        
        box_size = options.get('box_size', 10)
        border = options.get('border', 4)
        
        # Couleurs
        fill_color = options.get('fill_color', "black")
        back_color = options.get('back_color', "white")
        
        # Génération du QR code avec les options spécifiées
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Génération de l'image
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        # Sauvegarde de l'image
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
            **options: Options supplémentaires pour la génération du QR code.
                - version (int): Version du QR code
                - error_correction (int): Niveau de correction d'erreur
                - box_size (int): Taille de chaque "boîte" du QR code en pixels
                - border (int): Taille de la bordure en nombre de boîtes
                - fill_color (str/tuple): Couleur de remplissage du QR code
                - back_color (str/tuple): Couleur d'arrière-plan du QR code
                - logo_size (float): Taille du logo en pourcentage du QR code (0.0-1.0)
                - add_border (bool): Ajouter une bordure blanche autour du logo
            
        Returns:
            str: Chemin du fichier QR code généré.
        """
        if not filename:
            filename = f"qrcode_logo_{uuid.uuid4().hex}.png"
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Options par défaut avec niveau de correction d'erreur élevé pour compenser le logo
        version = options.get('version', 1)
        
        # Niveau de correction d'erreur élevé par défaut pour les QR codes avec logo
        error_correction_index = options.get('error_correction', 3)  # 3 = H par défaut
        error_correction = self.error_correction_levels.get(error_correction_index, ERROR_CORRECT_H)
        
        box_size = options.get('box_size', 10)
        border = options.get('border', 4)
        
        # Couleurs
        fill_color = options.get('fill_color', "black")
        back_color = options.get('back_color', "white")
        
        # Taille du logo
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
        
        # Génération de l'image QR code
        qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGBA')
        
        try:
            # Ouverture du logo
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
            if options.get('add_border', True):
                # Création d'un cercle blanc pour le fond du logo
                circle = Image.new('RGBA', (new_logo_width + 20, new_logo_height + 20), (255, 255, 255, 255))
                draw = ImageDraw.Draw(circle)
                
                # Calculer le centre du cercle
                center = ((new_logo_width + 20) // 2, (new_logo_height + 20) // 2)
                radius = min(center[0], center[1])
                
                # Dessiner un cercle blanc (remplir tout le cercle)
                for i in range(center[0] - radius, center[0] + radius):
                    for j in range(center[1] - radius, center[1] + radius):
                        if (i - center[0])**2 + (j - center[1])**2 <= radius**2:
                            circle.putpixel((i, j), (255, 255, 255, 255))
                
                # Placer le logo au centre du cercle
                circle.paste(logo, ((new_logo_width + 20 - new_logo_width) // 2, 
                                    (new_logo_height + 20 - new_logo_height) // 2), logo)
                logo = circle
                new_logo_width += 20
                new_logo_height += 20
            
            # Calcul de la position du logo (centre)
            position = ((qr_width - new_logo_width) // 2, (qr_height - new_logo_height) // 2)
            
            # Copie du QR code
            result = qr_img.copy()
            
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
            self._save_metadata(data, output_path, options)
            
            return output_path
    
    def generate_qrcode_from_history(self, history_id, **new_options):
        """
        Régénère un QR code à partir de l'historique avec de nouvelles options.
        
        Args:
            history_id (str): Identifiant du QR code dans l'historique
            **new_options: Nouvelles options à appliquer
            
        Returns:
            str: Chemin du fichier QR code généré, ou None si l'historique n'existe pas
        """
        # Chemin du fichier de métadonnées
        metadata_path = os.path.join(self.metadata_dir, f"{history_id}.txt")
        
        if not os.path.exists(metadata_path):
            return None
        
        # Lecture des métadonnées
        data = None
        options = {}
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("Données: "):
                    data = line[len("Données: "):].strip()
                elif line.startswith("Options:"):
                    continue  # Ligne d'en-tête des options
                elif line.startswith("  "):
                    # Ligne d'option
                    key_value = line.strip().split(": ", 1)
                    if len(key_value) == 2:
                        key, value = key_value
                        options[key] = value
        
        if not data:
            return None
        
        # Fusion des anciennes options avec les nouvelles
        options.update(new_options)
        
        # Génération du nouveau QR code
        return self.generate_qrcode_with_options(data, None, **options)
    
    def extract_qr_data(self, qr_image_path):
        """
        Extrait les données d'un QR code existant.
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code
            
        Returns:
            str: Données contenues dans le QR code, ou None si échec
        """
        try:
            from pyzbar.pyzbar import decode
            
            # Ouverture de l'image
            img = Image.open(qr_image_path)
            
            # Décodage du QR code
            decoded_objects = decode(img)
            
            # Retour des données si trouvées
            if decoded_objects and len(decoded_objects) > 0:
                return decoded_objects[0].data.decode('utf-8')
            
            return None
            
        except Exception as e:
            print(f"Erreur lors de l'extraction des données du QR code: {e}")
            return None
    
    def _save_metadata(self, data, output_path, options=None):
        """
        Enregistre les métadonnées du QR code généré.
        
        Args:
            data (str): Données encodées dans le QR code
            output_path (str): Chemin du fichier QR code généré
            options (dict, optional): Options utilisées pour la génération
        """
        # Nom du fichier de métadonnées basé sur le nom du QR code
        qr_filename = os.path.basename(output_path)
        metadata_filename = f"{os.path.splitext(qr_filename)[0]}.txt"
        metadata_path = os.path.join(self.metadata_dir, metadata_filename)
        
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
    
    def generate_batch_qrcodes(self, data_list, base_options=None, output_prefix=None):
        """
        Génère plusieurs QR codes en lot.
        
        Args:
            data_list (list): Liste des données à encoder
            base_options (dict, optional): Options de base communes à tous les QR codes
            output_prefix (str, optional): Préfixe pour les noms de fichiers
            
        Returns:
            list: Liste des chemins des QR codes générés
        """
        if base_options is None:
            base_options = {}
        
        if output_prefix is None:
            output_prefix = "batch_qrcode"
        
        # Liste des chemins des QR codes générés
        generated_paths = []
        
        # Génération des QR codes
        for index, data in enumerate(data_list):
            # Nom de fichier avec préfixe et index
            filename = f"{output_prefix}_{index+1}_{uuid.uuid4().hex[:4]}.png"
            
            # Génération du QR code
            qr_path = self.generate_qrcode_with_options(data, filename, **base_options)
            
            # Ajout du chemin à la liste
            generated_paths.append(qr_path)
        
        return generated_paths
