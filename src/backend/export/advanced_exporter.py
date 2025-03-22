#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module d'exportation amélioré pour les QR codes.
Ce module fournit des fonctionnalités avancées pour exporter les QR codes
dans différents formats (PNG, SVG, PDF, EPS, JPG) avec des options flexibles.
"""

import os
import uuid
import zipfile
import io
from datetime import datetime
from PIL import Image, ImageDraw
import qrcode
import svgwrite
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter, A3, A5
from reportlab.lib.units import mm


class EnhancedQRExporter:
    """
    Classe avancée pour l'exportation de QR codes dans différents formats.
    Fournit des méthodes complètes pour exporter en PNG, SVG, PDF, EPS et JPG
    avec des options de personnalisation étendues.
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
        
        # Configuration des formats d'exportation disponibles
        self.available_formats = {
            'png': {
                'name': 'PNG',
                'description': 'Format image standard',
                'file_extension': '.png',
                'mime_type': 'image/png'
            },
            'jpg': {
                'name': 'JPG',
                'description': 'Format image compressé',
                'file_extension': '.jpg',
                'mime_type': 'image/jpeg'
            },
            'svg': {
                'name': 'SVG',
                'description': 'Format vectoriel pour impression',
                'file_extension': '.svg',
                'mime_type': 'image/svg+xml'
            },
            'pdf': {
                'name': 'PDF',
                'description': 'Document portable',
                'file_extension': '.pdf',
                'mime_type': 'application/pdf'
            },
            'eps': {
                'name': 'EPS',
                'description': 'Format pour impression professionnelle',
                'file_extension': '.eps',
                'mime_type': 'application/postscript'
            }
        }
        
        # Configuration des tailles de page disponibles pour le PDF
        self.pdf_page_sizes = {
            'a4': A4,
            'a3': A3,
            'a5': A5,
            'letter': letter
        }
    
    def export_to_png(self, qr_image_path, filename=None, **options):
        """
        Exporte un QR code au format PNG avec options avancées.
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code à exporter
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation
                - dpi (int): Résolution en DPI (72, 150, 300, 600)
                - quality (int): Qualité de l'image (1-100)
                - size (tuple): Dimensions souhaitées (width, height) en pixels
                - transparent (bool): Rendre le fond transparent
                - optimize (bool): Optimiser l'image
            
        Returns:
            str: Chemin du fichier PNG exporté
        """
        if not filename:
            filename = f"qrcode_export_{uuid.uuid4().hex[:8]}.png"
        
        # Ajout de l'extension .png si nécessaire
        if not filename.lower().endswith('.png'):
            filename += '.png'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Ouverture de l'image QR code
        img = Image.open(qr_image_path)
        
        # Conversion en RGBA si transparent est demandé
        if options.get('transparent', False):
            img = img.convert('RGBA')
            
            # Rendre transparent tous les pixels blancs
            datas = img.getdata()
            newData = []
            for item in datas:
                # Si le pixel est blanc ou presque blanc, le rendre transparent
                if item[0] > 240 and item[1] > 240 and item[2] > 240:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)
            img.putdata(newData)
        
        # Redimensionnement si spécifié
        if 'size' in options:
            img = img.resize(options['size'], Image.LANCZOS)
        
        # Options d'exportation
        export_options = {
            'dpi': (options.get('dpi', 300), options.get('dpi', 300)),
            'quality': options.get('quality', 95)
        }
        
        # Optimisation si spécifiée
        if options.get('optimize', False):
            export_options['optimize'] = True
        
        # Sauvegarde de l'image
        img.save(output_path, format='PNG', **export_options)
        
        # Enregistrement des métadonnées
        self._save_metadata(qr_image_path, output_path, 'PNG', options)
        
        return output_path
    
    def export_to_jpg(self, qr_image_path, filename=None, **options):
        """
        Exporte un QR code au format JPG.
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code à exporter
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation
                - quality (int): Qualité de l'image (1-95)
                - dpi (int): Résolution en DPI
                - size (tuple): Dimensions souhaitées (width, height) en pixels
                - optimize (bool): Optimiser l'image
            
        Returns:
            str: Chemin du fichier JPG exporté
        """
        if not filename:
            filename = f"qrcode_export_{uuid.uuid4().hex[:8]}.jpg"
        
        # Ajout de l'extension .jpg si nécessaire
        if not filename.lower().endswith(('.jpg', '.jpeg')):
            filename += '.jpg'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Ouverture de l'image QR code
        img = Image.open(qr_image_path)
        
        # Conversion en RGB (JPG ne supporte pas l'alpha)
        img = img.convert('RGB')
        
        # Redimensionnement si spécifié
        if 'size' in options:
            img = img.resize(options['size'], Image.LANCZOS)
        
        # Options d'exportation
        export_options = {
            'quality': min(options.get('quality', 95), 95),  # JPG a une qualité max de 95
            'dpi': (options.get('dpi', 300), options.get('dpi', 300))
        }
        
        # Optimisation si spécifiée
        if options.get('optimize', False):
            export_options['optimize'] = True
        
        # Sauvegarde de l'image
        img.save(output_path, format='JPEG', **export_options)
        
        # Enregistrement des métadonnées
        self._save_metadata(qr_image_path, output_path, 'JPG', options)
        
        return output_path
    
    def export_to_svg(self, qr_image_path, filename=None, **options):
        """
        Exporte un QR code au format SVG (vectoriel).
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code à exporter
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation
                - scale (float): Échelle du SVG
                - size (tuple): Dimensions souhaitées (width, height) en pixels
                - include_xml_declaration (bool): Inclure la déclaration XML
                - include_namespace (bool): Inclure les namespaces SVG
                - embed_image (bool): Intégrer l'image plutôt que de la vectoriser
            
        Returns:
            str: Chemin du fichier SVG exporté
        """
        if not filename:
            filename = f"qrcode_export_{uuid.uuid4().hex[:8]}.svg"
        
        # Ajout de l'extension .svg si nécessaire
        if not filename.lower().endswith('.svg'):
            filename += '.svg'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Ouverture de l'image QR code
        img = Image.open(qr_image_path)
        
        # Conversion en mode 1 (noir et blanc) pour simplifier la conversion
        img_bw = img.convert('1')
        
        # Dimensions de l'image
        width, height = img_bw.size
        
        # Redimensionnement si spécifié
        if 'size' in options:
            width, height = options['size']
            img_bw = img_bw.resize((width, height), Image.LANCZOS)
        
        # Échelle
        scale = options.get('scale', 1.0)
        
        # Options de génération SVG
        svg_options = {
            'size': (f"{width * scale}px", f"{height * scale}px"),
            'profile': 'tiny'
        }
        
        # Création du document SVG
        dwg = svgwrite.Drawing(output_path, **svg_options)
        
        # Intégrer l'image complète ou vectoriser les modules individuels
        if options.get('embed_image', False):
            # Conversion en base64 pour intégration
            import base64
            from io import BytesIO
            
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            # Ajout de l'image encodée en base64
            dwg.add(dwg.image(
                href=f"data:image/png;base64,{img_str}",
                insert=(0, 0),
                size=(f"{width * scale}px", f"{height * scale}px")
            ))
        else:
            # Parcours des pixels de l'image et création des rectangles
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
        dwg.save(pretty=True, indent=4)
        
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
                - title (str): Titre du document PDF
                - author (str): Auteur du document
                - subject (str): Sujet du document
                - keywords (str): Mots-clés du document
                - size (tuple): Dimensions du QR code en mm
                - position (tuple): Position du QR code en mm depuis le coin inférieur gauche
                - page_size (str): Taille de la page ('a4', 'a3', 'a5', 'letter')
                - orientation (str): Orientation de la page ('portrait', 'landscape')
                - include_data (bool): Inclure les données du QR code sous l'image
                - data (str): Données du QR code
                - include_box (bool): Inclure un cadre autour du QR code
                - include_date (bool): Inclure la date de génération
            
        Returns:
            str: Chemin du fichier PDF exporté
        """
        if not filename:
            filename = f"qrcode_export_{uuid.uuid4().hex[:8]}.pdf"
        
        # Ajout de l'extension .pdf si nécessaire
        if not filename.lower().endswith('.pdf'):
            filename += '.pdf'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Ouverture de l'image QR code
        img = Image.open(qr_image_path)
        
        # Détermination de la taille de page
        page_size_name = options.get('page_size', 'a4').lower()
        page_size = self.pdf_page_sizes.get(page_size_name, A4)
        
        # Orientation de la page
        orientation = options.get('orientation', 'portrait').lower()
        if orientation == 'landscape':
            page_size = page_size[1], page_size[0]  # Inversion largeur/hauteur
        
        # Création du document PDF
        c = canvas.Canvas(output_path, pagesize=page_size)
        
        # Métadonnées du document
        c.setTitle(options.get('title', 'QR Code'))
        c.setAuthor(options.get('author', 'QR Code Generator'))
        c.setSubject(options.get('subject', 'QR Code'))
        c.setKeywords(options.get('keywords', 'QR Code, Generator'))
        
        # Dimensions du QR code (en mm)
        qr_width = options.get('size', (50, 50))[0] * mm
        qr_height = options.get('size', (50, 50))[1] * mm
        
        # Position du QR code (en mm depuis le coin inférieur gauche)
        page_width, page_height = page_size
        qr_x = options.get('position', ((page_width - qr_width) / 2, (page_height - qr_height) / 2))[0]
        qr_y = options.get('position', ((page_width - qr_width) / 2, (page_height - qr_height) / 2))[1]
        
        # Conversion temporaire de l'image en PNG pour l'ajout au PDF
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Ajout de l'image au PDF
        c.drawImage(img_buffer, qr_x, qr_y, width=qr_width, height=qr_height)
        
        # Ajout d'un cadre autour du QR code si demandé
        if options.get('include_box', False):
            c.rect(qr_x, qr_y, qr_width, qr_height)
        
        # Ajout des données du QR code sous l'image si demandé
        if options.get('include_data', False):
            data = options.get('data', '')
            c.setFont("Helvetica", 10)
            text_width = c.stringWidth(data, "Helvetica", 10)
            text_x = qr_x + (qr_width - text_width) / 2
            text_y = qr_y - 15 * mm
            c.drawString(text_x, text_y, data)
        
        # Ajout de la date de génération si demandé
        if options.get('include_date', False):
            date_str = f"Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            c.setFont("Helvetica", 8)
            c.drawString(30 * mm, 20 * mm, date_str)
        
        # Sauvegarde du document PDF
        c.save()
        
        # Enregistrement des métadonnées
        self._save_metadata(qr_image_path, output_path, 'PDF', options)
        
        return output_path
    
    def export_to_eps(self, qr_image_path, filename=None, **options):
        """
        Exporte un QR code au format EPS.
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code à exporter
            filename (str, optional): Nom du fichier de sortie. Si non spécifié,
                génère un nom basé sur un UUID.
            **options: Options supplémentaires pour l'exportation
                - dpi (int): Résolution en DPI
                - size (tuple): Dimensions souhaitées en pixels
                - title (str): Titre du document EPS
                - preview (bool): Inclure une prévisualisation
            
        Returns:
            str: Chemin du fichier EPS exporté
        """
        if not filename:
            filename = f"qrcode_export_{uuid.uuid4().hex[:8]}.eps"
        
        # Ajout de l'extension .eps si nécessaire
        if not filename.lower().endswith('.eps'):
            filename += '.eps'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Ouverture de l'image QR code
        img = Image.open(qr_image_path)
        
        # Redimensionnement si spécifié
        if 'size' in options:
            img = img.resize(options['size'], Image.LANCZOS)
        
        # Options d'exportation EPS
        eps_options = {
            'dpi': (options.get('dpi', 300), options.get('dpi', 300))
        }
        
        # Titre du document si spécifié
        if 'title' in options:
            eps_options['title'] = options['title']
        
        # Ajout d'une prévisualisation si demandé (EPS ne supporte pas la prévisualisation directement)
        if options.get('preview', False):
            # La prévisualisation n'est pas directement supportée par PIL, cette option est ignorée
            pass
        
        # Sauvegarde au format EPS
        img.save(output_path, format='EPS', **eps_options)
        
        # Enregistrement des métadonnées
        self._save_metadata(qr_image_path, output_path, 'EPS', options)
        
        return output_path
    
    def export_to_all_formats(self, qr_image_path, base_filename=None, create_zip=True, **options):
        """
        Exporte un QR code dans tous les formats disponibles.
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code à exporter
            base_filename (str, optional): Nom de base pour les fichiers de sortie.
                Si non spécifié, génère un nom basé sur un UUID.
            create_zip (bool): Créer un fichier ZIP contenant tous les formats
            **options: Options supplémentaires pour l'exportation
            
        Returns:
            dict: Dictionnaire des chemins des fichiers exportés par format
                  ou chemin du fichier ZIP si create_zip=True
        """
        if not base_filename:
            base_filename = f"qrcode_export_{uuid.uuid4().hex[:8]}"
        
        # Exportation dans chaque format
        export_paths = {}
        
        # PNG
        png_options = dict(options.get('png_options', {}))
        png_path = self.export_to_png(
            qr_image_path, 
            f"{base_filename}.png", 
            **png_options
        )
        export_paths['png'] = png_path
        
        # JPG
        jpg_options = dict(options.get('jpg_options', {}))
        jpg_path = self.export_to_jpg(
            qr_image_path, 
            f"{base_filename}.jpg", 
            **jpg_options
        )
        export_paths['jpg'] = jpg_path
        
        # SVG
        svg_options = dict(options.get('svg_options', {}))
        svg_path = self.export_to_svg(
            qr_image_path, 
            f"{base_filename}.svg", 
            **svg_options
        )
        export_paths['svg'] = svg_path
        
        # PDF
        pdf_options = dict(options.get('pdf_options', {}))
        pdf_path = self.export_to_pdf(
            qr_image_path, 
            f"{base_filename}.pdf", 
            **pdf_options
        )
        export_paths['pdf'] = pdf_path
        
        # EPS
        eps_options = dict(options.get('eps_options', {}))
        eps_path = self.export_to_eps(
            qr_image_path, 
            f"{base_filename}.eps", 
            **eps_options
        )
        export_paths['eps'] = eps_path
        
        # Création d'un fichier ZIP si demandé
        if create_zip:
            zip_filename = f"{base_filename}_all_formats.zip"
            zip_path = os.path.join(self.output_dir, zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for format_type, path in export_paths.items():
                    zipf.write(path, os.path.basename(path))
            
            # Informations sur le ZIP
            export_paths['zip'] = zip_path
            export_paths['all_formats_zip'] = zip_path
        
        return export_paths
    
    def export_batch(self, qr_images, format_type='png', create_zip=True, **options):
        """
        Exporte un lot de QR codes dans le format spécifié.
        
        Args:
            qr_images (list): Liste de tuples (chemin_image, nom_fichier, metadata)
            format_type (str): Format d'exportation ('png', 'jpg', 'svg', 'pdf', 'eps', 'all')
            create_zip (bool): Créer un fichier ZIP contenant tous les exports
            **options: Options supplémentaires pour l'exportation
            
        Returns:
            dict: Dictionnaire des chemins des fichiers exportés ou chemin du ZIP
        """
        # Vérification du format demandé
        if format_type != 'all' and format_type not in self.available_formats:
            raise ValueError(f"Format d'exportation non reconnu: {format_type}")
        
        # Création d'un sous-répertoire pour le lot
        batch_dir = os.path.join(self.output_dir, f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(batch_dir, exist_ok=True)
        
        # Sauvegarde du répertoire de sortie actuel
        original_output_dir = self.output_dir
        self.output_dir = batch_dir
        
        try:
            # Exportation de chaque QR code
            export_paths = {}
            
            for qr_image_path, filename, metadata in qr_images:
                # Détermination du nom de fichier
                if not filename:
                    filename = os.path.basename(qr_image_path)
                    filename_base = os.path.splitext(filename)[0]
                else:
                    filename_base = os.path.splitext(filename)[0]
                
                # Ajout des métadonnées aux options si présentes
                local_options = dict(options)
                if metadata:
                    local_options.update(metadata)
                
                # Exportation selon le format demandé
                if format_type == 'all':
                    # Exportation dans tous les formats
                    paths = self.export_to_all_formats(
                        qr_image_path, 
                        filename_base,
                        create_zip=False,
                        **local_options
                    )
                    
                    for fmt, path in paths.items():
                        export_paths[f"{filename_base}_{fmt}"] = path
                else:
                    # Exportation dans le format spécifié
                    export_func = getattr(self, f"export_to_{format_type}")
                    export_filename = f"{filename_base}.{self.available_formats[format_type]['file_extension']}"
                    path = export_func(qr_image_path, export_filename, **local_options)
                    export_paths[filename_base] = path
            
            # Création d'un fichier ZIP contenant tous les exports si demandé
            if create_zip:
                zip_filename = f"batch_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                zip_path = os.path.join(original_output_dir, zip_filename)
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for path in export_paths.values():
                        zipf.write(path, os.path.basename(path))
                
                return {'zip': zip_path, 'files': export_paths}
            
            return export_paths
            
        finally:
            # Restauration du répertoire de sortie original
            self.output_dir = original_output_dir
    
    def get_available_formats(self):
        """
        Retourne la liste des formats d'exportation disponibles.
        
        Returns:
            list: Liste des formats d'exportation disponibles
        """
        formats = []
        for format_id, format_info in self.available_formats.items():
            formats.append({
                'id': format_id,
                'name': format_info['name'],
                'description': format_info['description'],
                'file_extension': format_info['file_extension'],
                'mime_type': format_info['mime_type']
            })
        
        # Ajout du format "all" pour exporter dans tous les formats
        formats.append({
            'id': 'all',
            'name': 'Tous les formats',
            'description': 'Exporte dans tous les formats disponibles (PNG, JPG, SVG, PDF, EPS)',
            'file_extension': '.zip',
            'mime_type': 'application/zip'
        })
        
        return formats
    
    def get_pdf_page_sizes(self):
        """
        Retourne la liste des tailles de page disponibles pour le PDF.
        
        Returns:
            list: Liste des tailles de page disponibles
        """
        sizes = []
        for size_id, size_value in self.pdf_page_sizes.items():
            sizes.append({
                'id': size_id,
                'name': size_id.upper(),
                'width_mm': size_value[0] / mm,
                'height_mm': size_value[1] / mm
            })
        
        return sizes
    
    def _save_metadata(self, source_path, output_path, format_type, options=None):
        """
        Enregistre les métadonnées de l'exportation.
        
        Args:
            source_path (str): Chemin du fichier source
            output_path (str): Chemin du fichier exporté
            format_type (str): Type de format d'exportation
            options (dict, optional): Options utilisées pour l'exportation
        """
        metadata_dir = os.path.join(self.output_dir, 'metadata')
        os.makedirs(metadata_dir, exist_ok=True)
        
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
    exporter = EnhancedQRExporter()
    
    # Exemple d'exportation (nécessite un fichier QR code existant)
    # qr_image_path = "path/to/qrcode.png"
    # 
    # png_path = exporter.export_to_png(qr_image_path, "example_export.png", dpi=300, transparent=True)
    # print(f"QR code exporté en PNG: {png_path}")
    # 
    # svg_path = exporter.export_to_svg(qr_image_path, "example_export.svg", scale=1.5)
    # print(f"QR code exporté en SVG: {svg_path}")
    # 
    # pdf_path = exporter.export_to_pdf(qr_image_path, "example_export.pdf", include_data=True, data="https://example.com")
    # print(f"QR code exporté en PDF: {pdf_path}")
    # 
    # all_formats = exporter.export_to_all_formats(qr_image_path, "example_all_formats")
    # print(f"QR code exporté dans tous les formats: {all_formats}")
