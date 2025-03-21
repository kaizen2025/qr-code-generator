#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de création d'archive ZIP pour le déploiement manuel.
Ce script crée une archive ZIP du projet pour faciliter l'importation sur GitHub.
"""

import os
import sys
import zipfile
import shutil
from datetime import datetime

# Couleurs pour les messages dans le terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(message):
    """Affiche un message d'en-tête."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {message} ==={Colors.ENDC}\n")

def print_step(message):
    """Affiche une étape du processus."""
    print(f"{Colors.BLUE}→ {message}{Colors.ENDC}")

def print_success(message):
    """Affiche un message de succès."""
    print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")

def print_warning(message):
    """Affiche un avertissement."""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def print_error(message):
    """Affiche une erreur."""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def create_zip_archive():
    """Crée une archive ZIP du projet."""
    print_step("Création de l'archive ZIP du projet...")
    
    # Nom de l'archive avec horodatage
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"qr_code_generator_{timestamp}.zip"
    
    # Fichiers et dossiers à exclure
    exclude = [
        ".git",
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".DS_Store",
        "venv",
        "exports",
        "*.zip"
    ]
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk("."):
                # Exclusion des dossiers
                dirs[:] = [d for d in dirs if d not in exclude and not any(d.startswith(e) for e in exclude if '*' in e)]
                
                for file in files:
                    # Vérification si le fichier doit être exclu
                    if any(file == e or (e.startswith('*') and file.endswith(e[1:])) for e in exclude):
                        continue
                    
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, ".")
                    zipf.write(file_path, arcname)
        
        # Déplacement de l'archive vers le répertoire parent
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dest_path = os.path.join(parent_dir, zip_filename)
        shutil.move(zip_filename, dest_path)
        
        print_success(f"Archive ZIP créée avec succès: {dest_path}")
        return dest_path
    except Exception as e:
        print_error(f"Erreur lors de la création de l'archive ZIP: {e}")
        return None

def main():
    """Fonction principale."""
    print_header("Création d'archive ZIP pour déploiement manuel")
    print("Générateur de QR Codes Personnalisé - Anecoop-France")
    
    zip_path = create_zip_archive()
    
    if zip_path:
        print_header("Instructions pour le déploiement manuel")
        print("1. Téléchargez l'archive ZIP créée")
        print("2. Accédez à https://github.com/new pour créer un nouveau dépôt nommé 'qr-code-generator'")
        print("3. Après avoir créé le dépôt, importez l'archive ZIP via l'interface GitHub")
        print("4. Suivez les instructions dans le fichier MANUAL_DEPLOYMENT.md pour déployer sur Render")
    else:
        print_error("Échec de la création de l'archive ZIP")

if __name__ == "__main__":
    main()
