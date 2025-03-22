// script.js - Version améliorée

// Attendre le chargement complet du DOM
document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des composants
    initTabs();
    initRangeSliders();
    initColorPickers();
    initStyleOptions();
    initSocialOptions();
    initShapeOptions();
    initExportOptions();
    initLivePreview();
    initQRFormHandlers();
    initExportHandlers();
    initUploadHandlers();
    initNotifications();
    initUIEnhancements();
    
    // Vérification de l'état du serveur
    checkServerStatus();
});

// Initialisation des onglets
function initTabs() {
    const tabButtons = document.querySelectorAll('.qr-tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // Afficher par défaut le premier onglet
    if (tabContents.length > 0) {
        tabContents[0].classList.add('active');
    }
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.getAttribute('data-target');
            
            // Désactiver tous les onglets
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Activer l'onglet sélectionné
            button.classList.add('active');
            document.getElementById(targetId).classList.add('active');
        });
    });
}

// Initialisation des sliders avec affichage des valeurs
function initRangeSliders() {
    const rangeSliders = document.querySelectorAll('.form-range');
    
    rangeSliders.forEach(slider => {
        const valueDisplay = document.getElementById(`${slider.id}Value`);
        if (valueDisplay) {
            // Affichage initial
            valueDisplay.textContent = slider.value;
            
            // Mise à jour en temps réel
            slider.addEventListener('input', () => {
                valueDisplay.textContent = slider.value;
                
                // Déclencher l'événement pour la prévisualisation en direct
                slider.dispatchEvent(new Event('change', { bubbles: true }));
            });
        }
    });
    
    // Gestion spéciale pour les sliders de pourcentage (ex: taille du logo)
    const percentageSliders = document.querySelectorAll('.percentage-slider');
    percentageSliders.forEach(slider => {
        const valueDisplay = document.getElementById(`${slider.id}Value`);
        if (valueDisplay) {
            // Affichage initial en pourcentage
            valueDisplay.textContent = `${Math.round(slider.value * 100)}%`;
            
            // Mise à jour en temps réel
            slider.addEventListener('input', () => {
                valueDisplay.textContent = `${Math.round(slider.value * 100)}%`;
                slider.dispatchEvent(new Event('change', { bubbles: true }));
            });
        }
    });
}

// Initialisation des sélecteurs de couleur
function initColorPickers() {
    const colorInputs = document.querySelectorAll('.color-input');
    
    colorInputs.forEach(input => {
        const preview = document.querySelector(`.color-preview[data-for="${input.id}"]`);
        if (preview) {
            // Mise à jour initiale
            preview.style.backgroundColor = input.value;
            
            // Mise à jour quand la couleur change
            input.addEventListener('input', () => {
                preview.style.backgroundColor = input.value;
                input.dispatchEvent(new Event('change', { bubbles: true }));
            });
            
            // Ouvrir le sélecteur quand on clique sur la prévisualisation
            preview.addEventListener('click', () => {
                input.click();
            });
        }
    });
    
    // Options pour utiliser les couleurs de marque pour les icônes sociales
    const brandColorCheckbox = document.getElementById('useBrandedColors');
    if (brandColorCheckbox) {
        brandColorCheckbox.addEventListener('change', function() {
            const fillColorInput = document.getElementById('socialFillColor');
            if (fillColorInput) {
                fillColorInput.disabled = this.checked;
                
                // Mettre à jour la couleur si une plateforme est sélectionnée
                if (this.checked) {
                    const selectedPlatform = document.querySelector('input[name="social_platform"]:checked');
                    if (selectedPlatform) {
                        updateSocialBrandColor(selectedPlatform.value);
                    }
                }
            }
        });
    }
}

// Initialisation des options de style prédéfini
function initStyleOptions() {
    const styleOptions = document.querySelectorAll('input[name="style_name"]');
    
    styleOptions.forEach(option => {
        const container = option.closest('.style-option');
        if (container) {
            const preview = container.querySelector('.style-preview');
            
            // Marquer l'option active
            if (option.checked && preview) {
                preview.classList.add('active');
            }
            
            // Gestion du clic sur la prévisualisation
            if (preview) {
                preview.addEventListener('click', () => {
                    option.checked = true;
                    
                    // Désélectionner toutes les autres prévisualisations
                    document.querySelectorAll('.style-preview').forEach(p => {
                        p.classList.remove('active');
                    });
                    
                    // Sélectionner celle-ci
                    preview.classList.add('active');
                    
                    // Déclencher l'événement change pour la prévisualisation
                    option.dispatchEvent(new Event('change', { bubbles: true }));
                });
            }
        }
    });
}

