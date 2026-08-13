# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies (specifically ffmpeg for video/audio processing and espeak for pyttsx3 text-to-speech)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    espeak \
    libespeak1 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Pre-download the Whisper model to avoid memory spikes and timeouts during runtime
RUN python -c "from faster_whisper import WhisperModel; WhisperModel('tiny', device='cpu', compute_type='int8')"

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the application using uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
