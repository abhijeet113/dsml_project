import google.generativeai as genai
import os
import speech_recognition as sr
import edge_tts
import asyncio
import os
import pygame
import tempfile

genai.configure(api_key='AIzaSyDkk9QzHYqjP4jrMCAApApykKiVnynmhdc')
model = genai.GenerativeModel('gemini-1.5-flash')

async def text_to_speech(text, voice='en-US-AriaNeural'):
    try:
        # Create a Communicate instance with the text and voice
        communicate = edge_tts.Communicate(text, voice)
        
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            file_path = temp_audio.name
            await communicate.save(file_path)
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Load and play the audio file
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        # Wait for the playback to finish
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(1)
        
        # Stop playback
        pygame.mixer.music.stop()
        
        # Ensure the file is not in use before deleting
        pygame.mixer.quit()
        
        # Delete the temporary file
        os.remove(file_path)
        
    except edge_tts.exceptions.NoAudioReceived as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

voice_list=["en-IN-PrabhatNeural","ar-EG-SalmaNeural","en-US-AriaNeural"]


# Initialize recognizer
recognizer = sr.Recognizer()
def speakwithbot():
    # Use the microphone as the source for input.
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for speech...")
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Web Speech API
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# speakwithbot()
async def main():
    while(1):
        print("your turn:")
        response = model.generate_content(speakwithbot())
        print(response.text)
        await text_to_speech(str(response.text), voice='en-IN-PrabhatNeural')
        


asyncio.run(main())  