// Initialisation des options de réseaux sociaux
function initSocialOptions() {
    const socialOptions = document.querySelectorAll('input[name="social_platform"]');
    
    socialOptions.forEach(option => {
        const container = option.closest('.social-icon-item');
        if (container) {
            const preview = container.querySelector('.social-icon-preview');
            
            // Marquer l'option active
            if (option.checked && preview) {
                preview.classList.add('active');
            }
            
            // Gestion du clic sur la prévisualisation
            if (preview) {
                preview.addEventListener('click', () => {
                    option.checked = true;
                    
                    // Désélectionner toutes les autres prévisualisations
                    document.querySelectorAll('.social-icon-preview').forEach(p => {
                        p.classList.remove('active');
                    });
                    
                    // Sélectionner celle-ci
                    preview.classList.add('active');
                    
                    // Mise à jour de la couleur de marque si l'option est cochée
                    if (document.getElementById('useBrandedColors')?.checked) {
                        updateSocialBrandColor(option.value);
                    }
                    
                    // Déclencher l'événement change pour la prévisualisation
                    option.dispatchEvent(new Event('change', { bubbles: true }));
                });
            }
        }
    });
    
    // Options de mise en page pour les réseaux sociaux multiples
    const layoutOptions = document.querySelectorAll('input[name="layout"]');
    layoutOptions.forEach(option => {
        option.addEventListener('change', () => {
            // Déclencher la prévisualisation du QR code
            const form = option.closest('form');
            if (form) {
                updateLivePreview(form);
            }
        });
    });
    
    // Sélection multiple de réseaux sociaux
    const multiSocialCheckboxes = document.querySelectorAll('input[name="social_platforms[]"]');
    multiSocialCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            // Déclencher la prévisualisation du QR code
            const form = checkbox.closest('form');
            if (form) {
                updateLivePreview(form);
            }
        });
    });
}

// Mise à jour de la couleur de marque pour un réseau social
function updateSocialBrandColor(platform) {
    // Couleurs de marque des principales plateformes
    const brandColors = {
        'facebook': '#1877F2',
        'twitter': '#1DA1F2',
        'instagram': '#E4405F',
        'linkedin': '#0A66C2',
        'youtube': '#FF0000',
        'tiktok': '#000000',
        'snapchat': '#FFFC00',
        'pinterest': '#E60023',
        'whatsapp': '#25D366',
        'telegram': '#26A5E4',
        'reddit': '#FF4500',
        'github': '#181717',
        'discord': '#5865F2',
        'twitch': '#9146FF',
        'email': '#EA4335',
        'website': '#4285F4'
    };
    
    const fillColorInput = document.getElementById('socialFillColor');
    if (fillColorInput && platform in brandColors) {
        fillColorInput.value = brandColors[platform];
        
        // Mettre à jour la prévisualisation de couleur
        const preview = document.querySelector(`.color-preview[data-for="socialFillColor"]`);
        if (preview) {
            preview.style.backgroundColor = brandColors[platform];
        }
    }
}

// Initialisation des options de formes (modules, yeux, cadres)
function initShapeOptions() {
    // Formes des modules
    initShapeSelectors('module_shape');
    
    // Formes des yeux
    initShapeSelectors('eye_shape');
    
    // Formes des cadres
    initShapeSelectors('frame_shape');
}

