FROM python:3.11-slim

WORKDIR /app

# Install system audio and compilation dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential curl ca-certificates portaudio19-dev ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ensure silero_vad.onnx binary model is always properly downloaded
RUN curl -sL -o /usr/local/lib/python3.11/site-packages/livekit/plugins/silero/resources/silero_vad.onnx \
    https://github.com/snakers4/silero-vad/raw/master/src/silero_vad/data/silero_vad.onnx

COPY agent.py .

CMD ["python", "agent.py", "start"]