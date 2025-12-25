#!/usr/bin/env python3
"""
Standalone HEIC to JPG Converter
Converts HEIC/HEIF images to JPG format
"""

import os
import sys
from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIC support
register_heif_opener()


def convert_heic_to_jpg(heic_path: str, output_path: str = None, quality: int = 95) -> str:
    """
    Converts a HEIC image to JPG format.
    
    Args:
        heic_path: Path to the HEIC file
        output_path: Output JPG path (if None, replaces extension)
        quality: JPG quality (1-100, default 95)
    
    Returns:
        Path to the converted JPG file
    """
    try:
        # Open HEIC image
        with Image.open(heic_path) as img:
            # Convert to RGB if necessary (HEIC might be in other modes)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background for transparency
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = rgb_img
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Determine output path
            if output_path is None:
                base_name = os.path.splitext(heic_path)[0]
                output_path = f"{base_name}.jpg"
            
            # Save as JPG
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            return output_path
    
    except Exception as e:
        raise Exception(f"Error converting HEIC to JPG: {str(e)}")


def main():
    """Main function for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage: python convert_heic.py <heic_file> [output_file] [quality]")
        print("  heic_file: Path to HEIC/HEIF file")
        print("  output_file: Optional output JPG path (default: same name with .jpg extension)")
        print("  quality: Optional JPG quality 1-100 (default: 95)")
        sys.exit(1)
    
    heic_path = sys.argv[1]
    
    if not os.path.exists(heic_path):
        print(f"Error: File not found: {heic_path}")
        sys.exit(1)
    
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    quality = int(sys.argv[3]) if len(sys.argv) > 3 else 95
    
    try:
        jpg_path = convert_heic_to_jpg(heic_path, output_path, quality)
        original_size = os.path.getsize(heic_path)
        converted_size = os.path.getsize(jpg_path)
        
        print(f"✅ Successfully converted: {heic_path}")
        print(f"   → {jpg_path}")
        print(f"   Original size: {original_size / 1024:.1f} KB")
        print(f"   JPG size: {converted_size / 1024:.1f} KB")
        print(f"   Size change: {((converted_size - original_size) / original_size) * 100:+.1f}%")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()



