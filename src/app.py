#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application principale Flask pour le générateur de QR codes personnalisé.
Ce module fournit l'interface web pour interagir avec les modules de génération,
personnalisation et exportation de QR codes.
"""

import os
import sys
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for, redirect

# Add the parent directory to sys.path for imports to work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import des modules backend - with try/except for different environments
try:
    # Try direct imports first (when running from src directory)
    from backend.qr_generator.basic_generator import QRCodeGenerator
    from backend.customization.style_customizer import QRCodeCustomizer
    from backend.export.exporter import QRCodeExporter
except ImportError:
    # Fall back to fully qualified imports 
    from src.backend.qr_generator.basic_generator import QRCodeGenerator
    from src.backend.customization.style_customizer import QRCodeCustomizer
    from src.backend.export.exporter import QRCodeExporter

# Création de l'application Flask
app = Flask(__name__, 
            static_folder='frontend/static',
            template_folder='frontend/templates')

# Add context processor for datetime
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Base directory determination - ensures paths work both locally and on Render
if os.environ.get('RENDER'):
    # On Render
    BASE_DIR = os.environ.get('RENDER_PROJECT_DIR', os.getcwd())
else:
    # Local development
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuration de l'application with better path handling
for folder in [app.config['UPLOAD_FOLDER'], app.config['GENERATED_FOLDER'], app.config['EXPORTED_FOLDER']]:
    os.makedirs(folder, exist_ok=True)
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['GENERATED_FOLDER'] = os.path.join(BASE_DIR, 'generated_qrcodes')
app.config['EXPORTED_FOLDER'] = os.path.join(BASE_DIR, 'exported_qrcodes')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

# Création des dossiers nécessaires s'ils n'existent pas
for folder in [app.config['UPLOAD_FOLDER'], app.config['GENERATED_FOLDER'], app.config['EXPORTED_FOLDER']]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Initialisation des classes backend
qr_generator = QRCodeGenerator(output_dir=app.config['GENERATED_FOLDER'])
qr_customizer = QRCodeCustomizer(output_dir=app.config['GENERATED_FOLDER'])
qr_exporter = QRCodeExporter(output_dir=app.config['EXPORTED_FOLDER'])

# Liste des styles prédéfinis pour l'interface
PREDEFINED_STYLES = [
    {'id': 'classic', 'name': 'Classique', 'description': 'Style classique noir et blanc'},
    {'id': 'rounded', 'name': 'Arrondi', 'description': 'Modules arrondis noir et blanc'},
    {'id': 'dots', 'name': 'Points', 'description': 'Modules en forme de points'},
    {'id': 'modern_blue', 'name': 'Bleu Moderne', 'description': 'Style moderne avec dégradé bleu'},
    {'id': 'sunset', 'name': 'Coucher de Soleil', 'description': 'Dégradé orange-rouge'},
    {'id': 'forest', 'name': 'Forêt', 'description': 'Dégradé de verts'},
    {'id': 'ocean', 'name': 'Océan', 'description': 'Dégradé de bleus'},
    {'id': 'barcode', 'name': 'Code-barres', 'description': 'Style code-barres vertical'},
    {'id': 'elegant', 'name': 'Élégant', 'description': 'Style minimaliste avec espacement'}
]

# Liste des formats d'exportation disponibles
EXPORT_FORMATS = [
    {'id': 'png', 'name': 'PNG', 'description': 'Format image standard'},
    {'id': 'svg', 'name': 'SVG', 'description': 'Format vectoriel pour impression'},
    {'id': 'pdf', 'name': 'PDF', 'description': 'Document portable'}
]

@app.route('/')
def index():
    """Page d'accueil du générateur de QR codes."""
    return render_template('index.html', 
                          predefined_styles=PREDEFINED_STYLES,
                          export_formats=EXPORT_FORMATS)

