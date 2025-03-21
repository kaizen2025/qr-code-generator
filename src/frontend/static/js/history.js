// history.js - Script spécifique pour la page d'historique des QR codes

$(document).ready(function() {
    // Gestion de la recherche dans l'historique
    setupSearchFunctionality();
    
    // Gestion des boutons d'exportation
    setupExportButtons();
    
    // Gestion des boutons de réutilisation
    setupReuseButtons();
});

// Configuration de la fonctionnalité de recherche
function setupSearchFunctionality() {
    $('#searchInput').on('keyup', function() {
        const searchTerm = $(this).val().toLowerCase();
        
        // Filtrage des éléments de l'historique
        $('.qr-history-item').each(function() {
            const data = $(this).data('data').toLowerCase();
            const filename = $(this).find('.card-title').text().toLowerCase();
            
            if (data.includes(searchTerm) || filename.includes(searchTerm)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
    
    $('#searchButton').on('click', function() {
        const searchTerm = $('#searchInput').val().toLowerCase();
        
        // Filtrage des éléments de l'historique
        $('.qr-history-item').each(function() {
            const data = $(this).data('data').toLowerCase();
            const filename = $(this).find('.card-title').text().toLowerCase();
            
            if (data.includes(searchTerm) || filename.includes(searchTerm)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
}

// Configuration des boutons d'exportation
function setupExportButtons() {
    $('.export-btn').on('click', function() {
        const qrPath = $(this).data('qr-path');
        
        // Mise à jour du champ caché dans le modal
        $('#modalQrPathInput').val(qrPath);
        
        // Affichage du modal d'exportation
        $('#exportModal').modal('show');
    });
}

// Configuration des boutons de réutilisation
function setupReuseButtons() {
    $('.reuse-btn').on('click', function() {
        const qrData = $(this).data('qr-data');
        
        // Stockage des données dans le localStorage
        localStorage.setItem('reuseQrData', qrData);
        
        // Redirection vers la page d'accueil
        window.location.href = '/';
    });
    
    // Vérification au chargement de la page d'accueil
    if (window.location.pathname === '/') {
        const reuseData = localStorage.getItem('reuseQrData');
        
        if (reuseData) {
            // Remplissage des champs de données dans tous les onglets
            $('#basicData, #customData, #logoData, #styleData').val(reuseData);
            
            // Suppression des données du localStorage
            localStorage.removeItem('reuseQrData');
        }
    }
}
