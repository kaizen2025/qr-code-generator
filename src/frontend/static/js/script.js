// script.js - Script principal pour le générateur de QR codes

$(document).ready(function() {
    // Mise à jour des valeurs affichées pour les sliders
    updateSliderValues();
    
    // Gestion des formulaires de génération de QR code
    setupQRFormHandlers();
    
    // Gestion du formulaire d'exportation
    setupExportFormHandler();
    
    // Gestion des onglets et affichage des options d'exportation
    setupTabsAndExportOptions();
    
    // Configuration de la prévisualisation en temps réel
    setupLivePreview();
    
    // Configuration des options de personnalisation
    setupCustomizationOptions();
    
    // Configuration des réseaux sociaux
    setupSocialOptions();
    
    // Gestion des messages d'erreur et de succès
    setupNotifications();
});

// Mise à jour des valeurs affichées pour les sliders
function updateSliderValues() {
    // Taille des modules
    $('.box-size-slider').on('input', function() {
        const sliderId = $(this).attr('id');
        $(`#${sliderId}Value`).text($(this).val());
    });
    
    // Bordure
    $('.border-slider').on('input', function() {
        const sliderId = $(this).attr('id');
        $(`#${sliderId}Value`).text($(this).val());
    });
    
    // Taille du logo
    $('#logoSize').on('input', function() {
        $('#logoSizeValue').text(Math.round($(this).val() * 100));
    });
    
    // Options d'exportation
    $('.quality-slider').on('input', function() {
        const sliderId = $(this).attr('id');
        $(`#${sliderId}Value`).text($(this).val());
    });
    
    $('.scale-slider').on('input', function() {
        const sliderId = $(this).attr('id');
        $(`#${sliderId}Value`).text($(this).val());
    });
    
    // Taille de l'icône sociale
    $('#socialIconSize').on('input', function() {
        $('#socialIconSizeValue').text(Math.round($(this).val() * 100));
    });
    
    // Déclencher l'événement input pour initialiser les valeurs
    $('.range-slider').trigger('input');
}

// Configuration des gestionnaires de formulaires pour la génération de QR codes
function setupQRFormHandlers() {
    $('.qr-form').on('submit', function(e) {
        e.preventDefault();
        
        // Affichage d'un indicateur de chargement
        $('#qrPreview').html(`
            <div class="loading-container">
                <div class="loading-spinner"></div>
                <p class="loading-text">Génération du QR code en cours...</p>
            </div>
        `);
        
        // Récupération du formulaire
        const form = $(this);
        const formData = new FormData(form[0]);
        
        // Envoi de la requête AJAX
        $.ajax({
            url: '/generate',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    // Affichage du QR code généré
                    $('#qrPreview').html(`
                        <img src="${response.download_url}" class="qr-preview-image fade-in" alt="QR Code">
                    `);
                    
                    // Affichage des options d'exportation
                    $('#exportCard').show();
                    $('#qrPathInput').val(response.qr_path);
                    
                    // Affichage d'un message de succès
                    showNotification('QR code généré avec succès !', 'success');
                } else {
                    showError(response.error || 'Une erreur est survenue lors de la génération du QR code.');
                }
            },
            error: function(xhr) {
                let errorMessage = 'Une erreur est survenue lors de la génération du QR code.';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                }
                showError(errorMessage);
            }
        });
    });
}

// Configuration du gestionnaire de formulaire pour l'exportation
function setupExportFormHandler() {
    $('#exportForm').on('submit', function(e) {
        e.preventDefault();
        
        // Affichage d'un indicateur de chargement
        $('#exportStatus').html(`
            <div class="d-flex align-items-center">
                <div class="spinner-border spinner-border-sm me-2" role="status">
                    <span class="visually-hidden">Chargement...</span>
                </div>
                <span>Exportation en cours...</span>
            </div>
        `);
        
        // Récupération du formulaire
        const form = $(this);
        const formData = new FormData(form[0]);
        
        // Envoi de la requête AJAX
        $.ajax({
            url: '/export',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    // Effacement de l'indicateur de chargement
                    $('#exportStatus').html('');
                    
                    // Téléchargement du fichier exporté
                    if (response.download_url) {
                        window.location.href = response.download_url;
                        showNotification('QR code exporté avec succès !', 'success');
                    } else if (response.download_urls) {
                        // Si plusieurs formats ont été exportés
                        for (const format in response.download_urls) {
                            window.open(response.download_urls[format], '_blank');
                        }
                        showNotification('QR code exporté dans tous les formats avec succès !', 'success');
                    }
                } else {
                    $('#exportStatus').html('');
                    showError(response.error || 'Une erreur est survenue lors de l\'exportation du QR code.');
                }
            },
            error: function(xhr) {
                $('#exportStatus').html('');
                let errorMessage = 'Une erreur est survenue lors de l\'exportation du QR code.';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                }
                showError(errorMessage);
            }
        });
    });
    
    // Gestionnaire pour le bouton d'exportation dans le modal
    $('#modalExportButton').on('click', function() {
        // Affichage d'un indicateur de chargement
        $('#modalExportStatus').html(`
            <div class="d-flex align-items-center ms-3">
                <div class="spinner-border spinner-border-sm me-2" role="status">
                    <span class="visually-hidden">Chargement...</span>
                </div>
                <span>Exportation en cours...</span>
            </div>
        `);
        
        const formData = new FormData($('#modalExportForm')[0]);
        
        // Envoi de la requête AJAX
        $.ajax({
            url: '/export',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    // Effacement de l'indicateur de chargement
                    $('#modalExportStatus').html('');
                    
                    // Fermeture du modal
                    $('#exportModal').modal('hide');
                    
                    // Téléchargement du fichier exporté
                    if (response.download_url) {
                        window.location.href = response.download_url;
                        showNotification('QR code exporté avec succès !', 'success');
                    } else if (response.download_urls) {
                        // Si plusieurs formats ont été exportés
                        for (const format in response.download_urls) {
                            window.open(response.download_urls[format], '_blank');
                        }
                        showNotification('QR code exporté dans tous les formats avec succès !', 'success');
                    }
                } else {
                    $('#modalExportStatus').html('');
                    showError(response.error || 'Une erreur est survenue lors de l\'exportation du QR code.');
                }
            },
            error: function(xhr) {
                $('#modalExportStatus').html('');
                let errorMessage = 'Une erreur est survenue lors de l\'exportation du QR code.';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                }
                showError(errorMessage);
            }
        });
    });
}