@app.route('/generate', methods=['POST'])
def generate_qrcode():
    """
    Endpoint pour générer un QR code.
    Accepte les données du formulaire et génère un QR code selon les options spécifiées.
    """
    try:
        # Récupération des données du formulaire
        data = request.form.get('data', '')
        if not data:
            return jsonify({'error': 'Aucune donnée fournie pour le QR code'}), 400
        
        # Options de base
        options = {
            'version': int(request.form.get('version', 1)),
            'error_correction': int(request.form.get('error_correction', 0)),
            'box_size': int(request.form.get('box_size', 10)),
            'border': int(request.form.get('border', 4))
        }
        
        # Type de génération
        generation_type = request.form.get('generation_type', 'basic')
        
        # Nom de fichier unique
        filename = f"qrcode_{uuid.uuid4().hex}.png"
        qr_path = None
        
        if generation_type == 'basic':
            # Génération basique
            qr_path = qr_generator.generate_basic_qrcode(data, filename)
            
        elif generation_type == 'custom':
            # Personnalisation des couleurs
            options['fill_color'] = request.form.get('fill_color', '#000000')
            options['back_color'] = request.form.get('back_color', '#FFFFFF')
            
            qr_path = qr_generator.generate_qrcode_with_options(data, filename, **options)
            
        elif generation_type == 'logo':
            # Ajout d'un logo
            if 'logo' not in request.files:
                return jsonify({'error': 'Aucun logo fourni'}), 400
                
            logo_file = request.files['logo']
            if logo_file.filename == '':
                return jsonify({'error': 'Aucun logo sélectionné'}), 400
                
            # Sauvegarde du logo
            logo_filename = f"logo_{uuid.uuid4().hex}{os.path.splitext(logo_file.filename)[1]}"
            logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_filename)
            logo_file.save(logo_path)
            
            # Options pour le logo
            options['logo_size'] = float(request.form.get('logo_size', 0.2))
            
            qr_path = qr_generator.generate_qrcode_with_logo(data, logo_path, filename, **options)
            
        elif generation_type == 'styled':
            # Style personnalisé
            options['module_drawer'] = request.form.get('module_drawer', 'square')
            options['color_mask'] = request.form.get('color_mask', 'solid')
            
            # Couleurs pour les masques
            if options['color_mask'] == 'solid':
                options['front_color'] = request.form.get('front_color', '#000000')
                options['back_color'] = request.form.get('back_color', '#FFFFFF')
            else:
                # Options pour les gradients
                options['front_color'] = request.form.get('front_color', '#000000')
                options['edge_color'] = request.form.get('edge_color', '#666666')
                
                if 'gradient_center_x' in request.form and 'gradient_center_y' in request.form:
                    options['gradient_center'] = (
                        float(request.form.get('gradient_center_x', 0.5)),
                        float(request.form.get('gradient_center_y', 0.5))
                    )
            
            qr_path = qr_customizer.generate_styled_qrcode(data, filename, **options)
            
        elif generation_type == 'predefined':
            # Style prédéfini
            style_name = request.form.get('style_name', 'classic')
            
            qr_path = qr_customizer.apply_predefined_style(data, style_name, filename)
        
        else:
            return jsonify({'error': 'Type de génération non reconnu'}), 400
        
        if not qr_path or not os.path.exists(qr_path):
            return jsonify({'error': 'Erreur lors de la génération du QR code'}), 500
        
        # Chemin relatif pour l'affichage
        relative_path = os.path.relpath(qr_path, app.config['GENERATED_FOLDER'])
        
        return jsonify({
            'success': True,
            'qr_path': relative_path,
            'full_path': qr_path,
            'download_url': url_for('download_qrcode', filename=os.path.basename(qr_path))
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export', methods=['POST'])
def export_qrcode():
    """
    Endpoint pour exporter un QR code dans différents formats.
    """
    try:
        # Récupération des données du formulaire
        qr_path = request.form.get('qr_path', '')
        if not qr_path:
            return jsonify({'error': 'Aucun QR code à exporter'}), 400
        
        # Chemin complet du QR code
        full_qr_path = os.path.join(app.config['GENERATED_FOLDER'], qr_path)
        if not os.path.exists(full_qr_path):
            return jsonify({'error': 'QR code introuvable'}), 404
        
        # Format d'exportation
        export_format = request.form.get('export_format', 'png')
        
        # Options d'exportation
        options = {}
        
        if export_format == 'png':
            # Options pour PNG
            options['dpi'] = int(request.form.get('dpi', 300))
            options['quality'] = int(request.form.get('quality', 95))
            
            if 'size_width' in request.form and 'size_height' in request.form:
                options['size'] = (
                    int(request.form.get('size_width')),
                    int(request.form.get('size_height'))
                )
            
            export_path = qr_exporter.export_to_png(full_qr_path, **options)
            
        elif export_format == 'svg':
            # Options pour SVG
            if 'size_width' in request.form and 'size_height' in request.form:
                options['size'] = (
                    int(request.form.get('size_width')),
                    int(request.form.get('size_height'))
                )
            
            options['scale'] = float(request.form.get('scale', 1.0))
            
            export_path = qr_exporter.export_to_svg(full_qr_path, **options)
            
        elif export_format == 'pdf':
            # Options pour PDF
            options['title'] = request.form.get('title', 'QR Code')
            options['author'] = request.form.get('author', 'QR Code Generator')
            
            if 'size_width' in request.form and 'size_height' in request.form:
                options['size'] = (
                    float(request.form.get('size_width')),
                    float(request.form.get('size_height'))
                )
            
            if 'position_x' in request.form and 'position_y' in request.form:
                options['position'] = (
                    float(request.form.get('position_x')),
                    float(request.form.get('position_y'))
                )
            
            export_path = qr_exporter.export_to_pdf(full_qr_path, **options)
            
        elif export_format == 'all':
            # Exportation dans tous les formats
            export_paths = qr_exporter.export_to_all_formats(full_qr_path, **options)
            
            return jsonify({
                'success': True,
                'export_paths': export_paths,
                'download_urls': {
                    format_type: url_for('download_exported', filename=os.path.basename(path))
                    for format_type, path in export_paths.items()
                }
            })
            
        else:
            return jsonify({'error': 'Format d\'exportation non reconnu'}), 400
        
        if not export_path or not os.path.exists(export_path):
            return jsonify({'error': 'Erreur lors de l\'exportation du QR code'}), 500
        
        return jsonify({
            'success': True,
            'export_path': export_path,
            'download_url': url_for('download_exported', filename=os.path.basename(export_path))
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def history():
    """
    Page d'historique des QR codes générés.
    """
    # Récupération des QR codes générés
    qr_codes = []
    
    # Parcours du dossier des QR codes générés
    try:
        for filename in os.listdir(app.config['GENERATED_FOLDER']):
            if filename.endswith('.png') and filename.startswith('qrcode_'):
                # Chemin complet du fichier
                file_path = os.path.join(app.config['GENERATED_FOLDER'], filename)
                
                # Métadonnées
                metadata_path = os.path.join(app.config['GENERATED_FOLDER'], 'metadata', f"{os.path.splitext(filename)[0]}.txt")
                metadata = {}
                
                if os.path.exists(metadata_path):
                    try:
                        with open(metadata_path, 'r', encoding='utf-8') as f:
                            for line in f:
                                if ':' in line:
                                    key, value = line.split(':', 1)
                                    metadata[key.strip()] = value.strip()
                    except Exception as e:
                        app.logger.error(f"Error reading metadata file {metadata_path}: {e}")
                
                # Ajout à la liste
                qr_codes.append({
                    'filename': filename,
                    'path': file_path,
                    'relative_path': filename,
                    'download_url': url_for('download_qrcode', filename=filename),
                    'date': metadata.get('Date de création', 'Inconnue'),
                    'data': metadata.get('Données', 'Inconnue')
                })
    except Exception as e:
        app.logger.error(f"Error listing QR codes: {e}")
    
    # Tri par date (plus récent en premier)
    try:
        qr_codes.sort(key=lambda x: x['date'], reverse=True)
    except Exception as e:
        app.logger.error(f"Error sorting QR codes: {e}")
    
    return render_template('history.html', qr_codes=qr_codes, export_formats=EXPORT_FORMATS)

@app.route('/qrcodes/<filename>')
def download_qrcode(filename):
    """
    Endpoint pour télécharger un QR code généré.
    """
    return send_from_directory(app.config['GENERATED_FOLDER'], filename)

@app.route('/exports/<filename>')
def download_exported(filename):
    """
    Endpoint pour télécharger un QR code exporté.
    """
    return send_from_directory(app.config['EXPORTED_FOLDER'], filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Endpoint pour accéder aux fichiers uploadés (logos, etc.).
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.errorhandler(404)
def page_not_found(e):
    """Gestion des erreurs 404."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Gestion des erreurs 500."""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
