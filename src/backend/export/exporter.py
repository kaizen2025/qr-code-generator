#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module d'exportation pour les QR codes.
Ce module fournit des fonctionnalités pour exporter les QR codes générés
dans différents formats (PNG, SVG, PDF, EPS) avec diverses options.
"""

import os
import uuid
import zipfile
import io
from datetime import datetime
from PIL import Image
import svgwrite
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm


class QRCodeExporter:
    """
    Classe pour l'exportation de QR codes dans différents formats.
    Fournit des méthodes pour convertir et sauvegarder des QR codes
    en PNG, SVG, PDF et EPS avec différentes options de qualité et de taille.
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
        os.makedirs(self.output_dir, exist_ok=True)
    
    def export_to_png(self, qr_image_path, filename=None, **options):
        """
        Exporte un QR code au format PNG.
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code à exporter
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation
                - dpi (int): Résolution en DPI (72, 150, 300, 600)
                - quality (int): Qualité de l'image (1-100)
                - size (tuple): Dimensions souhaitées (width, height) en pixels
            
        Returns:
            str: Chemin du fichier PNG exporté
        """
        if not filename:
            filename = f"qrcode_export_{uuid.uuid4().hex}.png"
        
        # Ajout de l'extension .png si nécessaire
        if not filename.lower().endswith('.png'):
            filename += '.png'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Ouverture de l'image QR code
        img = Image.open(qr_image_path)
        
        # Redimensionnement si spécifié
        if 'size_width' in options and 'size_height' in options:
            try:
                width = int(options['size_width'])
                height = int(options['size_height'])
                img = img.resize((width, height), Image.LANCZOS)
            except (ValueError, TypeError) as e:
                print(f"Erreur lors du redimensionnement: {e}")
        
        # Qualité de l'image (pour JPEG, ignoré pour PNG)
        quality = min(max(int(options.get('quality', 95)), 1), 100)
        
        # DPI (résolution)
        dpi = (int(options.get('dpi', 300)), int(options.get('dpi', 300)))
        
        # Sauvegarde de l'image avec les options spécifiées
        img.save(output_path, format='PNG', dpi=dpi, quality=quality, optimize=True)
        
        return output_path
    
    def export_to_svg(self, qr_image_path, filename=None, **options):
        """
        Exporte un QR code au format SVG.
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code à exporter
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation
                - scale (float): Échelle de l'image (0.5-3.0)
                - size (tuple): Dimensions souhaitées (width, height) en pixels
            
        Returns:
            str: Chemin du fichier SVG exporté
        """
        if not filename:
            filename = f"qrcode_export_{uuid.uuid4().hex}.svg"
        
        # Ajout de l'extension .svg si nécessaire
        if not filename.lower().endswith('.svg'):
            filename += '.svg'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Ouverture de l'image QR code
        img = Image.open(qr_image_path)
        
        # Conversion en mode 1 (noir et blanc) pour simplifier la vectorisation
        img_bw = img.convert('1')
        
        # Dimensions de l'image
        width, height = img_bw.size
        
        # Redimensionnement si spécifié
        if 'size_width' in options and 'size_height' in options:
            try:
                width = int(options['size_width'])
                height = int(options['size_height'])
                img_bw = img_bw.resize((width, height), Image.LANCZOS)
            except (ValueError, TypeError) as e:
                print(f"Erreur lors du redimensionnement: {e}")
        
        # Échelle
        scale = float(options.get('scale', 1.0))
        
        # Options de génération SVG
        svg_options = {
            'size': (f"{width * scale}px", f"{height * scale}px"),
            'profile': 'tiny'
        }
        
        # Création du document SVG
        dwg = svgwrite.Drawing(output_path, **svg_options)
        
        # Parcours des pixels de l'image et création des rectangles vectoriels
        for y in range(height):
            for x in range(width):
                pixel = img_bw.getpixel((x, y))
                if pixel == 0:  # pixel noir
                    dwg.add(dwg.rect(
                        insert=(x * scale, y * scale),
                        size=(scale, scale),
                        fill='black'
                    ))
        
        # Ajouter des métadonnées au SVG
        description = f"QR Code généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        dwg.add(dwg.desc(description))
        
        # Sauvegarde du fichier SVG
        dwg.save(pretty=True)
        
        return output_path
    
    def export_to_pdf(self, qr_image_path, filename=None, **options):
        """
        Exporte un QR code au format PDF.
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code à exporter
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation
                - title (str): Titre du document PDF
                - author (str): Auteur du document
                - size (tuple): Dimensions du QR code en mm
                - position (tuple): Position du QR code en mm depuis le coin inférieur gauche
            
        Returns:
            str: Chemin du fichier PDF exporté
        """
        if not filename:
            filename = f"qrcode_export_{uuid.uuid4().hex}.pdf"
        
        # Ajout de l'extension .pdf si nécessaire
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Ouverture de l'image QR code
        img = Image.open(qr_image_path)
        
        # Création du document PDF avec une page A4
        c = canvas.Canvas(output_path, pagesize=A4)
        
        # Métadonnées du document
        c.setTitle(options.get('title', 'QR Code'))
        c.setAuthor(options.get('author', 'QR Code Generator'))
        
        # Dimensions du QR code (en mm)
        qr_width = float(options.get('size_width', 50)) * mm
        qr_height = float(options.get('size_height', 50)) * mm
        
        # Position du QR code (en mm depuis le coin inférieur gauche)
        qr_x = float(options.get('position_x', 80)) * mm
        qr_y = float(options.get('position_y', 150)) * mm
        
        # Conversion temporaire de l'image en PNG pour l'ajout au PDF
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Ajout de l'image au PDF
        c.drawImage(img_buffer, qr_x, qr_y, width=qr_width, height=qr_height)
        
        # Finalisation du PDF
        c.save()
        
        return output_path
    
    def export_to_eps(self, qr_image_path, filename=None, **options):
        """
        Exporte un QR code au format EPS (PostScript).
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code à exporter
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation
                - dpi (int): Résolution en DPI
            
        Returns:
            str: Chemin du fichier EPS exporté
        """
        if not filename:
            filename = f"qrcode_export_{uuid.uuid4().hex}.eps"
        
        # Ajout de l'extension .eps si nécessaire
        if not filename.lower().endswith('.eps'):
            filename += '.eps'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Ouverture de l'image QR code
        img = Image.open(qr_image_path)
        
        # Conversion en mode L (niveaux de gris) pour simplifier l'export EPS
        img = img.convert('L')
        
        # Options d'exportation
        export_options = {}
        
        # Résolution DPI
        if 'dpi' in options:
            try:
                dpi = int(options['dpi'])
                export_options['dpi'] = (dpi, dpi)
            except (ValueError, TypeError) as e:
                print(f"Erreur lors de la configuration du DPI: {e}")
        
        # Sauvegarde en EPS
        img.save(output_path, format='EPS', **export_options)
        
        return output_path
    
    def export_to_all_formats(self, qr_image_path, base_filename=None, **options):
        """
        Exporte un QR code dans tous les formats disponibles.
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code à exporter
            base_filename (str, optional): Base du nom de fichier pour les exports.
                Si non spécifié, génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation
            
        Returns:
            dict: Dictionnaire des chemins des fichiers exportés par format
        """
        if not base_filename:
            base_filename = f"qrcode_export_{uuid.uuid4().hex}"
        
        # Dictionnaire des chemins de fichiers exportés
        export_paths = {}
        
        # Export en PNG
        png_filename = f"{base_filename}.png"
        export_paths['png'] = self.export_to_png(qr_image_path, png_filename, **options)
        
        # Export en SVG
        svg_filename = f"{base_filename}.svg"
        export_paths['svg'] = self.export_to_svg(qr_image_path, svg_filename, **options)
        
        # Export en PDF
        pdf_filename = f"{base_filename}.pdf"
        export_paths['pdf'] = self.export_to_pdf(qr_image_path, pdf_filename, **options)
        
        # Export en EPS
        eps_filename = f"{base_filename}.eps"
        export_paths['eps'] = self.export_to_eps(qr_image_path, eps_filename, **options)
        
        return export_paths
    
    def create_zip_archive(self, filepaths, zip_filename=None):
        """
        Crée une archive ZIP contenant les fichiers spécifiés.
        
        Args:
            filepaths (list): Liste des chemins des fichiers à inclure
            zip_filename (str, optional): Nom du fichier ZIP. Si non spécifié,
                génère un nom basé sur un UUID.
            
        Returns:
            str: Chemin de l'archive ZIP créée
        """
        if not zip_filename:
            zip_filename = f"qrcode_export_{uuid.uuid4().hex}.zip"
        
        # Ajout de l'extension .zip si nécessaire
        if not zip_filename.lower().endswith('.zip'):
            zip_filename += '.zip'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, zip_filename)
        
        # Création de l'archive ZIP
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filepath in filepaths:
                if os.path.exists(filepath):
                    # Ajouter le fichier à l'archive avec son nom de base
                    zipf.write(filepath, os.path.basename(filepath))
        
        return output_path
    
    def export_to_multiple_formats(self, qr_image_path, formats, zip_archive=True, **options):
        """
        Exporte un QR code dans plusieurs formats spécifiés.
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code à exporter
            formats (list): Liste des formats à exporter ('png', 'svg', 'pdf', 'eps')
            zip_archive (bool): Créer une archive ZIP contenant tous les fichiers
            **options: Options supplémentaires pour l'exportation
            
        Returns:
            str or dict: Chemin de l'archive ZIP ou dictionnaire des chemins des 
                fichiers exportés si zip_archive=False
        """
        base_filename = f"qrcode_export_{uuid.uuid4().hex}"
        export_paths = {}
        
        # Export dans les formats spécifiés
        if 'png' in formats:
            png_filename = f"{base_filename}.png"
            export_paths['png'] = self.export_to_png(qr_image_path, png_filename, **options)
            
        if 'svg' in formats:
            svg_filename = f"{base_filename}.svg"
            export_paths['svg'] = self.export_to_svg(qr_image_path, svg_filename, **options)
            
        if 'pdf' in formats:
            pdf_filename = f"{base_filename}.pdf"
            export_paths['pdf'] = self.export_to_pdf(qr_image_path, pdf_filename, **options)
            
        if 'eps' in formats:
            eps_filename = f"{base_filename}.eps"
            export_paths['eps'] = self.export_to_eps(qr_image_path, eps_filename, **options)
        
        # Création d'une archive ZIP si demandé
        if zip_archive and export_paths:
            zip_filename = f"{base_filename}_all_formats.zip"
            zip_path = self.create_zip_archive(export_paths.values(), zip_filename)
            return zip_path
        
        return export_paths
    
    def batch_export(self, qr_image_paths, format, output_prefix=None, **options):
        """
        Exporte plusieurs QR codes en lot dans le même format.
        
        Args:
            qr_image_paths (list): Liste des chemins des images QR code à exporter
            format (str): Format d'exportation ('png', 'svg', 'pdf', 'eps')
            output_prefix (str, optional): Préfixe pour les noms de fichiers
            **options: Options supplémentaires pour l'exportation
            
        Returns:
            list: Liste des chemins des fichiers exportés
        """
        if not output_prefix:
            output_prefix = f"batch_export_{uuid.uuid4().hex[:8]}"
        
        # Liste des chemins des fichiers exportés
        exported_paths = []
        
        # Export des QR codes
        for i, qr_path in enumerate(qr_image_paths):
            if not os.path.exists(qr_path):
                continue
            
            # Nom de fichier avec préfixe et index
            filename = f"{output_prefix}_{i+1}.{format}"
            
            # Export dans le format spécifié
            if format == 'png':
                export_path = self.export_to_png(qr_path, filename, **options)
            elif format == 'svg':
                export_path = self.export_to_svg(qr_path, filename, **options)
            elif format == 'pdf':
                export_path = self.export_to_pdf(qr_path, filename, **options)
            elif format == 'eps':
                export_path = self.export_to_eps(qr_path, filename, **options)
            else:
                continue
            
            exported_paths.append(export_path)
        
        return exported_paths
