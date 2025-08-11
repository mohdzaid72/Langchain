import speech_recognition as sr
recognizer = sr.Recognizer() # Initialize the recognizer




sr.Recognizer()  # Initialize the recognizer
mic = sr.Microphone()  # Initialize the microphone
with mic as source:
    print("speak...")
    recognizer.adjust_for_ambient_noise(source) # Adjust for ambient noise
    audio = sr.Recognizer().listen(source)  # Listen for audio input
try:
    # Convert speech to text
    text = recognizer.recognize_google(audio)
    print("Transcribed Text:", text)

except sr.UnknownValueError:
    print("Sorry, I could not understand the audio.")
except sr.RequestError as e:
    print(f"Could not request results; {e}")
    