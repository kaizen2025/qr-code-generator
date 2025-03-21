#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module de test pour le générateur de QR codes basique.
Ce module contient les tests unitaires pour valider les fonctionnalités
du module de génération de QR codes.
"""

import os
import pytest
import qrcode
from PIL import Image
import sys
import uuid

# Ajout du chemin du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import du module à tester
from src.backend.qr_generator.basic_generator import QRCodeGenerator


class TestQRCodeGenerator:
    """Classe de test pour QRCodeGenerator"""

    @pytest.fixture
    def generator(self, tmp_path):
        """Fixture pour créer une instance de QRCodeGenerator avec un répertoire temporaire"""
        output_dir = tmp_path / "qrcodes"
        output_dir.mkdir()
        return QRCodeGenerator(output_dir=str(output_dir))

    @pytest.fixture
    def sample_logo(self, tmp_path):
        """Fixture pour créer un logo de test"""
        logo_path = tmp_path / "test_logo.png"
        # Création d'une image simple pour le test
        img = Image.new('RGB', (100, 100), color='red')
        img.save(logo_path)
        return str(logo_path)

    def test_init(self, generator, tmp_path):
        """Test de l'initialisation du générateur"""
        assert os.path.exists(generator.output_dir)
        assert generator.output_dir == str(tmp_path / "qrcodes")

    def test_generate_basic_qrcode(self, generator):
        """Test de la génération d'un QR code basique"""
        data = "https://www.example.com"
        filename = "test_basic.png"
        
        # Génération du QR code
        output_path = generator.generate_basic_qrcode(data, filename)
        
        # Vérification que le fichier existe
        assert os.path.exists(output_path)
        
        # Vérification que le fichier est une image valide
        img = Image.open(output_path)
        assert img.format == "PNG"
        
        # Vérification des métadonnées
        metadata_dir = os.path.join(generator.output_dir, 'metadata')
        metadata_file = os.path.join(metadata_dir, "test_basic.txt")
        assert os.path.exists(metadata_file)
        
        # Vérification du contenu des métadonnées
        with open(metadata_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert data in content
            assert filename in content

    def test_generate_qrcode_with_options(self, generator):
        """Test de la génération d'un QR code avec options personnalisées"""
        data = "https://www.example.com"
        filename = "test_options.png"
        options = {
            'version': 2,
            'error_correction': qrcode.constants.ERROR_CORRECT_Q,
            'box_size': 15,
            'border': 2,
            'fill_color': "blue",
            'back_color': "yellow"
        }
        
        # Génération du QR code
        output_path = generator.generate_qrcode_with_options(data, filename, **options)
        
        # Vérification que le fichier existe
        assert os.path.exists(output_path)
        
        # Vérification que le fichier est une image valide
        img = Image.open(output_path)
        assert img.format == "PNG"
        
        # Vérification des métadonnées
        metadata_dir = os.path.join(generator.output_dir, 'metadata')
        metadata_file = os.path.join(metadata_dir, "test_options.txt")
        assert os.path.exists(metadata_file)
        
        # Vérification du contenu des métadonnées
        with open(metadata_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert data in content
            assert filename in content
            assert "fill_color: blue" in content
            assert "back_color: yellow" in content

    def test_generate_qrcode_with_logo(self, generator, sample_logo):
        """Test de la génération d'un QR code avec logo"""
        data = "https://www.example.com"
        filename = "test_logo.png"
        
        # Génération du QR code avec logo
        output_path = generator.generate_qrcode_with_logo(data, sample_logo, filename)
        
        # Vérification que le fichier existe
        assert os.path.exists(output_path)
        
        # Vérification que le fichier est une image valide
        img = Image.open(output_path)
        assert img.format == "PNG"
        
        # Vérification des métadonnées
        metadata_dir = os.path.join(generator.output_dir, 'metadata')
        metadata_file = os.path.join(metadata_dir, "test_logo.txt")
        assert os.path.exists(metadata_file)
        
        # Vérification du contenu des métadonnées
        with open(metadata_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert data in content
            assert filename in content
            assert "logo_path" in content

    def test_auto_filename_generation(self, generator):
        """Test de la génération automatique des noms de fichiers"""
        data = "https://www.example.com"
        
        # Génération du QR code sans spécifier de nom de fichier
        output_path = generator.generate_basic_qrcode(data)
        
        # Vérification que le fichier existe
        assert os.path.exists(output_path)
        
        # Vérification que le nom de fichier contient "qrcode_" et se termine par ".png"
        filename = os.path.basename(output_path)
        assert filename.startswith("qrcode_")
        assert filename.endswith(".png")
        
        # Vérification que l'UUID est présent dans le nom de fichier
        uuid_part = filename[7:-4]  # Extraction de la partie UUID
        assert len(uuid_part) == 8  # UUID tronqué à 8 caractères
