FROM python:3.11

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         nginx \
         ffmpeg \
         dos2unix \
         ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py && \
    pip install flask gevent gunicorn torch torchaudio transformers sentencepiece sagemaker boto3 pydantic protobuf scipy && \
        rm -rf /root/.cache

# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

COPY meta-ai-seamless /opt/program
RUN find /opt/program -type f -print0 | xargs -0 dos2unix
WORKDIR /opt/program

# Expose the port that nginx listens on
EXPOSE 8080

CMD ["python", "serve"]
