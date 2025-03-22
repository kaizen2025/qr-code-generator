#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Enhanced QR code preview generator module.
Provides real-time preview generation with various styling options
compatible with QR Code Monkey functionality.
"""

import io
import base64
import qrcode
import math
from PIL import Image, ImageDraw, ImageOps, ImageFilter, ImageChops
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

class QRCodePreviewGenerator:
    """
    Enhanced class for generating QR code previews with various styling options.
    Supports real-time previews with custom shapes, colors, and patterns.
    """

    def __init__(self):
        """
        Initialize the QR code preview generator with all available styles.
        """
        # Dictionary of available module drawers
        self.module_drawers = {
            'square': SquareModuleDrawer(),
            'gapped_square': GappedSquareModuleDrawer(gap_width=0.15),
            'circle': CircleModuleDrawer(),
            'rounded': RoundedModuleDrawer(),
            'vertical_bars': VerticalBarsDrawer(),
            'horizontal_bars': HorizontalBarsDrawer(),
            'dot': CircleModuleDrawer(radius_ratio=0.6),
            'mini_square': SquareModuleDrawer(module_scale=0.8)
        }
        
        # Dictionary of available color masks
        self.color_masks = {
            'solid': SolidFillColorMask,
            'radial_gradient': RadialGradiantColorMask,
            'square_gradient': SquareGradiantColorMask,
            'horizontal_gradient': HorizontalGradiantColorMask,
            'vertical_gradient': VerticalGradiantColorMask
        }
        
        # Dictionary of predefined styles
        self.predefined_styles = {
            'classic': {
                'module_drawer': 'square',
                'color_mask': 'solid',
                'front_color': (0, 0, 0),
                'back_color': (255, 255, 255)
            },
            'rounded': {
                'module_drawer': 'rounded',
                'color_mask': 'solid',
                'front_color': (0, 0, 0),
                'back_color': (255, 255, 255)
            },
            'dots': {
                'module_drawer': 'circle',
                'color_mask': 'solid',
                'front_color': (0, 0, 0),
                'back_color': (255, 255, 255)
            },
            'modern_blue': {
                'module_drawer': 'rounded',
                'color_mask': 'vertical_gradient',
                'front_color': (0, 102, 204),
                'bottom_color': (0, 51, 153),
                'back_color': (255, 255, 255)
            },
            'sunset': {
                'module_drawer': 'circle',
                'color_mask': 'horizontal_gradient',
                'front_color': (255, 102, 0),
                'bottom_color': (204, 0, 0),
                'back_color': (255, 255, 255)
            },
            'forest': {
                'module_drawer': 'square',
                'color_mask': 'radial_gradient',
                'front_color': (0, 102, 0),
                'edge_color': (0, 51, 0),
                'gradient_center': (0.5, 0.5),
                'back_color': (255, 255, 255)
            },
            'ocean': {
                'module_drawer': 'rounded',
                'color_mask': 'radial_gradient',
                'front_color': (0, 153, 204),
                'edge_color': (0, 51, 102),
                'gradient_center': (0.5, 0.5),
                'back_color': (255, 255, 255)
            },
            'barcode': {
                'module_drawer': 'vertical_bars',
                'color_mask': 'solid',
                'front_color': (0, 0, 0),
                'back_color': (255, 255, 255)
            },
            'elegant': {
                'module_drawer': 'gapped_square',
                'color_mask': 'solid',
                'front_color': (51, 51, 51),
                'back_color': (245, 245, 245)
            }
        }
        
        # Dictionary of eye shapes
        self.eye_shapes = {
            'square': self._draw_square_eye,
            'circle': self._draw_circle_eye,
            'rounded': self._draw_rounded_eye,
            'diamond': self._draw_diamond_eye,
            'cushion': self._draw_cushion_eye,
            'star': self._draw_star_eye,
            'dots': self._draw_dots_eye,
            'rounded_rect': self._draw_rounded_rect_eye,
            'flower': self._draw_flower_eye,
            'leaf': self._draw_leaf_eye
        }
        
        # Dictionary of frame shapes
        self.frame_shapes = {
            'square': self._draw_square_frame,
            'rounded_square': self._draw_rounded_square_frame,
            'circle': self._draw_circle_frame,
            'rounded': self._draw_rounded_frame,
            'diamond': self._draw_diamond_frame,
            'corner_cut': self._draw_corner_cut_frame,
            'jagged': self._draw_jagged_frame,
            'dots': self._draw_dots_frame,
            'pointed': self._draw_pointed_frame,
            'pixel': self._draw_pixel_frame
        }
    
    def generate_preview_base64(self, data, preview_type='basic', **options):
        """
        Generate a QR code preview and return it as a base64 encoded string.
        
        Args:
            data (str): Data to encode in the QR code
            preview_type (str): Type of preview to generate:
                - 'basic': Basic QR code
                - 'custom': Custom colors and shapes
                - 'styled': Styled with module drawer and color mask
                - 'predefined': Using a predefined style
                - 'logo': QR code with logo
                - 'social': QR code with social media theme
                - 'custom_shape': Custom module, frame, and eye shapes
            **options: Additional options for customization
            
        Returns:
            str: Base64 encoded image data
        """
        # Default parameters
        version = options.get('version', 1)
        error_correction = options.get('error_correction', qrcode.constants.ERROR_CORRECT_M)
        box_size = options.get('box_size', 10)
        border = options.get('border', 4)
        
        # Map error correction level from integer to constant
        error_correction_map = {
            0: qrcode.constants.ERROR_CORRECT_L,
            1: qrcode.constants.ERROR_CORRECT_M,
            2: qrcode.constants.ERROR_CORRECT_Q,
            3: qrcode.constants.ERROR_CORRECT_H
        }
        
        # Convert string/integer error correction to constants
        if isinstance(error_correction, str) and error_correction.isdigit():
            error_correction = int(error_correction)
        if isinstance(error_correction, int) and error_correction in error_correction_map:
            error_correction = error_correction_map[error_correction]
        
        # Generate QR code based on preview type
        if preview_type == 'basic':
            img = self._generate_basic_preview(data, version, error_correction, box_size, border)
        
        elif preview_type == 'custom':
            fill_color = self._parse_color(options.get('fill_color', "black"))
            back_color = self._parse_color(options.get('back_color', "white"))
            
            # Get shapes
            module_shape = options.get('module_shape', 'square')
            frame_shape = options.get('frame_shape', 'square')
            eye_shape = options.get('eye_shape', 'square')
            
            img = self._generate_custom_preview(
                data, version, error_correction, box_size, border,
                fill_color, back_color, module_shape, frame_shape, eye_shape
            )
        
        elif preview_type == 'styled':
            module_drawer_name = options.get('module_drawer', 'square')
            color_mask_name = options.get('color_mask', 'solid')
            img = self._generate_styled_preview(
                data, version, error_correction, box_size, border,
                module_drawer_name, color_mask_name, **options
            )
        
        elif preview_type == 'predefined':
            style_name = options.get('style_name', 'classic')
            img = self._generate_predefined_preview(
                data, version, error_correction, box_size, border, style_name
            )
        
        elif preview_type == 'logo':
            logo_data = options.get('logo_data')
            if not logo_data:
                raise ValueError("Missing logo data for logo preview")
            
            fill_color = self._parse_color(options.get('fill_color', "black"))
            back_color = self._parse_color(options.get('back_color', "white"))
            logo_size = float(options.get('logo_size', 0.2))
            
            img = self._generate_logo_preview(
                data, version, error_correction, box_size, border,
                fill_color, back_color, logo_data, logo_size
            )
        
        elif preview_type == 'social':
            social_platform = options.get('social_platform')
            if not social_platform:
                raise ValueError("Missing social platform for social preview")
            
            fill_color = self._parse_color(options.get('fill_color', "#000000"))
            back_color = self._parse_color(options.get('back_color', "#FFFFFF"))
            
            # Check for platform color override
            use_platform_color = options.get('use_platform_color', False)
            if use_platform_color and social_platform:
                # Here we would ideally look up the platform color
                # This is simplified for the preview
                platform_colors = {
                    'facebook': '#1877F2',
                    'twitter': '#1DA1F2',
                    'instagram': '#E4405F',
                    'linkedin': '#0A66C2',
                    'youtube': '#FF0000',
                    'tiktok': '#000000',
                    'snapchat': '#FFFC00',
                    'pinterest': '#E60023',
                    'whatsapp': '#25D366',
                    'website': '#333333'
                }
                fill_color = self._parse_color(platform_colors.get(social_platform, "#000000"))
            
            img = self._generate_social_preview(
                data, version, error_correction, box_size, border,
                fill_color, back_color, social_platform
            )
        
        elif preview_type == 'custom_shape':
            module_shape = options.get('module_shape', 'square')
            frame_shape = options.get('frame_shape', 'square')
            eye_shape = options.get('eye_shape', 'square')
            fill_color = self._parse_color(options.get('fill_color', "black"))
            back_color = self._parse_color(options.get('back_color', "white"))
            
            img = self._generate_custom_shape_preview(
                data, version, error_correction, box_size, border,
                module_shape, frame_shape, eye_shape, fill_color, back_color
            )
        
        else:
            raise ValueError(f"Unknown preview type: {preview_type}")
        
        # Convert image to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    def _generate_basic_preview(self, data, version, error_correction, box_size, border):
        """Generate a basic QR code preview."""
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        return qr.make_image(fill_color="black", back_color="white")
    
    def _generate_custom_preview(self, data, version, error_correction, box_size, border,
                                fill_color, back_color, module_shape, frame_shape, eye_shape):
        """Generate a custom QR code preview with specified colors and shapes."""
        # Create QR code with basic settings
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Get the module drawer
        module_drawer = self.module_drawers.get(module_shape, self.module_drawers['square'])
        
        # Create basic QR image with the specified module drawer
        qr_img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=SolidFillColorMask(
                front_color=fill_color,
                back_color=back_color
            )
        )
        
        # Convert to PIL Image
        img_pil = qr_img.get_image() if hasattr(qr_img, 'get_image') else qr_img
        
        # Customize the eyes and frames if specified
        if frame_shape != 'square' or eye_shape != 'square':
            img_pil = self._customize_eyes(img_pil, qr, eye_shape, frame_shape, fill_color)
        
        return img_pil
    
    def _generate_styled_preview(self, data, version, error_correction, box_size, border,
                               module_drawer_name, color_mask_name, **options):
        """Generate a styled QR code preview with module drawer and color mask."""
        # Get module drawer
        module_drawer = self.module_drawers.get(module_drawer_name, self.module_drawers['square'])
        
        # Get color mask class
        color_mask_class = self.color_masks.get(color_mask_name, SolidFillColorMask)
        
        # Set up color mask options
        color_mask_kwargs = {}
        
        if color_mask_name == 'solid':
            color_mask_kwargs = {
                'front_color': self._parse_color(options.get('front_color', (0, 0, 0))),
                'back_color': self._parse_color(options.get('back_color', (255, 255, 255)))
            }
        elif color_mask_name == 'radial_gradient' or color_mask_name == 'square_gradient':
            color_mask_kwargs = {
                'center_color': self._parse_color(options.get('front_color', (0, 0, 0))),
                'edge_color': self._parse_color(options.get('edge_color', (100, 100, 100))),
                'back_color': self._parse_color(options.get('back_color', (255, 255, 255)))
            }
            if 'gradient_center' in options:
                color_mask_kwargs['center'] = options.get('gradient_center')
            elif 'gradient_center_x' in options and 'gradient_center_y' in options:
                try:
                    cx = float(options.get('gradient_center_x', 0.5))
                    cy = float(options.get('gradient_center_y', 0.5))
                    color_mask_kwargs['center'] = (cx, cy)
                except (ValueError, TypeError):
                    # Default center if conversion fails
                    color_mask_kwargs['center'] = (0.5, 0.5)
        elif color_mask_name == 'horizontal_gradient':
            color_mask_kwargs = {
                'left_color': self._parse_color(options.get('front_color', (0, 0, 0))),
                'right_color': self._parse_color(options.get('edge_color', (100, 100, 100))),
                'back_color': self._parse_color(options.get('back_color', (255, 255, 255)))
            }
        elif color_mask_name == 'vertical_gradient':
            color_mask_kwargs = {
                'top_color': self._parse_color(options.get('front_color', (0, 0, 0))),
                'bottom_color': self._parse_color(options.get('edge_color', (100, 100, 100))),
                'back_color': self._parse_color(options.get('back_color', (255, 255, 255)))
            }
        
        # Create color mask
        color_mask = color_mask_class(**color_mask_kwargs)
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create styled image
        return qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=color_mask
        )
    
    def _generate_predefined_preview(self, data, version, error_correction, box_size, border, style_name):
        """Generate a QR code preview with a predefined style."""
        # Check if style exists
        if style_name not in self.predefined_styles:
            raise ValueError(f"Unknown style: {style_name}. Available styles: {', '.join(self.predefined_styles.keys())}")
        
        # Get style options
        style_options = self.predefined_styles[style_name].copy()
        
        # Add basic options
        style_options['version'] = version
        style_options['error_correction'] = error_correction
        style_options['box_size'] = box_size
        style_options['border'] = border
        
        # Generate styled preview
        return self._generate_styled_preview(
            data, version, error_correction, box_size, border,
            style_options['module_drawer'],
            style_options['color_mask'],
            **style_options
        )
    
    def _generate_logo_preview(self, data, version, error_correction, box_size, border,
                              fill_color, back_color, logo_data, logo_size):
        """Generate a QR code preview with a centered logo."""
        # Generate QR code
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create QR code image
        qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGBA')
        
        try:
            # Decode logo from base64
            logo_data = logo_data.split(',')[1] if ',' in logo_data else logo_data
            logo_binary = base64.b64decode(logo_data)
            logo = Image.open(io.BytesIO(logo_binary)).convert('RGBA')
            
            # Calculate logo size
            qr_width, qr_height = qr_img.size
            logo_max_size = int(min(qr_width, qr_height) * logo_size)
            
            # Resize logo while maintaining aspect ratio
            logo_width, logo_height = logo.size
            ratio = min(logo_max_size / logo_width, logo_max_size / logo_height)
            new_logo_width = int(logo_width * ratio)
            new_logo_height = int(logo_height * ratio)
            logo = logo.resize((new_logo_width, new_logo_height), Image.LANCZOS)
            
            # Add white padding around the logo
            padding = 10
            logo_with_padding = Image.new('RGBA', (new_logo_width + padding * 2, new_logo_height + padding * 2), (255, 255, 255, 255))
            logo_with_padding.paste(logo, (padding, padding), logo)
            
            # Calculate logo position (center)
            position = ((qr_width - logo_with_padding.width) // 2, (qr_height - logo_with_padding.height) // 2)
            
            # Create result image
            result = Image.new('RGBA', qr_img.size, (0, 0, 0, 0))
            result.paste(qr_img, (0, 0))
            result.paste(logo_with_padding, position, logo_with_padding)
            
            return result
            
        except Exception as e:
            print(f"Error adding logo: {e}")
            # Return QR code without logo in case of error
            return qr_img
    
    def _generate_social_preview(self, data, version, error_correction, box_size, border,
                               fill_color, back_color, social_platform):
        """Generate a QR code preview with social media theme."""
        # Generate QR code
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create QR code image
        qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGBA')
        qr_width, qr_height = qr_img.size
        
        # Create a new image for the result
        result = Image.new('RGBA', qr_img.size, (0, 0, 0, 0))
        result.paste(qr_img, (0, 0))
        
        # Add social platform icon placeholder in the center
        social_icon_size = int(min(qr_width, qr_height) * 0.2)
        social_bg = Image.new('RGBA', (social_icon_size, social_icon_size), (255, 255, 255, 255))
        draw = ImageDraw.Draw(social_bg)
        
        # Draw a shape representing the platform
        if social_platform in ['facebook', 'twitter', 'linkedin']:
            # Blue circle
            draw.ellipse([0, 0, social_icon_size, social_icon_size], fill=(59, 89, 152, 255))
        elif social_platform in ['instagram', 'youtube']:
            # Pink/red square
            draw.rectangle([0, 0, social_icon_size, social_icon_size], fill=(225, 48, 108, 255))
        elif social_platform == 'snapchat':
            # Yellow square
            draw.rectangle([0, 0, social_icon_size, social_icon_size], fill=(255, 252, 0, 255))
        else:
            # Green circle
            draw.ellipse([0, 0, social_icon_size, social_icon_size], fill=(37, 211, 102, 255))
        
        # Add platform initial
        if len(social_platform) > 0:
            # Draw the first letter in white
            text_x = social_icon_size // 2
            text_y = social_icon_size // 2
            letter = social_platform[0].upper()
            # Note: Draw text in center if a proper font is available
            
        # Add social icon at the center
        position = ((qr_width - social_icon_size) // 2, (qr_height - social_icon_size) // 2)
        result.paste(social_bg, position, social_bg)
        
        return result
    
    def _generate_custom_shape_preview(self, data, version, error_correction, box_size, border,
                                     module_shape, frame_shape, eye_shape, fill_color, back_color):
        """Generate a QR code preview with custom module, frame, and eye shapes."""
        # Get module drawer
        module_drawer = self.module_drawers.get(module_shape, self.module_drawers['square'])
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create QR code image
        qr_img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=SolidFillColorMask(
                front_color=fill_color,
                back_color=back_color
            )
        )
        
        # Convert to PIL Image
        img_pil = qr_img.get_image() if hasattr(qr_img, 'get_image') else qr_img
        
        # Customize the eyes
        img_pil = self._customize_eyes(img_pil, qr, eye_shape, frame_shape, fill_color)
        
        return img_pil
    
    def _customize_eyes(self, qr_image, qr_code, eye_shape, frame_shape, fill_color):
        """
        Customize the eyes and frames of a QR code.
        
        Args:
            qr_image: PIL Image of the QR code
            qr_code: QRCode object
            eye_shape: Shape of the eyes
            frame_shape: Shape of the frames
            fill_color: Color of the eyes and frames
            
        Returns:
            PIL.Image: Modified QR code image
        """
        # Create a copy of the QR code image
        img = qr_image.copy().convert('RGBA')
        
        # Get the eye function and frame function
        eye_func = self.eye_shapes.get(eye_shape, self._draw_square_eye)
        frame_func = self.frame_shapes.get(frame_shape, self._draw_square_frame)
        
        # Calculate eye positions
        box_size = qr_code.box_size
        border = qr_code.border
        
        # Convert fill_color to RGB tuple if it's a string
        if isinstance(fill_color, str):
            fill_color = self._parse_color(fill_color)
        
        # Positions for the 3 eyes (top-left, top-right, bottom-left)
        positions = [
            (border, border),  # Top-left
            (qr_code.modules_count - 7 - border + 1, border),  # Top-right
            (border, qr_code.modules_count - 7 - border + 1)   # Bottom-left
        ]
        
        # Size of each eye (7 modules)
        eye_size = 7 * box_size
        
        # Create a transparent overlay for the eyes
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Draw each eye
        for x_pos, y_pos in positions:
            x = x_pos * box_size
            y = y_pos * box_size
            
            # Create a mask to remove the original eye
            mask = Image.new('RGBA', img.size, (0, 0, 0, 0))
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.rectangle([x, y, x + eye_size, y + eye_size], fill=(255, 255, 255, 255))
            
            # Remove the original eye by applying the mask
            cutout = ImageChops.multiply(img, ImageChops.invert(mask))
            
            # Draw the custom frame
            frame_func(draw, x, y, eye_size, fill_color)
            
            # Draw the eye on top
            eye_func(draw, x + eye_size//4, y + eye_size//4, eye_size//2, fill_color)
            
            # Paste the cutout back
            img = Image.alpha_composite(cutout, overlay)
        
        return img.convert('RGB')
    
    # Eye shape drawing functions
    def _draw_square_eye(self, draw, x, y, size, color):
        """Draw a square eye."""
        draw.rectangle([x, y, x + size, y + size], fill=color)
    
    def _draw_circle_eye(self, draw, x, y, size, color):
        """Draw a circular eye."""
        draw.ellipse([x, y, x + size, y + size], fill=color)
    
    def _draw_rounded_eye(self, draw, x, y, size, color):
        """Draw an eye with rounded corners."""
        radius = size // 4
        # Main rectangle
        draw.rectangle([x + radius, y, x + size - radius, y + size], fill=color)
        draw.rectangle([x, y + radius, x + size, y + size - radius], fill=color)
        # Corner arcs
        draw.pieslice([x, y, x + radius * 2, y + radius * 2], 180, 270, fill=color)
        draw.pieslice([x + size - radius * 2, y, x + size, y + radius * 2], 270, 360, fill=color)
        draw.pieslice([x, y + size - radius * 2, x + radius * 2, y + size], 90, 180, fill=color)
        draw.pieslice([x + size - radius * 2, y + size - radius * 2, x + size, y + size], 0, 90, fill=color)
    
    def _draw_diamond_eye(self, draw, x, y, size, color):
        """Draw a diamond-shaped eye."""
        center_x, center_y = x + size // 2, y + size // 2
        points = [
            (center_x, y),  # Top
            (x + size, center_y),  # Right
            (center_x, y + size),  # Bottom
            (x, center_y)  # Left
        ]
        draw.polygon(points, fill=color)
    
    def _draw_cushion_eye(self, draw, x, y, size, color):
        """Draw a cushion-shaped eye."""
        # Start with a square
        draw.rectangle([x, y, x + size, y + size], fill=color)
        
        # Add curved inward corners
        curve_size = size // 3
        # Top-left
        draw.pieslice([x - curve_size, y - curve_size, x + curve_size, y + curve_size],
                      0, 90, fill=(0, 0, 0, 0))
        # Top-right
        draw.pieslice([x + size - curve_size, y - curve_size, x + size + curve_size, y + curve_size],
                      90, 180, fill=(0, 0, 0, 0))
        # Bottom-right
        draw.pieslice([x + size - curve_size, y + size - curve_size, x + size + curve_size, y + size + curve_size],
                      180, 270, fill=(0, 0, 0, 0))
        # Bottom-left
        draw.pieslice([x - curve_size, y + size - curve_size, x + curve_size, y + size + curve_size],
                      270, 360, fill=(0, 0, 0, 0))
    
    def _draw_star_eye(self, draw, x, y, size, color):
        """Draw a star-shaped eye."""
        # Simple 4-point star
        center_x, center_y = x + size // 2, y + size // 2
        outer_radius = size // 2
        inner_radius = size // 4
        
        points = []
        for i in range(8):
            radius = outer_radius if i % 2 == 0 else inner_radius
            angle = i * (360 / 8)
            px = center_x + int(radius * math.cos(math.radians(angle)))
            py = center_y + int(radius * math.sin(math.radians(angle)))
            points.append((px, py))
        
        draw.polygon(points, fill=color)
    
    def _draw_dots_eye(self, draw, x, y, size, color):
        """Draw an eye made of dots."""
        # Main center dot
        center_x, center_y = x + size // 2, y + size // 2
        radius = size // 3
        draw.ellipse([center_x - radius, center_y - radius, 
                     center_x + radius, center_y + radius], fill=color)
        
        # Smaller surrounding dots
        small_radius = size // 6
        offset = radius + small_radius
        
        # Top dot
        draw.ellipse([center_x - small_radius, center_y - offset - small_radius,
                     center_x + small_radius, center_y - offset + small_radius], fill=color)
        # Right dot
        draw.ellipse([center_x + offset - small_radius, center_y - small_radius,
                     center_x + offset + small_radius, center_y + small_radius], fill=color)
        # Bottom dot
        draw.ellipse([center_x - small_radius, center_y + offset - small_radius,
                     center_x + small_radius, center_y + offset + small_radius], fill=color)
        # Left dot
        draw.ellipse([center_x - offset - small_radius, center_y - small_radius,
                     center_x - offset + small_radius, center_y + small_radius], fill=color)
    
    def _draw_rounded_rect_eye(self, draw, x, y, size, color):
        """Draw a rounded rectangle eye."""
        # Similar to rounded eye but with less rounding
        radius = size // 8
        # Main rectangle
        draw.rectangle([x + radius, y, x + size - radius, y + size], fill=color)
        draw.rectangle([x, y + radius, x + size, y + size - radius], fill=color)
        # Corner arcs
        draw.pieslice([x, y, x + radius * 2, y + radius * 2], 180, 270, fill=color)
        draw.pieslice([x + size - radius * 2, y, x + size, y + radius * 2], 270, 360, fill=color)
        draw.pieslice([x, y + size - radius * 2, x + radius * 2, y + size], 90, 180, fill=color)
        draw.pieslice([x + size - radius * 2, y + size - radius * 2, x + size, y + size], 0, 90, fill=color)
    
    def _draw_flower_eye(self, draw, x, y, size, color):
        """Draw a flower-shaped eye."""
        center_x, center_y = x + size // 2, y + size // 2
        radius = size // 3
        
        # Center circle
        draw.ellipse([center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius], fill=color)
        
        # Petals
        petal_radius = radius * 0.8
        for angle in range(0, 360, 90):
            petal_x = center_x + int(radius * math.cos(math.radians(angle)))
            petal_y = center_y + int(radius * math.sin(math.radians(angle)))
            draw.ellipse([petal_x - petal_radius, petal_y - petal_radius,
                         petal_x + petal_radius, petal_y + petal_radius], fill=color)
    
    def _draw_leaf_eye(self, draw, x, y, size, color):
        """Draw a leaf-shaped eye."""
        # Simplified leaf shape (triangular)
        center_x = x + size // 2
        points = [
            (center_x, y),  # Top
            (x + size, y + size),  # Bottom right
            (x, y + size)  # Bottom left
        ]
        draw.polygon(points, fill=color)
    
    # Frame shape drawing functions
    def _draw_square_frame(self, draw, x, y, size, color):
        """Draw a square frame."""
        thickness = size // 5
        draw.rectangle([x, y, x + size, y + size], fill=color)
        draw.rectangle([x + thickness, y + thickness, 
                       x + size - thickness, y + size - thickness],
                      fill=(0, 0, 0, 0))
    
    def _draw_rounded_square_frame(self, draw, x, y, size, color):
        """Draw a rounded square frame."""
        thickness = size // 5
        radius = size // 8
        
        # Outer rounded rectangle
        draw.rectangle([x + radius, y, x + size - radius, y + size], fill=color)
        draw.rectangle([x, y + radius, x + size, y + size - radius], fill=color)
        # Outer corner arcs
        draw.pieslice([x, y, x + radius * 2, y + radius * 2], 180, 270, fill=color)
        draw.pieslice([x + size - radius * 2, y, x + size, y + radius * 2], 270, 360, fill=color)
        draw.pieslice([x, y + size - radius * 2, x + radius * 2, y + size], 90, 180, fill=color)
        draw.pieslice([x + size - radius * 2, y + size - radius * 2, x + size, y + size], 0, 90, fill=color)
        
        # Inner rounded rectangle (transparent)
        inner_radius = max(1, radius - thickness // 2)
        inner_x = x + thickness
        inner_y = y + thickness
        inner_size = size - 2 * thickness
        
        draw.rectangle([inner_x + inner_radius, inner_y, 
                       inner_x + inner_size - inner_radius, inner_y + inner_size], 
                      fill=(0, 0, 0, 0))
        draw.rectangle([inner_x, inner_y + inner_radius, 
                       inner_x + inner_size, inner_y + inner_size - inner_radius], 
                      fill=(0, 0, 0, 0))
        
        # Inner corner arcs
        draw.pieslice([inner_x, inner_y, inner_x + inner_radius * 2, inner_y + inner_radius * 2], 
                     180, 270, fill=(0, 0, 0, 0))
        draw.pieslice([inner_x + inner_size - inner_radius * 2, inner_y, 
                      inner_x + inner_size, inner_y + inner_radius * 2], 
                     270, 360, fill=(0, 0, 0, 0))
        draw.pieslice([inner_x, inner_y + inner_size - inner_radius * 2, 
                      inner_x + inner_radius * 2, inner_y + inner_size], 
                     90, 180, fill=(0, 0, 0, 0))
        draw.pieslice([inner_x + inner_size - inner_radius * 2, inner_y + inner_size - inner_radius * 2, 
                      inner_x + inner_size, inner_y + inner_size], 
                     0, 90, fill=(0, 0, 0, 0))
    
    def _draw_circle_frame(self, draw, x, y, size, color):
        """Draw a circular frame."""
        thickness = size // 5
        # Outer circle
        draw.ellipse([x, y, x + size, y + size], fill=color)
        # Inner circle (transparent)
        draw.ellipse([x + thickness, y + thickness, 
                     x + size - thickness, y + size - thickness], 
                    fill=(0, 0, 0, 0))
    
    def _draw_rounded_frame(self, draw, x, y, size, color):
        """Draw a heavily rounded frame."""
        thickness = size // 5
        radius = size // 3
        
        # Outer rounded rectangle
        draw.rectangle([x + radius, y, x + size - radius, y + size], fill=color)
        draw.rectangle([x, y + radius, x + size, y + size - radius], fill=color)
        # Outer corner arcs
        draw.pieslice([x, y, x + radius * 2, y + radius * 2], 180, 270, fill=color)
        draw.pieslice([x + size - radius * 2, y, x + size, y + radius * 2], 270, 360, fill=color)
        draw.pieslice([x, y + size - radius * 2, x + radius * 2, y + size], 90, 180, fill=color)
        draw.pieslice([x + size - radius * 2, y + size - radius * 2, x + size, y + size], 0, 90, fill=color)
        
        # Inner rounded rectangle (transparent)
        inner_radius = max(1, radius - thickness)
        inner_x = x + thickness
        inner_y = y + thickness
        inner_size = size - 2 * thickness
        
        draw.rectangle([inner_x + inner_radius, inner_y, 
                       inner_x + inner_size - inner_radius, inner_y + inner_size], 
                      fill=(0, 0, 0, 0))
        draw.rectangle([inner_x, inner_y + inner_radius, 
                       inner_x + inner_size, inner_y + inner_size - inner_radius], 
                      fill=(0, 0, 0, 0))
        
        # Inner corner arcs
        draw.pieslice([inner_x, inner_y, inner_x + inner_radius * 2, inner_y + inner_radius * 2], 
                     180, 270, fill=(0, 0, 0, 0))
        draw.pieslice([inner_x + inner_size - inner_radius * 2, inner_y, 
                      inner_x + inner_size, inner_y + inner_radius * 2], 
                     270, 360, fill=(0, 0, 0, 0))
        draw.pieslice([inner_x, inner_y + inner_size - inner_radius * 2, 
                      inner_x + inner_radius * 2, inner_y + inner_size], 
                     90, 180, fill=(0, 0, 0, 0))
        draw.pieslice([inner_x + inner_size - inner_radius * 2, inner_y + inner_size - inner_radius * 2, 
                      inner_x + inner_size, inner_y + inner_size], 
                     0, 90, fill=(0, 0, 0, 0))
    
    def _draw_diamond_frame(self, draw, x, y, size, color):
        """Draw a diamond-shaped frame."""
        thickness = size // 5
        center_x, center_y = x + size // 2, y + size // 2
        
        # Outer diamond
        outer_points = [
            (center_x, y),  # Top
            (x + size, center_y),  # Right
            (center_x, y + size),  # Bottom
            (x, center_y)  # Left
        ]
        draw.polygon(outer_points, fill=color)
        
        # Inner diamond (transparent)
        inner_offset = thickness * 1.4  # Slightly increase for diamond shape
        inner_points = [
            (center_x, y + inner_offset),  # Top
            (x + size - inner_offset, center_y),  # Right
            (center_x, y + size - inner_offset),  # Bottom
            (x + inner_offset, center_y)  # Left
        ]
        draw.polygon(inner_points, fill=(0, 0, 0, 0))
    
    def _draw_corner_cut_frame(self, draw, x, y, size, color):
        """Draw a frame with cut corners."""
        thickness = size // 5
        cut_size = size // 5
        
        # Outer polygon with cut corners
        outer_points = [
            (x + cut_size, y),  # Top left
            (x + size - cut_size, y),  # Top right
            (x + size, y + cut_size),  # Right top
            (x + size, y + size - cut_size),  # Right bottom
            (x + size - cut_size, y + size),  # Bottom right
            (x + cut_size, y + size),  # Bottom left
            (x, y + size - cut_size),  # Left bottom
            (x, y + cut_size)  # Left top
        ]
        draw.polygon(outer_points, fill=color)
        
        # Inner polygon with cut corners (transparent)
        inner_x = x + thickness
        inner_y = y + thickness
        inner_size = size - 2 * thickness
        inner_cut = max(1, cut_size - thickness)
        
        inner_points = [
            (inner_x + inner_cut, inner_y),  # Top left
            (inner_x + inner_size - inner_cut, inner_y),  # Top right
            (inner_x + inner_size, inner_y + inner_cut),  # Right top
            (inner_x + inner_size, inner_y + inner_size - inner_cut),  # Right bottom
            (inner_x + inner_size - inner_cut, inner_y + inner_size),  # Bottom right
            (inner_x + inner_cut, inner_y + inner_size),  # Bottom left
            (inner_x, inner_y + inner_size - inner_cut),  # Left bottom
            (inner_x, inner_y + inner_cut)  # Left top
        ]
        draw.polygon(inner_points, fill=(0, 0, 0, 0))
    
    def _draw_jagged_frame(self, draw, x, y, size, color):
        """Draw a jagged frame."""
        thickness = size // 5
        teeth = 3  # Number of teeth per side
        teeth_depth = size // 10
        
        # Outer jagged polygon
        outer_points = []
        
        # Top side
        for i in range(teeth + 1):
            x_pos = x + i * (size / teeth)
            y_pos = y if i % 2 == 0 else y - teeth_depth
            outer_points.append((x_pos, y_pos))
        
        # Right side
        for i in range(1, teeth + 1):
            x_pos = x + size if i % 2 == 0 else x + size + teeth_depth
            y_pos = y + i * (size / teeth)
            outer_points.append((x_pos, y_pos))
        
        # Bottom side
        for i in range(teeth, -1, -1):
            x_pos = x + i * (size / teeth)
            y_pos = y + size if i % 2 == 0 else y + size + teeth_depth
            outer_points.append((x_pos, y_pos))
        
        # Left side
        for i in range(teeth, 0, -1):
            x_pos = x if i % 2 == 0 else x - teeth_depth
            y_pos = y + i * (size / teeth)
            outer_points.append((x_pos, y_pos))
        
        draw.polygon(outer_points, fill=color)
        
        # Inner jagged polygon (transparent)
        inner_x = x + thickness
        inner_y = y + thickness
        inner_size = size - 2 * thickness
        inner_teeth_depth = max(1, teeth_depth - thickness // 2)
        
        inner_points = []
        
        # Top side
        for i in range(teeth + 1):
            x_pos = inner_x + i * (inner_size / teeth)
            y_pos = inner_y if i % 2 == 0 else inner_y - inner_teeth_depth
            inner_points.append((x_pos, y_pos))
        
        # Right side
        for i in range(1, teeth + 1):
            x_pos = inner_x + inner_size if i % 2 == 0 else inner_x + inner_size + inner_teeth_depth
            y_pos = inner_y + i * (inner_size / teeth)
            inner_points.append((x_pos, y_pos))
        
        # Bottom side
        for i in range(teeth, -1, -1):
            x_pos = inner_x + i * (inner_size / teeth)
            y_pos = inner_y + inner_size if i % 2 == 0 else inner_y + inner_size + inner_teeth_depth
            inner_points.append((x_pos, y_pos))
        
        # Left side
        for i in range(teeth, 0, -1):
            x_pos = inner_x if i % 2 == 0 else inner_x - inner_teeth_depth
            y_pos = inner_y + i * (inner_size / teeth)
            inner_points.append((x_pos, y_pos))
        
        draw.polygon(inner_points, fill=(0, 0, 0, 0))
    
    def _draw_dots_frame(self, draw, x, y, size, color):
        """Draw a frame made of dots."""
        # Number of dots per side
        num_dots = 8
        dot_radius = size // 15
        
        # Calculate dot positions
        positions = []
        
        # Top and bottom sides
        for i in range(num_dots):
            pos_x = x + i * size // (num_dots - 1)
            # Top side
            positions.append((pos_x, y))
            # Bottom side
            positions.append((pos_x, y + size))
        
        # Left and right sides (excluding corners which are already added)
        for i in range(1, num_dots - 1):
            pos_y = y + i * size // (num_dots - 1)
            # Left side
            positions.append((x, pos_y))
            # Right side
            positions.append((x + size, pos_y))
        
        # Draw dots
        for pos_x, pos_y in positions:
            draw.ellipse([pos_x - dot_radius, pos_y - dot_radius,
                         pos_x + dot_radius, pos_y + dot_radius], fill=color)
    
    def _draw_pointed_frame(self, draw, x, y, size, color):
        """Draw a frame with pointed corners."""
        thickness = size // 5
        point_size = size // 4
        
        # Outer polygon with pointed corners
        outer_points = [
            (x, y + point_size),  # Top left
            (x + point_size, y),  # Top left point
            (x + size - point_size, y),  # Top right
            (x + size, y + point_size),  # Top right point
            (x + size, y + size - point_size),  # Bottom right
            (x + size - point_size, y + size),  # Bottom right point
            (x + point_size, y + size),  # Bottom left
            (x, y + size - point_size)  # Bottom left point
        ]
        draw.polygon(outer_points, fill=color)
        
        # Inner polygon with pointed corners (transparent)
        inner_x = x + thickness
        inner_y = y + thickness
        inner_size = size - 2 * thickness
        inner_point = max(1, point_size - thickness)
        
        inner_points = [
            (inner_x, inner_y + inner_point),  # Top left
            (inner_x + inner_point, inner_y),  # Top left point
            (inner_x + inner_size - inner_point, inner_y),  # Top right
            (inner_x + inner_size, inner_y + inner_point),  # Top right point
            (inner_x + inner_size, inner_y + inner_size - inner_point),  # Bottom right
            (inner_x + inner_size - inner_point, inner_y + inner_size),  # Bottom right point
            (inner_x + inner_point, inner_y + inner_size),  # Bottom left
            (inner_x, inner_y + inner_size - inner_point)  # Bottom left point
        ]
        draw.polygon(inner_points, fill=(0, 0, 0, 0))
    
    def _draw_pixel_frame(self, draw, x, y, size, color):
        """Draw a pixelated frame."""
        thickness = size // 5
        pixel_size = size // 10
        
        # Draw outer pixelated frame
        for i in range(0, size + 1, pixel_size):
            for j in range(0, size + 1, pixel_size):
                # Draw only pixels on the border
                if (i < thickness or i >= size - thickness or
                    j < thickness or j >= size - thickness):
                    draw.rectangle([x + i, y + j, x + i + pixel_size - 1, y + j + pixel_size - 1],
                                 fill=color)
    
    def _parse_color(self, color):
        """
        Convert a color from various formats to RGB tuple.
        
        Args:
            color: Color value (string: '#RRGGBB', 'red', etc., or tuple: (r,g,b))
            
        Returns:
            tuple: RGB color tuple (r, g, b)
        """
        if isinstance(color, tuple):
            return color
        
        if isinstance(color, str):
            # Convert hex color codes
            if color.startswith('#'):
                color = color.lstrip('#')
                if len(color) == 3:  # Short format #RGB
                    return tuple(int(c + c, 16) for c in color)
                elif len(color) == 6:  # Long format #RRGGBB
                    return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            
            # Named colors
            color_map = {
                'black': (0, 0, 0),
                'white': (255, 255, 255),
                'red': (255, 0, 0),
                'green': (0, 255, 0),
                'blue': (0, 0, 255),
                'yellow': (255, 255, 0),
                'cyan': (0, 255, 255),
                'magenta': (255, 0, 255),
                'gray': (128, 128, 128),
                'orange': (255, 165, 0),
                'purple': (128, 0, 128)
            }
            if color.lower() in color_map:
                return color_map[color.lower()]
        
        # Default black if conversion fails
        return (0, 0, 0)
