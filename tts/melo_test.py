import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
from melo.api import TTS
import os
import time

# os.chdir("/home/pill/smart-pill-box")
text = "拍照完成"
t1 = time.time()
model = TTS(
    language="ZH_MIX_EN",
    ckpt_path="tts/checkpoint.pth",
    config_path="tts/config.json",
)
t2 = time.time()
print(f"初始化时间{t2-t1}")
time.sleep(5)
speaker_ids = model.hps.data.spk2id
output_path = "tts/camera_finish.wav"
t1 = time.time()
model.tts_to_file(text, speaker_ids["ZH"], output_path)
t2 = time.time()
print(f"合成时间{t2-t1}")
