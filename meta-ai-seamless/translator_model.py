import torch
from pydub import AudioSegment

from seamless_communication.inference import Translator
from seamless_communication.streaming.dataloaders.s2tt import SileroVADSilenceRemover

model_name = "seamlessM4T_v2_large"
vocoder_name = "vocoder_v2" if model_name == "seamlessM4T_v2_large" else "vocoder_36langs"
device = "cuda:0" if torch.cuda.is_available() else "cpu"


class SeamlessTranslator:

    def __init__(self):
        self.translator = Translator(
            model_name,
            vocoder_name,
            device=device,
            dtype=torch.float16,
        )

    def translate(self, audio_file_path: str, target_lang: str):
        text_output, speech_output = self.translator.predict(
            input=audio_file_path,
            task_str="s2st",
            tgt_lang=tgt_lang,
        )