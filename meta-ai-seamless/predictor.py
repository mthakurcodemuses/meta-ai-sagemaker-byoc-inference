import json
import logging
from flask import Flask, Response, request

from postprocessor import Postprocessor
from preprocessor import Preprocessor
from translator_model import SeamlessTranslator

app = Flask(__name__)
translator = SeamlessTranslator()

@app.route('/ping', methods=['GET'])
def ping():
    # Check if the model was loaded successfully
    health = translator is not None
    status = 200 if health else 404
    return Response(response='pong', status=status, mimetype='application/json')


@app.route('/invocations', methods=['POST'])
def transformation():
    data = None
    if request.content_type == 'application/json':
        data = request.json
        logging.info(f"Received data: {data}")
    else:
        return Response(response='This predictor only supports JSON data', status=415, mimetype='text/plain')

    # Perform the transformation
    audio_input = Preprocessor().preprocess(data['audio_file_s3_location'])
    translated_output = translator.translate(**audio_input, tgt_lang="hin")[0].cpu().numpy().squeeze()

    # Post-processing
    # Write translated output to S3
    # Return S3 location of translated output
    translated_audio_message_s3_location = Postprocessor().postprocess(translated_output,
                                                                       data['audio_file_s3_location'])

    output = {
        "translated_audio_s3_location": translated_audio_message_s3_location,
        "translated_text": "This is a test message"
    }

    # Return JSON response
    return Response(response=json.dumps(output), status=200, mimetype='application/json')
