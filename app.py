import streamlit as st
from PIL import Image
import os
import shutil
import tempfile

# Register HEIC support
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIC_SUPPORT = True
except ImportError:
    HEIC_SUPPORT = False

# PDF support
try:
    from pdf2image import convert_from_path, convert_from_bytes
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

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
            
            # Get image dimensions
            width_px = img.width
            height_px = img.height
            
            result = {
                'status': 'success',
                'metadata_dpi': metadata_dpi,
                'effective_dpi': effective_dpi,
                'width_px': width_px,
                'height_px': height_px,
                'target_width_inch': target_width_inch,
                'message': ''
            }
            
            if metadata_dpi and metadata_dpi >= 300:
                result['message'] = f"✅ Metadata confirms {metadata_dpi} DPI - High Quality!"
                result['quality'] = 'high'
            elif effective_dpi >= 300:
                result['message'] = f"✅ Pixel density is high enough ({int(effective_dpi)} effective DPI) - High Quality!"
                result['quality'] = 'high'
            else:
                result['message'] = f"⚠️ Image too small. Only {int(effective_dpi)} DPI at {target_width_inch}\" - Low Quality"
                result['quality'] = 'low'
            
            return result
    
    except FileNotFoundError:
        return {'status': 'error', 'message': 'File not found.'}
    except Exception as e:
        return {'status': 'error', 'message': f'Error: {str(e)}'}


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
        if not HEIC_SUPPORT:
            raise ImportError("pillow-heif is not installed. Cannot convert HEIC files.")
        
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


def convert_pdf_to_images(pdf_path: str, dpi: int = 300, first_page: int = None, last_page: int = None):
    """
    Converts PDF pages to images.
    
    Args:
        pdf_path: Path to the PDF file
        dpi: Resolution for conversion (default 300)
        first_page: First page to convert (1-indexed, None = first page)
        last_page: Last page to convert (1-indexed, None = last page)
    
    Returns:
        List of PIL Image objects
    """
    try:
        if not PDF_SUPPORT:
            raise ImportError("pdf2image is not installed. Cannot convert PDF files.")
        
        # Convert PDF to images
        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            first_page=first_page,
            last_page=last_page
        )
        
        return images
    
    except Exception as e:
        raise Exception(f"Error converting PDF to images: {str(e)}")


def get_pdf_info(pdf_bytes: bytes):
    """
    Gets information about a PDF file.
    
    Args:
        pdf_bytes: PDF file as bytes
    
    Returns:
        Dictionary with PDF information
    """
    try:
        from io import BytesIO
        pdf_file = BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        info = {
            'num_pages': len(pdf_reader.pages),
            'metadata': pdf_reader.metadata or {},
            'encrypted': pdf_reader.is_encrypted
        }
        
        return info
    
    except Exception as e:
        return {'error': str(e)}