// Fonction générique pour initialiser les sélecteurs de forme
function initShapeSelectors(inputName) {
    const shapeOptions = document.querySelectorAll(`input[name="${inputName}"]`);
    
    shapeOptions.forEach(option => {
        const container = option.closest('.shape-item');
        if (container) {
            const preview = container.querySelector('.shape-preview');
            
            // Marquer l'option active
            if (option.checked && preview) {
                preview.classList.add('active');
            }
            
            // Gestion du clic sur la prévisualisation
            if (preview) {
                preview.addEventListener('click', () => {
                    option.checked = true;
                    
                    // Désélectionner toutes les autres prévisualisations du même groupe
                    document.querySelectorAll(`input[name="${inputName}"]`).forEach(input => {
                        const otherPreview = input.closest('.shape-item')?.querySelector('.shape-preview');
                        if (otherPreview) {
                            otherPreview.classList.remove('active');
                        }
                    });
                    
                    // Sélectionner celle-ci
                    preview.classList.add('active');
                    
                    // Déclencher l'événement change pour la prévisualisation
                    option.dispatchEvent(new Event('change', { bubbles: true }));
                });
            }
        }
    });
}

// Initialisation des options d'exportation
function initExportOptions() {
    const formatButtons = document.querySelectorAll('input[name="export_format"]');
    
    formatButtons.forEach(button => {
        button.addEventListener('change', () => {
            const format = button.value;
            
            // Masquer toutes les options spécifiques aux formats
            document.querySelectorAll('.format-options').forEach(element => {
                element.style.display = 'none';
            });
            
            // Afficher les options pour le format sélectionné
            const options = document.getElementById(`${format}Options`);
            if (options) {
                options.style.display = 'block';
            }
        });
    });
    
    // Afficher les options du format sélectionné par défaut
    const defaultFormat = document.querySelector('input[name="export_format"]:checked');
    if (defaultFormat) {
        defaultFormat.dispatchEvent(new Event('change'));
    }
    
    // Même chose pour le modal d'exportation
    const modalFormatButtons = document.querySelectorAll('input[name="modal_export_format"]');
    
    modalFormatButtons.forEach(button => {
        button.addEventListener('change', () => {
            const format = button.value;
            
            // Masquer toutes les options spécifiques aux formats
            document.querySelectorAll('.modal-format-options').forEach(element => {
                element.style.display = 'none';
            });
            
            // Afficher les options pour le format sélectionné
            const options = document.getElementById(`modal${format.charAt(0).toUpperCase() + format.slice(1)}Options`);
            if (options) {
                options.style.display = 'block';
            }
        });
    });
    
    // Afficher les options du format sélectionné par défaut dans le modal
    const defaultModalFormat = document.querySelector('input[name="modal_export_format"]:checked');
    if (defaultModalFormat) {
        defaultModalFormat.dispatchEvent(new Event('change'));
    }
}

// Initialisation de la prévisualisation en temps réel
function initLivePreview() {
    // Liste des onglets et leurs formulaires
    const tabForms = {
        'basicTab': 'basicForm',
        'customTab': 'customForm',
        'logoTab': 'logoForm',
        'styleTab': 'styleForm',
        'socialTab': 'socialForm',
        'multiSocialTab': 'multiSocialForm'
    };
    
    // Surveiller les changements dans chaque formulaire
    for (const [tabId, formId] of Object.entries(tabForms)) {
        const form = document.getElementById(formId);
        if (form) {
            // Surveillance des changements dans les champs du formulaire
            const formElements = form.querySelectorAll('input, select, textarea');
            formElements.forEach(element => {
                if (element.type === 'file') {
                    // Les fichiers sont traités séparément
                    return;
                }
                
                element.addEventListener('change', () => {
                    updateLivePreview(form);
                });
                
                // Pour les champs de texte, surveiller également les frappes
                if (element.tagName === 'TEXTAREA' || (element.tagName === 'INPUT' && 
                    (element.type === 'text' || element.type === 'url' || element.type === 'tel' || element.type === 'email'))) {
                    element.addEventListener('input', debounce(() => {
                        updateLivePreview(form);
                    }, 500)); // Délai de 500ms pour ne pas surcharger le serveur
                }
            });
        }
    }
}

// Fonction de debounce pour limiter les appels fréquents
function debounce(func, delay) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

