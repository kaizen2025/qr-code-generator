# Générateur de QR Codes Personnalisé

![Logo](src/frontend/static/img/logo.png)

## Présentation

Le Générateur de QR Codes Personnalisé est une application web développée pour Anecoop-France, permettant de créer des QR codes hautement personnalisables avec intégration de logos et d'éléments liés aux réseaux sociaux. L'application est disponible à la fois en ligne via Render et en mode local sans connexion internet.

## Fonctionnalités

- **Génération de QR codes** avec différents niveaux de correction d'erreur et versions
- **Personnalisation avancée** :
  - Couleurs personnalisables (remplissage et arrière-plan)
  - Formes des modules (carrés, ronds, barres, etc.)
  - Dégradés de couleurs (radial, horizontal, vertical)
  - Styles prédéfinis (classic, rounded, dots, modern_blue, sunset, etc.)
- **Intégration de logos** au centre du QR code
- **Intégration d'icônes de réseaux sociaux** (Facebook, Twitter, Instagram, LinkedIn, etc.)
- **Exportation multi-formats** :
  - PNG (avec options de résolution et qualité)
  - SVG (vectoriel)
  - PDF (avec métadonnées personnalisables)
  - EPS (pour impression professionnelle)
- **Gestion de l'historique** des QR codes générés
- **Interface responsive** adaptée à tous les appareils

## Installation locale

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation automatique

1. Clonez ce dépôt :
   ```
   git clone https://github.com/kaizen2025/qr-code-generator.git
   cd qr-code-generator
   ```

2. Exécutez le script d'installation :
   ```
   python setup.py
   ```

3. Suivez les instructions à l'écran pour :
   - Installer les dépendances
   - Lancer l'application
   - Créer un exécutable autonome (optionnel)

### Installation manuelle

1. Clonez ce dépôt :
   ```
   git clone https://github.com/kaizen2025/qr-code-generator.git
   cd qr-code-generator
   ```

2. Créez un environnement virtuel et activez-le :
   ```
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

4. Lancez l'application :
   ```
   python src/app.py
   ```

5. Ouvrez votre navigateur à l'adresse : http://localhost:5000

## Utilisation en ligne

L'application est également disponible en ligne à l'adresse suivante :
[https://qr-code-generator.onrender.com](https://qr-code-generator.onrender.com)

## Structure du projet

```
qr_code_generator/
├── .github/
│   └── workflows/
│       └── ci-cd.yml         # Configuration CI/CD pour GitHub Actions
├── docs/                     # Documentation
├── src/
│   ├── backend/
│   │   ├── qr_generator/     # Génération de QR codes de base
│   │   ├── customization/    # Personnalisation des QR codes
│   │   └── export/           # Exportation des QR codes
│   ├── frontend/
│   │   ├── static/           # Fichiers statiques (CSS, JS, images)
│   │   └── templates/        # Templates HTML
│   ├── utils/                # Fonctions utilitaires
│   └── app.py                # Application Flask principale
├── tests/                    # Tests unitaires et fonctionnels
├── .gitignore                # Fichiers à ignorer par Git
├── Procfile                  # Configuration pour Render
├── README.md                 # Ce fichier
├── render.yaml               # Configuration pour Render
├── requirements.txt          # Dépendances Python
└── setup.py                  # Script d'installation et de lancement
```

## Déploiement

### GitHub

Le code source est hébergé sur GitHub à l'adresse suivante :
[https://github.com/kaizen2025/qr-code-generator](https://github.com/kaizen2025/qr-code-generator)

### Render

L'application est déployée sur Render avec intégration continue depuis GitHub. Chaque push sur la branche `main` déclenche automatiquement un nouveau déploiement.

## Développement

### Tests

Pour exécuter les tests unitaires :
```
pytest
```

### Contribution

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Committez vos changements (`git commit -m 'Add some amazing feature'`)
4. Poussez vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

## Licence

Propriété d'Anecoop-France – Créé par Kevin BIVIA

## Contact

Pour toute question ou suggestion, veuillez contacter :
- Kevin BIVIA - [kevin.bivia@gmail.com](mailto:kevin.bivia@gmail.com)
