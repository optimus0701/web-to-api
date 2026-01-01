# src/app/endpoints/gemini.py
from fastapi import APIRouter, HTTPException
from app.logger import logger
from schemas.request import GeminiRequest
from app.services.gemini_client import get_gemini_client, GeminiClientNotInitializedError
from app.services.session_manager import get_gemini_chat_manager
from app.utils.image_processor import process_image_files, cleanup_temp_files

from pathlib import Path
from typing import Union, List, Optional

router = APIRouter()

@router.post("/gemini")
async def gemini_generate(request: GeminiRequest):
    try:
        gemini_client = get_gemini_client()
    except GeminiClientNotInitializedError as e:
        raise HTTPException(status_code=503, detail=str(e))

    temp_files: List[Path] = []
    try:
        # Process files (supports URL, base64, and local paths)
        files_to_send: Optional[List[Path]] = None
        if request.files:
            processed_paths, temp_files = await process_image_files(request.files)
            files_to_send = processed_paths
        
        response = await gemini_client.generate_content(
            request.message, 
            request.model.value, 
            files=files_to_send
        )
        
        # Cleanup temp files
        cleanup_temp_files(temp_files)
        
        return {"response": response.text}
    except Exception as e:
        # Cleanup on error
        cleanup_temp_files(temp_files)
        logger.error(f"Error in /gemini endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

@router.post("/gemini-chat")
async def gemini_chat(request: GeminiRequest):
    try:
        gemini_client = get_gemini_client()
    except GeminiClientNotInitializedError as e:
        raise HTTPException(status_code=503, detail=str(e))

    session_manager = get_gemini_chat_manager()
    if not session_manager:
        raise HTTPException(status_code=503, detail="Session manager is not initialized.")
    
    temp_files: List[Path] = []
    try:
        # Process files (supports URL, base64, and local paths)
        files_to_send: Optional[List[str]] = None
        if request.files:
            processed_paths, temp_files = await process_image_files(request.files)
            # Convert paths to strings for session manager
            files_to_send = [str(p) for p in processed_paths]
        
        response = await session_manager.get_response(
            request.model, 
            request.message, 
            files_to_send
        )
        
        # Cleanup temp files
        cleanup_temp_files(temp_files)
        
        return {"response": response.text}
    except Exception as e:
        # Cleanup on error
        cleanup_temp_files(temp_files)
        logger.error(f"Error in /gemini-chat endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")
