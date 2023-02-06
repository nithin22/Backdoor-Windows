from email.mime import audio
import speech_recognition as sr

r=sr.Recognizer()

with sr.Microphone() as source:
    audio = r.listen(source)

    with open('steal.wav','wb') as f:
        f.write(audio.get_wav_data())
print("Executed Sucessfuly")