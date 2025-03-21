# Guide d'installation - Générateur de QR Codes Personnalisé
*Propriété d'Anecoop-France – Créé par Kevin BIVIA*

## Table des matières

1. [Prérequis](#1-prérequis)
2. [Installation en ligne](#2-installation-en-ligne)
3. [Installation locale](#3-installation-locale)
   - [Installation via le script setup.py](#31-installation-via-le-script-setuppy)
   - [Installation manuelle](#32-installation-manuelle)
   - [Création d'un exécutable autonome](#33-création-dun-exécutable-autonome)
4. [Déploiement sur Render](#4-déploiement-sur-render)
   - [Prérequis pour le déploiement](#41-prérequis-pour-le-déploiement)
   - [Étapes de déploiement](#42-étapes-de-déploiement)
   - [Configuration des variables d'environnement](#43-configuration-des-variables-denvironnement)
5. [Configuration GitHub](#5-configuration-github)
   - [Création du dépôt](#51-création-du-dépôt)
   - [Configuration de l'intégration continue](#52-configuration-de-lintégration-continue)
6. [Mise à jour de l'application](#6-mise-à-jour-de-lapplication)
7. [Dépannage](#7-dépannage)

## 1. Prérequis

### Pour l'installation locale

- **Système d'exploitation** : Windows 10/11, macOS 10.14+, ou Linux (Ubuntu 20.04+ recommandé)
- **Python** : Version 3.8 ou supérieure
- **Espace disque** : Minimum 200 Mo
- **RAM** : Minimum 2 Go
- **Navigateur web** : Chrome, Firefox, Safari ou Edge (dernières versions)

### Pour le déploiement en ligne

- **Compte GitHub** : Pour héberger le code source
- **Compte Render** : Pour déployer l'application web

## 2. Installation en ligne

L'application est déjà déployée et accessible à l'adresse suivante :
[https://qr-code-generator.onrender.com](https://qr-code-generator.onrender.com)

Aucune installation n'est nécessaire pour utiliser la version en ligne. Il vous suffit d'avoir un navigateur web moderne et une connexion internet.

## 3. Installation locale

### 3.1 Installation via le script setup.py

Le moyen le plus simple d'installer et d'exécuter l'application en local est d'utiliser le script `setup.py` fourni :

1. **Téléchargement du code source** :
   ```bash
   git clone https://github.com/kaizen2025/qr-code-generator.git
   cd qr-code-generator
   ```

2. **Exécution du script d'installation** :
   ```bash
   python setup.py
   ```

3. **Utilisation du menu interactif** :
   - Sélectionnez l'option 1 pour installer les dépendances
   - Sélectionnez l'option 2 pour lancer l'application
   - Sélectionnez l'option 3 pour créer un exécutable autonome (optionnel)

Le script vérifiera automatiquement les prérequis, créera un environnement virtuel, installera les dépendances nécessaires et lancera l'application.

### 3.2 Installation manuelle

Si vous préférez installer l'application manuellement, suivez ces étapes :

1. **Téléchargement du code source** :
   ```bash
   git clone https://github.com/kaizen2025/qr-code-generator.git
   cd qr-code-generator
   ```

2. **Création d'un environnement virtuel** :
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Installation des dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancement de l'application** :
   ```bash
   python src/app.py
   ```

5. **Accès à l'application** :
   Ouvrez votre navigateur et accédez à l'adresse : http://localhost:5000

### 3.3 Création d'un exécutable autonome

Pour créer un exécutable autonome qui peut être distribué sans nécessiter une installation de Python :

1. **Installation de PyInstaller** :
   ```bash
   pip install pyinstaller
   ```

2. **Création de l'exécutable** :
   ```bash
   # Windows
   pyinstaller --name=QRCodeGenerator --onefile --windowed --icon=src/frontend/static/img/favicon.ico --add-data="src/frontend/templates;src/frontend/templates" --add-data="src/frontend/static;src/frontend/static" src/app.py

   # macOS/Linux
   pyinstaller --name=QRCodeGenerator --onefile --windowed --icon=src/frontend/static/img/favicon.ico --add-data="src/frontend/templates:src/frontend/templates" --add-data="src/frontend/static:src/frontend/static" src/app.py
   ```

3. **Localisation de l'exécutable** :
   L'exécutable sera créé dans le dossier `dist` et pourra être distribué tel quel.

## 4. Déploiement sur Render

### 4.1 Prérequis pour le déploiement

- Un compte Render (inscription gratuite sur [render.com](https://render.com))
- Un dépôt GitHub contenant le code source de l'application

### 4.2 Étapes de déploiement

1. **Connexion à Render** :
   - Connectez-vous à votre compte Render
   - Utilisez l'option "Login with GitHub" pour lier votre compte GitHub

2. **Création d'un nouveau service web** :
   - Cliquez sur "New" puis "Web Service"
   - Sélectionnez le dépôt GitHub contenant l'application

3. **Configuration du service** :
   - **Nom** : qr-code-generator (ou un autre nom de votre choix)
   - **Environnement** : Python
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn src.app:app`
   - **Plan** : Free (pour la version gratuite)

4. **Lancement du déploiement** :
   - Cliquez sur "Create Web Service"
   - Render va automatiquement déployer l'application

5. **Accès à l'application déployée** :
   - Une fois le déploiement terminé, l'application sera accessible à l'URL fournie par Render
   - Par exemple : https://qr-code-generator.onrender.com

### 4.3 Configuration des variables d'environnement

Pour configurer des variables d'environnement sur Render :

1. Accédez à votre service web sur le tableau de bord Render
2. Cliquez sur "Environment" dans le menu de gauche
3. Ajoutez les variables d'environnement nécessaires :
   - `FLASK_ENV` : production
   - `SECRET_KEY` : une clé secrète aléatoire pour sécuriser l'application

## 5. Configuration GitHub

### 5.1 Création du dépôt

1. **Connexion à GitHub** :
   - Connectez-vous à votre compte GitHub (ou créez-en un sur [github.com](https://github.com))

2. **Création d'un nouveau dépôt** :
   - Cliquez sur "New repository"
   - Nom : qr-code-generator
   - Description : Générateur de QR Codes Personnalisé pour Anecoop-France
   - Visibilité : Public ou Private selon vos préférences
   - Cliquez sur "Create repository"

3. **Initialisation du dépôt local et push** :
   ```bash
   # Dans le dossier du projet
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/kaizen2025/qr-code-generator.git
   git push -u origin main
   ```

### 5.2 Configuration de l'intégration continue

Pour configurer l'intégration continue avec GitHub Actions :

1. **Création du dossier de workflows** :
   ```bash
   mkdir -p .github/workflows
   ```

2. **Création du fichier de workflow** :
   Créez un fichier `.github/workflows/ci-cd.yml` avec le contenu suivant :
   ```yaml
   name: CI/CD Pipeline

   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]

   jobs:
     test:
       runs-on: ubuntu-latest
       
       steps:
       - uses: actions/checkout@v2
       
       - name: Set up Python
         uses: actions/setup-python@v2
         with:
           python-version: '3.10'
       
       - name: Install dependencies
         run: |
           python -m pip install --upgrade pip
           if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
           pip install pytest
       
       - name: Run tests
         run: |
           pytest
     
     deploy:
       needs: test
       runs-on: ubuntu-latest
       if: github.ref == 'refs/heads/main' && github.event_name == 'push'
       
       steps:
       - uses: actions/checkout@v2
       
       - name: Deploy to Render
         uses: JorgeLNJunior/render-deploy@v1.3.2
         with:
           service_id: ${{ secrets.RENDER_SERVICE_ID }}
           api_key: ${{ secrets.RENDER_API_KEY }}
           clear_cache: true
   ```

3. **Configuration des secrets GitHub** :
   - Accédez aux paramètres de votre dépôt GitHub
   - Cliquez sur "Secrets" puis "New repository secret"
   - Ajoutez les secrets suivants :
     - `RENDER_SERVICE_ID` : ID de votre service Render
     - `RENDER_API_KEY` : Clé API Render

## 6. Mise à jour de l'application

### Mise à jour de la version locale

1. **Mise à jour du code source** :
   ```bash
   cd qr-code-generator
   git pull origin main
   ```

2. **Mise à jour des dépendances** :
   ```bash
   # Activation de l'environnement virtuel
   source venv/bin/activate  # ou venv\Scripts\activate sur Windows
   
   # Mise à jour des dépendances
   pip install -r requirements.txt
   ```

### Mise à jour de la version en ligne

La mise à jour de la version en ligne est automatique grâce à l'intégration continue :

1. **Modification du code** :
   Effectuez vos modifications dans le code source

2. **Commit et push** :
   ```bash
   git add .
   git commit -m "Description des modifications"
   git push origin main
   ```

3. **Déploiement automatique** :
   GitHub Actions va automatiquement exécuter les tests et déployer l'application sur Render si les tests réussissent.

## 7. Dépannage

### Problèmes d'installation locale

#### Python non trouvé
- Vérifiez que Python est correctement installé : `python --version` ou `python3 --version`
- Assurez-vous que Python est dans votre PATH système

#### Erreurs lors de l'installation des dépendances
- Mettez à jour pip : `python -m pip install --upgrade pip`
- Vérifiez que vous avez les droits d'administrateur si nécessaire
- Sur Linux/macOS, installez les packages de développement : `sudo apt-get install python3-dev` (Ubuntu) ou équivalent

#### L'application ne démarre pas
- Vérifiez les logs d'erreur
- Assurez-vous que le port 5000 n'est pas déjà utilisé par une autre application

### Problèmes de déploiement

#### Échec du déploiement sur Render
- Vérifiez les logs de build sur Render
- Assurez-vous que le fichier `requirements.txt` est à jour
- Vérifiez que la commande de démarrage est correcte

#### Échec de l'intégration continue
- Vérifiez les logs GitHub Actions
- Assurez-vous que les tests passent localement
- Vérifiez que les secrets GitHub sont correctement configurés

---

*Ce guide d'installation est la propriété d'Anecoop-France. Tous droits réservés.*
