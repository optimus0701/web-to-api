# src/schemas/request.py
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field

class GeminiModels(str, Enum):
    """
    An enumeration of the available Gemini models.
    """

    # Gemini 3.0 Series
    PRO_3_0 = "gemini-3.0-pro"

    # Gemini 2.5 Series
    PRO_2_5 = "gemini-2.5-pro"
    FLASH_2_5 = "gemini-2.5-flash"


class GeminiRequest(BaseModel):
    message: str
    model: GeminiModels = Field(default=GeminiModels.FLASH_2_5, description="Model to use for Gemini.")
    files: Optional[List[str]] = []

class ImageUrl(BaseModel):
    """Image URL object for OpenAI Vision API compatibility"""
    url: str = Field(..., description="Either a URL or a base64 encoded image data")

class ContentPart(BaseModel):
    """Content part that can be either text or image"""
    type: str = Field(..., description="Type of content: 'text' or 'image_url'")
    text: Optional[str] = Field(None, description="Text content when type is 'text'")
    image_url: Optional[Union[ImageUrl, dict]] = Field(None, description="Image URL when type is 'image_url'")

class ChatMessage(BaseModel):
    """OpenAI compatible chat message"""
    role: str = Field(..., description="Role: 'system', 'user', or 'assistant'")
    content: Union[str, List[ContentPart]] = Field(..., description="Message content as string or array of content parts")

class OpenAIChatRequest(BaseModel):
    messages: List[Union[dict, ChatMessage]]
    model: Optional[GeminiModels] = None
    stream: Optional[bool] = False

class Part(BaseModel):
    text: str

class Content(BaseModel):
    parts: List[Part]

class GoogleGenerativeRequest(BaseModel):
    contents: List[Content]
