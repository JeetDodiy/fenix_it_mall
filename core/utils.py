"""
Core utility functions for image processing, sanitization, and security.
"""
import io
import os
import uuid
import logging
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.utils.text import slugify

logger = logging.getLogger(__name__)


def sanitize_and_process_image(uploaded_file, max_dimension=2048, quality=88):
    """
    Validates and normalizes any uploaded image file.
    Supports JPG, PNG, WEBP, AVIF, GIF, BMP, TIFF, JFIF, etc.
    
    1. Validates that the file is not empty.
    2. Uses Pillow to verify the file is genuinely an image (preventing corrupt files,
       HTML pages saved as images, or disguised non-images).
    3. Transposes EXIF orientation so photos taken on phones are upright.
    4. Converts transparent images (RGBA, LA, P with transparency) to standard clean PNG,
       and all other formats (including WEBP, AVIF, BMP, CMYK, etc.) to clean RGB JPEG.
    5. Strips corrupted/conflicting headers and generates a clean, URL-safe filename.
    6. Ensures compatibility with Cloudinary and local storage backends.
    
    Returns a ContentFile ready for Django model ImageField assignment.
    Raises ValueError if the file is invalid or not an image.
    """
    if not uploaded_file:
        raise ValueError("No file provided.")

    if hasattr(uploaded_file, 'size') and uploaded_file.size == 0:
        raise ValueError("The uploaded file is empty (0 bytes).")

    # Rewind stream before reading
    if hasattr(uploaded_file, 'seek'):
        uploaded_file.seek(0)

    try:
        img = Image.open(uploaded_file)
        img.verify()
    except Exception as e:
        logger.warning("Image verification failed for %s: %s", getattr(uploaded_file, 'name', 'unnamed'), e)
        raise ValueError("The uploaded file is not a valid or readable image. Please upload a standard JPG, PNG, or WebP image.")

    # Re-open after verify() as required by Pillow documentation
    if hasattr(uploaded_file, 'seek'):
        uploaded_file.seek(0)
    img = Image.open(uploaded_file)

    # Automatically correct EXIF orientation (e.g. mobile phone photos)
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    # Optionally resize excessively large images (e.g. 50 Megapixel RAW/phone photos)
    if max_dimension and (img.width > max_dimension or img.height > max_dimension):
        img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

    # Detect transparency
    has_alpha = (
        img.mode in ('RGBA', 'LA') or
        (img.mode == 'P' and 'transparency' in img.info)
    )

    output = io.BytesIO()
    if has_alpha:
        img = img.convert('RGBA')
        img.save(output, format='PNG', optimize=True)
        ext = 'png'
    else:
        # Convert any color mode (CMYK, Grayscale, WebP, etc.) to standard RGB JPEG
        img = img.convert('RGB')
        img.save(output, format='JPEG', quality=quality, optimize=True)
        ext = 'jpg'

    output.seek(0)

    # Generate safe, clean filename
    orig_name = getattr(uploaded_file, 'name', 'image') or 'image'
    base_name = os.path.splitext(os.path.basename(orig_name))[0]
    safe_slug = slugify(base_name)[:40] or 'img'
    clean_filename = f"{safe_slug}_{uuid.uuid4().hex[:8]}.{ext}"

    return ContentFile(output.read(), name=clean_filename)