// Configuration des onglets et des options d'exportation
function setupTabsAndExportOptions() {
    // Gestion des onglets
    $('#qrTabs button').on('click', function(e) {
        e.preventDefault();
        $(this).tab('show');
    });
    
    // Gestion des options d'exportation
    $('input[name="export_format"]').on('change', function() {
        const format = $(this).val();
        
        // Masquage de toutes les options
        $('.format-options').hide();
        
        // Affichage des options correspondant au format sélectionné
        $(`#${format}Options`).show();
    });
    
    // Gestion des options d'exportation dans le modal
    $('input[name="modal_export_format"]').on('change', function() {
        const format = $(this).val();
        
        // Masquage de toutes les options
        $('.modal-format-options').hide();
        
        // Affichage des options correspondant au format sélectionné
        $(`#modal${format.charAt(0).toUpperCase() + format.slice(1)}Options`).show();
    });
}

// Configuration de la prévisualisation en temps réel
function setupLivePreview() {
    // Debounce function pour limiter les requêtes
    const debounce = (func, delay) => {
        let timer;
        return function(...args) {
            clearTimeout(timer);
            timer = setTimeout(() => func.apply(this, args), delay);
        };
    };
    
    // Fonction pour mettre à jour la prévisualisation
    const updatePreview = debounce(function(form, previewType) {
        const formData = new FormData(form[0]);
        formData.append('preview_type', previewType);
        
        // Données minimales requises
        const data = formData.get('data');
        if (!data || data.trim() === '') {
            return;
        }
        
        // Affichage d'un indicateur de chargement
        $('#qrPreview').html(`
            <div class="loading-container">
                <div class="loading-spinner"></div>
                <p class="loading-text">Génération de la prévisualisation...</p>
            </div>
        `);
        
        // Envoi de la requête AJAX
        $.ajax({
            url: '/preview',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    // Affichage de la prévisualisation
                    $('#qrPreview').html(`
                        <img src="${response.preview}" class="qr-preview-image fade-in" alt="QR Code Preview">
                    `);
                } else {
                    // En cas d'erreur, on laisse la prévisualisation actuelle
                    console.error(response.error);
                }
            },
            error: function(xhr) {
                // En cas d'erreur, on ignore
                console.error('Erreur de prévisualisation:', xhr.responseText);
            }
        });
    }, 500);  // 500ms de délai
    
    // Écoute des changements dans les formulaires
    $('#basicForm').on('input change', 'input, select, textarea', function() {
        updatePreview($('#basicForm'), 'basic');
    });
    
    $('#customForm').on('input change', 'input, select, textarea', function() {
        updatePreview($('#customForm'), 'custom');
    });
    
    $('#styleForm').on('input change', 'input, select, textarea', function() {
        updatePreview($('#styleForm'), 'styled');
    });
    
    // Prévisualisation avec logo (quand un fichier est sélectionné)
    $('#logoFile').on('change', function() {
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const formData = new FormData($('#logoForm')[0]);
                formData.append('preview_type', 'logo');
                formData.append('logo_data', e.target.result);
                
                // Envoi de la requête AJAX
                $.ajax({
                    url: '/preview',
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function(response) {
                        if (response.success) {
                            // Affichage de la prévisualisation
                            $('#qrPreview').html(`
                                <img src="${response.preview}" class="qr-preview-image fade-in" alt="QR Code Preview">
                            `);
                        }
                    }
                });
            };
            reader.readAsDataURL(this.files[0]);
        }
    });
    
    // Autres entrées du formulaire logo
    $('#logoForm').on('input change', 'input:not(#logoFile), select, textarea', function() {
        if ($('#logoFile')[0].files && $('#logoFile')[0].files[0]) {
            $('#logoFile').trigger('change');
        }
    });
    
    // Prévisualisation pour l'onglet Social
    $('#socialForm').on('input change', 'input, select, textarea', function() {
        updatePreview($('#socialForm'), 'social');
    });
}

