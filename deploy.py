#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de déploiement pour le générateur de QR codes personnalisé.
Ce script automatise le processus de déploiement sur Render.
"""

import os
import sys
import subprocess
import requests
import json
import time
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

def check_render_credentials():
    """Vérifie que les identifiants Render sont disponibles."""
    print_step("Vérification des identifiants Render...")
    
    email = os.environ.get('RENDER_EMAIL')
    password = os.environ.get('RENDER_PASSWORD')
    
    if not email or not password:
        print_warning("Variables d'environnement RENDER_EMAIL et/ou RENDER_PASSWORD non définies")
        email = input("Email Render: ")
        password = input("Mot de passe Render: ")
    
    return email, password

def check_github_credentials():
    """Vérifie que les identifiants GitHub sont disponibles."""
    print_step("Vérification des identifiants GitHub...")
    
    username = os.environ.get('GITHUB_USERNAME')
    token = os.environ.get('GITHUB_TOKEN')
    
    if not username or not token:
        print_warning("Variables d'environnement GITHUB_USERNAME et/ou GITHUB_TOKEN non définies")
        username = input("Nom d'utilisateur GitHub: ")
        token = input("Token GitHub: ")
    
    return username, token

def create_github_repo(username, token, repo_name="qr-code-generator"):
    """Crée un dépôt GitHub pour le projet."""
    print_step(f"Création du dépôt GitHub '{repo_name}'...")
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'name': repo_name,
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
        print_success(f"Dépôt GitHub '{repo_name}' créé avec succès")
        return response.json()['html_url'], response.json()['clone_url']
    elif response.status_code == 422:
        print_warning(f"Le dépôt '{repo_name}' existe déjà")
        return f"https://github.com/{username}/{repo_name}", f"https://github.com/{username}/{repo_name}.git"
    else:
        print_error(f"Erreur lors de la création du dépôt GitHub: {response.status_code} - {response.text}")
        return None, None

def push_to_github(clone_url, username, token):
    """Pousse le code vers le dépôt GitHub."""
    print_step(f"Envoi du code vers GitHub...")
    
    # Vérification que git est installé
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.SubprocessError, FileNotFoundError):
        print_error("Git n'est pas installé ou n'est pas accessible")
        return False
    
    try:
        # Initialisation du dépôt git local
        subprocess.run(["git", "init"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Configuration de l'utilisateur git
        subprocess.run(["git", "config", "user.name", username], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["git", "config", "user.email", f"{username}@users.noreply.github.com"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Ajout de tous les fichiers
        subprocess.run(["git", "add", "."], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Commit
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Ajout du remote
        auth_url = clone_url.replace("https://", f"https://{username}:{token}@")
        subprocess.run(["git", "remote", "add", "origin", auth_url], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Push
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print_success("Code envoyé avec succès vers GitHub")
        return True
    except subprocess.SubprocessError as e:
        print_error(f"Erreur lors de l'envoi du code vers GitHub: {e}")
        return False

def deploy_to_render(email, password, github_url):
    """Déploie l'application sur Render."""
    print_step("Déploiement sur Render...")
    
    # Cette partie est simplifiée car Render n'a pas d'API publique pour l'authentification
    # Dans un cas réel, il faudrait utiliser Selenium ou une autre méthode pour automatiser le processus
    
    print_warning("Pour déployer sur Render, suivez ces étapes manuelles:")
    print(f"1. Connectez-vous à Render avec l'email: {email}")
    print("2. Créez un nouveau Web Service")
    print(f"3. Connectez-le au dépôt GitHub: {github_url}")
    print("4. Configurez le service avec:")
    print("   - Environnement: Python")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: gunicorn src.app:app")
    print("5. Cliquez sur 'Create Web Service'")
    
    service_url = input("Une fois le déploiement terminé, entrez l'URL du service Render: ")
    
    if service_url:
        print_success(f"Application déployée avec succès sur Render: {service_url}")
        return service_url
    else:
        print_warning("URL non fournie, impossible de confirmer le déploiement")
        return None

def update_readme_with_deployment_info(service_url, github_url):
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
        content = content.replace("https://qr-code-generator.onrender.com", service_url)
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
    parser = argparse.ArgumentParser(description='Déploiement du générateur de QR codes personnalisé')
    parser.add_argument('--github-only', action='store_true', help='Déployer uniquement sur GitHub')
    parser.add_argument('--render-only', action='store_true', help='Déployer uniquement sur Render')
    args = parser.parse_args()
    
    print_header("Déploiement du Générateur de QR Codes Personnalisé")
    print("Propriété d'Anecoop-France – Créé par Kevin BIVIA")
    
    # Déploiement sur GitHub
    if not args.render_only:
        github_username, github_token = check_github_credentials()
        github_url, clone_url = create_github_repo(github_username, github_token)
        
        if github_url and clone_url:
            push_success = push_to_github(clone_url, github_username, github_token)
            if not push_success:
                print_error("Échec du déploiement sur GitHub")
                if not args.github_only:
                    print_warning("Le déploiement sur Render sera ignoré")
                    return
        else:
            print_error("Échec de la création du dépôt GitHub")
            if not args.github_only:
                print_warning("Le déploiement sur Render sera ignoré")
                return
    
    # Déploiement sur Render
    if not args.github_only:
        render_email, render_password = check_render_credentials()
        service_url = deploy_to_render(render_email, render_password, github_url)
        
        if service_url:
            update_readme_with_deployment_info(service_url, github_url)
    
    print_header("Déploiement terminé")
    if not args.render_only:
        print(f"GitHub: {github_url}")
    if not args.github_only and service_url:
        print(f"Render: {service_url}")

if __name__ == "__main__":
    main()
