# src/app/endpoints/chat.py
import time
import base64
import tempfile
import os
from pathlib import Path
from typing import List, Union
from fastapi import APIRouter, HTTPException
from app.logger import logger
from schemas.request import GeminiRequest, OpenAIChatRequest
from app.services.gemini_client import get_gemini_client, GeminiClientNotInitializedError
from app.services.session_manager import get_translate_session_manager
import httpx

router = APIRouter()

@router.post("/translate")
async def translate_chat(request: GeminiRequest):
    try:
        gemini_client = get_gemini_client()
    except GeminiClientNotInitializedError as e:
        raise HTTPException(status_code=503, detail=str(e))

    session_manager = get_translate_session_manager()
    if not session_manager:
        raise HTTPException(status_code=503, detail="Session manager is not initialized.")
    try:
        # This call now correctly uses the fixed session manager
        response = await session_manager.get_response(request.model, request.message, request.files)
        return {"response": response.text}
    except Exception as e:
        logger.error(f"Error in /translate endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error during translation: {str(e)}")

def convert_to_openai_format(response_text: str, model: str, stream: bool = False):
    return {
        "id": f"chatcmpl-{int(time.time())}",
        "object": "chat.completion.chunk" if stream else "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_text,
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        },
    }

async def process_image_content(image_data: Union[str, dict]) -> Path:
    """
    Process image from URL or base64 data and return a temporary file path.
    
    Args:
        image_data: Either a URL string, a dict with 'url' key, or base64 data
        
    Returns:
        Path to temporary image file
    """
    # Extract URL from dict if needed
    if isinstance(image_data, dict):
        url = image_data.get("url", "")
    else:
        url = image_data
    
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
        elif url.startswith("http://") or url.startswith("https://"):
            # Download image from URL
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                temp_file.write(response.content)
                temp_file.close()
        else:
            # Assume it's a local file path
            temp_file.close()
            os.unlink(temp_file.name)
            return Path(url)
            
        return temp_path
    except Exception as e:
        temp_file.close()
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(status_code=400, detail=f"Failed to process image: {str(e)}")

@router.post("/v1/chat/completions")
async def chat_completions(request: OpenAIChatRequest):
    try:
        gemini_client = get_gemini_client()
    except GeminiClientNotInitializedError as e:
        raise HTTPException(status_code=503, detail=str(e))

    is_stream = request.stream if request.stream is not None else False

    if not request.messages:
        raise HTTPException(status_code=400, detail="No messages provided.")

    # Build conversation prompt with system prompt and full history
    conversation_parts = []
    image_files: List[Path] = []
    temp_files: List[Path] = []  # Track temp files for cleanup

    for msg in request.messages:
        # Handle both dict and ChatMessage objects
        if hasattr(msg, 'role'):
            role = msg.role
            content = msg.content
        else:
            role = msg.get("role", "user")
            content = msg.get("content", "")
        
        if not content:
            continue

        # Handle complex content with images (OpenAI Vision API format)
        if isinstance(content, list):
            text_parts = []
            for part in content:
                # Handle both Pydantic models and dicts
                if hasattr(part, 'type'):
                    part_type = part.type
                    part_text = part.text
                    part_image = part.image_url
                else:
                    part_type = part.get("type", "")
                    part_text = part.get("text")
                    part_image = part.get("image_url")
                
                if part_type == "text" and part_text:
                    text_parts.append(part_text)
                elif part_type == "image_url" and part_image:
                    # Process image and add to files list
                    try:
                        image_path = await process_image_content(part_image)
                        image_files.append(image_path)
                        # Track if it's a temp file (not a local path from user)
                        if str(image_path).startswith(tempfile.gettempdir()):
                            temp_files.append(image_path)
                    except Exception as e:
                        logger.error(f"Error processing image: {e}")
                        # Clean up any temp files created so far
                        for temp_file in temp_files:
                            try:
                                os.unlink(temp_file)
                            except:
                                pass
                        raise
            
            # Combine text parts
            combined_text = " ".join(text_parts)
            if combined_text:
                if role == "system":
                    conversation_parts.append(f"System: {combined_text}")
                elif role == "user":
                    conversation_parts.append(f"User: {combined_text}")
                elif role == "assistant":
                    conversation_parts.append(f"Assistant: {combined_text}")
        else:
            # Simple string content
            if role == "system":
                conversation_parts.append(f"System: {content}")
            elif role == "user":
                conversation_parts.append(f"User: {content}")
            elif role == "assistant":
                conversation_parts.append(f"Assistant: {content}")

    if not conversation_parts:
        raise HTTPException(status_code=400, detail="No valid messages found.")

    # Join all parts with newlines
    final_prompt = "\n\n".join(conversation_parts)

    if request.model:
        try:
            # Pass image files if any were found
            files_to_send = image_files if image_files else None
            response = await gemini_client.generate_content(
                message=final_prompt, 
                model=request.model.value, 
                files=files_to_send
            )
            
            # Clean up temporary files
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except Exception as e:
                    logger.warning(f"Failed to delete temp file {temp_file}: {e}")
            
            return convert_to_openai_format(response.text, request.model.value, is_stream)
        except Exception as e:
            # Clean up temp files on error
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except:
                    pass
            logger.error(f"Error in /v1/chat/completions endpoint: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Error processing chat completion: {str(e)}")
    else:
        # Clean up temp files if model not specified
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        raise HTTPException(status_code=400, detail="Model not specified in the request.")
