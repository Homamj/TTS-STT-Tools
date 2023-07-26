from fastapi import FastAPI, File, Form, UploadFile
import openai
import speech_recognition as sr
from pydub import AudioSegment
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
app = FastAPI()

@app.get('/supported_models')
def get_supported_models():
    return {'models': [{"model_id": 0, "model_name": "Google Speech Recognition"}, 
                       {"model_id": 1, "model_name": "whisper"}]}


@app.post('/STT/transcriber')
async def transcriber(lang: str = Form(...),
                model_id: int = Form(...),
                audio_file: UploadFile = File(...)):

    transcript = ""
    current_path = Path(__file__).parent
    if model_id == 0:
        r = sr.Recognizer()
        # Convert MP3 to WAV
        audio = AudioSegment.from_mp3(audio_file.file)
        wav_file = f"{current_path}/audio.wav"
        audio.export(wav_file, format="wav")

        # Open the WAV audio file for speech recognition
        with sr.AudioFile(wav_file) as source:
            # Read the audio data from the file
            audio_data = r.record(source)

            # Perform speech recognition
            transcript = r.recognize_google(audio_data, language=lang)
        os.remove(wav_file)

    elif model_id == 1:
        file_path = f'{current_path}/audio_file.filename'
        with open(file_path, "wb") as f:
            f.write(await audio_file.read())
        audio_file2 = open(file_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file2)
        os.remove(file_path)

    return {"message": transcript}