def save_uploaded_file(uploaded_file, destination_dir: str = "images/", convert_heic: bool = False):
    """Save uploaded file to destination directory, optionally converting HEIC to JPG"""
    try:
        # Create destination directory if it doesn't exist
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        # Check if it's a HEIC file and conversion is requested
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        is_heic = file_ext in ['.heic', '.heif']
        
        if is_heic and convert_heic and HEIC_SUPPORT:
            # Save HEIC temporarily, convert to JPG, then save
            with tempfile.NamedTemporaryFile(delete=False, suffix='.heic') as tmp_heic:
                tmp_heic.write(uploaded_file.getbuffer())
                tmp_heic_path = tmp_heic.name
            
            # Convert to JPG
            base_name = os.path.splitext(uploaded_file.name)[0]
            jpg_filename = f"{base_name}.jpg"
            jpg_path = os.path.join(destination_dir, jpg_filename)
            
            convert_heic_to_jpg(tmp_heic_path, jpg_path)
            
            # Clean up temp file
            try:
                os.unlink(tmp_heic_path)
            except:
                pass
            
            return jpg_path, None
        else:
            # Save the file as-is
            file_path = os.path.join(destination_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            return file_path, None
    except Exception as e:
        return None, str(e)


# Page configuration
st.set_page_config(
    page_title="Print Shop - Image Quality Checker",
    page_icon="🖨️",
    layout="wide"
)

# Title and description
st.title("🖨️ Print Shop - Image Quality Checker")
st.markdown("Upload images to check if they meet print quality standards (300 DPI minimum)")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    target_width = st.number_input(
        "Target Print Width (inches)",
        min_value=0.1,
        max_value=100.0,
        value=8.0,
        step=0.5,
        help="The width you want to print the image at"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Quality Standards")
    st.info("**High Quality:** ≥ 300 DPI\n\n**Low Quality:** < 300 DPI")

# Main content area
tabs_list = ["📤 Upload & Check", "📁 Batch Process"]
if HEIC_SUPPORT:
    tabs_list.append("🔄 HEIC Converter")
if PDF_SUPPORT:
    tabs_list.append("📄 PDF Processor")
else:
    if not HEIC_SUPPORT:
        st.warning("⚠️ PDF support not available. Install pdf2image and PyPDF2, and ensure poppler-utils is installed.")

tabs = st.tabs(tabs_list)
tab1 = tabs[0]
tab2 = tabs[1]
tab3 = None
pdf_tab = None
if HEIC_SUPPORT:
    tab3 = tabs[2] if "🔄 HEIC Converter" in tabs_list else None
if PDF_SUPPORT:
    pdf_tab = tabs[-1] if "📄 PDF Processor" in tabs_list else None

with tab1:
    st.header("Upload Single Image")
    
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'heic', 'heif'] if HEIC_SUPPORT else ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'],
        help="Upload an image to check its print quality" + (" (HEIC files will be converted to JPG)" if HEIC_SUPPORT else "")
    )
    
    # HEIC conversion option
    convert_heic = False
    if uploaded_file and HEIC_SUPPORT:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        if file_ext in ['.heic', '.heif']:
            convert_heic = st.checkbox(
                "🔄 Convert HEIC to JPG",
                value=True,
                help="Automatically convert HEIC files to JPG format when saving"
            )
    
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📷 Image Preview")
            # Display image (handle HEIC files)
            try:
                # Save temporarily to open with PIL (needed for HEIC)
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_preview:
                    tmp_preview.write(uploaded_file.getbuffer())
                    tmp_preview_path = tmp_preview.name
                
                image = Image.open(tmp_preview_path)
                st.image(image, caption=uploaded_file.name, use_container_width=True)
                
                # Image info
                st.markdown("### Image Information")
                st.write(f"**Filename:** {uploaded_file.name}")
                st.write(f"**Dimensions:** {image.width} × {image.height} pixels")
                st.write(f"**Format:** {image.format}")
                
                # Show conversion info for HEIC
                file_ext = os.path.splitext(uploaded_file.name)[1].lower()
                if file_ext in ['.heic', '.heif'] and convert_heic:
                    st.info("📝 This HEIC file will be converted to JPG when saved")
                
                # Clean up temp file
                try:
                    os.unlink(tmp_preview_path)
                except:
                    pass
            except Exception as e:
                st.error(f"Error loading image: {str(e)}")
                if not HEIC_SUPPORT and os.path.splitext(uploaded_file.name)[1].lower() in ['.heic', '.heif']:
                    st.warning("💡 Install pillow-heif to view and convert HEIC files")
        
        with col2:
            st.subheader("🔍 Quality Analysis")
            
            # Save uploaded file temporarily
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            tmp_suffix = '.heic' if file_ext in ['.heic', '.heif'] else file_ext
            with tempfile.NamedTemporaryFile(delete=False, suffix=tmp_suffix) as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                tmp_path = tmp_file.name
            
            # Check image quality (works with HEIC if pillow-heif is installed)
            result = check_image_resolution(tmp_path, target_width)
            
            if result['status'] == 'success':
                # Display result with color coding
                if result['quality'] == 'high':
                    st.success(result['message'])
                else:
                    st.warning(result['message'])
                
                # Detailed metrics
                st.markdown("### 📐 Detailed Metrics")
                
                col_metric1, col_metric2, col_metric3 = st.columns(3)
                with col_metric1:
                    st.metric("Metadata DPI", result['metadata_dpi'] or "N/A")
                with col_metric2:
                    st.metric("Effective DPI", f"{int(result['effective_dpi'])}")
                with col_metric3:
                    st.metric("Target Width", f"{target_width}\"")
                
                # Calculate recommended max print size
                if result['effective_dpi'] > 0:
                    max_width = result['width_px'] / 300
                    max_height = result['height_px'] / 300
                    st.info(f"**Recommended max print size for 300 DPI:** {max_width:.2f}\" × {max_height:.2f}\"")
                
                # Save to images directory option
                st.markdown("---")
                if st.button("💾 Save to Images Directory", use_container_width=True):
                    file_path, error = save_uploaded_file(uploaded_file, convert_heic=convert_heic)
                    if error:
                        st.error(f"Error saving file: {error}")
                    else:
                        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
                        if file_ext in ['.heic', '.heif'] and convert_heic:
                            st.success(f"✅ Converted and saved as JPG: {file_path}")
                        else:
                            st.success(f"✅ Saved to {file_path}")
            else:
                st.error(result['message'])
            
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except:
                pass

