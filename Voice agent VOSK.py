import vosk
import sys
import json
import pyaudio
import wave
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
import ollama

class AIVoiceAgent:
    def __init__(self):
        self.client = ElevenLabs(api_key="sk_a206eef560153aaf086264694d1fbd8db5154448312e7287")
        
        self.model_path = r"C:\\Users\\kulan\\vosk-model-en-us-0.22"
        try:
            self.model = vosk.Model(self.model_path)
            self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        except Exception as e:
            print(f"Error loading Vosk model: {e}")
            sys.exit(1)
        
        self.full_transcript = [
            {"role": "system", "content": "You are an AI assistant. Answer questions clearly and concisely."},
        ]

    def start_transcription(self):
        print("Listening for speech...")
        
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()

        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                if "text" in result and result["text"].strip():
                    self.generate_ai_response(result["text"])

    def generate_ai_response(self, transcript):
        self.full_transcript.append({"role": "user", "content": transcript})
        print(f"User: {transcript}")

        ollama_response = ollama.chat(
            model="deepseek-r1:7b",
            messages=self.full_transcript,
            stream=False,
        )
        
        response_text = ollama_response['message']['content']
        print("AI Response:", response_text)
        
        self.full_transcript.append({"role": "assistant", "content": response_text})
        
        self.speak_response(response_text)

    def speak_response(self, text):
        print("Generating speech...")
        audio_stream = self.client.generate(text=text, model="eleven_turbo_v2", stream=True)
        
        print("Playing response...")
        stream(audio_stream)  # Directly stream the audio instead of saving to a file

ai_voice_agent = AIVoiceAgent()
ai_voice_agent.start_transcription()
