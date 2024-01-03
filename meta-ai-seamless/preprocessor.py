import boto3
import torch
import torchaudio
from transformers import AutoProcessor
from app_logger import app_logger as log
from message import Message

device = "cuda:0" if torch.cuda.is_available() else "cpu"
processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")

SAMPLING_RATE = 16000


class Preprocessor:
    def __init__(self):
        session = boto3.Session()
        s3 = session.resource("s3")
        self.chat_bucket = s3.Bucket("mt86-chat-app-media")

    def preprocess(self, message: Message):
        # Retrieve audio file from s3
        audio_message_s3_location = message.audio_file_location
        log.info(f"Retrieving audio message from {audio_message_s3_location}")
        local_audio_message_file_name = "audio_message.wav"
        self.chat_bucket.download_file(audio_message_s3_location, local_audio_message_file_name)
        # Check sampling rate and convert if necessary
        sig, sr = torchaudio.load(local_audio_message_file_name)
        log.info(f"Audio message shape: {sig.shape} and sampling rate: {sr}")
        audio_message_torch = torch.tensor(sig)
        if sr != SAMPLING_RATE:
            audio_message_torch = torchaudio.functional.resample(audio_message_torch, orig_freq=sr, new_freq=16000)
        audio_inputs = processor(audios=audio_message_torch, return_tensors="pt").to(device)
        return audio_inputs
