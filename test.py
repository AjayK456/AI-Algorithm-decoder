
from elevenlabs import ElevenLabs, play

# Initialize the client with your API key
client = ElevenLabs(api_key="sk_a60ff55b9f3cffc14072c39def3833aee6850ebfd6c2e169")
audio = client.generate(
    text="Your text here",
    voice="Aria"
)

# Play the generated audio
play(audio)
