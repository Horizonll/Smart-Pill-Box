# Smart Pill Box

2024 年清华大学第 27 届硬件设计大赛三等奖

2024 年清华大学第 27 届硬件设计大赛民生赛道一等奖

## TODO

### 算法

1. [x] 对说明书拍照，提取用量用法
1. [x] 对报纸拍照，提取文字转换音频
1. [x] asr功能
1. [x] AI聊天功能

### 应用程序开发

1. [x] 主菜单创建
1. [x] 药品录入功能实现
1. [x] 报纸朗读功能实现
1. [x] 系统设置功能实现
1. [ ] 美化界面

### 机械设计

## 有线连接nano

1. 插网线,自己电脑有线IP设为192.168.240.9,子网掩玛24
1. 终端运行ssh pill@192.168.240.11,密码pill

### 环境配置

```bash
cd smart-pill-box
pip install -r requirements.txt

git clone https://github.com/myshell-ai/MeloTTS.git
cd MeloTTS
pip install -e .
python -m unidic download

cd
pip install torch- torchaudio-
```

修改huggingface timeout
/home/pill/miniconda3/envs/pill/lib/python3.10/site-packages/huggingface_hub/constants.py


I'm excited to introduce our innovative project, PillPalPro, a multifunctional smart pill box designed to serve the elderly.

## PillPalPro Features

1. **Automatic Pill Dispensation**: Our smart pill box can dispense medication at the scheduled time, ensuring that users take their pills on time.
2. **Medication Reminders**: With our reminder function, PillPalPro helps users maintain a consistent medication schedule.
3. **Usage and Dosage Extraction**: PillPalPro can extract usage and dosage information directly from the medication's instructions, reducing the risk of errors.
4. **Audio Playback**: The device can play audio messages, providing additional guidance and support for users.
5. **AI ChatBot**: Our built-in AI chat feature offers companionship and assistance, addressing the emotional needs of the elderly.

## Achievements

We are proud to have received the Third Prize in the Tsinghua University Hardware Design Competition and the First Prize in the People's Livelihood Track.

## Collaboration

PillPalPro is the result of a collaborative effort between myself, Fan Bin, and Lin Tianhao. Our combined skills and dedication have brought this innovative solution to life.

## Open Source

Our project is open source, and you can find the code and documentation at the following address: https://github.com/Horizonll/Smart-Pill-Box

We invite you to explore our project and contribute to making PillPalPro even better!
