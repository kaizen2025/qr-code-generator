/**
 * Advanced QR Code Generator Script
 * Enhanced version with better user interaction and previews
 */

document.addEventListener('DOMContentLoaded', function() {
    // ===== DOM Elements =====
    const qrForm = document.getElementById('qr-form');
    const qrDataInputs = document.querySelectorAll('[id^="qr-data"]');
    const qrPreview = document.getElementById('qr-preview');
    const qrPreviewContainer = document.getElementById('preview-wrapper');
    const generateBtn = document.getElementById('generate-btn');
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    const exportButtons = document.querySelectorAll('.export-button');
    const colorPickers = document.querySelectorAll('input[type="color"]');
    const rangeInputs = document.querySelectorAll('input[type="range"]');
    const logoUpload = document.getElementById('logo-upload');
    const styleOptions = document.querySelectorAll('.style-option');
    const socialPlatforms = document.querySelectorAll('.social-platform');
    const moduleShapes = document.querySelectorAll('.module-shape');
    const frameShapes = document.querySelectorAll('.frame-shape');
    const eyeShapes = document.querySelectorAll('.eye-shape');
    const downloadLink = document.getElementById('download-link');
    const exportFormatButtons = document.querySelectorAll('.export-format-button');

    // ===== State Variables =====
    let currentQRPath = null;
    let currentTab = 'basic'; // Default tab
    let debounceTimer;
    const DEBOUNCE_DELAY = 300; // Delay to avoid too many requests during rapid changes
    let previewInProgress = false;
    let lastQRData = '';
    let lastOptions = {};

    // ===== Initialization =====
    function init() {
        // Initialize tabs
        initTabs();
        
        // Initialize color pickers
        initColorPickers();
        
        // Initialize range sliders
        initRangeInputs();

        // Form submission event
        if (qrForm) {
            qrForm.addEventListener('submit', handleFormSubmit);
        }

        // Data input events (real-time preview)
        initDataInputs();

        // Initialize all option selectors
        initOptionSelectors();
        
        // Initialize logo upload
        initLogoUpload();
        
        // Initialize export buttons
        initExportButtons();
        
        // Synchronize data inputs across tabs
        syncDataInputs();
        
        // Show initial preview if data is present
        if (qrDataInputs[0] && qrDataInputs[0].value) {
            generatePreview();
        }
        
        // Initialize format selection for export
        initExportFormatSelection();
    }

    // ===== Tab Management =====
    function initTabs() {
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const tabId = button.getAttribute('data-tab');
                switchTab(tabId);
            });
        });

        // Activate default tab
        if (tabButtons.length > 0) {
            const defaultTab = tabButtons[0].getAttribute('data-tab');
            switchTab(defaultTab);
        }
    }

    function switchTab(tabId) {
        // Update active tab
        tabButtons.forEach(button => {
            if (button.getAttribute('data-tab') === tabId) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });

        // Show active tab content
        tabContents.forEach(content => {
            if (content.getAttribute('id') === `tab-${tabId}`) {
                content.classList.add('active');
                content.style.display = 'block';
            } else {
                content.classList.remove('active');
                content.style.display = 'none';
            }
        });

        // Update current tab
        currentTab = tabId;
        
        // Generate preview with active tab options
        generatePreview();
    }

    // ===== Data Input Management =====
    function initDataInputs() {
        qrDataInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                // Sync the value to all data inputs
                const newValue = e.target.value;
                syncDataValue(newValue);
                debouncePreview();
            });
        });
    }

    function syncDataInputs() {
        // Initial sync to make sure all have the same value
        if (qrDataInputs.length > 0) {
            const masterValue = qrDataInputs[0].value;
            syncDataValue(masterValue);
        }
    }

    function syncDataValue(value) {
        qrDataInputs.forEach(input => {
            input.value = value;
        });
    }

    // ===== Color Pickers =====
    function initColorPickers() {
        colorPickers.forEach(picker => {
            picker.addEventListener('input', debouncePreview);
            
            // Add color preview box next to the picker
            const colorPreview = document.createElement('div');
            colorPreview.className = 'color-preview';
            colorPreview.style.backgroundColor = picker.value;
            
            // Insert the preview after the picker
            picker.parentNode.insertBefore(colorPreview, picker.nextSibling);
            
            // Update preview on change
            picker.addEventListener('input', () => {
                colorPreview.style.backgroundColor = picker.value;
            });
        });
    }

    // ===== Range Inputs =====
    function initRangeInputs() {
        rangeInputs.forEach(input => {
            // Update the displayed value
            const valueDisplay = document.getElementById(`${input.id}-value`);
            if (valueDisplay) {
                valueDisplay.textContent = formatRangeValue(input);
                
                input.addEventListener('input', () => {
                    valueDisplay.textContent = formatRangeValue(input);
                    debouncePreview();
                });
            } else {
                input.addEventListener('input', debouncePreview);
            }
        });
    }
    
    function formatRangeValue(rangeInput) {
        // Format the value according to input type
        const value = rangeInput.value;
        
        // Add percentage sign to certain inputs
        if (rangeInput.id === 'logo-size') {
            return Math.round(value * 100) + '%';
        }
        
        // Return raw value for other inputs
        return value;
    }

    // ===== Option Selectors =====
    function initOptionSelectors() {
        // Style options
        styleOptions.forEach(option => {
            option.addEventListener('click', () => {
                // Deselect all options
                styleOptions.forEach(opt => opt.classList.remove('selected'));
                
                // Select the clicked option
                option.classList.add('selected');
                
                // Generate preview
                debouncePreview();
            });
        });

        // Social platforms
        socialPlatforms.forEach(platform => {
            platform.addEventListener('click', () => {
                if (currentTab === 'social') {
                    // Single selection for social tab
                    socialPlatforms.forEach(p => p.classList.remove('selected'));
                    platform.classList.add('selected');
                } else {
                    // Toggle selection for multi_social tab
                    platform.classList.toggle('selected');
                }
                
                // Generate preview
                debouncePreview();
            });
        });

        // Module shapes
        moduleShapes.forEach(shape => {
            shape.addEventListener('click', () => {
                // Deselect all shapes
                moduleShapes.forEach(s => s.classList.remove('selected'));
                
                // Select the clicked shape
                shape.classList.add('selected');
                
                // Generate preview
                debouncePreview();
            });
        });

        // Frame shapes
        frameShapes.forEach(shape => {
            shape.addEventListener('click', () => {
                // Deselect all shapes
                frameShapes.forEach(s => s.classList.remove('selected'));
                
                // Select the clicked shape
                shape.classList.add('selected');
                
                // Generate preview
                debouncePreview();
            });
        });

        // Eye shapes
        eyeShapes.forEach(shape => {
            shape.addEventListener('click', () => {
                // Deselect all shapes
                eyeShapes.forEach(s => s.classList.remove('selected'));
                
                // Select the clicked shape
                shape.classList.add('selected');
                
                // Generate preview
                debouncePreview();
            });
        });
        
        // Color mask selector
        const colorMaskSelect = document.getElementById('color-mask');
        if (colorMaskSelect) {
            colorMaskSelect.addEventListener('change', updateColorMaskOptions);
        }
        
        // Use platform color checkbox
        const usePlatformColorCheckbox = document.getElementById('use-platform-color');
        if (usePlatformColorCheckbox) {
            usePlatformColorCheckbox.addEventListener('change', () => {
                const socialFillColor = document.getElementById('social-fill-color');
                if (socialFillColor) {
                    if (usePlatformColorCheckbox.checked) {
                        // Get selected platform's color
                        const selectedPlatform = document.querySelector('.social-platform.selected');
                        if (selectedPlatform) {
                            const platformColor = selectedPlatform.style.getPropertyValue('--platform-color') || '#000000';
                            socialFillColor.value = platformColor;
                            const colorPreview = socialFillColor.nextElementSibling;
                            if (colorPreview && colorPreview.classList.contains('color-preview')) {
                                colorPreview.style.backgroundColor = platformColor;
                            }
                        }
                    }
                    debouncePreview();
                }
            });
        }
        
        // Layout options
        const layoutOptions = document.querySelectorAll('.layout-option');
        layoutOptions.forEach(option => {
            option.addEventListener('click', () => {
                // Deselect all options
                layoutOptions.forEach(opt => opt.classList.remove('selected'));
                
                // Select the clicked option
                option.classList.add('selected');
                
                // Update hidden input
                const layoutType = document.getElementById('layout-type');
                if (layoutType) {
                    layoutType.value = option.classList[1].replace('layout-', '');
                }
                
                // Generate preview
                debouncePreview();
            });
        });
    }
    
    function updateColorMaskOptions() {
        const colorMask = document.getElementById('color-mask').value;
        
        // Hide all color mask option containers
        document.querySelectorAll('.color-mask-options').forEach(container => {
            container.style.display = 'none';
        });
        
        // Show the appropriate container
        const selectedContainer = document.getElementById(`${colorMask}-options`);
        if (selectedContainer) {
            selectedContainer.style.display = 'block';
        }
        
        // Generate a preview with the new mask
        debouncePreview();
    }

    // ===== Logo Upload =====
    function initLogoUpload() {
        if (logoUpload) {
            logoUpload.addEventListener('change', handleLogoUpload);
            
            // Logo removal button
            const removeLogoBtn = document.getElementById('remove-logo');
            if (removeLogoBtn) {
                removeLogoBtn.addEventListener('click', () => {
                    // Reset file input
                    logoUpload.value = '';
                    
                    // Hide logo preview
                    const logoPreview = document.getElementById('logo-preview');
                    const logoPlaceholder = document.getElementById('logo-placeholder');
                    if (logoPreview) {
                        logoPreview.style.display = 'none';
                        logoPreview.src = '';
                    }
                    if (logoPlaceholder) {
                        logoPlaceholder.style.display = 'block';
                    }
                    
                    // Generate preview without logo
                    debouncePreview();
                });
            }
        }
    }

    function handleLogoUpload(event) {
        const file = event.target.files[0];
        if (file) {
            // Check file type
            if (!file.type.match('image.*')) {
                showError('The selected file is not an image');
                return;
            }
            
            // Check file size (max 2 MB)
            if (file.size > 2 * 1024 * 1024) {
                showError('The image is too large (max 2 MB)');
                return;
            }
            
            // Show logo preview
            const reader = new FileReader();
            reader.onload = function(e) {
                const logoPreview = document.getElementById('logo-preview');
                const logoPlaceholder = document.getElementById('logo-placeholder');
                if (logoPreview) {
                    logoPreview.style.display = 'block';
                    logoPreview.src = e.target.result;
                }
                if (logoPlaceholder) {
                    logoPlaceholder.style.display = 'none';
                }
                
                // Generate preview with logo
                debouncePreview();
            };
            reader.readAsDataURL(file);
        }
    }

    // ===== Export Buttons =====
    function initExportButtons() {
        exportButtons.forEach(button => {
            button.disabled = true;
            button.classList.add('disabled');
            
            button.addEventListener('click', () => {
                const format = button.getAttribute('data-format');
                exportQRCode(format);
            });
        });
    }
    
    function initExportFormatSelection() {
        exportFormatButtons.forEach(button => {
            button.addEventListener('click', () => {
                const format = button.getAttribute('data-format');
                
                // Update active button
                exportFormatButtons.forEach(btn => {
                    btn.classList.remove('active');
                });
                button.classList.add('active');
                
                // Show corresponding options
                document.querySelectorAll('.export-format-options').forEach(container => {
                    container.style.display = 'none';
                });
                
                const optionsContainer = document.getElementById(`${format}-options`);
                if (optionsContainer) {
                    optionsContainer.style.display = 'block';
                }
            });
        });
    }

    // ===== Form Submission =====
    function handleFormSubmit(event) {
        event.preventDefault();
        generateQRCode();
    }

    // ===== QR Code Generation =====
    function generateQRCode() {
        // Verify data is present
        const activeDataInput = document.querySelector(`#tab-${currentTab} [id^="qr-data"]`);
        if (!activeDataInput || !activeDataInput.value.trim()) {
            showError('Please enter content for the QR code');
            return;
        }
        
        // Show loading indicator
        showLoading(true);
        
        // Get options based on active tab
        const formData = new FormData();
        formData.append('data', activeDataInput.value.trim());
        
        // Common options
        const version = document.getElementById('qr-version')?.value || 1;
        const errorCorrection = document.getElementById('qr-error-correction')?.value || 1;
        const boxSize = document.getElementById('qr-box-size')?.value || 10;
        const border = document.getElementById('qr-border')?.value || 4;
        
        formData.append('version', version);
        formData.append('error_correction', errorCorrection);
        formData.append('box_size', boxSize);
        formData.append('border', border);
        
        // Generation type based on active tab
        formData.append('generation_type', currentTab);
        
        // Tab-specific options
        if (currentTab === 'custom') {
            const fillColor = document.getElementById('fill-color')?.value || '#000000';
            const backColor = document.getElementById('back-color')?.value || '#FFFFFF';
            
            formData.append('fill_color', fillColor);
            formData.append('back_color', backColor);
            
            // Custom shapes
            const moduleShape = document.querySelector('.module-shape.selected')?.getAttribute('data-value') || 'square';
            const frameShape = document.querySelector('.frame-shape.selected')?.getAttribute('data-value') || 'square';
            const eyeShape = document.querySelector('.eye-shape.selected')?.getAttribute('data-value') || 'square';
            
            formData.append('module_shape', moduleShape);
            formData.append('frame_shape', frameShape);
            formData.append('eye_shape', eyeShape);
        }
        
        else if (currentTab === 'logo') {
            // Logo
            const logoFile = logoUpload?.files[0];
            if (logoFile) {
                formData.append('logo', logoFile);
            }
            
            // Logo size
            const logoSize = document.getElementById('logo-size')?.value || 0.2;
            formData.append('logo_size', logoSize);
            
            // Colors
            const fillColor = document.getElementById('logo-fill-color')?.value || '#000000';
            const backColor = document.getElementById('logo-back-color')?.value || '#FFFFFF';
            
            formData.append('fill_color', fillColor);
            formData.append('back_color', backColor);
            
            // Error correction for logo should be higher
            const logoErrorCorrection = document.getElementById('logo-error-correction')?.value || 3;
            formData.append('error_correction', logoErrorCorrection);
        }
        
        else if (currentTab === 'styled') {
            const moduleDrawer = document.getElementById('module-drawer')?.value || 'square';
            const colorMask = document.getElementById('color-mask')?.value || 'solid';
            
            formData.append('module_drawer', moduleDrawer);
            formData.append('color_mask', colorMask);
            
            // Colors for the mask
            if (colorMask === 'solid') {
                const frontColor = document.getElementById('front-color')?.value || '#000000';
                const backColor = document.getElementById('back-color')?.value || '#FFFFFF';
                
                formData.append('front_color', frontColor);
                formData.append('back_color', backColor);
            } else {
                // Gradient options
                const frontColor = document.getElementById('gradient-start-color')?.value || '#000000';
                const edgeColor = document.getElementById('gradient-end-color')?.value || '#666666';
                const backColor = document.getElementById('gradient-back-color')?.value || '#FFFFFF';
                
                formData.append('front_color', frontColor);
                formData.append('edge_color', edgeColor);
                formData.append('back_color', backColor);
                
                // Gradient center
                if (document.getElementById('gradient-center-x') && document.getElementById('gradient-center-y')) {
                    formData.append('gradient_center_x', document.getElementById('gradient-center-x').value);
                    formData.append('gradient_center_y', document.getElementById('gradient-center-y').value);
                }
            }
        }
        
        else if (currentTab === 'predefined') {
            const styleName = document.querySelector('.style-option.selected')?.getAttribute('data-value') || 'classic';
            formData.append('style_name', styleName);
            
            // Error correction
            const styleErrorCorrection = document.getElementById('style-error-correction')?.value || 1;
            formData.append('error_correction', styleErrorCorrection);
        }
        
        else if (currentTab === 'social') {
            const socialPlatform = document.querySelector('.social-platform.selected')?.getAttribute('data-value');
            
            if (socialPlatform) {
                formData.append('social_platform', socialPlatform);
            } else {
                showError('Please select a social platform');
                showLoading(false);
                return;
            }
            
            // Colors
            const fillColor = document.getElementById('social-fill-color')?.value || '#000000';
            const backColor = document.getElementById('social-back-color')?.value || '#FFFFFF';
            
            formData.append('fill_color', fillColor);
            formData.append('back_color', backColor);
            
            // Use platform color
            formData.append('use_platform_color', document.getElementById('use-platform-color')?.checked || false);
        }
        
        // Ajax request
        fetch('/generate', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error generating QR code');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Update preview
                qrPreview.src = `/qrcodes/${data.qr_path}?${new Date().getTime()}`; // Add timestamp to avoid caching
                
                // Store the QR code path
                currentQRPath = data.qr_path;
                
                // Enable export buttons
                enableExportButtons();
                
                // Show success message
                showSuccess('QR code generated successfully');
            } else {
                showError(data.error || 'Error generating QR code');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Error generating QR code');
        })
        .finally(() => {
            showLoading(false);
        });
    }

    function generatePreview() {
        // Skip if preview is already in progress
        if (previewInProgress) {
            return;
        }
        
        // Get data from active tab
        const activeDataInput = document.querySelector(`#tab-${currentTab} [id^="qr-data"]`);
        if (!activeDataInput || !activeDataInput.value.trim()) {
            return;
        }
        
        // Skip if data and options haven't changed
        const currentData = activeDataInput.value.trim();
        const currentOptions = getPreviewOptions();
        
        if (currentData === lastQRData && JSON.stringify(currentOptions) === JSON.stringify(lastOptions)) {
            return;
        }
        
        // Update last values
        lastQRData = currentData;
        lastOptions = currentOptions;
        
        // Set preview in progress flag
        previewInProgress = true;
        
        // Add loading effect to preview
        if (qrPreviewContainer) {
            qrPreviewContainer.classList.add('loading');
        }
        
        // Get options based on active tab
        const formData = new FormData();
        formData.append('data', currentData);
        
        // Preview type based on active tab
        formData.append('preview_type', currentTab);
        
        // Common options
        const version = document.getElementById('qr-version')?.value || 1;
        const errorCorrection = document.getElementById('qr-error-correction')?.value || 1;
        const boxSize = document.getElementById('qr-box-size')?.value || 10;
        const border = document.getElementById('qr-border')?.value || 4;
        
        formData.append('version', version);
        formData.append('error_correction', errorCorrection);
        formData.append('box_size', boxSize);
        formData.append('border', border);
        
        // Tab-specific options
        if (currentTab === 'custom') {
            const fillColor = document.getElementById('fill-color')?.value || '#000000';
            const backColor = document.getElementById('back-color')?.value || '#FFFFFF';
            
            formData.append('fill_color', fillColor);
            formData.append('back_color', backColor);
            
            // Custom shapes
            const moduleShape = document.querySelector('.module-shape.selected')?.getAttribute('data-value') || 'square';
            const frameShape = document.querySelector('.frame-shape.selected')?.getAttribute('data-value') || 'square';
            const eyeShape = document.querySelector('.eye-shape.selected')?.getAttribute('data-value') || 'square';
            
            formData.append('module_shape', moduleShape);
            formData.append('frame_shape', frameShape);
            formData.append('eye_shape', eyeShape);
        }
        
        else if (currentTab === 'logo') {
            // Logo (if present in preview)
            const logoPreview = document.getElementById('logo-preview');
            if (logoPreview && logoPreview.style.display !== 'none' && logoPreview.src) {
                formData.append('logo_data', logoPreview.src);
            }
            
            // Logo size
            const logoSize = document.getElementById('logo-size')?.value || 0.2;
            formData.append('logo_size', logoSize);
            
            // Colors
            const fillColor = document.getElementById('logo-fill-color')?.value || '#000000';
            const backColor = document.getElementById('logo-back-color')?.value || '#FFFFFF';
            
            formData.append('fill_color', fillColor);
            formData.append('back_color', backColor);
            
            // Error correction for logo should be higher
            const logoErrorCorrection = document.getElementById('logo-error-correction')?.value || 3;
            formData.append('error_correction', logoErrorCorrection);
        }
        
        else if (currentTab === 'styled') {
            const moduleDrawer = document.getElementById('module-drawer')?.value || 'square';
            const colorMask = document.getElementById('color-mask')?.value || 'solid';
            
            formData.append('module_drawer', moduleDrawer);
            formData.append('color_mask', colorMask);
            
            // Colors for the mask
            if (colorMask === 'solid') {
                const frontColor = document.getElementById('front-color')?.value || '#000000';
                const backColor = document.getElementById('back-color')?.value || '#FFFFFF';
                
                formData.append('front_color', frontColor);
                formData.append('back_color', backColor);
            } else {
                // Gradient options
                const frontColor = document.getElementById('gradient-start-color')?.value || '#000000';
                const edgeColor = document.getElementById('gradient-end-color')?.value || '#666666';
                const backColor = document.getElementById('gradient-back-color')?.value || '#FFFFFF';
                
                formData.append('front_color', frontColor);
                formData.append('edge_color', edgeColor);
                formData.append('back_color', backColor);
                
                // Gradient center
                if (document.getElementById('gradient-center-x') && document.getElementById('gradient-center-y')) {
                    formData.append('gradient_center_x', document.getElementById('gradient-center-x').value);
                    formData.append('gradient_center_y', document.getElementById('gradient-center-y').value);
                }
            }
        }
        
        else if (currentTab === 'predefined') {
            const styleName = document.querySelector('.style-option.selected')?.getAttribute('data-value') || 'classic';
            formData.append('style_name', styleName);
            
            // Error correction
            const styleErrorCorrection = document.getElementById('style-error-correction')?.value || 1;
            formData.append('error_correction', styleErrorCorrection);
        }
        
        else if (currentTab === 'social') {
            const socialPlatform = document.querySelector('.social-platform.selected')?.getAttribute('data-value');
            
            if (socialPlatform) {
                formData.append('social_platform', socialPlatform);
                
                // Colors
                const fillColor = document.getElementById('social-fill-color')?.value || '#000000';
                const backColor = document.getElementById('social-back-color')?.value || '#FFFFFF';
                
                formData.append('fill_color', fillColor);
                formData.append('back_color', backColor);
                
                // Use platform color
                formData.append('use_platform_color', document.getElementById('use-platform-color')?.checked || false);
            }
        }
        
        // Ajax request
        fetch('/preview', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error generating preview');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Update preview
                qrPreview.src = data.preview;
            }
        })
        .catch(error => {
            console.error('Preview error:', error);
            // Don't show error to avoid disrupting the user experience
        })
        .finally(() => {
            // Remove loading effect
            if (qrPreviewContainer) {
                qrPreviewContainer.classList.remove('loading');
            }
            
            // Reset preview in progress flag
            previewInProgress = false;
        });
    }
    
    function getPreviewOptions() {
        // Collect current options for comparison
        const options = {
            tab: currentTab,
            version: document.getElementById('qr-version')?.value,
            errorCorrection: document.getElementById('qr-error-correction')?.value,
            boxSize: document.getElementById('qr-box-size')?.value,
            border: document.getElementById('qr-border')?.value
        };
        
        // Tab-specific options
        if (currentTab === 'custom') {
            options.fillColor = document.getElementById('fill-color')?.value;
            options.backColor = document.getElementById('back-color')?.value;
            options.moduleShape = document.querySelector('.module-shape.selected')?.getAttribute('data-value');
            options.frameShape = document.querySelector('.frame-shape.selected')?.getAttribute('data-value');
            options.eyeShape = document.querySelector('.eye-shape.selected')?.getAttribute('data-value');
        }
        else if (currentTab === 'logo') {
            options.logoSize = document.getElementById('logo-size')?.value;
            options.fillColor = document.getElementById('logo-fill-color')?.value;
            options.backColor = document.getElementById('logo-back-color')?.value;
            options.errorCorrection = document.getElementById('logo-error-correction')?.value;
        }
        else if (currentTab === 'styled') {
            options.moduleDrawer = document.getElementById('module-drawer')?.value;
            options.colorMask = document.getElementById('color-mask')?.value;
            if (options.colorMask === 'solid') {
                options.frontColor = document.getElementById('front-color')?.value;
                options.backColor = document.getElementById('back-color')?.value;
            } else {
                options.frontColor = document.getElementById('gradient-start-color')?.value;
                options.edgeColor = document.getElementById('gradient-end-color')?.value;
                options.backColor = document.getElementById('gradient-back-color')?.value;
                options.gradientCenterX = document.getElementById('gradient-center-x')?.value;
                options.gradientCenterY = document.getElementById('gradient-center-y')?.value;
            }
        }
        else if (currentTab === 'predefined') {
            options.styleName = document.querySelector('.style-option.selected')?.getAttribute('data-value');
            options.errorCorrection = document.getElementById('style-error-correction')?.value;
        }
        else if (currentTab === 'social') {
            options.socialPlatform = document.querySelector('.social-platform.selected')?.getAttribute('data-value');
            options.fillColor = document.getElementById('social-fill-color')?.value;
            options.backColor = document.getElementById('social-back-color')?.value;
            options.usePlatformColor = document.getElementById('use-platform-color')?.checked;
        }
        
        return options;
    }

    // ===== Export QR Code =====
    function exportQRCode(format) {
        // Verify that a QR code has been generated
        if (!currentQRPath) {
            showError('Please generate a QR code first');
            return;
        }
        
        // Show loading indicator
        showLoading(true);
        
        // Get export options
        const formData = new FormData();
        formData.append('qr_path', currentQRPath);
        formData.append('export_format', format);
        
        // Format-specific options
        if (format === 'png') {
            // PNG options
            const dpi = document.getElementById('png-dpi')?.value || 300;
            const quality = document.getElementById('png-quality')?.value || 95;
            
            formData.append('dpi', dpi);
            formData.append('quality', quality);
            
            // Dimensions
            if (document.getElementById('png-width') && document.getElementById('png-height')) {
                formData.append('size_width', document.getElementById('png-width').value);
                formData.append('size_height', document.getElementById('png-height').value);
            }
        }
        else if (format === 'svg') {
            // SVG options
            const scale = document.getElementById('svg-scale')?.value || 1;
            formData.append('scale', scale);
            
            // Dimensions
            if (document.getElementById('svg-width') && document.getElementById('svg-height')) {
                formData.append('size_width', document.getElementById('svg-width').value);
                formData.append('size_height', document.getElementById('svg-height').value);
            }
        }
        else if (format === 'pdf') {
            // PDF options
            const title = document.getElementById('pdf-title')?.value || 'QR Code';
            const author = document.getElementById('pdf-author')?.value || 'QR Code Generator';
            
            formData.append('title', title);
            formData.append('author', author);
            
            // Dimensions
            if (document.getElementById('pdf-width') && document.getElementById('pdf-height')) {
                formData.append('size_width', document.getElementById('pdf-width').value);
                formData.append('size_height', document.getElementById('pdf-height').value);
            }
            
            // Position
            if (document.getElementById('pdf-x') && document.getElementById('pdf-y')) {
                formData.append('position_x', document.getElementById('pdf-x').value);
                formData.append('position_y', document.getElementById('pdf-y').value);
            }
        }
        else if (format === 'eps') {
            // EPS options
            const dpi = document.getElementById('eps-dpi')?.value || 300;
            formData.append('dpi', dpi);
        }
        
        // Ajax request
        fetch('/export', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error exporting QR code');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Download the exported file
                if (format === 'all') {
                    // For all formats, we get a ZIP with all files
                    window.location.href = data.download_urls.zip;
                } else {
                    window.location.href = data.download_url;
                }
                
                // Show success message
                showSuccess(`QR code exported successfully as ${format.toUpperCase()}`);
                
                // Update download link
                if (downloadLink) {
                    downloadLink.href = data.download_url;
                    downloadLink.style.display = 'inline-block';
                    downloadLink.textContent = `Download ${format.toUpperCase()}`;
                }
            } else {
                showError(data.error || 'Error exporting QR code');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Error exporting QR code');
        })
        .finally(() => {
            showLoading(false);
        });
    }

    // ===== Utilities =====
    function enableExportButtons(enable = true) {
        exportButtons.forEach(button => {
            button.disabled = !enable;
            if (enable) {
                button.classList.remove('disabled');
            } else {
                button.classList.add('disabled');
            }
        });
        
        // Show the download section
        const downloadContainer = document.querySelector('.download-container');
        if (downloadContainer) {
            downloadContainer.style.display = enable ? 'block' : 'none';
        }
    }

    function showLoading(show) {
        const loadingIndicator = document.getElementById('loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.style.display = show ? 'flex' : 'none';
        }
    }

    function showError(message) {
        const errorContainer = document.getElementById('error-container');
        if (errorContainer) {
            errorContainer.textContent = message;
            errorContainer.style.display = 'block';
            
            // Hide after 5 seconds
            setTimeout(() => {
                errorContainer.style.display = 'none';
            }, 5000);
        }
    }

    function showSuccess(message) {
        const successContainer = document.getElementById('success-container');
        if (successContainer) {
            successContainer.textContent = message;
            successContainer.style.display = 'block';
            
            // Hide after 3 seconds
            setTimeout(() => {
                successContainer.style.display = 'none';
            }, 3000);
        }
    }

    function debouncePreview() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(generatePreview, DEBOUNCE_DELAY);
    }

    // ===== Initialize Application =====
    init();
});