// Mise à jour de la prévisualisation en temps réel
function updateLivePreview(form) {
    // Vérification des données minimales requises
    const dataInput = form.querySelector('[name="data"]');
    if (!dataInput || dataInput.value.trim() === '') {
        return;
    }
    
    // Détermination du type de prévisualisation
    let previewType;
    
    if (form.id === 'basicForm') {
        previewType = 'basic';
    } else if (form.id === 'customForm') {
        previewType = 'custom';
    } else if (form.id === 'styleForm') {
        previewType = 'styled';
    } else if (form.id === 'logoForm') {
        // Le logo nécessite un traitement spécial
        return handleLogoPreview(form);
    } else if (form.id === 'socialForm') {
        previewType = 'social';
    } else if (form.id === 'multiSocialForm') {
        previewType = 'multi_social';
    }
    
    // Préparation des données du formulaire
    const formData = new FormData(form);
    formData.append('preview_type', previewType);
    
    // Affichage d'un indicateur de chargement
    const previewContainer = document.getElementById('qrPreview');
    if (previewContainer) {
        previewContainer.innerHTML = `
            <div class="loading-container">
                <div class="loading-spinner"></div>
                <p class="loading-text">Génération de la prévisualisation...</p>
            </div>
        `;
    }
    
    // Envoi de la requête AJAX
    fetch('/preview', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success && previewContainer) {
            // Affichage de la prévisualisation
            previewContainer.innerHTML = `
                <img src="${data.preview}" class="qr-preview-image fade-in" alt="QR Code Preview">
            `;
        } else {
            console.error('Erreur de prévisualisation:', data.error);
        }
    })
    .catch(error => {
        console.error('Erreur lors de la prévisualisation:', error);
        // En cas d'erreur, ne pas modifier la prévisualisation actuelle
    });
}

// Gestion spéciale pour la prévisualisation avec logo
function handleLogoPreview(form) {
    const logoFile = form.querySelector('#logoFile');
    if (!logoFile || !logoFile.files || logoFile.files.length === 0) {
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const formData = new FormData(form);
        formData.append('preview_type', 'logo');
        formData.append('logo_data', e.target.result);
        
        // Affichage d'un indicateur de chargement
        const previewContainer = document.getElementById('qrPreview');
        if (previewContainer) {
            previewContainer.innerHTML = `
                <div class="loading-container">
                    <div class="loading-spinner"></div>
                    <p class="loading-text">Génération de la prévisualisation...</p>
                </div>
            `;
        }
        
        // Envoi de la requête AJAX
        fetch('/preview', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success && previewContainer) {
                // Affichage de la prévisualisation
                previewContainer.innerHTML = `
                    <img src="${data.preview}" class="qr-preview-image fade-in" alt="QR Code Preview">
                `;
            } else {
                console.error('Erreur de prévisualisation:', data.error);
            }
        })
        .catch(error => {
            console.error('Erreur lors de la prévisualisation avec logo:', error);
        });
    };
    
    reader.readAsDataURL(logoFile.files[0]);
}

