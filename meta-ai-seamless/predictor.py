import json
from app_logger import app_logger as log

import torch
from flask import Flask, Response, request
from transformers import SeamlessM4Tv2Model
from message import Message

from postprocessor import Postprocessor
from preprocessor import Preprocessor

app = Flask(__name__)

seamless_model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large")
device = "cuda:0" if torch.cuda.is_available() else "cpu"
log.info(f"Device: {device}")
seamless_model.to(device)

@app.route('/ping', methods=['GET'])
def ping():
    # Check if the model was loaded successfully
    health = seamless_model is not None
    status = 200 if health else 404
    return Response(response='pong', status=status, mimetype='application/json')


@app.route('/invocations', methods=['POST'])
def transformation():
    data = None
    if request.content_type == 'application/json':
        data = request.json
        log.info(f"Received data: {data}")
    else:
        return Response(response='This predictor only supports JSON data', status=415, mimetype='text/plain')

    # Perform the transformation
    chat_message = Message.from_json(data)
    log.info(f"Chat Message: {chat_message}")
    audio_input = Preprocessor().preprocess(chat_message)
    translated_output = seamless_model.generate(**audio_input, tgt_lang="hin", speaker_id=17)[0].cpu().numpy().squeeze()
    log.info(f"Translated Output: {type(translated_output)}")

    # Post-processing
    # Write translated output to S3
    # Return S3 location of translated output
    translated_audio_message_s3_location = Postprocessor().postprocess(chat_message, translated_output)

    output = {
        "translated_audio_s3_location": translated_audio_message_s3_location,
        "translated_text": "This is a test message"
    }

    # Return JSON response
    return Response(response=json.dumps(output), status=200, mimetype='application/json')
