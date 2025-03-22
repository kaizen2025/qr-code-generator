/**
 * Script principal pour le générateur de QR codes personnalisé
 * Gère les interactions utilisateur, les requêtes AJAX et les mises à jour de l'interface
 */

document.addEventListener('DOMContentLoaded', function() {
    // Éléments DOM principaux
    const qrForm = document.getElementById('qr-form');
    const qrDataInput = document.getElementById('qr-data');
    const qrPreview = document.getElementById('qr-preview');
    const generateBtn = document.getElementById('generate-btn');
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    const exportButtons = document.querySelectorAll('.export-button');
    const colorPickers = document.querySelectorAll('.color-picker');
    const rangeInputs = document.querySelectorAll('input[type="range"]');
    const logoUpload = document.getElementById('logo-upload');
    const styleOptions = document.querySelectorAll('.style-option');
    const socialPlatforms = document.querySelectorAll('.social-platform');
    const moduleShapes = document.querySelectorAll('.module-shape');
    const frameShapes = document.querySelectorAll('.frame-shape');
    const eyeShapes = document.querySelectorAll('.eye-shape');
    
    // Variables globales
    let currentQRPath = null;
    let currentTab = 'basic'; // Tab par défaut
    let debounceTimer;
    const DEBOUNCE_DELAY = 300; // Délai pour éviter trop de requêtes lors des changements rapides

    // ------- Initialisation -------

    /**
     * Initialise les événements et l'état initial de l'application
     */
    function init() {
        // Initialiser les onglets
        initTabs();
        
        // Initialiser les sélecteurs de couleur
        initColorPickers();
        
        // Initialiser les sliders
        initRangeInputs();

        // Événement de soumission du formulaire
        if (qrForm) {
            qrForm.addEventListener('submit', handleFormSubmit);
        }

        // Événements pour les modifications d'input (prévisualisation en temps réel)
        if (qrDataInput) {
            qrDataInput.addEventListener('input', debouncePreview);
        }

        // Initialiser tous les sélecteurs d'options
        initOptionSelectors();
        
        // Initialiser l'upload de logo
        initLogoUpload();
        
        // Initialiser les boutons d'exportation
        initExportButtons();
        
        // Afficher la prévisualisation initiale si des données sont présentes
        if (qrDataInput && qrDataInput.value) {
            generatePreview();
        }
    }

    // ------- Gestion des onglets -------

    /**
     * Initialise les onglets et leurs événements
     */
    function initTabs() {
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const tabId = button.getAttribute('data-tab');
                switchTab(tabId);
            });
        });

        // Activer l'onglet par défaut
        if (tabButtons.length > 0) {
            const defaultTab = tabButtons[0].getAttribute('data-tab');
            switchTab(defaultTab);
        }
    }

    /**
     * Change l'onglet actif
     * @param {string} tabId - ID de l'onglet à activer
     */
    function switchTab(tabId) {
        // Mettre à jour l'onglet actif
        tabButtons.forEach(button => {
            if (button.getAttribute('data-tab') === tabId) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });

        // Afficher le contenu de l'onglet actif
        tabContents.forEach(content => {
            if (content.getAttribute('id') === `tab-${tabId}`) {
                content.classList.add('active');
            } else {
                content.classList.remove('active');
            }
        });

        // Mettre à jour l'onglet courant
        currentTab = tabId;
        
        // Générer une prévisualisation avec les options de l'onglet actif
        generatePreview();
    }

    // ------- Gestion des couleurs -------

    /**
     * Initialise les sélecteurs de couleur
     */
    function initColorPickers() {
        colorPickers.forEach(picker => {
            picker.addEventListener('input', debouncePreview);
        });
    }

    // ------- Gestion des sliders -------

    /**
     * Initialise les inputs de type range
     */
    function initRangeInputs() {
        rangeInputs.forEach(input => {
            // Mise à jour de la valeur affichée
            const valueDisplay = document.getElementById(`${input.id}-value`);
            if (valueDisplay) {
                valueDisplay.textContent = input.value;
                
                input.addEventListener('input', () => {
                    valueDisplay.textContent = input.value;
                    debouncePreview();
                });
            } else {
                input.addEventListener('input', debouncePreview);
            }
        });
    }

    // ------- Gestion des sélecteurs d'options -------

    /**
     * Initialise tous les sélecteurs d'options (styles, formes, etc.)
     */
    function initOptionSelectors() {
        // Options de style
        styleOptions.forEach(option => {
            option.addEventListener('click', () => {
                // Désélectionner toutes les options
                styleOptions.forEach(opt => opt.classList.remove('selected'));
                
                // Sélectionner l'option cliquée
                option.classList.add('selected');
                
                // Générer la prévisualisation
                debouncePreview();
            });
        });

        // Plateformes sociales
        socialPlatforms.forEach(platform => {
            platform.addEventListener('click', () => {
                // Toggle de la sélection (pour permettre la sélection multiple)
                platform.classList.toggle('selected');
                
                // Générer la prévisualisation
                debouncePreview();
            });
        });

        // Formes de modules
        moduleShapes.forEach(shape => {
            shape.addEventListener('click', () => {
                // Désélectionner toutes les formes
                moduleShapes.forEach(s => s.classList.remove('selected'));
                
                // Sélectionner la forme cliquée
                shape.classList.add('selected');
                
                // Générer la prévisualisation
                debouncePreview();
            });
        });

        // Formes de contour
        frameShapes.forEach(shape => {
            shape.addEventListener('click', () => {
                // Désélectionner toutes les formes
                frameShapes.forEach(s => s.classList.remove('selected'));
                
                // Sélectionner la forme cliquée
                shape.classList.add('selected');
                
                // Générer la prévisualisation
                debouncePreview();
            });
        });

        // Formes des yeux
        eyeShapes.forEach(shape => {
            shape.addEventListener('click', () => {
                // Désélectionner toutes les formes
                eyeShapes.forEach(s => s.classList.remove('selected'));
                
                // Sélectionner la forme cliquée
                shape.classList.add('selected');
                
                // Générer la prévisualisation
                debouncePreview();
            });
        });
    }

    // ------- Gestion de l'upload de logo -------

    /**
     * Initialise l'upload de logo
     */
    function initLogoUpload() {
        if (logoUpload) {
            logoUpload.addEventListener('change', handleLogoUpload);
            
            // Bouton de suppression du logo
            const removeLogoBtn = document.getElementById('remove-logo');
            if (removeLogoBtn) {
                removeLogoBtn.addEventListener('click', () => {
                    // Réinitialiser l'input file
                    logoUpload.value = '';
                    
                    // Masquer l'aperçu du logo
                    const logoPreview = document.getElementById('logo-preview');
                    if (logoPreview) {
                        logoPreview.style.display = 'none';
                        logoPreview.src = '';
                    }
                    
                    // Générer la prévisualisation sans logo
                    debouncePreview();
                });
            }
        }
    }

    /**
     * Gère l'upload d'un logo
     * @param {Event} event - Événement de changement de l'input file
     */
    function handleLogoUpload(event) {
        const file = event.target.files[0];
        if (file) {
            // Vérifier le type de fichier
            if (!file.type.match('image.*')) {
                showError('Le fichier sélectionné n\'est pas une image');
                return;
            }
            
            // Vérifier la taille du fichier (max 2 Mo)
            if (file.size > 2 * 1024 * 1024) {
                showError('L\'image est trop volumineuse (max 2 Mo)');
                return;
            }
            
            // Afficher l'aperçu du logo
            const reader = new FileReader();
            reader.onload = function(e) {
                const logoPreview = document.getElementById('logo-preview');
                if (logoPreview) {
                    logoPreview.style.display = 'block';
                    logoPreview.src = e.target.result;
                }
                
                // Générer la prévisualisation avec le logo
                debouncePreview();
            };
            reader.readAsDataURL(file);
        }
    }

    // ------- Gestion des boutons d'exportation -------

    /**
     * Initialise les boutons d'exportation
     */
    function initExportButtons() {
        exportButtons.forEach(button => {
            button.addEventListener('click', () => {
                const format = button.getAttribute('data-format');
                exportQRCode(format);
            });
        });
    }

    // ------- Gestion des formulaires -------

    /**
     * Gère la soumission du formulaire (génération du QR code)
     * @param {Event} event - Événement de soumission du formulaire
     */
    function handleFormSubmit(event) {
        event.preventDefault();
        generateQRCode();
    }

    // ------- Génération de QR code -------

    /**
     * Génère un QR code avec les options sélectionnées
     */
    function generateQRCode() {
        // Vérifier que des données sont présentes
        if (!qrDataInput || !qrDataInput.value.trim()) {
            showError('Veuillez saisir du contenu pour le QR code');
            return;
        }
        
        // Afficher un indicateur de chargement
        showLoading(true);
        
        // Récupérer les options en fonction de l'onglet actif
        const formData = new FormData();
        formData.append('data', qrDataInput.value.trim());
        
        // Options communes
        const version = document.getElementById('qr-version')?.value || 1;
        const errorCorrection = document.getElementById('qr-error-correction')?.value || 1;
        const boxSize = document.getElementById('qr-box-size')?.value || 10;
        const border = document.getElementById('qr-border')?.value || 4;
        
        formData.append('version', version);
        formData.append('error_correction', errorCorrection);
        formData.append('box_size', boxSize);
        formData.append('border', border);
        
        // Type de génération en fonction de l'onglet actif
        formData.append('generation_type', currentTab);
        
        // Options spécifiques à l'onglet "custom"
        if (currentTab === 'custom') {
            const fillColor = document.getElementById('fill-color')?.value || '#000000';
            const backColor = document.getElementById('back-color')?.value || '#FFFFFF';
            
            formData.append('fill_color', fillColor);
            formData.append('back_color', backColor);
        }
        
        // Options spécifiques à l'onglet "logo"
        else if (currentTab === 'logo') {
            // Logo
            const logoFile = logoUpload?.files[0];
            if (logoFile) {
                formData.append('logo', logoFile);
            }
            
            // Taille du logo
            const logoSize = document.getElementById('logo-size')?.value || 0.2;
            formData.append('logo_size', logoSize);
            
            // Couleurs
            const fillColor = document.getElementById('logo-fill-color')?.value || '#000000';
            const backColor = document.getElementById('logo-back-color')?.value || '#FFFFFF';
            
            formData.append('fill_color', fillColor);
            formData.append('back_color', backColor);
        }
        
        // Options spécifiques à l'onglet "styled"
        else if (currentTab === 'styled') {
            const moduleDrawer = document.querySelector('.module-shape.selected')?.getAttribute('data-value') || 'square';
            const colorMask = document.getElementById('color-mask')?.value || 'solid';
            
            formData.append('module_drawer', moduleDrawer);
            formData.append('color_mask', colorMask);
            
            // Couleurs pour le masque
            if (colorMask === 'solid') {
                const frontColor = document.getElementById('front-color')?.value || '#000000';
                const backColor = document.getElementById('back-color')?.value || '#FFFFFF';
                
                formData.append('front_color', frontColor);
                formData.append('back_color', backColor);
            } else {
                // Options pour les gradients
                const frontColor = document.getElementById('gradient-start-color')?.value || '#000000';
                const edgeColor = document.getElementById('gradient-end-color')?.value || '#666666';
                const backColor = document.getElementById('gradient-back-color')?.value || '#FFFFFF';
                
                formData.append('front_color', frontColor);
                formData.append('edge_color', edgeColor);
                formData.append('back_color', backColor);
                
                // Centre du gradient
                if (document.getElementById('gradient-center-x') && document.getElementById('gradient-center-y')) {
                    const gradientCenterX = document.getElementById('gradient-center-x').value;
                    const gradientCenterY = document.getElementById('gradient-center-y').value;
                    
                    formData.append('gradient_center_x', gradientCenterX);
                    formData.append('gradient_center_y', gradientCenterY);
                }
            }
        }
        
        // Options spécifiques à l'onglet "predefined"
        else if (currentTab === 'predefined') {
            const styleName = document.querySelector('.style-option.selected')?.getAttribute('data-value') || 'classic';
            formData.append('style_name', styleName);
        }
        
        // Options spécifiques à l'onglet "social"
        else if (currentTab === 'social') {
            const socialPlatform = document.querySelector('.social-platform.selected')?.getAttribute('data-value') || '';
            
            if (socialPlatform) {
                formData.append('social_platform', socialPlatform);
            } else {
                showError('Veuillez sélectionner une plateforme sociale');
                showLoading(false);
                return;
            }
            
            // Couleurs
            const fillColor = document.getElementById('social-fill-color')?.value || '#000000';
            const backColor = document.getElementById('social-back-color')?.value || '#FFFFFF';
            
            formData.append('fill_color', fillColor);
            formData.append('back_color', backColor);
        }
        
        // Options spécifiques à l'onglet "multi_social"
        else if (currentTab === 'multi_social') {
            const selectedPlatforms = document.querySelectorAll('.social-platform.selected');
            
            if (selectedPlatforms.length === 0) {
                showError('Veuillez sélectionner au moins une plateforme sociale');
                showLoading(false);
                return;
            }
            
            // Ajouter toutes les plateformes sélectionnées
            selectedPlatforms.forEach(platform => {
                formData.append('social_platforms', platform.getAttribute('data-value'));
            });
            
            // Layout (disposition des icônes)
            const layout = document.getElementById('social-layout')?.value || 'circle';
            formData.append('layout', layout);
            
            // Couleurs
            const fillColor = document.getElementById('multi-social-fill-color')?.value || '#000000';
            const backColor = document.getElementById('multi-social-back-color')?.value || '#FFFFFF';
            
            formData.append('fill_color', fillColor);
            formData.append('back_color', backColor);
        }
        
        // Options spécifiques à l'onglet "custom_shape"
        else if (currentTab === 'custom_shape') {
            const moduleShape = document.querySelector('.module-shape.selected')?.getAttribute('data-value') || 'square';
            const frameShape = document.querySelector('.frame-shape.selected')?.getAttribute('data-value') || 'square';
            const eyeShape = document.querySelector('.eye-shape.selected')?.getAttribute('data-value') || 'square';
            
            formData.append('module_shape', moduleShape);
            formData.append('frame_shape', frameShape);
            formData.append('eye_shape', eyeShape);
            
            // Couleurs
            const fillColor = document.getElementById('custom-shape-fill-color')?.value || '#000000';
            const backColor = document.getElementById('custom-shape-back-color')?.value || '#FFFFFF';
            
            formData.append('fill_color', fillColor);
            formData.append('back_color', backColor);
        }
        
        // Envoi de la requête AJAX
        fetch('/generate', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de la génération du QR code');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Mise à jour de l'aperçu
                qrPreview.src = `/qrcodes/${data.qr_path}`;
                
                // Enregistrement du chemin du QR code généré
                currentQRPath = data.qr_path;
                
                // Activer les boutons d'exportation
                enableExportButtons();
                
                // Afficher un message de succès
                showSuccess('QR code généré avec succès');
            } else {
                showError(data.error || 'Erreur lors de la génération du QR code');
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            showError('Erreur lors de la génération du QR code');
        })
        .finally(() => {
            showLoading(false);
        });
    }

    /**
     * Génère une prévisualisation du QR code avec les options actuelles
     */
    function generatePreview() {
        // Vérifier que des données sont présentes
        if (!qrDataInput || !qrDataInput.value.trim()) {
            return;
        }
        
        // Récupérer les options en fonction de l'onglet actif
        const formData = new FormData();
        formData.append('data', qrDataInput.value.trim());
        
        // Type de prévisualisation en fonction de l'onglet actif
        formData.append('preview_type', currentTab);
        
        // Options communes
        const version = document.getElementById('qr-version')?.value || 1;
        const errorCorrection = document.getElementById('qr-error-correction')?.value || 1;
        const boxSize = document.getElementById('qr-box-size')?.value || 10;
        const border = document.getElementById('qr-border')?.value || 4;
        
        formData.append('version', version);
        formData.append('error_correction', errorCorrection);
        formData.append('box_size', boxSize);
        formData.append('border', border);
        
        // Options spécifiques à l'onglet "custom"
        if (currentTab === 'custom') {
            const fillColor = document.getElementById('fill-color')?.value || '#000000';
            const backColor = document.getElementById('back-color')?.value || '#FFFFFF';
            
            formData.append('fill_color', fillColor);
            formData.append('back_color', backColor);
        }
        
        // Options spécifiques à l'onglet "logo"
        else if (currentTab === 'logo') {
            // Logo (si présent dans l'aperçu)
            const logoPreview = document.getElementById('logo-preview');
            if (logoPreview && logoPreview.style.display !== 'none' && logoPreview.src) {
                formData.append('logo_data', logoPreview.src);
            }
            
            // Taille du logo
            const logoSize = document.getElementById('logo-size')?.value || 0.2;
            formData.append('logo_size', logoSize);
            
            // Couleurs
            const fillColor = document.getElementById('logo-fill-color')?.value || '#000000';
            const backColor = document.getElementById('logo-back-color')?.value || '#FFFFFF';
            
            formData.append('fill_color', fillColor);
            formData.append('back_color', backColor);
        }
        
        // Options spécifiques à l'onglet "styled"
        else if (currentTab === 'styled') {
            const moduleDrawer = document.querySelector('.module-shape.selected')?.getAttribute('data-value') || 'square';
            const colorMask = document.getElementById('color-mask')?.value || 'solid';
            
            formData.append('module_drawer', moduleDrawer);
            formData.append('color_mask', colorMask);
            
            // Couleurs pour le masque
            if (colorMask === 'solid') {
                const frontColor = document.getElementById('front-color')?.value || '#000000';
                const backColor = document.getElementById('back-color')?.value || '#FFFFFF';
                
                formData.append('front_color', frontColor);
                formData.append('back_color', backColor);
            } else {
                // Options pour les gradients
                const frontColor = document.getElementById('gradient-start-color')?.value || '#000000';
                const edgeColor = document.getElementById('gradient-end-color')?.value || '#666666';
                const backColor = document.getElementById('gradient-back-color')?.value || '#FFFFFF';
                
                formData.append('front_color', frontColor);
                formData.append('edge_color', edgeColor);
                formData.append('back_color', backColor);
                
                // Centre du gradient
                if (document.getElementById('gradient-center-x') && document.getElementById('gradient-center-y')) {
                    const gradientCenterX = document.getElementById('gradient-center-x').value;
                    const gradientCenterY = document.getElementById('gradient-center-y').value;
                    
                    formData.append('gradient_center_x', gradientCenterX);
                    formData.append('gradient_center_y', gradientCenterY);
                }
            }
        }
        
        // Options spécifiques à l'onglet "predefined"
        else if (currentTab === 'predefined') {
            const styleName = document.querySelector('.style-option.selected')?.getAttribute('data-value') || 'classic';
            formData.append('style_name', styleName);
        }
        
        // Options spécifiques à l'onglet "social"
        else if (currentTab === 'social') {
            const socialPlatform = document.querySelector('.social-platform.selected')?.getAttribute('data-value');
            
            if (socialPlatform) {
                formData.append('social_platform', socialPlatform);
                
                // Couleurs
                const fillColor = document.getElementById('social-fill-color')?.value || '#000000';
                const backColor = document.getElementById('social-back-color')?.value || '#FFFFFF';
                
                formData.append('fill_color', fillColor);
                formData.append('back_color', backColor);
            }
        }
        
        // Options spécifiques à l'onglet "custom_shape"
        else if (currentTab === 'custom_shape') {
            const moduleShape = document.querySelector('.module-shape.selected')?.getAttribute('data-value') || 'square';
            const frameShape = document.querySelector('.frame-shape.selected')?.getAttribute('data-value') || 'square';
            const eyeShape = document.querySelector('.eye-shape.selected')?.getAttribute('data-value') || 'square';
            
            formData.append('module_shape', moduleShape);
            formData.append('frame_shape', frameShape);
            formData.append('eye_shape', eyeShape);
            
            // Couleurs
            const fillColor = document.getElementById('custom-shape-fill-color')?.value || '#000000';
            const backColor = document.getElementById('custom-shape-back-color')?.value || '#FFFFFF';
            
            formData.append('fill_color', fillColor);
            formData.append('back_color', backColor);
        }
        
        // Envoi de la requête AJAX
        fetch('/preview', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de la génération de la prévisualisation');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Mise à jour de l'aperçu
                qrPreview.src = data.preview;
            }
        })
        .catch(error => {
            console.error('Erreur de prévisualisation:', error);
            // Ne pas afficher d'erreur pour ne pas perturber l'expérience utilisateur
        });
    }

    // ------- Exportation de QR code -------

    /**
     * Exporte le QR code dans le format spécifié
     * @param {string} format - Format d'exportation (png, svg, pdf, eps, etc.)
     */
    function exportQRCode(format) {
        // Vérifier qu'un QR code a été généré
        if (!currentQRPath) {
            showError('Veuillez d\'abord générer un QR code');
            return;
        }
        
        // Afficher un indicateur de chargement
        showLoading(true);
        
        // Récupérer les options d'exportation
        const formData = new FormData();
        formData.append('qr_path', currentQRPath);
        formData.append('export_format', format);
        
        // Options spécifiques au format
        if (format === 'png') {
            // Options pour PNG
            const dpi = document.getElementById('png-dpi')?.value || 300;
            const quality = document.getElementById('png-quality')?.value || 95;
            
            formData.append('dpi', dpi);
            formData.append('quality', quality);
            
            // Dimensions
            if (document.getElementById('png-width') && document.getElementById('png-height')) {
                const width = document.getElementById('png-width').value;
                const height = document.getElementById('png-height').value;
                
                formData.append('size_width', width);
                formData.append('size_height', height);
            }
        }
        else if (format === 'svg') {
            // Options pour SVG
            const scale = document.getElementById('svg-scale')?.value || 1;
            formData.append('scale', scale);
            
            // Dimensions
            if (document.getElementById('svg-width') && document.getElementById('svg-height')) {
                const width = document.getElementById('svg-width').value;
                const height = document.getElementById('svg-height').value;
                
                formData.append('size_width', width);
                formData.append('size_height', height);
            }
        }
        else if (format === 'pdf') {
            // Options pour PDF
            const title = document.getElementById('pdf-title')?.value || 'QR Code';
            const author = document.getElementById('pdf-author')?.value || 'QR Code Generator';
            
            formData.append('title', title);
            formData.append('author', author);
            
            // Dimensions
            if (document.getElementById('pdf-width') && document.getElementById('pdf-height')) {
                const width = document.getElementById('pdf-width').value;
                const height = document.getElementById('pdf-height').value;
                
                formData.append('size_width', width);
                formData.append('size_height', height);
            }
            
            // Position
            if (document.getElementById('pdf-x') && document.getElementById('pdf-y')) {
                const x = document.getElementById('pdf-x').value;
                const y = document.getElementById('pdf-y').value;
                
                formData.append('position_x', x);
                formData.append('position_y', y);
            }
        }
        else if (format === 'eps') {
            // Options pour EPS
            const dpi = document.getElementById('eps-dpi')?.value || 300;
            formData.append('dpi', dpi);
        }
        
        // Envoi de la requête AJAX
        fetch('/export', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de l\'exportation du QR code');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Téléchargement du fichier exporté
                window.location.href = data.download_url;
                
                // Afficher un message de succès
                showSuccess(`QR code exporté avec succès en format ${format.toUpperCase()}`);
            } else {
                showError(data.error || 'Erreur lors de l\'exportation du QR code');
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            showError('Erreur lors de l\'exportation du QR code');
        })
        .finally(() => {
            showLoading(false);
        });
    }

    // ------- Utilitaires -------

    /**
     * Active ou désactive les boutons d'exportation
     * @param {boolean} enable - Activer (true) ou désactiver (false) les boutons
     */
    function enableExportButtons(enable = true) {
        exportButtons.forEach(button => {
            button.disabled = !enable;
            if (enable) {
                button.classList.remove('disabled');
            } else {
                button.classList.add('disabled');
            }
        });
    }

    /**
     * Affiche ou masque l'indicateur de chargement
     * @param {boolean} show - Afficher (true) ou masquer (false) l'indicateur
     */
    function showLoading(show) {
        const loadingIndicator = document.getElementById('loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.style.display = show ? 'flex' : 'none';
        }
    }

    /**
     * Affiche un message d'erreur
     * @param {string} message - Message d'erreur à afficher
     */
    function showError(message) {
        const errorContainer = document.getElementById('error-container');
        if (errorContainer) {
            errorContainer.textContent = message;
            errorContainer.style.display = 'block';
            
            // Masquer après 5 secondes
            setTimeout(() => {
                errorContainer.style.display = 'none';
            }, 5000);
        }
    }

    /**
     * Affiche un message de succès
     * @param {string} message - Message de succès à afficher
     */
    function showSuccess(message) {
        const successContainer = document.getElementById('success-container');
        if (successContainer) {
            successContainer.textContent = message;
            successContainer.style.display = 'block';
            
            // Masquer après 3 secondes
            setTimeout(() => {
                successContainer.style.display = 'none';
            }, 3000);
        }
    }

    /**
     * Fonction debounce pour éviter trop de requêtes lors des modifications rapides
     */
    function debouncePreview() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(generatePreview, DEBOUNCE_DELAY);
    }

    // --------- Fonctions pour l'affichage dynamique des options ---------

    /**
     * Met à jour les options affichées en fonction du masque de couleur sélectionné
     */
    document.addEventListener('change', function(event) {
        if (event.target.id === 'color-mask') {
            const colorMask = event.target.value;
            
            // Masquer tous les conteneurs d'options
            document.querySelectorAll('.color-mask-options').forEach(container => {
                container.style.display = 'none';
            });
            
            // Afficher le conteneur correspondant au masque sélectionné
            const selectedContainer = document.getElementById(`${colorMask}-options`);
            if (selectedContainer) {
                selectedContainer.style.display = 'block';
            }
            
            // Générer une prévisualisation avec le nouveau masque
            debouncePreview();
        }
    });

    /**
     * Met à jour l'affichage en fonction de la disposition des icônes sélectionnée
     */
    document.addEventListener('change', function(event) {
        if (event.target.id === 'social-layout') {
            // Mettre à jour la classe CSS pour l'affichage des icônes
            const layout = event.target.value;
            
            const socialIconsPreview = document.getElementById('social-icons-preview');
            if (socialIconsPreview) {
                // Supprimer toutes les classes de disposition
                socialIconsPreview.classList.remove('layout-circle', 'layout-line', 'layout-grid');
                
                // Ajouter la classe de la disposition sélectionnée
                socialIconsPreview.classList.add(`layout-${layout}`);
            }
            
            // Générer une prévisualisation avec la nouvelle disposition
            debouncePreview();
        }
    });

    // --------- Initialisation de l'application ---------
    init();
});