with tab2:
    st.header("Batch Process Images")
    
    uploaded_files = st.file_uploader(
        "Choose multiple image files",
        type=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'heic', 'heif'] if HEIC_SUPPORT else ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'],
        accept_multiple_files=True,
        help="Upload multiple images to check their print quality" + (" (HEIC files can be converted to JPG)" if HEIC_SUPPORT else "")
    )
    
    # Batch HEIC conversion option
    batch_convert_heic = False
    if uploaded_files and HEIC_SUPPORT:
        has_heic = any(os.path.splitext(f.name)[1].lower() in ['.heic', '.heif'] for f in uploaded_files)
        if has_heic:
            batch_convert_heic = st.checkbox(
                "🔄 Convert HEIC files to JPG",
                value=True,
                help="Automatically convert HEIC files to JPG format when saving"
            )
    
    if uploaded_files:
        st.info(f"📁 {len(uploaded_files)} file(s) selected")
        
        if st.button("🚀 Process All Images", use_container_width=True, type="primary"):
            progress_bar = st.progress(0)
            results_container = st.container()
            
            results = []
            for idx, uploaded_file in enumerate(uploaded_files):
                # Update progress
                progress = (idx + 1) / len(uploaded_files)
                progress_bar.progress(progress)
                
                # Save file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_path = tmp_file.name
                
                # Check quality
                result = check_image_resolution(tmp_path, target_width)
                result['filename'] = uploaded_file.name
                results.append(result)
                
                # Clean up temp file
                try:
                    os.unlink(tmp_path)
                except:
                    pass
            
            progress_bar.empty()
            
            # Display results
            with results_container:
                st.markdown("### 📊 Results Summary")
                
                high_quality = sum(1 for r in results if r.get('quality') == 'high')
                low_quality = sum(1 for r in results if r.get('quality') == 'low')
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("✅ High Quality", high_quality)
                with col2:
                    st.metric("⚠️ Low Quality", low_quality)
                
                st.markdown("---")
                st.markdown("### 📋 Detailed Results")
                
                for result in results:
                    with st.expander(f"📷 {result['filename']}", expanded=False):
                        if result['status'] == 'success':
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if result['quality'] == 'high':
                                    st.success(result['message'])
                                else:
                                    st.warning(result['message'])
                            
                            with col_b:
                                st.write(f"**Dimensions:** {result['width_px']} × {result['height_px']} px")
                                st.write(f"**Metadata DPI:** {result['metadata_dpi'] or 'N/A'}")
                                st.write(f"**Effective DPI:** {int(result['effective_dpi'])}")
                        else:
                            st.error(result['message'])
                
                # Batch save option
                st.markdown("---")
                if st.button("💾 Save All to Images Directory", use_container_width=True):
                    saved_count = 0
                    converted_count = 0
                    for uploaded_file in uploaded_files:
                        file_path, error = save_uploaded_file(uploaded_file, convert_heic=batch_convert_heic)
                        if not error:
                            saved_count += 1
                            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
                            if file_ext in ['.heic', '.heif'] and batch_convert_heic:
                                converted_count += 1
                    if converted_count > 0:
                        st.success(f"✅ Saved {saved_count} file(s) ({converted_count} converted from HEIC) to images/ directory")
                    else:
                        st.success(f"✅ Saved {saved_count} file(s) to images/ directory")

