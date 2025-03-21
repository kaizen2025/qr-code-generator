#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de configuration pour le déploiement permanent sur Render.
Ce script prépare l'application pour un déploiement continu via GitHub et Render.
"""

import os
import sys
import subprocess
import json
import argparse

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

def check_dependencies():
    """Vérifie que les dépendances nécessaires sont installées."""
    print_step("Vérification des dépendances...")
    
    try:
        # Vérification de gunicorn
        subprocess.run([sys.executable, "-m", "pip", "show", "gunicorn"], 
                      check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print_success("gunicorn est installé")
    except subprocess.SubprocessError:
        print_warning("gunicorn n'est pas installé, installation en cours...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "gunicorn"], 
                          check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print_success("gunicorn installé avec succès")
        except subprocess.SubprocessError as e:
            print_error(f"Erreur lors de l'installation de gunicorn: {e}")
            return False
    
    # Mise à jour du fichier requirements.txt
    print_step("Mise à jour du fichier requirements.txt...")
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read()
        
        if "gunicorn" not in requirements:
            with open("requirements.txt", "a") as f:
                f.write("\ngunicorn==20.1.0\n")
            print_success("gunicorn ajouté à requirements.txt")
        else:
            print_success("gunicorn déjà présent dans requirements.txt")
    except Exception as e:
        print_error(f"Erreur lors de la mise à jour de requirements.txt: {e}")
        return False
    
    return True

def create_render_config():
    """Crée les fichiers de configuration pour Render."""
    print_step("Création des fichiers de configuration pour Render...")
    
    # Vérification que le fichier render.yaml existe
    if not os.path.exists("render.yaml"):
        print_warning("Fichier render.yaml non trouvé, création en cours...")
        render_config = {
            "services": [
                {
                    "type": "web",
                    "name": "qr-code-generator",
                    "env": "python",
                    "buildCommand": "pip install -r requirements.txt",
                    "startCommand": "gunicorn src.app:app",
                    "envVars": [
                        {
                            "key": "FLASK_ENV",
                            "value": "production"
                        },
                        {
                            "key": "SECRET_KEY",
                            "generateValue": True
                        }
                    ],
                    "autoDeploy": True
                }
            ]
        }
        
        try:
            with open("render.yaml", "w") as f:
                json.dump(render_config, f, indent=2)
            print_success("Fichier render.yaml créé avec succès")
        except Exception as e:
            print_error(f"Erreur lors de la création du fichier render.yaml: {e}")
            return False
    else:
        print_success("Fichier render.yaml existant")
    
    return True

def create_procfile():
    """Crée ou met à jour le Procfile pour Render."""
    print_step("Création/mise à jour du Procfile...")
    
    procfile_content = "web: gunicorn src.app:app"
    
    try:
        with open("Procfile", "w") as f:
            f.write(procfile_content)
        print_success("Procfile créé/mis à jour avec succès")
        return True
    except Exception as e:
        print_error(f"Erreur lors de la création/mise à jour du Procfile: {e}")
        return False

def test_local_deployment():
    """Teste le déploiement en local avec gunicorn."""
    print_step("Test du déploiement en local avec gunicorn...")
    
    try:
        # Lancement de gunicorn en arrière-plan
        process = subprocess.Popen(
            ["gunicorn", "src.app:app", "--bind", "0.0.0.0:8000", "--timeout", "120"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print_success("Application lancée avec gunicorn sur http://localhost:8000")
        print_warning("Appuyez sur Entrée pour arrêter le serveur...")
        input()
        
        # Arrêt du serveur
        process.terminate()
        process.wait()
        
        print_success("Serveur arrêté avec succès")
        return True
    except Exception as e:
        print_error(f"Erreur lors du test de déploiement local: {e}")
        return False

def create_deployment_instructions():
    """Crée un fichier d'instructions pour le déploiement."""
    print_step("Création des instructions de déploiement...")
    
    instructions = """# Instructions de déploiement permanent

## Déploiement sur GitHub

1. Créez un compte GitHub si vous n'en avez pas déjà un
2. Créez un nouveau dépôt nommé "qr-code-generator"
3. Initialisez Git dans le dossier du projet:
   ```
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/votre-nom-utilisateur/qr-code-generator.git
   git push -u origin main
   ```

## Déploiement sur Render

1. Créez un compte Render si vous n'en avez pas déjà un
2. Connectez-vous à Render et liez votre compte GitHub
3. Créez un nouveau Web Service:
   - Sélectionnez le dépôt GitHub "qr-code-generator"
   - Nom: qr-code-generator
   - Environnement: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn src.app:app`
   - Plan: Free
4. Cliquez sur "Create Web Service"

## Configuration de l'intégration continue

1. Dans votre dépôt GitHub, accédez à Settings > Secrets > Actions
2. Ajoutez les secrets suivants:
   - RENDER_SERVICE_ID: l'ID de votre service Render (visible dans l'URL)
   - RENDER_API_KEY: votre clé API Render (disponible dans les paramètres de votre compte)

## Mise à jour de l'application

Pour mettre à jour l'application déployée:
1. Effectuez vos modifications
2. Committez et poussez vers GitHub:
   ```
   git add .
   git commit -m "Description des modifications"
   git push origin main
   ```
3. Le déploiement sur Render sera automatiquement déclenché

## Vérification du déploiement

1. Accédez à votre tableau de bord Render
2. Vérifiez l'état du déploiement dans l'onglet "Deploys"
3. Une fois le déploiement terminé, cliquez sur l'URL fournie pour accéder à l'application
"""
    
    try:
        with open("DEPLOYMENT.md", "w") as f:
            f.write(instructions)
        print_success("Instructions de déploiement créées avec succès dans DEPLOYMENT.md")
        return True
    except Exception as e:
        print_error(f"Erreur lors de la création des instructions de déploiement: {e}")
        return False

def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(description='Configuration pour le déploiement permanent')
    parser.add_argument('--test-local', action='store_true', help='Tester le déploiement en local')
    args = parser.parse_args()
    
    print_header("Configuration pour le déploiement permanent")
    print("Générateur de QR Codes Personnalisé - Anecoop-France")
    
    # Vérification des dépendances
    if not check_dependencies():
        print_error("Échec de la vérification des dépendances")
        return
    
    # Création des fichiers de configuration
    if not create_render_config():
        print_error("Échec de la création des fichiers de configuration pour Render")
        return
    
    # Création/mise à jour du Procfile
    if not create_procfile():
        print_error("Échec de la création/mise à jour du Procfile")
        return
    
    # Création des instructions de déploiement
    if not create_deployment_instructions():
        print_error("Échec de la création des instructions de déploiement")
        return
    
    # Test du déploiement en local si demandé
    if args.test_local:
        if not test_local_deployment():
            print_error("Échec du test de déploiement local")
            return
    
    print_header("Configuration pour le déploiement permanent terminée avec succès")
    print("Suivez les instructions dans le fichier DEPLOYMENT.md pour déployer l'application")

if __name__ == "__main__":
    main()
