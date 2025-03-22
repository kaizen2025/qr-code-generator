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
});

// JavaScript à ajouter au fichier script.js pour gérer les sélections de forme

// Configuration pour la personnalisation avancée des QR codes
$(document).ready(function() {
    // Gestion des sélections de forme des modules
    $('input[name="module_shape"]').on('change', function() {
        const selectedShape = $(this).val();
        console.log('Forme de module sélectionnée:', selectedShape);
        
        // Mettre à jour l'aperçu si possible
        updateQRPreview();
    });
    
    // Gestion des sélections de forme de contour des marqueurs
    $('input[name="frame_shape"]').on('change', function() {
        const selectedShape = $(this).val();
        console.log('Forme de contour sélectionnée:', selectedShape);
        
        // Mettre à jour l'aperçu si possible
        updateQRPreview();
    });
    
    // Gestion des sélections de forme du centre des marqueurs
    $('input[name="eye_shape"]').on('change', function() {
        const selectedShape = $(this).val();
        console.log('Forme d\'œil sélectionnée:', selectedShape);
        
        // Mettre à jour l'aperçu si possible
        updateQRPreview();
    });
    
    // Fonction pour mettre à jour l'aperçu du QR code
    function updateQRPreview() {
        const data = $('#styleData').val();
        if (!data) return; // Ne pas générer si aucune donnée
        
        const moduleShape = $('input[name="module_shape"]:checked').val();
        const frameShape = $('input[name="frame_shape"]:checked').val();
        const eyeShape = $('input[name="eye_shape"]:checked').val();
        
        // Afficher un indicateur de chargement
        $('#qrPreview').html(`
            <div class="loading-container">
                <div class="loading-spinner"></div>
                <p class="loading-text">Génération du QR code en cours...</p>
            </div>
        `);
        
        // Préparation des données pour l'envoi
        const formData = new FormData();
        formData.append('data', data);
        formData.append('generation_type', 'custom_shape');
        formData.append('module_shape', moduleShape);
        formData.append('frame_shape', frameShape);
        formData.append('eye_shape', eyeShape);
        formData.append('error_correction', $('#styleErrorCorrection').val());
        formData.append('box_size', $('#styleBoxSize').val());
        
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
    }
    
    // Génération automatique lorsque le contenu change
    $('#styleData').on('input', _.debounce(function() {
        if ($(this).val().trim().length > 0) {
            updateQRPreview();
        }
    }, 500));
});
// Mise à jour des valeurs affichées pour les sliders
function updateSliderValues() {
    // Taille des modules
    $('#basicBoxSize').on('input', function() {
        $('#basicBoxSizeValue').text($(this).val());
    });
    
    $('#customBoxSize').on('input', function() {
        $('#customBoxSizeValue').text($(this).val());
    });
    
    $('#logoBoxSize').on('input', function() {
        $('#logoBoxSizeValue').text($(this).val());
    });
    
    $('#styleBoxSize').on('input', function() {
        $('#styleBoxSizeValue').text($(this).val());
    });
    
    // Bordure
    $('#basicBorder').on('input', function() {
        $('#basicBorderValue').text($(this).val());
    });
    
    $('#customBorder').on('input', function() {
        $('#customBorderValue').text($(this).val());
    });
    
    // Taille du logo
    $('#logoSize').on('input', function() {
        $('#logoSizeValue').text(Math.round($(this).val() * 100));
    });
    
    // Options d'exportation PNG
    $('#pngQuality').on('input', function() {
        $('#pngQualityValue').text($(this).val());
    });
    
    // Options d'exportation SVG
    $('#svgScale').on('input', function() {
        $('#svgScaleValue').text($(this).val());
    });
    
    // Options d'exportation dans le modal
    $('#modalPngQuality').on('input', function() {
        $('#modalPngQualityValue').text($(this).val());
    });
    
    $('#modalSvgScale').on('input', function() {
        $('#modalSvgScaleValue').text($(this).val());
    });
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
                    // Téléchargement du fichier exporté
                    if (response.download_url) {
                        window.location.href = response.download_url;
                    } else if (response.download_urls) {
                        // Si plusieurs formats ont été exportés
                        for (const format in response.download_urls) {
                            window.open(response.download_urls[format], '_blank');
                        }
                    }
                } else {
                    showError(response.error || 'Une erreur est survenue lors de l\'exportation du QR code.');
                }
            },
            error: function(xhr) {
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
                    // Fermeture du modal
                    $('#exportModal').modal('hide');
                    
                    // Téléchargement du fichier exporté
                    if (response.download_url) {
                        window.location.href = response.download_url;
                    } else if (response.download_urls) {
                        // Si plusieurs formats ont été exportés
                        for (const format in response.download_urls) {
                            window.open(response.download_urls[format], '_blank');
                        }
                    }
                } else {
                    showError(response.error || 'Une erreur est survenue lors de l\'exportation du QR code.');
                }
            },
            error: function(xhr) {
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
        if (format === 'png') {
            $('#pngOptions').show();
        } else if (format === 'svg') {
            $('#svgOptions').show();
        } else if (format === 'pdf') {
            $('#pdfOptions').show();
        }
    });
    
    // Gestion des options d'exportation dans le modal
    $('input[name="export_format"]').on('change', function() {
        const format = $(this).val();
        
        // Masquage de toutes les options
        $('.format-options').hide();
        
        // Affichage des options correspondant au format sélectionné
        if (format === 'png') {
            $('#modalPngOptions').show();
        } else if (format === 'svg') {
            $('#modalSvgOptions').show();
        } else if (format === 'pdf') {
            $('#modalPdfOptions').show();
        }
    });
}

// Affichage d'un message d'erreur
function showError(message) {
    $('#errorMessage').text(message);
    $('#errorModal').modal('show');
}