# HEIC Converter Tab
if HEIC_SUPPORT:
    with tab3:
        st.header("🔄 HEIC to JPG Converter")
        st.markdown("Convert HEIC/HEIF images to JPG format for better compatibility")
        
        heic_files = st.file_uploader(
            "Upload HEIC/HEIF files to convert",
            type=['heic', 'heif'],
            accept_multiple_files=True,
            help="Select one or more HEIC files to convert to JPG"
        )
        
        if heic_files:
            col_quality, col_auto = st.columns(2)
            with col_quality:
                jpg_quality = st.slider(
                    "JPG Quality",
                    min_value=50,
                    max_value=100,
                    value=95,
                    help="Higher quality = larger file size (95 is recommended)"
                )
            
            with col_auto:
                auto_save = st.checkbox(
                    "💾 Auto-save to images/ directory",
                    value=True,
                    help="Automatically save converted JPG files"
                )
            
            if st.button("🚀 Convert All HEIC Files", use_container_width=True, type="primary"):
                progress_bar = st.progress(0)
                results_container = st.container()
                
                converted_files = []
                errors = []
                
                for idx, heic_file in enumerate(heic_files):
                    # Update progress
                    progress = (idx + 1) / len(heic_files)
                    progress_bar.progress(progress)
                    
                    try:
                        # Save HEIC temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.heic') as tmp_heic:
                            tmp_heic.write(heic_file.getbuffer())
                            tmp_heic_path = tmp_heic.name
                        
                        # Determine output path
                        base_name = os.path.splitext(heic_file.name)[0]
                        if auto_save:
                            output_dir = "images/"
                            if not os.path.exists(output_dir):
                                os.makedirs(output_dir)
                            output_path = os.path.join(output_dir, f"{base_name}.jpg")
                        else:
                            output_path = f"{base_name}.jpg"
                        
                        # Convert
                        jpg_path = convert_heic_to_jpg(tmp_heic_path, output_path, quality=jpg_quality)
                        
                        # Get file size info
                        original_size = os.path.getsize(tmp_heic_path)
                        converted_size = os.path.getsize(jpg_path)
                        
                        converted_files.append({
                            'original': heic_file.name,
                            'converted': os.path.basename(jpg_path),
                            'path': jpg_path,
                            'original_size': original_size,
                            'converted_size': converted_size
                        })
                        
                        # Clean up temp file
                        try:
                            os.unlink(tmp_heic_path)
                        except:
                            pass
                    
                    except Exception as e:
                        errors.append({'file': heic_file.name, 'error': str(e)})
                
                progress_bar.empty()
                
                # Display results
                with results_container:
                    if converted_files:
                        st.success(f"✅ Successfully converted {len(converted_files)} file(s)")
                        
                        st.markdown("### 📋 Conversion Results")
                        for result in converted_files:
                            with st.expander(f"✅ {result['original']} → {result['converted']}", expanded=False):
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Original Size", f"{result['original_size'] / 1024:.1f} KB")
                                with col2:
                                    st.metric("JPG Size", f"{result['converted_size'] / 1024:.1f} KB")
                                with col3:
                                    size_change = ((result['converted_size'] - result['original_size']) / result['original_size']) * 100
                                    st.metric("Size Change", f"{size_change:+.1f}%")
                                
                                st.write(f"**Saved to:** `{result['path']}`")
                                
                                # Download button
                                with open(result['path'], 'rb') as f:
                                    st.download_button(
                                        label=f"📥 Download {result['converted']}",
                                        data=f.read(),
                                        file_name=result['converted'],
                                        mime="image/jpeg",
                                        key=f"download_{result['converted']}"
                                    )
                    
                    if errors:
                        st.error(f"❌ {len(errors)} conversion(s) failed")
                        for error in errors:
                            st.error(f"**{error['file']}:** {error['error']}")

