# Instructions de déploiement permanent

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