// Initialisation des gestionnaires de formulaires QR
function initQRFormHandlers() {
    const qrForms = document.querySelectorAll('.qr-form');
    
    qrForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Affichage d'un indicateur de chargement
            const previewContainer = document.getElementById('qrPreview');
            if (previewContainer) {
                previewContainer.innerHTML = `
                    <div class="loading-container">
                        <div class="loading-spinner"></div>
                        <p class="loading-text">Génération du QR code en cours...</p>
                    </div>
                `;
            }
            
            // Détermination du type de génération basé sur l'ID du formulaire
            let generationType;
            switch (form.id) {
                case 'basicForm':
                    generationType = 'basic';
                    break;
                case 'customForm':
                    generationType = 'custom';
                    break;
                case 'logoForm':
                    generationType = 'logo';
                    break;
                case 'styleForm':
                    generationType = 'styled';
                    break;
                case 'socialForm':
                    generationType = 'social';
                    break;
                case 'multiSocialForm':
                    generationType = 'multi_social';
                    break;
                default:
                    generationType = 'basic';
            }
            
            // Préparation des données du formulaire
            const formData = new FormData(form);
            formData.append('generation_type', generationType);
            
            // Envoi de la requête AJAX
            fetch('/generate', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || `Erreur HTTP: ${response.status}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Affichage du QR code généré
                    if (previewContainer) {
                        previewContainer.innerHTML = `
                            <img src="${data.download_url}" class="qr-preview-image fade-in" alt="QR Code">
                        `;
                    }
                    
                    // Affichage des options d'exportation
                    const exportCard = document.getElementById('exportCard');
                    if (exportCard) {
                        exportCard.style.display = 'block';
                    }
                    
                    // Mise à jour du champ caché pour l'exportation
                    const qrPathInput = document.getElementById('qrPathInput');
                    if (qrPathInput) {
                        qrPathInput.value = data.qr_path;
                    }
                    
                    // Notification de succès
                    showNotification('QR code généré avec succès !', 'success');
                } else {
                    // Notification d'erreur
                    showNotification(data.error || 'Une erreur est survenue lors de la génération du QR code.', 'error');
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
                showNotification(error.message || 'Une erreur est survenue lors de la génération du QR code.', 'error');
            });
        });
    });
}

// Initialisation des gestionnaires d'exportation
function initExportHandlers() {
    // Formulaire d'exportation principal
    const exportForm = document.getElementById('exportForm');
    if (exportForm) {
        exportForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleExport(this);
        });
    }
    
    // Formulaire d'exportation dans le modal
    const modalExportForm = document.getElementById('modalExportForm');
    if (modalExportForm) {
        const modalExportButton = document.getElementById('modalExportButton');
        if (modalExportButton) {
            modalExportButton.addEventListener('click', function() {
                handleExport(modalExportForm);
            });
        }
    }
}

// Fonction de gestion de l'exportation
function handleExport(form) {
    // Récupération du statut d'exportation
    const statusElement = form.id === 'exportForm' ? 
                          document.getElementById('exportStatus') : 
                          document.getElementById('modalExportStatus');
    
    // Affichage de l'indicateur de chargement
    if (statusElement) {
        statusElement.innerHTML = `
            <div class="d-flex align-items-center">
                <div class="loading-spinner"></div>
                <span class="ms-2">Exportation en cours...</span>
            </div>
        `;
    }
    
    // Préparation des données du formulaire
    const formData = new FormData(form);
    
    // Envoi de la requête AJAX
    fetch('/export', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || `Erreur HTTP: ${response.status}`);
            });
        }
        return response.json();
    })
    .then(data => {
        // Effacement de l'indicateur de chargement
        if (statusElement) {
            statusElement.innerHTML = '';
        }
        
        if (data.success) {
            // Fermeture du modal si c'est une exportation depuis le modal
            if (form.id === 'modalExportForm') {
                const modal = document.getElementById('exportModal');
                if (modal && typeof bootstrap !== 'undefined') {
                    const bsModal = bootstrap.Modal.getInstance(modal);
                    if (bsModal) {
                        bsModal.hide();
                    }
                }
            }
            
            // Téléchargement du fichier exporté
            if (data.download_url) {
                window.location.href = data.download_url;
                showNotification('QR code exporté avec succès !', 'success');
            } else if (data.download_urls) {
                // Si plusieurs formats ont été exportés
                for (const format in data.download_urls) {
                    window.open(data.download_urls[format], '_blank');
                }
                showNotification('QR code exporté dans tous les formats avec succès !', 'success');
            }
        } else {
            showNotification(data.error || 'Une erreur est survenue lors de l\'exportation du QR code.', 'error');
        }
    })
    .catch(error => {
        // Effacement de l'indicateur de chargement
        if (statusElement) {
            statusElement.innerHTML = '';
        }
        
        console.error('Erreur:', error);
        showNotification(error.message || 'Une erreur est survenue lors de l\'exportation du QR code.', 'error');
    });
}

// Initialisation des gestionnaires d'upload
function initUploadHandlers() {
    // Gestion du changement de fichier logo
    const logoFileInput = document.getElementById('logoFile');
    if (logoFileInput) {
        logoFileInput.addEventListener('change', function(e) {
            const fileNameDisplay = document.getElementById('selectedFileName');
            const file = this.files[0];
            
            if (file) {
                // Affichage du nom du fichier
                if (fileNameDisplay) {
                    fileNameDisplay.textContent = file.name;
                    fileNameDisplay.classList.remove('text-muted');
                    fileNameDisplay.classList.add('text-success');
                }
                
                // Prévisualisation du logo
                const logoPreview = document.getElementById('logoPreview');
                if (logoPreview) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        logoPreview.innerHTML = `
                            <img src="${e.target.result}" class="img-fluid" style="max-height: 100px;" alt="Logo Preview">
                        `;
                    };
                    reader.readAsDataURL(file);
                }
                
                // Mise à jour de la prévisualisation du QR code
                handleLogoPreview(this.closest('form'));
            } else {
                // Réinitialisation si aucun fichier n'est sélectionné
                if (fileNameDisplay) {
                    fileNameDisplay.textContent = 'Aucun fichier sélectionné';
                    fileNameDisplay.classList.remove('text-success');
                    fileNameDisplay.classList.add('text-muted');
                }
                
                if (logoPreview) {
                    logoPreview.innerHTML = '';
                }
            }
        });
    }
}

// Initialisation des notifications
function initNotifications() {
    // Création du conteneur de notifications s'il n'existe pas
    if (!document.getElementById('notificationsContainer')) {
        const container = document.createElement('div');
        container.id = 'notificationsContainer';
        container.style.position = 'fixed';
        container.style.bottom = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
}

// Affichage d'une notification
function showNotification(message, type = 'info', duration = 5000) {
    const container = document.getElementById('notificationsContainer');
    if (!container) return;
    
    // Création de l'ID unique pour la notification
    const id = `notification-${Date.now()}`;
    
    // Détermination des classes et icônes selon le type
    let typeClass, icon;
    switch (type) {
        case 'success':
            typeClass = 'notification-success';
            icon = 'fas fa-check-circle';
            break;
        case 'error':
            typeClass = 'notification-error';
            icon = 'fas fa-exclamation-circle';
            break;
        case 'warning':
            typeClass = 'notification-warning';
            icon = 'fas fa-exclamation-triangle';
            break;
        default:
            typeClass = 'notification-info';
            icon = 'fas fa-info-circle';
    }
    
    // Création de la notification
    const notification = document.createElement('div');
    notification.id = id;
    notification.className = `notification ${typeClass}`;
    notification.innerHTML = `
        <div class="notification-icon">
            <i class="${icon}"></i>
        </div>
        <div class="notification-content">
            <div class="notification-title">${type.charAt(0).toUpperCase() + type.slice(1)}</div>
            <div class="notification-message">${message}</div>
        </div>
        <button class="notification-close" aria-label="Fermer">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Ajout de la notification au conteneur
    container.appendChild(notification);
    
    // Animation d'apparition
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Configuration du bouton de fermeture
    const closeButton = notification.querySelector('.notification-close');
    if (closeButton) {
        closeButton.addEventListener('click', () => {
            closeNotification(notification);
        });
    }
    
    // Fermeture automatique après la durée spécifiée
    setTimeout(() => {
        closeNotification(notification);
    }, duration);
}

// Fermeture d'une notification
function closeNotification(notification) {
    // Animation de disparition
    notification.classList.remove('show');
    
    // Suppression après l'animation
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 300);
}

