print("Hello, World!")
import warnings
# Suppress pymp warnings
warnings.filterwarnings('ignore')
try:
    import pymp
    Pymp_AVAILABLE = True
except ImportError:
    Pymp_AVAILABLE = False
    # pymp is optional - script will work fine without it using sequential processing

from PIL import Image
import os
import shutil

def check_image_resolution(file_path: str, target_width_inch: float = 8.0):
    """
    Checks if an image is high-quality for a specific print size.
    Standard high quality is 300 DPI.
    """
    try:
        with Image.open(file_path) as img:
            # 1. Check Metadata DPI
            dpi_info = img.info.get('dpi')
            metadata_dpi = int(dpi_info[0]) if dpi_info else None
            
            # 2. Calculate Effective DPI (Pixels / Target Print Size)
            # Formula: DPI = Pixels / Inches
            effective_dpi = img.width / target_width_inch
            
            if metadata_dpi and metadata_dpi >= 300:
                return f"Success: Metadata confirms {metadata_dpi} DPI."
            
            if effective_dpi >= 300:
                return f"Success: Pixel density is high enough ({int(effective_dpi)} effective DPI)."
            
            return f"Error: Image too small. Only {int(effective_dpi)} DPI at {target_width_inch}\"."
    
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error: {str(e)}"


def copy_image_to_directory(source_path: str, destination_dir: str = "images/") -> str:
    """
    Copies an image file into the images directory.
    
    Args:
        source_path: Path to the source image file
        destination_dir: Destination directory (default: "images/")
    
    Returns:
        Success message or error message
    """
    try:
        # Create destination directory if it doesn't exist
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        # Validate that source file exists
        if not os.path.exists(source_path):
            return f"Error: Source file '{source_path}' not found."
        
        # Validate that source is an image
        if not source_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
            return f"Error: '{source_path}' is not a recognized image file."
        
        # Get filename and create destination path
        filename = os.path.basename(source_path)
        destination_path = os.path.join(destination_dir, filename)
        
        # Copy the file
        shutil.copy2(source_path, destination_path)
        return f"Success: Copied '{filename}' to {destination_dir}"
    
    except PermissionError:
        return f"Error: Permission denied when copying '{source_path}'"
    except Exception as e:
        return f"Error: {str(e)}"


# --- Parallel Processing Setup ---
image_dir = "images/"

if not os.path.exists(image_dir):
    os.makedirs(image_dir)

files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) 
         if f.lower().endswith(('.jpg', '.png'))]

if not files:
    print("No image files found in the images/ directory.")
else:
    results = {}
    
    if Pymp_AVAILABLE:
        # Use parallel processing with pymp
        with pymp.Parallel(4) as p:
            results = pymp.shared.dict()
            
            for i in p.range(len(files)):
                path = files[i]
                name = os.path.basename(path)
                results[name] = check_image_resolution(path)
    else:
        # Fallback to sequential processing
        for path in files:
            name = os.path.basename(path)
            results[name] = check_image_resolution(path)
    
    for filename, status in results.items():
        print(f"{filename}: {status}")

        