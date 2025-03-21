#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module d'exportation pour les QR codes.
Ce module fournit des fonctionnalités pour exporter les QR codes dans différents formats.
"""

import os
import uuid
from PIL import Image
import svgwrite
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import datetime


class QRCodeExporter:
    """
    Classe pour l'exportation des QR codes dans différents formats.
    Fournit des méthodes pour convertir et exporter les QR codes en PNG, SVG et PDF.
    """

    def __init__(self, output_dir=None):
        """
        Initialise l'exportateur de QR codes.
        
        Args:
            output_dir (str, optional): Répertoire de sortie pour les QR codes exportés.
                Si non spécifié, utilise le répertoire courant.
        """
        self.output_dir = output_dir or os.path.join(os.getcwd(), 'exported_qrcodes')
        
        # Création du répertoire de sortie s'il n'existe pas
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def export_to_png(self, qr_image_path, filename=None, dpi=300, **options):
        """
        Exporte un QR code au format PNG avec la résolution spécifiée.
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code à exporter
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            dpi (int, optional): Résolution en points par pouce (DPI)
            **options: Options supplémentaires pour l'exportation
                - size (tuple): Taille de l'image en pixels (width, height)
                - quality (int): Qualité de l'image (0-100)
            
        Returns:
            str: Chemin du fichier PNG exporté
        """
        if not filename:
            filename = f"qrcode_export_{uuid.uuid4().hex[:8]}.png"
        
        # Vérification de l'extension
        if not filename.lower().endswith('.png'):
            filename += '.png'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Ouverture de l'image QR code
        img = Image.open(qr_image_path)
        
        # Redimensionnement si spécifié
        if 'size' in options:
            img = img.resize(options['size'], Image.LANCZOS)
        
        # Sauvegarde avec les options spécifiées
        quality = options.get('quality', 95)
        img.save(output_path, dpi=(dpi, dpi), quality=quality)
        
        # Enregistrement des métadonnées
        self._save_metadata(qr_image_path, output_path, 'PNG', options)
        
        return output_path
    
    def export_to_svg(self, qr_image_path, filename=None, **options):
        """
        Exporte un QR code au format SVG.
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code à exporter
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation
                - size (tuple): Taille de l'image en pixels (width, height)
                - scale (float): Facteur d'échelle pour le SVG
            
        Returns:
            str: Chemin du fichier SVG exporté
        """
        if not filename:
            filename = f"qrcode_export_{uuid.uuid4().hex[:8]}.svg"
        
        # Vérification de l'extension
        if not filename.lower().endswith('.svg'):
            filename += '.svg'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Ouverture de l'image QR code
        img = Image.open(qr_image_path)
        
        # Redimensionnement si spécifié
        if 'size' in options:
            img = img.resize(options['size'], Image.LANCZOS)
        
        # Conversion en mode 1 (noir et blanc) pour simplifier la conversion en SVG
        img = img.convert('1')
        
        # Dimensions de l'image
        width, height = img.size
        
        # Facteur d'échelle
        scale = options.get('scale', 1.0)
        
        # Création du document SVG
        dwg = svgwrite.Drawing(output_path, size=(width*scale, height*scale), profile='tiny')
        
        # Parcours des pixels de l'image et création des rectangles pour les pixels noirs
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))
                if pixel == 0:  # Pixel noir
                    dwg.add(dwg.rect(
                        insert=(x*scale, y*scale),
                        size=(scale, scale),
                        fill='black'
                    ))
        
        # Sauvegarde du fichier SVG
        dwg.save()
        
        # Enregistrement des métadonnées
        self._save_metadata(qr_image_path, output_path, 'SVG', options)
        
        return output_path
    
    def export_to_pdf(self, qr_image_path, filename=None, **options):
        """
        Exporte un QR code au format PDF.
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code à exporter
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation
                - size (tuple): Taille de l'image en mm (width, height)
                - position (tuple): Position de l'image en mm (x, y)
                - title (str): Titre du document PDF
                - author (str): Auteur du document PDF
                - subject (str): Sujet du document PDF
                - keywords (str): Mots-clés du document PDF
            
        Returns:
            str: Chemin du fichier PDF exporté
        """
        if not filename:
            filename = f"qrcode_export_{uuid.uuid4().hex[:8]}.pdf"
        
        # Vérification de l'extension
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Ouverture de l'image QR code
        img = Image.open(qr_image_path)
        
        # Création d'un fichier temporaire pour l'image
        temp_img_path = os.path.join(self.output_dir, f"temp_{uuid.uuid4().hex[:8]}.png")
        img.save(temp_img_path)
        
        # Création du document PDF
        c = canvas.Canvas(output_path)
        
        # Définition des métadonnées du PDF
        c.setTitle(options.get('title', 'QR Code'))
        c.setAuthor(options.get('author', 'QR Code Generator'))
        c.setSubject(options.get('subject', 'QR Code'))
        c.setKeywords(options.get('keywords', 'QR Code, Generator'))
        
        # Position et taille de l'image
        position = options.get('position', (10, 10))
        size = options.get('size', (50, 50))
        
        # Ajout de l'image au PDF
        c.drawImage(temp_img_path, position[0]*mm, position[1]*mm, width=size[0]*mm, height=size[1]*mm)
        
        # Finalisation du document
        c.save()
        
        # Suppression du fichier temporaire
        os.remove(temp_img_path)
        
        # Enregistrement des métadonnées
        self._save_metadata(qr_image_path, output_path, 'PDF', options)
        
        return output_path
    
    def export_to_all_formats(self, qr_image_path, base_filename=None, **options):
        """
        Exporte un QR code dans tous les formats disponibles (PNG, SVG, PDF).
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code à exporter
            base_filename (str, optional): Nom de base pour les fichiers de sortie.
                Si non spécifié, génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation
            
        Returns:
            dict: Dictionnaire des chemins des fichiers exportés par format
        """
        if not base_filename:
            base_filename = f"qrcode_export_{uuid.uuid4().hex[:8]}"
        
        # Exportation dans chaque format
        png_path = self.export_to_png(qr_image_path, f"{base_filename}.png", **options)
        svg_path = self.export_to_svg(qr_image_path, f"{base_filename}.svg", **options)
        pdf_path = self.export_to_pdf(qr_image_path, f"{base_filename}.pdf", **options)
        
        return {
            'png': png_path,
            'svg': svg_path,
            'pdf': pdf_path
        }
    
    def _save_metadata(self, source_path, output_path, format_type, options=None):
        """
        Enregistre les métadonnées de l'exportation.
        
        Args:
            source_path (str): Chemin du fichier source
            output_path (str): Chemin du fichier exporté
            format_type (str): Type de format d'exportation (PNG, SVG, PDF)
            options (dict, optional): Options utilisées pour l'exportation
        """
        metadata_dir = os.path.join(self.output_dir, 'metadata')
        if not os.path.exists(metadata_dir):
            os.makedirs(metadata_dir)
        
        # Nom du fichier de métadonnées basé sur le nom du fichier exporté
        export_filename = os.path.basename(output_path)
        metadata_filename = f"{os.path.splitext(export_filename)[0]}_metadata.txt"
        metadata_path = os.path.join(metadata_dir, metadata_filename)
        
        # Création du contenu des métadonnées
        metadata_content = [
            f"Date d'exportation: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Fichier source: {os.path.basename(source_path)}",
            f"Fichier exporté: {export_filename}",
            f"Format: {format_type}",
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
    exporter = QRCodeExporter()
    
    # Exemple d'exportation (nécessite un fichier QR code existant)
    # qr_image_path = "path/to/qrcode.png"
    # 
    # png_path = exporter.export_to_png(qr_image_path, "example_export.png", dpi=300)
    # print(f"QR code exporté en PNG: {png_path}")
    # 
    # svg_path = exporter.export_to_svg(qr_image_path, "example_export.svg")
    # print(f"QR code exporté en SVG: {svg_path}")
    # 
    # pdf_path = exporter.export_to_pdf(qr_image_path, "example_export.pdf")
    # print(f"QR code exporté en PDF: {pdf_path}")
    # 
    # all_formats = exporter.export_to_all_formats(qr_image_path, "example_all_formats")
    # print(f"QR code exporté dans tous les formats: {all_formats}")
