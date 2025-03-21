#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de déploiement automatisé pour GitHub et Render.
Ce script utilise les identifiants fournis pour créer un dépôt GitHub
et configurer le déploiement sur Render.
"""

import os
import sys
import subprocess
import requests
import json
import time

# Identifiants GitHub
GITHUB_USERNAME = "kaizen2025"
GITHUB_TOKEN = "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"
REPO_NAME = "qr-code-generator"

# Identifiants Render
RENDER_EMAIL = "kevin.bivia@gmail.com"
RENDER_PASSWORD = "87YS@we@jDf2y8H"

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

def create_github_repo():
    """Crée un dépôt GitHub pour le projet."""
    print_step(f"Création du dépôt GitHub '{REPO_NAME}'...")
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'name': REPO_NAME,
        'description': 'Générateur de QR Codes Personnalisé pour Anecoop-France',
        'private': False,
        'has_issues': True,
        'has_projects': True,
        'has_wiki': True
    }
    
    response = requests.post(
        'https://api.github.com/user/repos',
        headers=headers,
        data=json.dumps(data)
    )
    
    if response.status_code == 201:
        print_success(f"Dépôt GitHub '{REPO_NAME}' créé avec succès")
        return response.json()['html_url'], response.json()['clone_url']
    elif response.status_code == 422:
        print_warning(f"Le dépôt '{REPO_NAME}' existe déjà")
        return f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}", f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
    else:
        print_error(f"Erreur lors de la création du dépôt GitHub: {response.status_code} - {response.text}")
        return None, None

def push_to_github(clone_url):
    """Pousse le code vers le dépôt GitHub."""
    print_step(f"Envoi du code vers GitHub...")
    
    # Vérification que git est installé
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.SubprocessError, FileNotFoundError):
        print_error("Git n'est pas installé ou n'est pas accessible")
        return False
    
    try:
        # Configuration de l'utilisateur git
        subprocess.run(["git", "config", "user.name", GITHUB_USERNAME], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["git", "config", "user.email", f"{RENDER_EMAIL}"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Ajout du remote (ou mise à jour s'il existe déjà)
        auth_url = clone_url.replace("https://", f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@")
        
        # Vérification si le remote existe déjà
        result = subprocess.run(["git", "remote", "-v"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if "origin" in result.stdout.decode():
            subprocess.run(["git", "remote", "set-url", "origin", auth_url], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print_step("Remote 'origin' mis à jour")
        else:
            subprocess.run(["git", "remote", "add", "origin", auth_url], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print_step("Remote 'origin' ajouté")
        
        # Push
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print_success("Code envoyé avec succès vers GitHub")
        return True
    except subprocess.SubprocessError as e:
        print_error(f"Erreur lors de l'envoi du code vers GitHub: {e}")
        return False

def create_render_deployment_instructions(github_url):
    """Crée des instructions pour le déploiement sur Render."""
    print_step("Création des instructions pour le déploiement sur Render...")
    
    instructions = f"""# Déploiement sur Render

## Étapes pour déployer l'application sur Render

1. Connectez-vous à Render avec l'email: {RENDER_EMAIL}
2. Accédez à https://dashboard.render.com/
3. Cliquez sur "New" puis "Web Service"
4. Connectez votre compte GitHub si ce n'est pas déjà fait
5. Sélectionnez le dépôt: {github_url}
6. Configurez le service:
   - Nom: qr-code-generator
   - Environnement: Python
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn src.app:app
   - Plan: Free
7. Cliquez sur "Create Web Service"

Une fois le déploiement terminé, l'application sera accessible à l'URL fournie par Render.
"""
    
    try:
        with open("RENDER_DEPLOYMENT.md", "w") as f:
            f.write(instructions)
        print_success("Instructions pour le déploiement sur Render créées avec succès")
        return True
    except Exception as e:
        print_error(f"Erreur lors de la création des instructions pour le déploiement sur Render: {e}")
        return False

def update_readme_with_deployment_info(github_url):
    """Met à jour le README avec les informations de déploiement."""
    print_step("Mise à jour du README avec les informations de déploiement...")
    
    readme_path = "README.md"
    
    if not os.path.exists(readme_path):
        print_error(f"Fichier README.md non trouvé")
        return False
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Mise à jour des URLs
        content = content.replace("https://github.com/kaizen2025/qr-code-generator", github_url)
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print_success("README mis à jour avec les informations de déploiement")
        return True
    except Exception as e:
        print_error(f"Erreur lors de la mise à jour du README: {e}")
        return False

def main():
    """Fonction principale."""
    print_header("Déploiement automatisé sur GitHub et Render")
    print("Générateur de QR Codes Personnalisé - Anecoop-France")
    
    # Création du dépôt GitHub
    github_url, clone_url = create_github_repo()
    
    if github_url and clone_url:
        # Mise à jour du README avec les informations de déploiement
        update_readme_with_deployment_info(github_url)
        
        # Envoi du code vers GitHub
        push_success = push_to_github(clone_url)
        
        if push_success:
            # Création des instructions pour le déploiement sur Render
            create_render_deployment_instructions(github_url)
            
            print_header("Déploiement GitHub terminé avec succès")
            print(f"URL du dépôt GitHub: {github_url}")
            print("\nPour déployer l'application sur Render, suivez les instructions dans le fichier RENDER_DEPLOYMENT.md")
        else:
            print_error("Échec du déploiement sur GitHub")
    else:
        print_error("Échec de la création du dépôt GitHub")

if __name__ == "__main__":
    main()
