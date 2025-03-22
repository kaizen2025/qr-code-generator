#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script pour initialiser les dossiers et fichiers statiques nécessaires
sur l'environnement Render. À exécuter au démarrage.
"""

import os
import shutil
import qrcode
from PIL import Image

# Création des dossiers nécessaires avec des droits d'accès corrects
def setup_directories():
    # Définition des chemins de base
    base_dir = os.environ.get('RENDER_PROJECT_DIR', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    static_dir = os.path.join(base_dir, 'src', 'frontend', 'static')
    img_dir = os.path.join(static_dir, 'img')
    styles_dir = os.path.join(img_dir, 'styles')
    
    # Dossiers pour les fichiers générés
    uploads_dir = os.path.join(base_dir, 'uploads')
    qrcodes_dir = os.path.join(base_dir, 'generated_qrcodes')
    exported_dir = os.path.join(base_dir, 'exported_qrcodes')
    
    # Création des dossiers s'ils n'existent pas
    for directory in [img_dir, styles_dir, uploads_dir, qrcodes_dir, exported_dir]:
        os.makedirs(directory, exist_ok=True)
        # S'assurer que les permissions sont correctes (lecture/écriture)
        os.chmod(directory, 0o755)
    
    return {
        'styles_dir': styles_dir,
        'uploads_dir': uploads_dir,
        'qrcodes_dir': qrcodes_dir,
        'exported_dir': exported_dir
    }

# Génération des images de styles (prévisualisations)
def generate_style_images(styles_dir):
    styles = {
        'classic': {'module_drawer': 'square', 'color': "#000000"},
        'rounded': {'module_drawer': 'rounded', 'color': "#000000"},
        'dots': {'module_drawer': 'circle', 'color': "#000000"},
        'modern_blue': {'module_drawer': 'rounded', 'color': "#0066CC"},
        'sunset': {'module_drawer': 'circle', 'color': "#FF6600"},
        'forest': {'module_drawer': 'square', 'color': "#006600"},
        'ocean': {'module_drawer': 'rounded', 'color': "#0099CC"},
        'barcode': {'module_drawer': 'vertical_bars', 'color': "#000000"},
        'elegant': {'module_drawer': 'gapped_square', 'color': "#333333"}
    }
    
    # Génération d'un QR code de base pour chaque style
    for style_name, style_options in styles.items():
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data("https://example.com")
        qr.make(fit=True)
        
        img = qr.make_image(fill_color=style_options['color'], back_color="white")
        img.save(os.path.join(styles_dir, f"{style_name}.png"))
        
    print(f"Images de styles générées dans: {styles_dir}")

# Création d'un QR code de test pour vérifier les permissions
def create_test_qrcode(qrcodes_dir):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data("https://test.com")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    test_path = os.path.join(qrcodes_dir, "test_qrcode.png")
    img.save(test_path)
    
    # Vérifier que le fichier est accessible en lecture
    os.chmod(test_path, 0o644)
    print(f"QR code de test créé: {test_path}")

# Fonction principale
def main():
    print("Initialisation de l'environnement Render...")
    directories = setup_directories()
    
    # Génération des images de styles
    generate_style_images(directories['styles_dir'])
    
    # Création d'un QR code de test
    create_test_qrcode(directories['qrcodes_dir'])
    
    print("Initialisation terminée avec succès")

if __name__ == "__main__":
    main()
