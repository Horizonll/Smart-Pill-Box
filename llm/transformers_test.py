import os
import threading
import whisper
import speech_recognition as sr
from melo.api import TTS
import pygame
from transformers import AutoModelForCausalLM, AutoTokenizer

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.chdir("/home/pill/smart-pill-box")


class ASRProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.model = whisper.load_model("base")

    def recognize(self):
        with sr.Microphone() as source:
            print("Please say something")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            print("Recording finished")
        with open("llm/in.wav", "wb") as f:
            f.write(audio.get_wav_data())
        result = self.model.transcribe("llm/in.wav")
        print(result["text"])
        return result["text"]


class TTSProcessor:
    def __init__(self):
        self.model = TTS(language="ZH_MIX_EN", ckpt_path="tts/checkpoint.pth", config_path="tts/config.json")
        self.speaker_ids = self.model.hps.data.spk2id

    def tts_to_file(self, text, speaker_id, file_path):
        self.model.tts_to_file(text, speaker_id, file_path)


class LLM:
    def __init__(self):
        self.device = "cuda"
        self.model = AutoModelForCausalLM.from_pretrained("/home/pill/.cache/huggingface/hub/models--Qwen--Qwen2-0.5B-Instruct/snapshots/c291d6fce4804a1d39305f388dd32897d1f7acc4", torch_dtype="auto", device_map="auto")
        self.tokenizer = AutoTokenizer.from_pretrained("/home/pill/.cache/huggingface/hub/models--Qwen--Qwen2-0.5B-Instruct/snapshots/c291d6fce4804a1d39305f388dd32897d1f7acc4")
        self.conversation_history = [{"role": "system", "content": "你是一个老人陪伴助手，记住你的每次回答都不要超过100个汉字"}]

    def ask_question(self, prompt):
        self.conversation_history.append({"role": "user", "content": prompt})
        text = self.tokenizer.apply_chat_template(self.conversation_history, tokenize=False, add_generation_prompt=True)
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
        generated_ids = self.model.generate(model_inputs.input_ids, max_new_tokens=512)
        generated_ids = [output_ids[len(input_ids) :] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        self.conversation_history.append({"role": "assistant", "content": response})
        return response


class ChatBotThread(threading.Thread):
    def __init__(self, llm: LLM, asr_processor: ASRProcessor, tts_processor: TTSProcessor):
        super().__init__()
        self._stop_event = threading.Event()
        self.llm = llm
        self.tts_processor = tts_processor
        self.asr_processor = asr_processor

    def run(self):
        while not self._stop_event.is_set():
            user_input = self.asr_processor.recognize()
            if user_input.lower() in ["exit", "quit"]:
                self._stop_event.set()
                return
            answer = self.llm.ask_question(user_input)
            print("Assistant:", answer)
            self.tts_processor.tts_to_file(answer, self.tts_processor.speaker_ids["ZH"], "llm/out.wav")
            self.play_audio()

    def stop(self):
        self._stop_event.set()

    def play_audio(self):
        pygame.mixer.init()
        pygame.mixer.music.load("llm/out.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() and not self._stop_event.is_set():
            continue


if __name__ == "__main__":
    llm = LLM()
    asr_processor = ASRProcessor()
    tts_processor = TTSProcessor()
    chat_bot_thread = ChatBotThread(llm, asr_processor, tts_processor)
    chat_bot_thread.start()
    chat_bot_thread.join()
