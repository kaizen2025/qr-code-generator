# Guide d'utilisation - Générateur de QR Codes Personnalisé
*Propriété d'Anecoop-France – Créé par Kevin BIVIA*

## Table des matières

1. [Introduction](#1-introduction)
2. [Installation](#2-installation)
   - [Installation en ligne](#21-installation-en-ligne)
   - [Installation locale](#22-installation-locale)
3. [Interface utilisateur](#3-interface-utilisateur)
   - [Page d'accueil](#31-page-daccueil)
   - [Historique](#32-historique)
4. [Création de QR codes](#4-création-de-qr-codes)
   - [QR code basique](#41-qr-code-basique)
   - [QR code personnalisé](#42-qr-code-personnalisé)
   - [QR code avec logo](#43-qr-code-avec-logo)
   - [QR code avec style prédéfini](#44-qr-code-avec-style-prédéfini)
   - [QR code avec icônes de réseaux sociaux](#45-qr-code-avec-icônes-de-réseaux-sociaux)
5. [Exportation](#5-exportation)
   - [Formats disponibles](#51-formats-disponibles)
   - [Options d'exportation](#52-options-dexportation)
6. [Gestion de l'historique](#6-gestion-de-lhistorique)
   - [Recherche](#61-recherche)
   - [Réutilisation](#62-réutilisation)
   - [Exportation depuis l'historique](#63-exportation-depuis-lhistorique)
7. [Conseils et bonnes pratiques](#7-conseils-et-bonnes-pratiques)
8. [Dépannage](#8-dépannage)
9. [Support technique](#9-support-technique)

## 1. Introduction

Le Générateur de QR Codes Personnalisé est une application développée pour Anecoop-France permettant de créer des QR codes hautement personnalisables avec intégration de logos et d'éléments liés aux réseaux sociaux. Cette application est disponible à la fois en ligne via Render et en mode local sans connexion internet.

Ce guide vous accompagnera dans l'utilisation de toutes les fonctionnalités de l'application, de l'installation à la création et l'exportation de QR codes personnalisés.

## 2. Installation

### 2.1 Installation en ligne

L'application est accessible en ligne à l'adresse suivante :
[https://qr-code-generator.onrender.com](https://qr-code-generator.onrender.com)

Aucune installation n'est nécessaire pour utiliser la version en ligne. Il vous suffit d'avoir un navigateur web moderne (Chrome, Firefox, Safari, Edge) et une connexion internet.

### 2.2 Installation locale

Pour utiliser l'application en mode local sans connexion internet, suivez ces étapes :

#### Méthode 1 : Utilisation du script d'installation

1. Téléchargez le code source depuis GitHub :
   ```
   git clone https://github.com/kaizen2025/qr-code-generator.git
   cd qr-code-generator
   ```

2. Exécutez le script d'installation :
   ```
   python setup.py
   ```

3. Dans le menu qui s'affiche, sélectionnez l'option 1 pour installer les dépendances, puis l'option 2 pour lancer l'application.

4. L'application s'ouvrira automatiquement dans votre navigateur par défaut à l'adresse http://localhost:5000

#### Méthode 2 : Utilisation de l'exécutable

1. Téléchargez l'exécutable depuis la page des releases sur GitHub :
   [https://github.com/kaizen2025/qr-code-generator/releases](https://github.com/kaizen2025/qr-code-generator/releases)

2. Double-cliquez sur l'exécutable téléchargé (QRCodeGenerator.exe pour Windows).

3. L'application s'ouvrira automatiquement dans votre navigateur par défaut.

## 3. Interface utilisateur

### 3.1 Page d'accueil

La page d'accueil est divisée en deux sections principales :

- **Panneau de gauche** : Formulaires pour la création et la personnalisation de QR codes, organisés en onglets.
- **Panneau de droite** : Aperçu du QR code généré et options d'exportation.

Les onglets disponibles sont :
- **Basique** : Création de QR codes simples
- **Personnalisé** : Personnalisation des couleurs et des dimensions
- **Logo** : Ajout d'un logo au centre du QR code
- **Style** : Application de styles prédéfinis

### 3.2 Historique

La page d'historique affiche tous les QR codes précédemment générés, avec les options suivantes :

- **Recherche** : Filtrer les QR codes par contenu ou nom de fichier
- **Téléchargement** : Télécharger directement un QR code
- **Exportation** : Exporter un QR code dans différents formats
- **Réutilisation** : Utiliser les données d'un QR code existant pour en créer un nouveau

## 4. Création de QR codes

### 4.1 QR code basique

Pour créer un QR code basique :

1. Accédez à l'onglet **Basique**
2. Saisissez le contenu du QR code (URL, texte, coordonnées, etc.)
3. Sélectionnez la version du QR code (taille de la matrice)
4. Choisissez le niveau de correction d'erreur
5. Ajustez la taille des modules et la bordure si nécessaire
6. Cliquez sur **Générer le QR Code**

### 4.2 QR code personnalisé

Pour créer un QR code avec des couleurs personnalisées :

1. Accédez à l'onglet **Personnalisé**
2. Saisissez le contenu du QR code
3. Sélectionnez la couleur des modules (noir par défaut)
4. Sélectionnez la couleur d'arrière-plan (blanc par défaut)
5. Ajustez les autres paramètres selon vos besoins
6. Cliquez sur **Générer le QR Code**

### 4.3 QR code avec logo

Pour ajouter un logo au centre de votre QR code :

1. Accédez à l'onglet **Logo**
2. Saisissez le contenu du QR code
3. Cliquez sur **Parcourir** pour sélectionner un fichier image (PNG recommandé avec transparence)
4. Ajustez la taille du logo (20% par défaut)
5. Personnalisez les couleurs si nécessaire
6. Sélectionnez un niveau de correction d'erreur élevé (H recommandé)
7. Cliquez sur **Générer le QR Code**

### 4.4 QR code avec style prédéfini

Pour utiliser un style prédéfini :

1. Accédez à l'onglet **Style**
2. Saisissez le contenu du QR code
3. Sélectionnez l'un des styles prédéfinis disponibles :
   - Classic (carré classique)
   - Rounded (coins arrondis)
   - Dots (points)
   - Modern Blue (dégradé bleu moderne)
   - Sunset (dégradé orange-rouge)
   - Forest (dégradé vert)
   - Ocean (dégradé bleu océan)
   - Barcode (barres verticales)
   - Elegant (carré avec espacement)
4. Ajustez les autres paramètres selon vos besoins
5. Cliquez sur **Générer le QR Code**

### 4.5 QR code avec icônes de réseaux sociaux

Pour ajouter des icônes de réseaux sociaux à votre QR code :

1. Accédez à l'onglet **Personnalisé**
2. Saisissez le contenu du QR code (généralement une URL)
3. Cliquez sur **Générer le QR Code**
4. Dans les options d'exportation, cochez **Ajouter des icônes de réseaux sociaux**
5. Sélectionnez les plateformes sociales souhaitées
6. Choisissez la disposition des icônes (cercle, ligne, colonne)
7. Cliquez sur **Exporter**

## 5. Exportation

### 5.1 Formats disponibles

L'application permet d'exporter les QR codes dans les formats suivants :

- **PNG** : Format d'image standard pour le web et les applications
- **SVG** : Format vectoriel idéal pour l'impression et le redimensionnement
- **PDF** : Document portable avec métadonnées personnalisables
- **EPS** : Format vectoriel pour l'impression professionnelle
- **Tous** : Exportation simultanée dans tous les formats ci-dessus (fichier ZIP)

### 5.2 Options d'exportation

Selon le format sélectionné, différentes options sont disponibles :

#### PNG
- **Résolution (DPI)** : 72 (web), 150, 300 (impression), 600 (haute qualité)
- **Qualité** : De 70% à 100%

#### SVG
- **Échelle** : De 0.5x à 3x

#### PDF
- **Titre du document** : Personnalisable
- **Dimensions** : Largeur et hauteur en mm

## 6. Gestion de l'historique

### 6.1 Recherche

Pour rechercher un QR code dans l'historique :

1. Accédez à la page **Historique**
2. Utilisez la barre de recherche en haut à droite
3. Saisissez un terme de recherche (contenu du QR code ou nom de fichier)
4. Les résultats s'affichent automatiquement pendant la saisie

### 6.2 Réutilisation

Pour réutiliser les données d'un QR code existant :

1. Accédez à la page **Historique**
2. Trouvez le QR code que vous souhaitez réutiliser
3. Cliquez sur le bouton **Réutiliser**
4. Vous serez redirigé vers la page d'accueil avec les données pré-remplies
5. Modifiez les paramètres selon vos besoins
6. Cliquez sur **Générer le QR Code**

### 6.3 Exportation depuis l'historique

Pour exporter un QR code depuis l'historique :

1. Accédez à la page **Historique**
2. Trouvez le QR code que vous souhaitez exporter
3. Cliquez sur le bouton **Exporter**
4. Sélectionnez le format d'exportation et les options souhaitées
5. Cliquez sur **Exporter**

## 7. Conseils et bonnes pratiques

- **Niveau de correction d'erreur** : Utilisez un niveau élevé (H) lorsque vous ajoutez un logo ou des icônes
- **Taille du logo** : Ne dépassez pas 30% de la taille du QR code pour garantir la lisibilité
- **Test de lecture** : Testez toujours vos QR codes avec différentes applications de lecture avant de les utiliser
- **Contraste** : Assurez-vous que le contraste entre les modules et l'arrière-plan est suffisant
- **Version du QR code** : Utilisez une version plus élevée pour les contenus longs ou lorsque vous ajoutez un logo

## 8. Dépannage

### Problèmes courants et solutions

#### Le QR code ne se génère pas
- Vérifiez que vous avez saisi un contenu
- Essayez de réduire la taille du logo si vous en utilisez un
- Utilisez une version plus élevée du QR code

#### Le QR code ne peut pas être lu
- Augmentez le niveau de correction d'erreur
- Réduisez la taille du logo
- Assurez-vous que le contraste est suffisant
- Évitez les dégradés trop complexes

#### L'exportation échoue
- Vérifiez que vous avez sélectionné un format d'exportation
- Essayez un autre format d'exportation
- Réduisez la résolution pour les grands QR codes

#### L'application locale ne démarre pas
- Vérifiez que Python 3.8 ou supérieur est installé
- Assurez-vous que toutes les dépendances sont installées
- Consultez les logs pour plus d'informations

## 9. Support technique

Pour toute question ou assistance technique, veuillez contacter :

- **Email** : kevin.bivia@gmail.com
- **GitHub** : Ouvrez une issue sur le dépôt GitHub [https://github.com/kaizen2025/qr-code-generator/issues](https://github.com/kaizen2025/qr-code-generator/issues)

---

*Ce guide d'utilisation est la propriété d'Anecoop-France. Tous droits réservés.*