// Configuration des options de personnalisation
function setupCustomizationOptions() {
    // Changement de style prédéfini
    $('input[name="style_name"]').on('change', function() {
        const styleId = $(this).val();
        
        // Mise à jour des options en fonction du style sélectionné
        // Cette fonctionnalité pourrait être enrichie avec des options spécifiques par style
        console.log(`Style sélectionné: ${styleId}`);
        
        // Génération de la prévisualisation si des données sont présentes
        if ($('#styleData').val().trim() !== '') {
            $('#styleForm').trigger('change');
        }
    });
    
    // Gestion des sélections de forme des modules
    $('input[name="module_shape"]').on('change', function() {
        const selectedShape = $(this).val();
        console.log('Forme de module sélectionnée:', selectedShape);
        
        // Mettre à jour l'aperçu si possible
        if ($('#styleData').val().trim() !== '') {
            $('#styleForm').trigger('change');
        }
    });
    
    // Gestion des sélections de forme de contour des marqueurs
    $('input[name="frame_shape"]').on('change', function() {
        const selectedShape = $(this).val();
        console.log('Forme de contour sélectionnée:', selectedShape);
        
        // Mettre à jour l'aperçu si possible
        if ($('#styleData').val().trim() !== '') {
            $('#styleForm').trigger('change');
        }
    });
    
    // Gestion des sélections de forme du centre des marqueurs
    $('input[name="eye_shape"]').on('change', function() {
        const selectedShape = $(this).val();
        console.log('Forme d\'œil sélectionnée:', selectedShape);
        
        // Mettre à jour l'aperçu si possible
        if ($('#styleData').val().trim() !== '') {
            $('#styleForm').trigger('change');
        }
    });
}

// Configuration des options de réseaux sociaux
function setupSocialOptions() {
    // Sélection d'une plateforme sociale
    $('input[name="social_platform"]').on('change', function() {
        const platform = $(this).val();
        
        // Mettre à jour l'aperçu si des données sont présentes
        if ($('#socialData').val().trim() !== '') {
            $('#socialForm').trigger('change');
        }
        
        // Mettre à jour la couleur de marque si l'option est cochée
        if ($('#useBrandedColors').is(':checked')) {
            // Cette partie nécessiterait de connaître les couleurs des marques
            // Pour une démonstration, on peut utiliser des couleurs fictives
            const brandColors = {
                'facebook': '#1877F2',
                'twitter': '#1DA1F2',
                'instagram': '#E4405F',
                'linkedin': '#0A66C2',
                'youtube': '#FF0000',
                'tiktok': '#000000',
                'whatsapp': '#25D366',
                'website': '#333333'
            };
            
            if (platform in brandColors) {
                $('#socialFillColor').val(brandColors[platform]);
            }
        }
    });
    
    // Option pour utiliser les couleurs de marque
    $('#useBrandedColors').on('change', function() {
        if ($(this).is(':checked')) {
            // Récupérer la plateforme sélectionnée
            const platform = $('input[name="social_platform"]:checked').val();
            
            // Simuler un changement de plateforme pour mettre à jour la couleur
            $(`input[name="social_platform"][value="${platform}"]`).trigger('change');
            
            // Désactiver la sélection manuelle de couleur
            $('#socialFillColor').prop('disabled', true);
        } else {
            // Réactiver la sélection manuelle de couleur
            $('#socialFillColor').prop('disabled', false);
        }
    });
    
    // Sélection du layout pour les multi-icônes
    $('input[name="layout"]').on('change', function() {
        // Mettre à jour l'aperçu si des données sont présentes
        if ($('#multiSocialData').val().trim() !== '') {
            $('#multiSocialForm').trigger('change');
        }
    });
}

// Gestion des notifications
function setupNotifications() {
    // Créer un conteneur pour les notifications s'il n'existe pas
    if ($('#notificationsContainer').length === 0) {
        $('body').append('<div id="notificationsContainer" class="position-fixed bottom-0 end-0 p-3" style="z-index: 5"></div>');
    }
}

// Affichage d'une notification
function showNotification(message, type = 'info') {
    const id = `notification-${Date.now()}`;
    const bgClass = type === 'success' ? 'bg-success' : type === 'warning' ? 'bg-warning' : type === 'danger' ? 'bg-danger' : 'bg-info';
    
    const notification = `
        <div id="${id}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header ${bgClass} text-white">
                <strong class="me-auto">${type === 'success' ? 'Succès' : type === 'warning' ? 'Attention' : type === 'danger' ? 'Erreur' : 'Information'}</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    $('#notificationsContainer').append(notification);
    
    const toast = new bootstrap.Toast(document.getElementById(id), {
        delay: 5000
    });
    toast.show();
}

// Affichage d'un message d'erreur
function showError(message) {
    showNotification(message, 'danger');
}