# PDF Processor Tab
if PDF_SUPPORT and pdf_tab:
    with pdf_tab:
        st.header("📄 PDF to Images Converter")
        st.markdown("Convert PDF pages to images and check their print quality")
        
        uploaded_pdf = st.file_uploader(
            "Upload a PDF file",
            type=['pdf'],
            help="Select a PDF file to convert pages to images"
        )
        
        if uploaded_pdf:
            # Get PDF info
            pdf_bytes = uploaded_pdf.getvalue()
            pdf_info = get_pdf_info(pdf_bytes)
            
            if 'error' not in pdf_info:
                st.success(f"📄 PDF loaded: {uploaded_pdf.name}")
                
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.metric("Number of Pages", pdf_info['num_pages'])
                with col_info2:
                    st.metric("Encrypted", "Yes" if pdf_info['encrypted'] else "No")
                
                # Conversion settings
                st.markdown("### ⚙️ Conversion Settings")
                col_dpi, col_pages = st.columns(2)
                
                with col_dpi:
                    pdf_dpi = st.slider(
                        "DPI (Resolution)",
                        min_value=72,
                        max_value=600,
                        value=300,
                        step=72,
                        help="Higher DPI = better quality but larger files (300 is recommended for print)"
                    )
                
                with col_pages:
                    page_range = st.selectbox(
                        "Pages to Convert",
                        ["All pages", "First page only", "Custom range"],
                        help="Select which pages to convert"
                    )
                    
                    first_page = None
                    last_page = None
                    
                    if page_range == "First page only":
                        first_page = 1
                        last_page = 1
                    elif page_range == "Custom range":
                        col_start, col_end = st.columns(2)
                        with col_start:
                            first_page = st.number_input(
                                "Start Page",
                                min_value=1,
                                max_value=pdf_info['num_pages'],
                                value=1
                            )
                        with col_end:
                            last_page = st.number_input(
                                "End Page",
                                min_value=1,
                                max_value=pdf_info['num_pages'],
                                value=min(5, pdf_info['num_pages'])
                            )
                
                # Auto-save option
                auto_save_pdf = st.checkbox(
                    "💾 Auto-save converted images",
                    value=True,
                    help="Automatically save converted images to images/ directory"
                )
                
                if st.button("🚀 Convert PDF to Images", use_container_width=True, type="primary"):
                    progress_bar = st.progress(0)
                    results_container = st.container()
                    
                    try:
                        # Save PDF temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
                            tmp_pdf.write(pdf_bytes)
                            tmp_pdf_path = tmp_pdf.name
                        
                        # Convert PDF to images
                        with st.spinner("Converting PDF pages to images..."):
                            images = convert_pdf_to_images(
                                tmp_pdf_path,
                                dpi=pdf_dpi,
                                first_page=first_page,
                                last_page=last_page
                            )
                        
                        progress_bar.progress(1.0)
                        progress_bar.empty()
                        
                        # Display results
                        with results_container:
                            st.success(f"✅ Successfully converted {len(images)} page(s) to images")
                            
                            # Save images
                            saved_images = []
                            output_dir = "images/" if auto_save_pdf else None
                            
                            if output_dir and not os.path.exists(output_dir):
                                os.makedirs(output_dir)
                            
                            base_name = os.path.splitext(uploaded_pdf.name)[0]
                            
                            for idx, img in enumerate(images):
                                page_num = (first_page or 1) + idx if first_page else idx + 1
                                
                                # Save image
                                if auto_save_pdf:
                                    img_filename = f"{base_name}_page_{page_num:03d}.jpg"
                                    img_path = os.path.join(output_dir, img_filename)
                                    img.save(img_path, 'JPEG', quality=95, optimize=True)
                                    saved_images.append({
                                        'page': page_num,
                                        'path': img_path,
                                        'image': img,
                                        'filename': img_filename
                                    })
                                
                                # Display image with quality check
                                st.markdown(f"### 📄 Page {page_num}")
                                
                                col_img, col_analysis = st.columns(2)
                                
                                with col_img:
                                    st.image(img, caption=f"Page {page_num}", use_container_width=True)
                                    st.write(f"**Dimensions:** {img.width} × {img.height} pixels")
                                
                                with col_analysis:
                                    # Check quality
                                    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_img:
                                        img.save(tmp_img.name, 'JPEG')
                                        tmp_img_path = tmp_img.name
                                    
                                    result = check_image_resolution(tmp_img_path, target_width)
                                    
                                    if result['status'] == 'success':
                                        if result['quality'] == 'high':
                                            st.success(result['message'])
                                        else:
                                            st.warning(result['message'])
                                        
                                        st.metric("Effective DPI", f"{int(result['effective_dpi'])}")
                                        
                                        if result['effective_dpi'] > 0:
                                            max_width = result['width_px'] / 300
                                            max_height = result['height_px'] / 300
                                            st.info(f"**Max print size (300 DPI):** {max_width:.2f}\" × {max_height:.2f}\"")
                                    
                                    # Clean up temp image
                                    try:
                                        os.unlink(tmp_img_path)
                                    except:
                                        pass
                                
                                st.markdown("---")
                            
                            # Download buttons
                            if saved_images:
                                st.markdown("### 📥 Download Converted Images")
                                for saved_img in saved_images:
                                    with open(saved_img['path'], 'rb') as f:
                                        st.download_button(
                                            label=f"📥 Download {saved_img['filename']}",
                                            data=f.read(),
                                            file_name=saved_img['filename'],
                                            mime="image/jpeg",
                                            key=f"pdf_download_{saved_img['page']}"
                                        )
                            
                            # Clean up temp PDF
                            try:
                                os.unlink(tmp_pdf_path)
                            except:
                                pass
                    
                    except Exception as e:
                        st.error(f"❌ Error converting PDF: {str(e)}")
                        if "poppler" in str(e).lower() or "pdftoppm" in str(e).lower():
                            st.warning("""
                            **Poppler not found!** 
                            
                            Please install poppler-utils:
                            - **macOS:** `brew install poppler`
                            - **Ubuntu/Debian:** `sudo apt-get install poppler-utils`
                            - **Windows:** Download from https://github.com/oschwartz10612/poppler-windows/releases
                            """)
            else:
                st.error(f"❌ Error reading PDF: {pdf_info['error']}")

# Footer
st.markdown("---")
st.markdown("### 📝 How it works")
st.markdown("""
1. **Upload an image** using the file uploader
2. The app checks the image's DPI (dots per inch) at your target print width
3. **High quality** images have ≥ 300 DPI (standard for professional printing)
4. **Low quality** images have < 300 DPI and may appear pixelated when printed
""")



