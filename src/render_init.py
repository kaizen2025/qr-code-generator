#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script d'initialisation pour Render - Prépare l'environnement et les fichiers nécessaires
"""

import os
import sys
from style_generator import QRStyleGenerator

def setup_directories():
    """Crée les dossiers requis pour l'application"""
    base_dir = os.environ.get('RENDER_PROJECT_DIR', os.getcwd())
    
    # Définition des chemins
    if os.environ.get('RENDER'):
        upload_dir = '/tmp/uploads'
        qrcodes_dir = '/tmp/generated_qrcodes'
        exported_dir = '/tmp/exported_qrcodes'
        static_dir = '/tmp/static'
    else:
        upload_dir = os.path.join(base_dir, 'uploads')
        qrcodes_dir = os.path.join(base_dir, 'generated_qrcodes')
        exported_dir = os.path.join(base_dir, 'exported_qrcodes')
        static_dir = os.path.join(base_dir, 'src', 'frontend', 'static')
    
    # Création des dossiers
    for directory in [upload_dir, qrcodes_dir, exported_dir, static_dir]:
        os.makedirs(directory, exist_ok=True)
        # Permissions correctes
        os.chmod(directory, 0o755)
    
    # Création du dossier pour les styles
    styles_dir = os.path.join(static_dir, 'img', 'styles')
    os.makedirs(styles_dir, exist_ok=True)
    
    return {
        'upload_dir': upload_dir,
        'qrcodes_dir': qrcodes_dir,
        'exported_dir': exported_dir,
        'static_dir': static_dir,
        'styles_dir': styles_dir
    }

def main():
    """Fonction principale d'initialisation"""
    print("Initialisation de l'environnement...")
    directories = setup_directories()
    
    # Génération des styles QR
    print("Génération des styles QR...")
    style_generator = QRStyleGenerator(directories['styles_dir'])
    styles = style_generator.generate_style_samples()
    print(f"Styles générés: {len(styles)}")
    
    # Création d'un fichier pour indiquer que l'initialisation est terminée
    with open(os.path.join(directories['static_dir'], 'init_complete.txt'), 'w') as f:
        f.write("Initialisation terminée le " + os.popen('date').read())
    
    print("Initialisation terminée avec succès")

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
