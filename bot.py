import google.generativeai as genai
import os
import speech_recognition as sr

genai.configure(api_key='AIzaSyDkk9QzHYqjP4jrMCAApApykKiVnynmhdc')
model = genai.GenerativeModel('gemini-1.5-flash')


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
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

speakwithbot()

while(1):
    response = model.generate_content(input("your command: \n"))
    print(response.text)


        