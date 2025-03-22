/**
 * Script pour la page d'historique des QR codes
 * Gère les interactions utilisateur et les fonctionnalités d'exportation
 */

document.addEventListener('DOMContentLoaded', function() {
    // Éléments DOM
    const searchInput = document.getElementById('search-input');
    const historyItems = document.querySelectorAll('.history-item');
    const exportButtons = document.querySelectorAll('.export-btn');
    const formatButtons = document.querySelectorAll('.format-btn');
    const reuseButtons = document.querySelectorAll('.reuse-btn');
    
    // Recherche dans l'historique
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            historyItems.forEach(item => {
                const metadata = item.querySelector('.qr-metadata').textContent.toLowerCase();
                
                if (metadata.includes(searchTerm)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
    
    // Toggle des options d'exportation
    exportButtons.forEach(button => {
        button.addEventListener('click', function() {
            const historyItem = this.closest('.history-item');
            const exportContainer = historyItem.querySelector('.export-options-container');
            
            // Fermer tous les conteneurs d'exportation
            document.querySelectorAll('.export-options-container').forEach(container => {
                if (container !== exportContainer) {
                    container.style.display = 'none';
                }
            });
            
            // Toggle du conteneur actuel
            if (exportContainer.style.display === 'none') {
                exportContainer.style.display = 'block';
            } else {
                exportContainer.style.display = 'none';
            }
        });
    });
    
    // Exportation vers un format spécifique
    formatButtons.forEach(button => {
        button.addEventListener('click', function() {
            const format = this.getAttribute('data-format');
            const qrPath = this.getAttribute('data-qr-path');
            
            if (!qrPath) {
                showError('Chemin du QR code manquant');
                return;
            }
            
            // Afficher l'indicateur de chargement
            showLoading(true);
            
            // Préparation des données d'exportation
            const formData = new FormData();
            formData.append('qr_path', qrPath);
            formData.append('export_format', format);
            
            // Options par défaut selon le format
            switch (format) {
                case 'png':
                    formData.append('dpi', '300');
                    formData.append('quality', '95');
                    break;
                case 'svg':
                    formData.append('scale', '1');
                    break;
                case 'pdf':
                    formData.append('title', 'QR Code');
                    formData.append('author', 'Anecoop-France');
                    formData.append('size_width', '50');
                    formData.append('size_height', '50');
                    break;
                case 'eps':
                    formData.append('dpi', '300');
                    break;
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
        });
    });
    
    // Réutilisation d'un QR code
    reuseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const qrData = this.getAttribute('data-qr-data');
            
            if (!qrData) {
                showError('Données du QR code manquantes');
                return;
            }
            
            // Redirection vers la page générateur avec les données pré-remplies
            window.location.href = `/?data=${encodeURIComponent(qrData)}`;
        });
    });
    
    // Fonctions utilitaires
    
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
});
