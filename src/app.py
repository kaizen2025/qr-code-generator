#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
QR Code Generator API
A Flask-based backend API for generating, customizing, and exporting QR codes
"""

import os
import io
import uuid
import base64
from datetime import datetime

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageColor
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer, 
    GappedSquareModuleDrawer,
    CircleModuleDrawer, 
    RoundedModuleDrawer,
    VerticalBarsDrawer, 
    HorizontalBarsDrawer
)
from qrcode.image.styles.colormasks import (
    SolidFillColorMask,
    RadialGradiantColorMask,
    SquareGradiantColorMask,
    HorizontalGradiantColorMask,
    VerticalGradiantColorMask
)
import svgwrite
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Set up directories
if os.environ.get('PRODUCTION'):
    UPLOAD_FOLDER = '/tmp/uploads'
    GENERATED_FOLDER = '/tmp/qrcodes'
    EXPORTED_FOLDER = '/tmp/exports'
else:
    # Development paths
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    GENERATED_FOLDER = os.path.join(os.getcwd(), 'qrcodes')
    EXPORTED_FOLDER = os.path.join(os.getcwd(), 'exports')

# Create directories if they don't exist
for folder in [UPLOAD_FOLDER, GENERATED_FOLDER, EXPORTED_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Configure Flask app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GENERATED_FOLDER'] = GENERATED_FOLDER
app.config['EXPORTED_FOLDER'] = EXPORTED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload

# Module drawer mapping
MODULE_DRAWERS = {
    'square': SquareModuleDrawer(),
    'dot': CircleModuleDrawer(radius_ratio=0.6),
    'round': RoundedModuleDrawer(),
    'circle': CircleModuleDrawer(),
    'gapped_square': GappedSquareModuleDrawer(gap_width=0.15),
    'vertical_bars': VerticalBarsDrawer(),
    'horizontal_bars': HorizontalBarsDrawer(),
    # Custom shapes would be implemented here
    'diamond': SquareModuleDrawer(),  # Placeholder - would need custom implementation
    'star': SquareModuleDrawer(),     # Placeholder - would need custom implementation
    'triangle': SquareModuleDrawer()  # Placeholder - would need custom implementation
}

# Color mask mapping
COLOR_MASKS = {
    'solid': SolidFillColorMask,
    'radial_gradient': RadialGradiantColorMask,
    'square_gradient': SquareGradiantColorMask,
    'horizontal_gradient': HorizontalGradiantColorMask,
    'vertical_gradient': VerticalGradiantColorMask
}

# Error correction levels
ERROR_CORRECTION = {
    0: qrcode.constants.ERROR_CORRECT_L,  # 7%
    1: qrcode.constants.ERROR_CORRECT_M,  # 15%
    2: qrcode.constants.ERROR_CORRECT_Q,  # 25%
    3: qrcode.constants.ERROR_CORRECT_H   # 30%
}

# Helper Functions
def parse_color(color):
    """Convert color string to RGB tuple"""
    if isinstance(color, str):
        if color.startswith('#'):
            color = color.lstrip('#')
            if len(color) == 3:
                return tuple(int(c + c, 16) for c in color)
            elif len(color) == 6:
                return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        # Add named color support if needed
    elif isinstance(color, tuple) and len(color) >= 3:
        return color[:3]
    # Default to black
    return (0, 0, 0)

def customize_qr_eyes(qr_image, eye_shape, frame_shape, fill_color):
    """
    Customize the QR code's eyes with different shapes
    
    Args:
        qr_image: PIL Image of the QR code
        eye_shape: Shape for the eye (inner part)
        frame_shape: Shape for the frame (outer part)
        fill_color: Color for the eyes
    
    Returns:
        Modified PIL Image
    """
    # This is a simplified implementation for demonstration
    # A complete implementation would detect eye positions and replace them
    # with custom shapes based on eye_shape and frame_shape parameters
    
    # For now, we just return the original image
    return qr_image

def save_metadata(data, output_path, options=None):
    """Save metadata about the generated QR code"""
    metadata_dir = os.path.join(os.path.dirname(output_path), 'metadata')
    os.makedirs(metadata_dir, exist_ok=True)
    
    qr_filename = os.path.basename(output_path)
    metadata_filename = f"{os.path.splitext(qr_filename)[0]}.txt"
    metadata_path = os.path.join(metadata_dir, metadata_filename)
    
    metadata_content = [
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Data: {data}",
        f"File: {qr_filename}"
    ]
    
    if options:
        metadata_content.append("Options:")
        for key, value in options.items():
            metadata_content.append(f"  {key}: {value}")
    
    with open(metadata_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(metadata_content))

# API Routes
@app.route('/api/status', methods=['GET'])
def api_status():
    """Check if the API is running"""
    return jsonify({
        'status': 'ok',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/preview', methods=['POST'])
def generate_preview():
    """Generate a QR code preview and return as base64 image"""
    try:
        data = request.form.get('data')
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        preview_type = request.form.get('preview_type', 'basic')
        
        # Basic options
        version = int(request.form.get('version', 1))
        error_correction_level = int(request.form.get('error_correction', 1))
        error_correction = ERROR_CORRECTION.get(error_correction_level, qrcode.constants.ERROR_CORRECT_M)
        box_size = int(request.form.get('box_size', 10))
        border = int(request.form.get('border', 4))
        
        # Create basic QR code
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        if preview_type == 'basic':
            # Basic black and white QR code
            img = qr.make_image(fill_color="black", back_color="white")
        
        elif preview_type == 'custom':
            # Get custom colors
            fill_color = request.form.get('fill_color', '#000000')
            back_color = request.form.get('back_color', '#FFFFFF')
            
            # Get module shape
            module_shape = request.form.get('module_shape', 'square')
            module_drawer = MODULE_DRAWERS.get(module_shape, SquareModuleDrawer())
            
            # Create the QR code with styled PIL image
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=module_drawer,
                color_mask=SolidFillColorMask(
                    front_color=parse_color(fill_color),
                    back_color=parse_color(back_color)
                )
            )
            
            # Customize eyes if requested
            eye_shape = request.form.get('eye_shape')
            frame_shape = request.form.get('frame_shape')
            
            if eye_shape or frame_shape:
                img_pil = img.get_image() if hasattr(img, 'get_image') else img
                img = customize_qr_eyes(
                    img_pil,
                    eye_shape or 'square',
                    frame_shape or 'square',
                    parse_color(fill_color)
                )
            
            # Add logo if provided
            logo_data = request.form.get('logo_data')
            if logo_data and logo_data.startswith('data:image'):
                # Extract base64 data
                logo_data = logo_data.split(',')[1]
                logo_binary = base64.b64decode(logo_data)
                logo = Image.open(io.BytesIO(logo_binary)).convert('RGBA')
                
                # Resize logo
                qr_img = img.get_image() if hasattr(img, 'get_image') else img
                qr_width, qr_height = qr_img.size
                logo_size = float(request.form.get('logo_size', 0.2))
                logo_max_size = int(min(qr_width, qr_height) * logo_size)
                
                # Keep aspect ratio
                logo_width, logo_height = logo.size
                ratio = min(logo_max_size / logo_width, logo_max_size / logo_height)
                new_logo_width = int(logo_width * ratio)
                new_logo_height = int(logo_height * ratio)
                logo = logo.resize((new_logo_width, new_logo_height), Image.LANCZOS)
                
                # Add white padding
                padding = 10
                logo_with_padding = Image.new('RGBA', (new_logo_width + padding * 2, new_logo_height + padding * 2), (255, 255, 255, 255))
                logo_with_padding.paste(logo, (padding, padding), logo)
                
                # Center the logo
                position = ((qr_width - logo_with_padding.width) // 2, (qr_height - logo_with_padding.height) // 2)
                
                # Create a new image and paste logo
                qr_img = qr_img.convert('RGBA')
                result = Image.new('RGBA', qr_img.size, (0, 0, 0, 0))
                result.paste(qr_img, (0, 0))
                result.paste(logo_with_padding, position, logo_with_padding)
                img = result
        
        # Convert image to base64
        buffered = io.BytesIO()
        if isinstance(img, Image.Image):
            img.save(buffered, format="PNG")
        else:
            img.get_image().save(buffered, format="PNG")
        
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'preview': f"data:image/png;base64,{img_str}"
        })
        
    except Exception as e:
        print(f"Error generating preview: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate_qrcode():
    """Generate a QR code and save it"""
    try:
        data = request.form.get('data')
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Generate a unique filename
        filename = f"qrcode_{uuid.uuid4().hex}.png"
        output_path = os.path.join(app.config['GENERATED_FOLDER'], filename)
        
        # Get common options
        version = int(request.form.get('version', 1))
        error_correction_level = int(request.form.get('error_correction', 1))
        error_correction = ERROR_CORRECTION.get(error_correction_level, qrcode.constants.ERROR_CORRECT_M)
        box_size = int(request.form.get('box_size', 10))
        border = int(request.form.get('border', 4))
        
        # Create QR code object
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Get generation type
        generation_type = request.form.get('generation_type', 'basic')
        
        if generation_type == 'basic':
            # Basic black and white QR code
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(output_path)
            
        elif generation_type == 'custom':
            # Get custom colors
            fill_color = request.form.get('fill_color', '#000000')
            back_color = request.form.get('back_color', '#FFFFFF')
            
            # Get module shape
            module_shape = request.form.get('module_shape', 'square')
            module_drawer = MODULE_DRAWERS.get(module_shape, SquareModuleDrawer())
            
            # Create the QR code with styled PIL image
            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=module_drawer,
                color_mask=SolidFillColorMask(
                    front_color=parse_color(fill_color),
                    back_color=parse_color(back_color)
                )
            )
            
            # Customize eyes if requested
            eye_shape = request.form.get('eye_shape')
            frame_shape = request.form.get('frame_shape')
            
            if eye_shape or frame_shape:
                img_pil = img.get_image() if hasattr(img, 'get_image') else img
                img = customize_qr_eyes(
                    img_pil,
                    eye_shape or 'square',
                    frame_shape or 'square',
                    parse_color(fill_color)
                )
            
            # Add logo if provided
            if 'logo' in request.files:
                logo_file = request.files['logo']
                if logo_file.filename:
                    logo = Image.open(logo_file).convert('RGBA')
                    
                    # Save logo to uploads folder
                    logo_filename = f"logo_{uuid.uuid4().hex}{os.path.splitext(logo_file.filename)[1]}"
                    logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_filename)
                    logo.save(logo_path)
                    
                    # Resize logo
                    qr_img = img.get_image() if hasattr(img, 'get_image') else img
                    qr_width, qr_height = qr_img.size
                    logo_size = float(request.form.get('logo_size', 0.2))
                    logo_max_size = int(min(qr_width, qr_height) * logo_size)
                    
                    # Keep aspect ratio
                    logo_width, logo_height = logo.size
                    ratio = min(logo_max_size / logo_width, logo_max_size / logo_height)
                    new_logo_width = int(logo_width * ratio)
                    new_logo_height = int(logo_height * ratio)
                    logo = logo.resize((new_logo_width, new_logo_height), Image.LANCZOS)
                    
                    # Add white padding
                    padding = 10
                    logo_with_padding = Image.new('RGBA', (new_logo_width + padding * 2, new_logo_height + padding * 2), (255, 255, 255, 255))
                    logo_with_padding.paste(logo, (padding, padding), logo)
                    
                    # Center the logo
                    position = ((qr_width - logo_with_padding.width) // 2, (qr_height - logo_with_padding.height) // 2)
                    
                    # Create a new image and paste logo
                    qr_img = qr_img.convert('RGBA')
                    result = Image.new('RGBA', qr_img.size, (0, 0, 0, 0))
                    result.paste(qr_img, (0, 0))
                    result.paste(logo_with_padding, position, logo_with_padding)
                    img = result
                    
                    # Update options for metadata
                    if isinstance(options, dict):
                        options['logo_path'] = logo_path
            
            # Save the final image
            if isinstance(img, Image.Image):
                img.save(output_path)
            else:
                img.get_image().save(output_path)
        
        # Save metadata
        options = {
            'version': version,
            'error_correction': error_correction_level,
            'box_size': box_size,
            'border': border,
            'generation_type': generation_type
        }
        
        if generation_type == 'custom':
            options['fill_color'] = request.form.get('fill_color')
            options['back_color'] = request.form.get('back_color')
            options['module_shape'] = request.form.get('module_shape')
            options['eye_shape'] = request.form.get('eye_shape')
            options['frame_shape'] = request.form.get('frame_shape')
        
        save_metadata(data, output_path, options)
        
        return jsonify({
            'success': True,
            'qr_path': filename,
            'download_url': f"/qrcodes/{filename}"
        })
        
    except Exception as e:
        print(f"Error generating QR code: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/export', methods=['POST'])
def export_qrcode():
    """Export QR code to different formats"""
    try:
        qr_path = request.form.get('qr_path')
        if not qr_path:
            return jsonify({'error': 'No QR code path provided'}), 400
        
        # Get full path
        input_path = os.path.join(app.config['GENERATED_FOLDER'], qr_path)
        if not os.path.exists(input_path):
            return jsonify({'error': 'QR code file not found'}), 404
        
        # Get export format
        export_format = request.form.get('export_format', 'png')
        
        # Generate a unique filename
        filename = f"qrcode_export_{uuid.uuid4().hex}.{export_format}"
        output_path = os.path.join(app.config['EXPORTED_FOLDER'], filename)
        
        # Open the QR code image
        img = Image.open(input_path)
        
        if export_format == 'png':
            # Export as PNG
            dpi = int(request.form.get('dpi', 300))
            
            # Resize if dimensions provided
            if 'size_width' in request.form and 'size_height' in request.form:
                width = int(request.form.get('size_width'))
                height = int(request.form.get('size_height'))
                img = img.resize((width, height), Image.LANCZOS)
            
            # Save with DPI
            img.save(output_path, format='PNG', dpi=(dpi, dpi))
            
        elif export_format == 'svg':
            # Export as SVG
            scale = float(request.form.get('scale', 1.0))
            
            # Get dimensions
            width, height = img.size
            
            # Create SVG
            dwg = svgwrite.Drawing(output_path, size=(f"{width * scale}px", f"{height * scale}px"))
            
            # Convert to black and white for simplicity
            img_bw = img.convert('1')
            
            # Add each black pixel as a rectangle
            for y in range(height):
                for x in range(width):
                    if img_bw.getpixel((x, y)) == 0:  # Black pixel
                        dwg.add(dwg.rect(
                            insert=(x * scale, y * scale),
                            size=(scale, scale),
                            fill='black'
                        ))
            
            # Save SVG
            dwg.save()
            
        elif export_format == 'pdf':
            # Export as PDF
            # Get options
            title = request.form.get('title', 'QR Code')
            size_width = float(request.form.get('size_width', 50))
            size_height = float(request.form.get('size_height', 50))
            
            # Create PDF
            c = canvas.Canvas(output_path, pagesize=A4)
            c.setTitle(title)
            
            # Position on page (centered)
            page_width, page_height = A4
            qr_x = (page_width - size_width * mm) / 2
            qr_y = (page_height - size_height * mm) / 2
            
            # Convert image to temp PNG for embedding
            tmp_path = os.path.join(app.config['EXPORTED_FOLDER'], f"tmp_{uuid.uuid4().hex}.png")
            img.save(tmp_path, format='PNG')
            
            # Add to PDF
            c.drawImage(tmp_path, qr_x, qr_y, width=size_width * mm, height=size_height * mm)
            c.save()
            
            # Remove temp file
            os.remove(tmp_path)
            
        elif export_format == 'eps':
            # Export as EPS
            dpi = int(request.form.get('dpi', 300))
            
            # EPS needs to be in RGB or CMYK
            if img.mode not in ['RGB', 'CMYK']:
                img = img.convert('RGB')
            
            # Save as EPS
            img.save(output_path, format='EPS', dpi=(dpi, dpi))
            
        else:
            return jsonify({'error': f'Unsupported export format: {export_format}'}), 400
        
        return jsonify({
            'success': True,
            'export_format': export_format,
            'download_url': f"/exports/{filename}"
        })
        
    except Exception as e:
        print(f"Error exporting QR code: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/qrcodes/<filename>')
def serve_qrcode(filename):
    """Serve generated QR code file"""
    return send_from_directory(app.config['GENERATED_FOLDER'], filename)

@app.route('/exports/<filename>')
def serve_export(filename):
    """Serve exported QR code file"""
    return send_from_directory(app.config['EXPORTED_FOLDER'], filename)

@app.route('/')
def index():
    """Serve the main app"""
    return app.send_static_file('index.html')

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=not os.environ.get('PRODUCTION'))
