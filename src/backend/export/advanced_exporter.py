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
from PIL import Image, ImageDraw, ImageFont
import qrcode
import svgwrite
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter, A3, A5
from reportlab.lib.units import mm, inch
from reportlab.lib.colors import black, white, HexColor


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
        
        # Conversion en mode 1 (noir et blanc) pour simplifier la vectorisation
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
                - logo_path (str): Chemin vers un logo à inclure
            
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
        c.drawImage(img_buffer, qr_x, qr_y, width=qr_width, height=qr_height, mask='auto')
        
        # Ajout d'un cadre autour du QR code si demandé
        if options.get('include_box', False):
            c.rect(qr_x - 2*mm, qr_y - 2*mm, qr_width + 4*mm, qr_height + 4*mm, stroke=1, fill=0)
        
        # Ajout des données du QR code si demandé
        if options.get('include_data', False):
            data = options.get('data', 'QR Code')
            c.setFont("Helvetica", 10)
            text_width = c.stringWidth(data, "Helvetica", 10)
            c.drawString((page_width - text_width) / 2, qr_y - 10*mm, data)
        
        # Ajout de la date de génération si demandé
        if options.get('include_date', False):
            date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.setFont("Helvetica", 8)
            c.drawString(20*mm, 20*mm, f"Généré le: {date_str}")
        
        # Ajout d'un logo si spécifié
        logo_path = options.get('logo_path', None)
        if logo_path and os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path)
                # Calcul de la taille du logo (25% de la largeur du QR code)
                logo_width = qr_width * 0.25
                logo_height = qr_height * 0.25
                
                # Position du logo (en haut du QR code)
                logo_x = qr_x + (qr_width - logo_width) / 2
                logo_y = qr_y + qr_height + 5*mm
                
                # Conversion en PNG pour l'ajout au PDF
                logo_buffer = io.BytesIO()
                logo.save(logo_buffer, format='PNG')
                logo_buffer.seek(0)
                
                # Ajout du logo au PDF
                c.drawImage(logo_buffer, logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')
            except Exception as e:
                print(f"Erreur lors de l'ajout du logo: {e}")
        
        # Finalisation du PDF
        c.save()
        
        # Enregistrement des métadonnées
        self._save_metadata(qr_image_path, output_path, 'PDF', options)
        
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
                - size (tuple): Dimensions souhaitées (width, height) en pixels
                - include_preview (bool): Inclure une prévisualisation TIFF
            
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
        
        # Conversion en mode L (niveaux de gris) pour simplifier l'export EPS
        img = img.convert('L')
        
        # Options d'exportation
        export_options = {}
        
        # Résolution DPI
        if 'dpi' in options:
            export_options['dpi'] = (options['dpi'], options['dpi'])
        
        # Inclure une prévisualisation TIFF
        if options.get('include_preview', True):
            export_options['eps_preview'] = 1
        
        # Sauvegarde en EPS
        img.save(output_path, format='EPS', **export_options)
        
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
            **options: Options supplémentaires pour l'exportation de chaque format
            
        Returns:
            dict or str: Dictionnaire des chemins par format, ou chemin du ZIP si create_zip=True
        """
        if not base_filename:
            base_filename = f"qrcode_export_{uuid.uuid4().hex[:8]}"
        
        # Dictionnaire pour stocker les chemins des fichiers exportés
        export_paths = {}
        
        # Exportation dans chaque format
        for format_id, format_info in self.available_formats.items():
            try:
                filename = f"{base_filename}{format_info['file_extension']}"
                
                # Sélection de la méthode d'exportation appropriée
                if format_id == 'png':
                    path = self.export_to_png(qr_image_path, filename, **options)
                elif format_id == 'jpg':
                    path = self.export_to_jpg(qr_image_path, filename, **options)
                elif format_id == 'svg':
                    path = self.export_to_svg(qr_image_path, filename, **options)
                elif format_id == 'pdf':
                    path = self.export_to_pdf(qr_image_path, filename, **options)
                elif format_id == 'eps':
                    path = self.export_to_eps(qr_image_path, filename, **options)
                else:
                    continue
                
                export_paths[format_id] = path
                
            except Exception as e:
                print(f"Erreur lors de l'exportation au format {format_id}: {e}")
        
        # Création d'un fichier ZIP si demandé
        if create_zip and export_paths:
            zip_path = os.path.join(self.output_dir, f"{base_filename}_all_formats.zip")
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for format_id, path in export_paths.items():
                    zipf.write(path, os.path.basename(path))
            
            return zip_path
        
        return export_paths
    
    def _save_metadata(self, source_path, output_path, format_type, options=None):
        """
        Enregistre les métadonnées du QR code exporté.
        
        Args:
            source_path (str): Chemin de l'image QR code source
            output_path (str): Chemin du fichier exporté
            format_type (str): Type de format d'exportation
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
            f"Format d'exportation: {format_type}"
        ]
        
        # Ajout des options si spécifiées
        if options:
            metadata_content.append("Options d'exportation:")
            for key, value in options.items():
                metadata_content.append(f"  {key}: {value}")
        
        # Écriture des métadonnées dans le fichier
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(metadata_content))
    
    def add_social_icons_to_qrcode(self, qr_image_path, social_platforms, filename=None, **options):
        """
        Ajoute des icônes de réseaux sociaux autour d'un QR code.
        
        Args:
            qr_image_path (str): Chemin vers l'image QR code
            social_platforms (list): Liste des identifiants de plateformes sociales
            filename (str, optional): Nom du fichier de sortie
            **options: Options supplémentaires
                - layout (str): Disposition des icônes ('circle', 'row', 'column')
                - size (int): Taille des icônes en pixels
                - padding (int): Espacement entre les icônes et le QR code
                - background_color (tuple): Couleur d'arrière-plan (R,G,B)
                
        Returns:
            str: Chemin de l'image QR code avec icônes sociales
        """
        if not filename:
            filename = f"social_qrcode_{uuid.uuid4().hex[:8]}.png"
        
        # Ajout de l'extension .png si nécessaire
        if not filename.lower().endswith('.png'):
            filename += '.png'
        
        # Chemin complet du fichier de sortie
        output_path = os.path.join(self.output_dir, filename)
        
        # Ouverture de l'image QR code
        qr_img = Image.open(qr_image_path).convert('RGBA')
        qr_width, qr_height = qr_img.size
        
        # Options par défaut
        layout = options.get('layout', 'circle')
        icon_size = options.get('size', 36)  # taille par défaut des icônes
        padding = options.get('padding', 20)  # espace entre le QR code et les icônes
        bg_color = options.get('background_color', (255, 255, 255, 255))
        
        # Chargement des icônes
        icons = []
        for platform_id in social_platforms:
            try:
                # Chemin vers l'icône (à adapter selon votre structure de fichiers)
                icon_path = os.path.join('src', 'frontend', 'static', 'img', 'social_icons', f"{platform_id}.png")
                if os.path.exists(icon_path):
                    icon = Image.open(icon_path).convert('RGBA')
                    icon = icon.resize((icon_size, icon_size), Image.LANCZOS)
                    icons.append(icon)
            except Exception as e:
                print(f"Erreur lors du chargement de l'icône {platform_id}: {e}")
        
        # Si aucune icône n'a été chargée, retourner l'image originale
        if not icons:
            qr_img.save(output_path)
            return output_path
        
        # Calcul des dimensions de l'image finale selon la disposition
        if layout == 'circle':
            # Disposition en cercle autour du QR code
            circle_radius = (max(qr_width, qr_height) // 2) + padding + (icon_size // 2)
            final_width = final_height = 2 * circle_radius + icon_size
        elif layout == 'row':
            # Disposition en ligne horizontale sous le QR code
            final_width = max(qr_width, len(icons) * (icon_size + padding) - padding)
            final_height = qr_height + padding + icon_size
        elif layout == 'column':
            # Disposition en colonne verticale à droite du QR code
            final_width = qr_width + padding + icon_size
            final_height = max(qr_height, len(icons) * (icon_size + padding) - padding)
        else:
            # Disposition par défaut (cercle)
            circle_radius = (max(qr_width, qr_height) // 2) + padding + (icon_size // 2)
            final_width = final_height = 2 * circle_radius + icon_size
        
        # Création de l'image finale
        final_img = Image.new('RGBA', (final_width, final_height), bg_color)
        
        # Position du QR code au centre
        qr_pos_x = (final_width - qr_width) // 2
        qr_pos_y = (final_height - qr_height) // 2
        final_img.paste(qr_img, (qr_pos_x, qr_pos_y), qr_img)
        
        # Placement des icônes selon la disposition
        if layout == 'circle':
            # Disposition en cercle
            num_icons = len(icons)
            center_x, center_y = final_width // 2, final_height // 2
            
            for i, icon in enumerate(icons):
                angle = 2 * 3.14159 * i / num_icons
                icon_x = center_x + int(circle_radius * (i % 2 == 0)) * int(angle)  # Position x
                icon_y = center_y + int(circle_radius * (i % 2 == 1)) * int(angle)  # Position y
                
                # Ajustement pour que l'icône soit centrée
                icon_pos_x = int(center_x + circle_radius * (i % 2 == 0)) - icon_size // 2
                icon_pos_y = int(center_y + circle_radius * (i % 2 == 1)) - icon_size // 2
                
                final_img.paste(icon, (icon_pos_x, icon_pos_y), icon)
                
        elif layout == 'row':
            # Disposition en ligne horizontale
            total_icons_width = len(icons) * (icon_size + padding) - padding
            start_x = (final_width - total_icons_width) // 2
            
            for i, icon in enumerate(icons):
                icon_pos_x = start_x + i * (icon_size + padding)
                icon_pos_y = qr_pos_y + qr_height + padding
                final_img.paste(icon, (icon_pos_x, icon_pos_y), icon)
                
        elif layout == 'column':
            # Disposition en colonne verticale
            total_icons_height = len(icons) * (icon_size + padding) - padding
            start_y = (final_height - total_icons_height) // 2
            
            for i, icon in enumerate(icons):
                icon_pos_x = qr_pos_x + qr_width + padding
                icon_pos_y = start_y + i * (icon_size + padding)
                final_img.paste(icon, (icon_pos_x, icon_pos_y), icon)
        
        # Sauvegarde de l'image finale
        final_img.save(output_path)
        
        # Enregistrement des métadonnées
        options['social_platforms'] = social_platforms
        options['layout'] = layout
        self._save_metadata(qr_image_path, output_path, 'PNG+Social', options)
        
        return output_pathr_image_path)
        
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
        img = Image.open(q
