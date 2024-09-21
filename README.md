# Smart Pill Box

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
