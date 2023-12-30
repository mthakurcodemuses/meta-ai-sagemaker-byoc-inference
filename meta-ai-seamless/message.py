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

    def from_json(self, json_string):
        json_dict = json.loads(json_string)
        return Message(**json_dict)


