from pydantic import BaseModel
import json

class Message(BaseModel):
    message_id: str = None
    chat_id: str
    sender_id: str
    message_type: str
    text: str = ''
    audio_file_location: str = ''
    timestamp: str = ''
    translated_text: str = ''
    translated_audio_file_location: str = ''
    original_language: str = '' # comes in UI message
    recipient_preferred_language: str = '' # comes in UI message
    status: str = ''

    @staticmethod
    def from_json(data):
        return Message(**data)


