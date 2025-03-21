#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module d'exportation avancée pour les QR codes.
Ce module fournit des fonctionnalités pour exporter les QR codes
dans différents formats (PNG, SVG, PDF, EPS) avec des options avancées.
"""

import os
import uuid
import zipfile
from io import BytesIO
from datetime import datetime
from PIL import Image
import qrcode
import svgwrite
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm


class QRCodeExporter:
    """
    Classe pour l'exportation de QR codes dans différents formats.
    Fournit des méthodes pour exporter les QR codes en PNG, SVG, PDF et EPS.
    """

    def __init__(self, output_dir=None):
        """
        Initialise l'exportateur de QR codes.
        
        Args:
            output_dir (str, optional): Répertoire de sortie pour les QR codes exportés.
                Si non spécifié, utilise le répertoire courant.
        """
        self.output_dir = output_dir or os.path.join(os.getcwd(), 'exports')
        
        # Création du répertoire s'il n'existe pas
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def export_png(self, qr_image, filename=None, **options):
        """
        Exporte un QR code au format PNG.
        
        Args:
            qr_image: Image PIL du QR code à exporter
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation.
                - dpi (int): Résolution en DPI (par défaut: 300)
                - quality (int): Qualité de l'image (0-100, par défaut: 95)
                - transparent (bool): Fond transparent (par défaut: False)
            
        Returns:
            str: Chemin du fichier PNG exporté.
        """
        if not filename:
            filename = f"qrcode_{uuid.uuid4().hex[:8]}.png"
        
        # Ajout de l'extension .png si nécessaire
        if not filename.lower().endswith('.png'):
            filename += '.png'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Paramètres par défaut
        dpi = options.get('dpi', 300)
        quality = options.get('quality', 95)
        transparent = options.get('transparent', False)
        
        # Conversion en mode RGBA si transparent est True
        if transparent and qr_image.mode != 'RGBA':
            qr_image = qr_image.convert('RGBA')
        
        # Sauvegarde de l'image
        qr_image.save(output_path, format='PNG', dpi=(dpi, dpi), quality=quality)
        
        return output_path
    
    def export_svg(self, qr_image, filename=None, **options):
        """
        Exporte un QR code au format SVG.
        
        Args:
            qr_image: Image PIL du QR code à exporter
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation.
                - scale (float): Échelle de l'image (par défaut: 1.0)
                - include_xml_declaration (bool): Inclure la déclaration XML (par défaut: True)
            
        Returns:
            str: Chemin du fichier SVG exporté.
        """
        if not filename:
            filename = f"qrcode_{uuid.uuid4().hex[:8]}.svg"
        
        # Ajout de l'extension .svg si nécessaire
        if not filename.lower().endswith('.svg'):
            filename += '.svg'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Paramètres par défaut
        scale = options.get('scale', 1.0)
        include_xml_declaration = options.get('include_xml_declaration', True)
        
        # Conversion en mode 1 (noir et blanc) pour simplifier la conversion en SVG
        qr_image_bw = qr_image.convert('1')
        
        # Dimensions de l'image
        width, height = qr_image_bw.size
        
        # Création du document SVG
        dwg = svgwrite.Drawing(output_path, size=(width * scale, height * scale), profile='tiny')
        
        # Parcours des pixels de l'image et création de rectangles pour les pixels noirs
        for y in range(height):
            for x in range(width):
                pixel = qr_image_bw.getpixel((x, y))
                if pixel == 0:  # Pixel noir
                    dwg.add(dwg.rect(
                        insert=(x * scale, y * scale),
                        size=(scale, scale),
                        fill='black'
                    ))
        
        # Sauvegarde du fichier SVG
        dwg.save(pretty=True, indent=4)
        
        return output_path
    
    def export_pdf(self, qr_image, filename=None, **options):
        """
        Exporte un QR code au format PDF.
        
        Args:
            qr_image: Image PIL du QR code à exporter
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation.
                - title (str): Titre du document (par défaut: "QR Code")
                - author (str): Auteur du document (par défaut: "QR Code Generator")
                - subject (str): Sujet du document (par défaut: "QR Code")
                - keywords (str): Mots-clés du document (par défaut: "QR Code, Generator")
                - size_width (int): Largeur du QR code en mm (par défaut: 50)
                - size_height (int): Hauteur du QR code en mm (par défaut: 50)
                - position_x (int): Position X du QR code en mm (par défaut: centré)
                - position_y (int): Position Y du QR code en mm (par défaut: centré)
                - page_size (tuple): Taille de la page (par défaut: A4)
                - include_data (bool): Inclure les données du QR code (par défaut: False)
                - data (str): Données du QR code (par défaut: "")
            
        Returns:
            str: Chemin du fichier PDF exporté.
        """
        if not filename:
            filename = f"qrcode_{uuid.uuid4().hex[:8]}.pdf"
        
        # Ajout de l'extension .pdf si nécessaire
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Paramètres par défaut
        title = options.get('title', "QR Code")
        author = options.get('author', "QR Code Generator")
        subject = options.get('subject', "QR Code")
        keywords = options.get('keywords', "QR Code, Generator")
        size_width = options.get('size_width', 50) * mm
        size_height = options.get('size_height', 50) * mm
        page_size = options.get('page_size', A4)
        include_data = options.get('include_data', False)
        data = options.get('data', "")
        
        # Calcul des positions par défaut (centrées)
        page_width, page_height = page_size
        position_x = options.get('position_x', (page_width - size_width) / 2)
        position_y = options.get('position_y', (page_height - size_height) / 2)
        
        # Conversion de l'image en format PNG pour l'intégration dans le PDF
        img_buffer = BytesIO()
        qr_image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Création du document PDF
        c = canvas.Canvas(output_path, pagesize=page_size)
        
        # Métadonnées du document
        c.setTitle(title)
        c.setAuthor(author)
        c.setSubject(subject)
        c.setKeywords(keywords)
        
        # Ajout de l'image QR code
        c.drawImage(img_buffer, position_x, position_y, width=size_width, height=size_height)
        
        # Ajout des données du QR code si demandé
        if include_data and data:
            c.setFont("Helvetica", 10)
            text_width = c.stringWidth(data, "Helvetica", 10)
            text_x = (page_width - text_width) / 2
            text_y = position_y - 15 * mm
            c.drawString(text_x, text_y, data)
        
        # Sauvegarde du document PDF
        c.save()
        
        return output_path
    
    def export_eps(self, qr_image, filename=None, **options):
        """
        Exporte un QR code au format EPS.
        
        Args:
            qr_image: Image PIL du QR code à exporter
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation.
                - dpi (int): Résolution en DPI (par défaut: 300)
            
        Returns:
            str: Chemin du fichier EPS exporté.
        """
        if not filename:
            filename = f"qrcode_{uuid.uuid4().hex[:8]}.eps"
        
        # Ajout de l'extension .eps si nécessaire
        if not filename.lower().endswith('.eps'):
            filename += '.eps'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Paramètres par défaut
        dpi = options.get('dpi', 300)
        
        # Sauvegarde de l'image au format EPS
        qr_image.save(output_path, format='EPS', dpi=(dpi, dpi))
        
        return output_path
    
    def export_all_formats(self, qr_image, base_filename=None, **options):
        """
        Exporte un QR code dans tous les formats disponibles.
        
        Args:
            qr_image: Image PIL du QR code à exporter
            base_filename (str, optional): Nom de base pour les fichiers de sortie.
                Si non spécifié, génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation.
            
        Returns:
            dict: Dictionnaire des chemins des fichiers exportés par format.
        """
        if not base_filename:
            base_filename = f"qrcode_{uuid.uuid4().hex[:8]}"
        
        # Exportation dans chaque format
        png_path = self.export_png(qr_image, f"{base_filename}.png", **options)
        svg_path = self.export_svg(qr_image, f"{base_filename}.svg", **options)
        pdf_path = self.export_pdf(qr_image, f"{base_filename}.pdf", **options)
        eps_path = self.export_eps(qr_image, f"{base_filename}.eps", **options)
        
        # Création d'un fichier ZIP contenant tous les formats
        zip_filename = f"{base_filename}_all_formats.zip"
        zip_path = os.path.join(self.output_dir, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(png_path, os.path.basename(png_path))
            zipf.write(svg_path, os.path.basename(svg_path))
            zipf.write(pdf_path, os.path.basename(pdf_path))
            zipf.write(eps_path, os.path.basename(eps_path))
        
        # Retour des chemins des fichiers exportés
        return {
            'png': png_path,
            'svg': svg_path,
            'pdf': pdf_path,
            'eps': eps_path,
            'zip': zip_path
        }
    
    def export_batch(self, qr_images, format_type='png', **options):
        """
        Exporte un lot de QR codes dans le format spécifié.
        
        Args:
            qr_images (list): Liste de tuples (image, nom_fichier) des QR codes à exporter
            format_type (str): Format d'exportation ('png', 'svg', 'pdf', 'eps', 'all')
            **options: Options supplémentaires pour l'exportation.
            
        Returns:
            list: Liste des chemins des fichiers exportés.
        """
        exported_paths = []
        
        # Création d'un répertoire spécifique pour le lot
        batch_dir = os.path.join(self.output_dir, f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        if not os.path.exists(batch_dir):
            os.makedirs(batch_dir)
        
        # Sauvegarde du répertoire de sortie actuel
        original_output_dir = self.output_dir
        self.output_dir = batch_dir
        
        try:
            # Exportation de chaque QR code
            for qr_image, filename in qr_images:
                if format_type == 'png':
                    path = self.export_png(qr_image, filename, **options)
                elif format_type == 'svg':
                    path = self.export_svg(qr_image, filename, **options)
                elif format_type == 'pdf':
                    path = self.export_pdf(qr_image, filename, **options)
                elif format_type == 'eps':
                    path = self.export_eps(qr_image, filename, **options)
                elif format_type == 'all':
                    paths = self.export_all_formats(qr_image, filename, **options)
                    path = paths['zip']  # Utilisation du fichier ZIP comme chemin principal
                else:
                    raise ValueError(f"Format d'exportation non reconnu: {format_type}")
                
                exported_paths.append(path)
            
            # Création d'un fichier ZIP contenant tous les QR codes exportés
            zip_filename = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            zip_path = os.path.join(original_output_dir, zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for path in exported_paths:
                    zipf.write(path, os.path.basename(path))
            
            # Ajout du fichier ZIP à la liste des chemins exportés
            exported_paths.append(zip_path)
            
            return exported_paths
            
        finally:
            # Restauration du répertoire de sortie original
            self.output_dir = original_output_dir


# Exemple d'utilisation si exécuté directement
if __name__ == "__main__":
    # Création d'un QR code de test
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data("https://www.example.com")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Exportation du QR code
    exporter = QRCodeExporter()
    
    # Exportation en PNG
    png_path = exporter.export_png(qr_img, "example.png", dpi=300, quality=95)
    print(f"QR code exporté en PNG: {png_path}")
    
    # Exportation en SVG
    svg_path = exporter.export_svg(qr_img, "example.svg", scale=1.5)
    print(f"QR code exporté en SVG: {svg_path}")
    
    # Exportation en PDF
    pdf_path = exporter.export_pdf(qr_img, "example.pdf", title="Exemple de QR Code", include_data=True, data="https://www.example.com")
    print(f"QR code exporté en PDF: {pdf_path}")
    
    # Exportation en EPS
    eps_path = exporter.export_eps(qr_img, "example.eps", dpi=300)
    print(f"QR code exporté en EPS: {eps_path}")
    
    # Exportation dans tous les formats
    all_paths = exporter.export_all_formats(qr_img, "example_all")
    print(f"QR code exporté dans tous les formats: {all_paths}")
