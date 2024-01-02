import boto3
import scipy
from numpy.typing import NDArray

from app_logger import app_logger as log
from message import Message


class Postprocessor:
    def __init__(self):
        session = boto3.Session()
        s3 = session.resource("s3")
        self.chat_bucket = s3.Bucket("mt86-chat-app-media")

    def postprocess(self, message: Message, audio_message_content_array: NDArray,
                             target_language: str = "hin",
                             sample_rate: int = 16000) -> str:
        chat_id = message.chat_id
        message_id = message.message_id
        translated_audio_message_s3_location = f"chats/{chat_id}/{message_id}-{target_language}.wav"
        try:
            translated_audio_file_name = f"{message_id}-{target_language}.wav"
            log.info(f"Writing audio message for chat_id {chat_id} in file {translated_audio_file_name}")
            scipy.io.wavfile.write(translated_audio_file_name, rate=sample_rate, data=audio_message_content_array) # audio_array_from_audio
            log.info(f"Uploading audio message for chat_id {chat_id} with key {translated_audio_message_s3_location}")
            self.chat_bucket.upload_file(translated_audio_file_name, translated_audio_message_s3_location)
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