// Vérification de l'état du serveur
function checkServerStatus() {
    fetch('/api/status')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Statut du serveur:', data);
            
            // Vérification des problèmes potentiels
            const directories = data.directories || {};
            let hasIssues = false;
            
            for (const [key, info] of Object.entries(directories)) {
                if (!info.exists) {
                    console.warn(`Avertissement: Le répertoire ${key} n'existe pas.`);
                    hasIssues = true;
                }
            }
            
            if (hasIssues) {
                showNotification('Des problèmes ont été détectés avec la configuration du serveur. Certaines fonctionnalités pourraient ne pas fonctionner correctement.', 'warning');
            }
        })
        .catch(error => {
            console.error('Erreur lors de la vérification du statut du serveur:', error);
            showNotification('Impossible de vérifier l\'état du serveur. Certaines fonctionnalités pourraient ne pas fonctionner correctement.', 'error');
        });
}

// Améliorations de l'interface utilisateur
function initUIEnhancements() {
    // Ajout de la classe active aux onglets
    const currentTab = document.querySelector('.qr-tab.active');
    if (!currentTab && document.querySelector('.qr-tab')) {
        document.querySelector('.qr-tab').classList.add('active');
    }
    
    // Gestion des modals
    initModals();
    
    // Réutilisation des données QR depuis l'historique
    initQRReuse();
    
    // Amélioration des formulaires (validation, auto-focus, etc.)
    enhanceForms();
}

