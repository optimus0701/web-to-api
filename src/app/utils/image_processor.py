# src/app/utils/image_processor.py
import base64
import tempfile
import os
from pathlib import Path
from typing import Union, List
from fastapi import HTTPException
from app.logger import logger
import httpx


async def process_image_url(image_url: Union[str, dict]) -> Path:
    """
    Process image from URL, base64 data, or local path and return a Path object.
    
    Args:
        image_url: Either a URL string, a dict with 'url' key, base64 data, or local path
        
    Returns:
        Path to image file (either temporary or existing local file)
    """
    # Extract URL from dict if needed
    if isinstance(image_url, dict):
        url = image_url.get("url", "")
    else:
        url = image_url
    
    # Create temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    temp_path = Path(temp_file.name)
    
    try:
        if url.startswith("data:image"):
            # Handle base64 encoded image
            # Format: data:image/jpeg;base64,<base64_data>
            header, base64_data = url.split(",", 1)
            image_bytes = base64.b64decode(base64_data)
            temp_file.write(image_bytes)
            temp_file.close()
            logger.debug(f"Processed base64 image to {temp_path}")
            return temp_path
        elif url.startswith("http://") or url.startswith("https://"):
            # Download image from URL
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                temp_file.write(response.content)
                temp_file.close()
            logger.debug(f"Downloaded image from {url} to {temp_path}")
            return temp_path
        else:
            # Assume it's a local file path
            temp_file.close()
            os.unlink(temp_file.name)
            local_path = Path(url)
            if not local_path.exists():
                raise HTTPException(status_code=400, detail=f"Local file not found: {url}")
            logger.debug(f"Using local file: {local_path}")
            return local_path
            
    except HTTPException:
        # Re-raise HTTPException as-is
        temp_file.close()
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise
    except Exception as e:
        temp_file.close()
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(status_code=400, detail=f"Failed to process image: {str(e)}")


async def process_image_files(files: List[str]) -> tuple[List[Path], List[Path]]:
    """
    Process a list of image URLs/paths and return processed paths and temp files.
    
    Args:
        files: List of URLs, base64 strings, or local paths
        
    Returns:
        Tuple of (processed_paths, temp_files_to_cleanup)
    """
    processed_paths: List[Path] = []
    temp_files: List[Path] = []
    
    try:
        for file_url in files:
            path = await process_image_url(file_url)
            processed_paths.append(path)
            
            # Track temp files for cleanup
            if str(path).startswith(tempfile.gettempdir()):
                temp_files.append(path)
                
        return processed_paths, temp_files
    except Exception as e:
        # Cleanup on error
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        raise


def cleanup_temp_files(temp_files: List[Path]):
    """Clean up temporary files."""
    for temp_file in temp_files:
        try:
            if temp_file.exists():
                os.unlink(temp_file)
                logger.debug(f"Cleaned up temp file: {temp_file}")
        except Exception as e:
            logger.warning(f"Failed to delete temp file {temp_file}: {e}")
