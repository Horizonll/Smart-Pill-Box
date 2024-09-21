import whisper
import os
import speech_recognition as sr


def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        print("Recording finished")
    return audio


def save_audio(audio, file_path):
    with open(file_path, "wb") as f:
        f.write(audio.get_wav_data())
        print(f"Audio saved to {file_path}")


def transcribe_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]


def main():
    os.chdir("/home/pill/smart-pill-box")
    try:
        audio = record_audio()
        file_path = "llm/zh.wav"
        save_audio(audio, file_path)
        transcription = transcribe_audio(file_path)
        print("Transcription:", transcription)
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except sr.UnknownValueError:
        print("Unknown error occurred")


if __name__ == "__main__":
    main()