// Initialisation des modals
function initModals() {
    // Pour Bootstrap, mais peut être adapté pour d'autres frameworks
    document.querySelectorAll('[data-bs-toggle="modal"]').forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-bs-target') || this.getAttribute('href');
            if (targetId) {
                const modal = document.querySelector(targetId);
                if (modal && typeof bootstrap !== 'undefined') {
                    const bsModal = new bootstrap.Modal(modal);
                    bsModal.show();
                } else {
                    // Fallback si Bootstrap n'est pas disponible
                    const modal = document.querySelector(targetId);
                    if (modal) {
                        modal.classList.add('show');
                        modal.style.display = 'block';
                    }
                }
            }
        });
    });
    
    // Boutons de fermeture des modals
    document.querySelectorAll('[data-bs-dismiss="modal"]').forEach(button => {
        button.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal && typeof bootstrap !== 'undefined') {
                const bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) {
                    bsModal.hide();
                }
            } else {
                // Fallback si Bootstrap n'est pas disponible
                const modal = this.closest('.modal');
                if (modal) {
                    modal.classList.remove('show');
                    modal.style.display = 'none';
                }
            }
        });
    });
    
    // Mise à jour du champ caché dans le modal d'exportation
    document.querySelectorAll('.export-btn').forEach(button => {
        button.addEventListener('click', function() {
            const qrPath = this.getAttribute('data-qr-path');
            const modalQrPathInput = document.getElementById('modalQrPathInput');
            
            if (modalQrPathInput && qrPath) {
                modalQrPathInput.value = qrPath;
            }
        });
    });
}

// Initialisation de la réutilisation des QR codes
function initQRReuse() {
    document.querySelectorAll('.reuse-btn').forEach(button => {
        button.addEventListener('click', function() {
            const qrData = this.getAttribute('data-qr-data');
            
            if (qrData) {
                // Stockage des données pour la réutilisation
                localStorage.setItem('reuseQrData', qrData);
                
                // Redirection vers la page d'accueil
                window.location.href = '/';
            }
        });
    });
    
    // Vérification au chargement de la page d'accueil
    if (window.location.pathname === '/' || window.location.pathname === '/index.html') {
        const reuseData = localStorage.getItem('reuseQrData');
        
        if (reuseData) {
            // Remplissage des champs de données dans tous les onglets
            document.querySelectorAll('textarea[name="data"], input[name="data"]').forEach(input => {
                input.value = reuseData;
            });
            
            // Suppression des données du localStorage
            localStorage.removeItem('reuseQrData');
            
            // Lancement de la prévisualisation
            const activeTab = document.querySelector('.tab-content.active');
            if (activeTab) {
                const form = activeTab.querySelector('form');
                if (form) {
                    updateLivePreview(form);
                }
            } else if (document.querySelector('form')) {
                updateLivePreview(document.querySelector('form'));
            }
            
            // Notification
            showNotification('Données du QR code chargées avec succès.', 'info');
        }
    }
}

// Amélioration des formulaires
function enhanceForms() {
    // Auto-focus sur le premier champ des formulaires
    document.querySelectorAll('form').forEach(form => {
        const firstInput = form.querySelector('input:not([type="hidden"]), textarea, select');
        if (firstInput && !firstInput.value) {
            firstInput.focus();
        }
    });
    
    // Validation des formulaires
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                
                // Marquer tous les champs invalides
                this.querySelectorAll(':invalid').forEach(field => {
                    field.classList.add('is-invalid');
                    
                    // Ajouter un gestionnaire d'événements pour retirer la classe lorsque l'utilisateur modifie le champ
                    field.addEventListener('input', function() {
                        this.classList.remove('is-invalid');
                    }, { once: true });
                });
                
                // Notification d'erreur
                showNotification('Veuillez corriger les erreurs dans le formulaire avant de continuer.', 'warning');
            }
            
            this.classList.add('was-validated');
        });
    });
    
    // Synchronisation des champs de données entre les onglets
    const dataFields = document.querySelectorAll('textarea[name="data"], input[name="data"]');
    if (dataFields.length > 1) {
        dataFields.forEach(field => {
            field.addEventListener('input', function() {
                const value = this.value;
                dataFields.forEach(f => {
                    if (f !== this) {
                        f.value = value;
                    }
                });
            });
        });
    }
}
