import React, { useState, useEffect } from 'react';
import { AlertCircle, Download, Upload, Check, X } from 'lucide-react';

// Main QR Code Generator component
const QRCodeGenerator = () => {
  // State for QR code data
  const [qrData, setQrData] = useState('https://example.com');
  const [activeTab, setActiveTab] = useState('content');
  const [previewUrl, setPreviewUrl] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [notification, setNotification] = useState(null);
  const [generatedQrPath, setGeneratedQrPath] = useState(null);

  // QR Code options
  const [options, setOptions] = useState({
    // Content options
    data: 'https://example.com',
    dataType: 'url',
    
    // Colors options
    foregroundColor: '#000000',
    backgroundColor: '#ffffff',
    
    // Style options
    pattern: 'square',
    eyeShape: 'square',
    eyeballShape: 'square',
    
    // Logo options
    logo: null,
    logoSize: 25,
    
    // General options
    errorCorrection: 'M',
    margin: 4,
    size: 1000,
    
    // Export options
    format: 'png',
    dpi: 300
  });

  // Predefined QR styles
  const patterns = [
    { id: 'square', name: 'Square', icon: '■' },
    { id: 'dot', name: 'Dot', icon: '●' },
    { id: 'round', name: 'Round', icon: '◉' },
    { id: 'diamond', name: 'Diamond', icon: '◆' },
    { id: 'star', name: 'Star', icon: '★' },
    { id: 'triangle', name: 'Triangle', icon: '▲' }
  ];
  
  const eyeShapes = [
    { id: 'square', name: 'Square', icon: '■' },
    { id: 'circle', name: 'Circle', icon: '●' },
    { id: 'rounded', name: 'Rounded', icon: '◉' },
    { id: 'diamond', name: 'Diamond', icon: '◆' },
    { id: 'leaf', name: 'Leaf', icon: '♠' }
  ];
  
  const eyeballShapes = [
    { id: 'square', name: 'Square', icon: '■' },
    { id: 'circle', name: 'Circle', icon: '●' },
    { id: 'diamond', name: 'Diamond', icon: '◆' }
  ];

  // Update options when input changes
  const handleOptionsChange = (key, value) => {
    setOptions(prev => ({ ...prev, [key]: value }));
  };

  // Handle logo upload
  const handleLogoUpload = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        handleOptionsChange('logo', e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  // Remove logo
  const handleRemoveLogo = () => {
    handleOptionsChange('logo', null);
  };

  // Generate QR code preview
  useEffect(() => {
    // Only generate preview if we have data
    if (!options.data) return;
    
    const generatePreview = async () => {
      try {
        const formData = new FormData();
        formData.append('data', options.data);
        formData.append('preview_type', 'custom');
        formData.append('fill_color', options.foregroundColor);
        formData.append('back_color', options.backgroundColor);
        formData.append('module_shape', options.pattern);
        formData.append('eye_shape', options.eyeShape);
        
        // Add logo if present
        if (options.logo) {
          formData.append('logo_data', options.logo);
          formData.append('logo_size', options.logoSize / 100);
        }
        
        // Send request to backend
        const response = await fetch('/preview', {
          method: 'POST',
          body: formData
        });
        
        if (!response.ok) {
          throw new Error('Preview generation failed');
        }
        
        const data = await response.json();
        if (data.success) {
          setPreviewUrl(data.preview);
        }
      } catch (error) {
        console.error('Error generating preview:', error);
      }
    };
    
    // Debounce preview generation
    const timer = setTimeout(() => {
      generatePreview();
    }, 300);
    
    return () => clearTimeout(timer);
  }, [options]);

  // Generate final QR code
  const generateQRCode = async () => {
    if (!options.data) {
      showNotification('Please enter content for your QR code', 'error');
      return;
    }
    
    setIsGenerating(true);
    
    try {
      const formData = new FormData();
      formData.append('data', options.data);
      formData.append('generation_type', 'custom');
      formData.append('fill_color', options.foregroundColor);
      formData.append('back_color', options.backgroundColor);
      formData.append('module_shape', options.pattern);
      formData.append('frame_shape', options.eyeShape);
      formData.append('eye_shape', options.eyeballShape);
      formData.append('error_correction', options.errorCorrection === 'L' ? 0 : 
                                       options.errorCorrection === 'M' ? 1 : 
                                       options.errorCorrection === 'Q' ? 2 : 3);
      formData.append('border', options.margin);
      
      // Add logo if present
      if (options.logo && options.logo.startsWith('data:image')) {
        // For the preview we already have a base64 string
        const response = await fetch(options.logo);
        const blob = await response.blob();
        formData.append('logo', blob);
        formData.append('logo_size', options.logoSize / 100);
      }
      
      const response = await fetch('/generate', {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) {
        throw new Error('QR code generation failed');
      }
      
      const data = await response.json();
      if (data.success) {
        setGeneratedQrPath(data.qr_path);
        showNotification('QR code generated successfully', 'success');
      } else {
        throw new Error(data.error || 'Unknown error');
      }
    } catch (error) {
      console.error('Error generating QR code:', error);
      showNotification(error.message || 'Failed to generate QR code', 'error');
    } finally {
      setIsGenerating(false);
    }
  };

  // Export QR code
  const exportQRCode = async (format = 'png') => {
    if (!generatedQrPath) {
      showNotification('Please generate a QR code first', 'error');
      return;
    }
    
    try {
      const formData = new FormData();
      formData.append('qr_path', generatedQrPath);
      formData.append('export_format', format);
      
      // Add format-specific options
      if (format === 'png') {
        formData.append('dpi', options.dpi);
        formData.append('size_width', options.size);
        formData.append('size_height', options.size);
      } else if (format === 'svg') {
        formData.append('scale', 1);
      } else if (format === 'pdf') {
        formData.append('title', 'QR Code');
        formData.append('size_width', 50);
        formData.append('size_height', 50);
      }
      
      const response = await fetch('/export', {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) {
        throw new Error('Export failed');
      }
      
      const data = await response.json();
      if (data.success) {
        // Trigger file download
        window.location.href = data.download_url;
        showNotification(`QR code exported as ${format.toUpperCase()}`, 'success');
      } else {
        throw new Error(data.error || 'Unknown error');
      }
    } catch (error) {
      console.error('Error exporting QR code:', error);
      showNotification(error.message || 'Failed to export QR code', 'error');
    }
  };

  // Show notification
  const showNotification = (message, type = 'info') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-blue-600 text-white py-4">
        <div className="container mx-auto px-4">
          <h1 className="text-2xl font-bold">QR Code Generator</h1>
          <p className="text-sm opacity-80">Create custom QR codes with advanced styling options</p>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-grow container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left column: Options */}
          <div className="lg:col-span-2 bg-white rounded-lg shadow-md overflow-hidden">
            {/* Tabs */}
            <div className="flex border-b">
              <button 
                className={`px-4 py-3 font-medium ${activeTab === 'content' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600'}`}
                onClick={() => setActiveTab('content')}
              >
                Content
              </button>
              <button 
                className={`px-4 py-3 font-medium ${activeTab === 'colors' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600'}`}
                onClick={() => setActiveTab('colors')}
              >
                Colors
              </button>
              <button 
                className={`px-4 py-3 font-medium ${activeTab === 'style' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600'}`}
                onClick={() => setActiveTab('style')}
              >
                Style
              </button>
              <button 
                className={`px-4 py-3 font-medium ${activeTab === 'logo' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600'}`}
                onClick={() => setActiveTab('logo')}
              >
                Logo
              </button>
              <button 
                className={`px-4 py-3 font-medium ${activeTab === 'options' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-600'}`}
                onClick={() => setActiveTab('options')}
              >
                Options
              </button>
            </div>

            {/* Tab content */}
            <div className="p-6">
              {/* Content tab */}
              {activeTab === 'content' && (
                <div>
                  <h2 className="text-lg font-semibold mb-4">QR Code Content</h2>
                  
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Data Type
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {['url', 'text', 'email', 'phone', 'sms', 'vcard', 'wifi'].map(type => (
                        <button
                          key={type}
                          className={`px-3 py-1 rounded-md text-sm ${options.dataType === type ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'}`}
                          onClick={() => handleOptionsChange('dataType', type)}
                        >
                          {type.charAt(0).toUpperCase() + type.slice(1)}
                        </button>
                      ))}
                    </div>
                  </div>
                  
                  <div className="mb-4">
                    <label htmlFor="qr-data" className="block text-sm font-medium text-gray-700 mb-1">
                      {options.dataType === 'url' ? 'URL' : 
                       options.dataType === 'email' ? 'Email Address' : 
                       options.dataType === 'phone' ? 'Phone Number' : 
                       options.dataType === 'sms' ? 'SMS Number & Message' : 
                       options.dataType === 'vcard' ? 'Contact Information' : 
                       options.dataType === 'wifi' ? 'WiFi Network Details' : 'Text Content'}
                    </label>
                    <textarea
                      id="qr-data"
                      value={options.data}
                      onChange={(e) => {
                        handleOptionsChange('data', e.target.value);
                        setQrData(e.target.value);
                      }}
                      className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      rows="4"
                      placeholder={options.dataType === 'url' ? 'https://example.com' : 'Enter your content here...'}
                    ></textarea>
                  </div>
                </div>
              )}

              {/* Colors tab */}
              {activeTab === 'colors' && (
                <div>
                  <h2 className="text-lg font-semibold mb-4">Colors</h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="mb-4">
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Foreground Color
                      </label>
                      <div className="flex items-center">
                        <div className="w-10 h-10 rounded-md border border-gray-300 mr-2" style={{ backgroundColor: options.foregroundColor }}></div>
                        <input
                          type="color"
                          value={options.foregroundColor}
                          onChange={(e) => handleOptionsChange('foregroundColor', e.target.value)}
                          className="w-10 h-10 rounded-md border border-gray-300"
                        />
                        <input
                          type="text"
                          value={options.foregroundColor}
                          onChange={(e) => handleOptionsChange('foregroundColor', e.target.value)}
                          className="ml-2 p-2 border border-gray-300 rounded-md w-28"
                        />
                      </div>
                    </div>
                    
                    <div className="mb-4">
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Background Color
                      </label>
                      <div className="flex items-center">
                        <div className="w-10 h-10 rounded-md border border-gray-300 mr-2" style={{ backgroundColor: options.backgroundColor }}></div>
                        <input
                          type="color"
                          value={options.backgroundColor}
                          onChange={(e) => handleOptionsChange('backgroundColor', e.target.value)}
                          className="w-10 h-10 rounded-md border border-gray-300"
                        />
                        <input
                          type="text"
                          value={options.backgroundColor}
                          onChange={(e) => handleOptionsChange('backgroundColor', e.target.value)}
                          className="ml-2 p-2 border border-gray-300 rounded-md w-28"
                        />
                      </div>
                    </div>
                  </div>

                  {/* Common color presets */}
                  <div className="mt-6">
                    <h3 className="text-sm font-medium text-gray-700 mb-2">Presets</h3>
                    <div className="grid grid-cols-5 gap-2">
                      {[
                        { fg: '#000000', bg: '#ffffff', name: 'Standard' },
                        { fg: '#0277BD', bg: '#ffffff', name: 'Blue' },
                        { fg: '#4CAF50', bg: '#ffffff', name: 'Green' },
                        { fg: '#E91E63', bg: '#ffffff', name: 'Pink' },
                        { fg: '#FF9800', bg: '#ffffff', name: 'Orange' },
                      ].map((preset, idx) => (
                        <button
                          key={idx}
                          className="p-1 border border-gray-200 rounded-md hover:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                          onClick={() => {
                            handleOptionsChange('foregroundColor', preset.fg);
                            handleOptionsChange('backgroundColor', preset.bg);
                          }}
                        >
                          <div className="aspect-square rounded-md mb-1" style={{ backgroundColor: preset.fg }}></div>
                          <span className="text-xs block truncate">{preset.name}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Style tab */}
              {activeTab === 'style' && (
                <div>
                  <h2 className="text-lg font-semibold mb-4">QR Style</h2>
                  
                  <div className="mb-6">
                    <h3 className="text-sm font-medium text-gray-700 mb-2">Pattern</h3>
                    <div className="grid grid-cols-3 sm:grid-cols-6 gap-2">
                      {patterns.map(pattern => (
                        <button
                          key={pattern.id}
                          className={`p-3 border rounded-md flex flex-col items-center ${options.pattern === pattern.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}`}
                          onClick={() => handleOptionsChange('pattern', pattern.id)}
                        >
                          <span className="text-2xl mb-1">{pattern.icon}</span>
                          <span className="text-xs">{pattern.name}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                  
                  <div className="mb-6">
                    <h3 className="text-sm font-medium text-gray-700 mb-2">Eyes</h3>
                    <div className="grid grid-cols-3 sm:grid-cols-5 gap-2">
                      {eyeShapes.map(shape => (
                        <button
                          key={shape.id}
                          className={`p-3 border rounded-md flex flex-col items-center ${options.eyeShape === shape.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}`}
                          onClick={() => handleOptionsChange('eyeShape', shape.id)}
                        >
                          <span className="text-2xl mb-1">{shape.icon}</span>
                          <span className="text-xs">{shape.name}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                  
                  <div className="mb-6">
                    <h3 className="text-sm font-medium text-gray-700 mb-2">Eye Balls</h3>
                    <div className="grid grid-cols-3 gap-2">
                      {eyeballShapes.map(shape => (
                        <button
                          key={shape.id}
                          className={`p-3 border rounded-md flex flex-col items-center ${options.eyeballShape === shape.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}`}
                          onClick={() => handleOptionsChange('eyeballShape', shape.id)}
                        >
                          <span className="text-2xl mb-1">{shape.icon}</span>
                          <span className="text-xs">{shape.name}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Logo tab */}
              {activeTab === 'logo' && (
                <div>
                  <h2 className="text-lg font-semibold mb-4">Add Logo</h2>
                  
                  <div className="mb-6">
                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                      {options.logo ? (
                        <div className="flex flex-col items-center">
                          <img 
                            src={options.logo} 
                            alt="Logo" 
                            className="max-w-full max-h-32 mb-4"
                          />
                          <button
                            className="px-4 py-2 bg-red-100 text-red-700 rounded-md flex items-center"
                            onClick={handleRemoveLogo}
                          >
                            <X size={16} className="mr-1" />
                            Remove Logo
                          </button>
                        </div>
                      ) : (
                        <div>
                          <Upload size={24} className="mx-auto text-gray-400 mb-2" />
                          <p className="text-sm text-gray-500 mb-4">Upload your logo or image</p>
                          <label className="px-4 py-2 bg-blue-600 text-white rounded-md cursor-pointer inline-block">
                            Upload Image
                            <input
                              type="file"
                              className="hidden"
                              accept="image/*"
                              onChange={handleLogoUpload}
                            />
                          </label>
                          <p className="text-xs text-gray-500 mt-2">Supported formats: JPG, PNG, SVG (max 2MB)</p>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div className="mb-6">
                    <label htmlFor="logo-size" className="block text-sm font-medium text-gray-700 mb-1">
                      Logo Size: {options.logoSize}%
                    </label>
                    <input
                      id="logo-size"
                      type="range"
                      min="5"
                      max="40"
                      value={options.logoSize}
                      onChange={(e) => handleOptionsChange('logoSize', parseInt(e.target.value))}
                      className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>5%</span>
                      <span>40%</span>
                    </div>
                  </div>
                </div>
              )}

              {/* Options tab */}
              {activeTab === 'options' && (
                <div>
                  <h2 className="text-lg font-semibold mb-4">Advanced Options</h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="mb-4">
                      <label htmlFor="error-correction" className="block text-sm font-medium text-gray-700 mb-1">
                        Error Correction
                      </label>
                      <select
                        id="error-correction"
                        value={options.errorCorrection}
                        onChange={(e) => handleOptionsChange('errorCorrection', e.target.value)}
                        className="w-full p-2 border border-gray-300 rounded-md"
                      >
                        <option value="L">Low (7%)</option>
                        <option value="M">Medium (15%)</option>
                        <option value="Q">Quartile (25%)</option>
                        <option value="H">High (30%)</option>
                      </select>
                      <p className="text-xs text-gray-500 mt-1">Higher levels allow more data to be recovered if the code is damaged</p>
                    </div>
                    
                    <div className="mb-4">
                      <label htmlFor="margin" className="block text-sm font-medium text-gray-700 mb-1">
                        Margin: {options.margin}
                      </label>
                      <input
                        id="margin"
                        type="range"
                        min="0"
                        max="10"
                        value={options.margin}
                        onChange={(e) => handleOptionsChange('margin', parseInt(e.target.value))}
                        className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                      />
                      <div className="flex justify-between text-xs text-gray-500 mt-1">
                        <span>0</span>
                        <span>10</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mb-4">
                    <label htmlFor="size" className="block text-sm font-medium text-gray-700 mb-1">
                      Output Size: {options.size}px
                    </label>
                    <input
                      id="size"
                      type="range"
                      min="100"
                      max="2000"
                      step="100"
                      value={options.size}
                      onChange={(e) => handleOptionsChange('size', parseInt(e.target.value))}
                      className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>100px</span>
                      <span>2000px</span>
                    </div>
                  </div>
                </div>
              )}
              
              <div className="mt-8 flex justify-end">
                <button
                  className="px-6 py-2 bg-blue-600 text-white rounded-md font-medium shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
                  onClick={generateQRCode}
                  disabled={isGenerating || !qrData}
                >
                  {isGenerating ? 'Generating...' : 'Generate QR Code'}
                </button>
              </div>
            </div>
          </div>

          {/* Right column: Preview & Download */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold mb-4">Preview</h2>
            
            <div className="bg-gray-100 rounded-lg flex items-center justify-center p-4 mb-6" style={{ height: '300px' }}>
              {previewUrl ? (
                <img 
                  src={previewUrl} 
                  alt="QR Code Preview" 
                  className="max-w-full max-h-full" 
                />
              ) : (
                <div className="text-center text-gray-400">
                  <p>Enter content to see preview</p>
                </div>
              )}
            </div>
            
            {generatedQrPath && (
              <div>
                <h3 className="text-md font-medium mb-3">Download</h3>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-4">
                  {['png', 'svg', 'pdf', 'eps'].map(format => (
                    <button
                      key={format}
                      className="px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded-md text-sm uppercase font-medium flex items-center justify-center"
                      onClick={() => exportQRCode(format)}
                    >
                      <Download size={16} className="mr-1" />
                      {format}
                    </button>
                  ))}
                </div>
                
                <div className="mt-4">
                  <label htmlFor="dpi" className="block text-sm font-medium text-gray-700 mb-1">
                    DPI (for PNG): {options.dpi}
                  </label>
                  <select
                    id="dpi"
                    value={options.dpi}
                    onChange={(e) => handleOptionsChange('dpi', parseInt(e.target.value))}
                    className="w-full p-2 border border-gray-300 rounded-md"
                  >
                    <option value="72">72 DPI (Web)</option>
                    <option value="150">150 DPI</option>
                    <option value="300">300 DPI (Print)</option>
                    <option value="600">600 DPI (High Quality)</option>
                  </select>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-4 mt-8">
        <div className="container mx-auto px-4 text-center text-sm">
          <p>&copy; {new Date().getFullYear()} QR Code Generator. All rights reserved.</p>
        </div>
      </footer>

      {/* Notification */}
      {notification && (
        <div className={`fixed bottom-4 right-4 px-4 py-3 rounded-md shadow-lg max-w-md ${
          notification.type === 'error' ? 'bg-red-100 text-red-800' : 
          notification.type === 'success' ? 'bg-green-100 text-green-800' : 
          'bg-blue-100 text-blue-800'
        }`}>
          <div className="flex items-center">
            {notification.type === 'error' ? (
              <AlertCircle className="mr-2" size={20} />
            ) : (
              <Check className="mr-2" size={20} />
            )}
            <p>{notification.message}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default QRCodeGenerator;
