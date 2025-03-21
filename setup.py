#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script d'installation et de lancement pour le générateur de QR codes personnalisé.
Ce script permet d'installer les dépendances nécessaires et de lancer l'application
en mode local, sans nécessiter de connexion internet pour l'utilisation.
"""

import os
import sys
import subprocess
import platform
import shutil
import time
import webbrowser
from pathlib import Path

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

def check_python_version():
    """Vérifie que la version de Python est compatible."""
    print_step("Vérification de la version de Python...")
    
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 8):
        print_error(f"Python 3.8 ou supérieur est requis. Version actuelle: {major}.{minor}")
        return False
    
    print_success(f"Version de Python compatible: {major}.{minor}")
    return True

def check_pip():
    """Vérifie que pip est installé."""
    print_step("Vérification de pip...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print_success("pip est installé")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print_error("pip n'est pas installé ou n'est pas accessible")
        return False

def create_virtual_env():
    """Crée un environnement virtuel Python."""
    print_step("Création de l'environnement virtuel...")
    
    venv_dir = Path("venv")
    if venv_dir.exists():
        print_warning("L'environnement virtuel existe déjà")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print_success("Environnement virtuel créé avec succès")
        return True
    except subprocess.SubprocessError as e:
        print_error(f"Erreur lors de la création de l'environnement virtuel: {e}")
        return False

def install_dependencies():
    """Installe les dépendances requises."""
    print_step("Installation des dépendances...")
    
    # Détermination du chemin de l'exécutable Python dans l'environnement virtuel
    if platform.system() == "Windows":
        python_executable = Path("venv/Scripts/python.exe")
        pip_executable = Path("venv/Scripts/pip.exe")
    else:
        python_executable = Path("venv/bin/python")
        pip_executable = Path("venv/bin/pip")
    
    if not python_executable.exists():
        print_error(f"Exécutable Python non trouvé dans l'environnement virtuel: {python_executable}")
        return False
    
    # Mise à jour de pip
    try:
        print_step("Mise à jour de pip...")
        subprocess.run([str(pip_executable), "install", "--upgrade", "pip"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print_success("pip mis à jour avec succès")
    except subprocess.SubprocessError as e:
        print_warning(f"Erreur lors de la mise à jour de pip: {e}")
    
    # Installation des dépendances à partir du fichier requirements.txt
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print_error("Fichier requirements.txt non trouvé")
        return False
    
    try:
        subprocess.run([str(pip_executable), "install", "-r", "requirements.txt"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print_success("Dépendances installées avec succès")
        return True
    except subprocess.SubprocessError as e:
        print_error(f"Erreur lors de l'installation des dépendances: {e}")
        return False

def run_application():
    """Lance l'application."""
    print_header("Lancement de l'application")
    
    # Détermination du chemin de l'exécutable Python dans l'environnement virtuel
    if platform.system() == "Windows":
        python_executable = Path("venv/Scripts/python.exe")
    else:
        python_executable = Path("venv/bin/python")
    
    if not python_executable.exists():
        print_error(f"Exécutable Python non trouvé dans l'environnement virtuel: {python_executable}")
        return False
    
    # Vérification que le fichier app.py existe
    app_file = Path("src/app.py")
    if not app_file.exists():
        print_error("Fichier app.py non trouvé")
        return False
    
    # Lancement de l'application
    print_step("Démarrage du serveur Flask...")
    
    # Ouverture du navigateur après un court délai
    def open_browser():
        time.sleep(2)
        webbrowser.open("http://localhost:5000")
    
    try:
        # Lancement du navigateur dans un thread séparé
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Lancement de l'application Flask
        subprocess.run([str(python_executable), "src/app.py"], check=True)
        return True
    except subprocess.SubprocessError as e:
        print_error(f"Erreur lors du lancement de l'application: {e}")
        return False
    except KeyboardInterrupt:
        print_warning("\nArrêt de l'application...")
        return True

def create_executable():
    """Crée un exécutable autonome avec PyInstaller."""
    print_header("Création de l'exécutable autonome")
    
    # Détermination du chemin de l'exécutable Python dans l'environnement virtuel
    if platform.system() == "Windows":
        python_executable = Path("venv/Scripts/python.exe")
        pip_executable = Path("venv/Scripts/pip.exe")
    else:
        python_executable = Path("venv/bin/python")
        pip_executable = Path("venv/bin/pip")
    
    if not python_executable.exists():
        print_error(f"Exécutable Python non trouvé dans l'environnement virtuel: {python_executable}")
        return False
    
    # Installation de PyInstaller
    print_step("Installation de PyInstaller...")
    try:
        subprocess.run([str(pip_executable), "install", "pyinstaller"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print_success("PyInstaller installé avec succès")
    except subprocess.SubprocessError as e:
        print_error(f"Erreur lors de l'installation de PyInstaller: {e}")
        return False
    
    # Création de l'exécutable
    print_step("Création de l'exécutable...")
    try:
        # Détermination du chemin de PyInstaller
        if platform.system() == "Windows":
            pyinstaller_executable = Path("venv/Scripts/pyinstaller.exe")
        else:
            pyinstaller_executable = Path("venv/bin/pyinstaller")
        
        # Options pour PyInstaller
        pyinstaller_options = [
            "--name=QRCodeGenerator",
            "--onefile",
            "--windowed",
            "--icon=src/frontend/static/img/favicon.ico",
            "--add-data=src/frontend/templates:src/frontend/templates",
            "--add-data=src/frontend/static:src/frontend/static",
            "src/app.py"
        ]
        
        # Adaptation des options pour Windows
        if platform.system() == "Windows":
            pyinstaller_options = [opt.replace(":", ";") for opt in pyinstaller_options]
        
        # Exécution de PyInstaller
        subprocess.run([str(pyinstaller_executable)] + pyinstaller_options, check=True)
        
        print_success("Exécutable créé avec succès")
        
        # Chemin de l'exécutable généré
        if platform.system() == "Windows":
            exe_path = Path("dist/QRCodeGenerator.exe")
        else:
            exe_path = Path("dist/QRCodeGenerator")
        
        if exe_path.exists():
            print_success(f"Exécutable disponible à l'emplacement: {exe_path.absolute()}")
        else:
            print_warning(f"Exécutable non trouvé à l'emplacement attendu: {exe_path.absolute()}")
        
        return True
    except subprocess.SubprocessError as e:
        print_error(f"Erreur lors de la création de l'exécutable: {e}")
        return False

def main():
    """Fonction principale."""
    print_header("Générateur de QR Codes Personnalisé - Installation et Lancement")
    print("Propriété d'Anecoop-France – Créé par Kevin BIVIA")
    
    # Vérification des prérequis
    if not check_python_version() or not check_pip():
        print_error("Prérequis non satisfaits. Installation annulée.")
        sys.exit(1)
    
    # Menu principal
    while True:
        print_header("Menu Principal")
        print("1. Installer les dépendances")
        print("2. Lancer l'application")
        print("3. Créer un exécutable autonome")
        print("4. Quitter")
        
        choice = input("\nVotre choix (1-4): ")
        
        if choice == "1":
            if create_virtual_env() and install_dependencies():
                print_success("Installation terminée avec succès")
        elif choice == "2":
            run_application()
        elif choice == "3":
            create_executable()
        elif choice == "4":
            print_header("Au revoir !")
            break
        else:
            print_warning("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
