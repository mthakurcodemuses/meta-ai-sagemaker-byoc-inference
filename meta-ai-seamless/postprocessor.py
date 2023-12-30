import boto3
from io import BytesIO
from app_logger import app_logger as log
from message import Message

class Postprocessor:
    def __init__(self):
        session = boto3.Session()
        s3 = session.resource("s3")
        self.chat_bucket = s3.Bucket("mt86-chat-app-media")

    def postprocess(self, message: Message, audio_message_content: bytes,
                             audio_file_content_type: str = "audio/wav") -> str:
        chat_id = message.chat_id
        translated_audio_message_s3_location = f"chats/{chat_id}/{message.message_id}"
        try:
            log.info(f"Uploading audio message for chat_id {chat_id} with key {translated_audio_message_s3_location}")
            self.chat_bucket.put_object(Key=translated_audio_message_s3_location, Body=BytesIO(audio_message_content),
                                        ContentType=audio_file_content_type)
            log.info(f"Uploaded audio message for chat_id {chat_id} with key {translated_audio_message_s3_location}")
        except Exception as err:
            log.error(
                "Couldn't upload audio message for chat_id %s with key %s. Here's why: %s",
                chat_id,
                translated_audio_message_s3_location,
                err,
            )
            raise
        return translated_audio_message_s3_location