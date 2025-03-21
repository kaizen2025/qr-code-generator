# Instructions de déploiement manuel

## Déploiement sur GitHub

1. Clonez le dépôt GitHub que j'ai créé pour vous :
   ```bash
   git clone https://github.com/kaizen2025/qr-code-generator.git
   cd qr-code-generator
   ```

2. Copiez tous les fichiers du projet dans ce dépôt cloné

3. Ajoutez, committez et poussez les modifications vers GitHub :
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

## Déploiement sur Render

1. Connectez-vous à Render avec votre email (kevin.bivia@gmail.com)
2. Accédez à https://dashboard.render.com/
3. Cliquez sur "New" puis "Web Service"
4. Connectez votre compte GitHub si ce n'est pas déjà fait
5. Sélectionnez le dépôt : https://github.com/kaizen2025/qr-code-generator
6. Configurez le service :
   - Nom : qr-code-generator
   - Environnement : Python
   - Build Command : pip install -r requirements.txt
   - Start Command : gunicorn src.app:app
   - Plan : Free
7. Cliquez sur "Create Web Service"

Une fois le déploiement terminé, l'application sera accessible à l'URL fournie par Render.

## Création d'un fichier ZIP pour importation directe sur GitHub

Si vous préférez utiliser l'interface web de GitHub pour importer le projet :

1. Créez une archive ZIP du projet :
   ```bash
   cd /home/ubuntu
   zip -r qr_code_generator.zip qr_code_generator
   ```

2. Téléchargez ce fichier ZIP

3. Accédez à https://github.com/new pour créer un nouveau dépôt nommé "qr-code-generator"

4. Après avoir créé le dépôt, cliquez sur "uploading an existing file" et importez le fichier ZIP

## Configuration de l'intégration continue

Pour configurer l'intégration continue entre GitHub et Render :

1. Dans votre dépôt GitHub, accédez à Settings > Secrets > Actions
2. Ajoutez les secrets suivants :
   - RENDER_SERVICE_ID : l'ID de votre service Render (visible dans l'URL)
   - RENDER_API_KEY : votre clé API Render (disponible dans les paramètres de votre compte)

Ces secrets permettront au workflow GitHub Actions de déclencher automatiquement un déploiement sur Render à chaque push sur la branche main.
