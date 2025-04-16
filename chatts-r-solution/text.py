import torch
import torchaudio
import os
import time
import ChatTTS
import pygame
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import numpy as np
from pydub import AudioSegment

# 初始化 ChatTTS
chat = ChatTTS.Chat()
chat.load(compile=False)  # 设置为 True 提升性能

with open("speaker_token1.txt", "r", encoding="utf-8") as f:
    rand_spk = f.read()

# 设置语音生成参数
params_infer_code = ChatTTS.Chat.InferCodeParams(
    spk_emb=rand_spk,      # 添加固定音色
    temperature=0.3,       # 使用自定义温度
    top_P=0.7,             # top P 解码
    top_K=20               # top K 解码
)

def text_to_speech(text, output_path):
    """
    使用 ChatTTS 将文本转换为语音并保存为 MP3 格式
    """
    wavs = chat.infer([text], params_infer_code=params_infer_code)

    # 确保输出路径的文件夹存在
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # 将生成的语音保存为 WAV 格式
        wav_file_path = output_path.replace(".mp3", ".wav")
        torchaudio.save(wav_file_path, torch.from_numpy(wavs[0]).unsqueeze(0), 24000)

        # 使用 pydub 将 WAV 转换为 MP3 格式
        audio = AudioSegment.from_wav(wav_file_path)
        audio.export(output_path, format="mp3")
        os.remove(wav_file_path)  # 删除中间的 WAV 文件

        print(f"音频保存成功: {output_path}")
    except Exception as e:
        print(f"保存音频时出错: {e}")

def play_audio(file_path):
    """
    播放音频文件
    """
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

class TxtFileHandler(FileSystemEventHandler):
    def __init__(self, txt_file_path, output_dir):
        self.txt_file_path = txt_file_path
        self.output_dir = output_dir
        self.last_modified_time = None

    def on_modified(self, event):
        if event.src_path == self.txt_file_path:
            # 检查文件是否修改
            current_modified_time = os.path.getmtime(self.txt_file_path)
            if self.last_modified_time != current_modified_time:
                self.last_modified_time = current_modified_time

                # 读取文件内容
                with open(self.txt_file_path, 'r', encoding='utf-8') as f:
                    text = f.read()

                # 生成唯一的文件名（可以使用时间戳）
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                output_path = os.path.join(self.output_dir, f"response_{timestamp}.mp3")

                # 生成语音并播放
                text_to_speech(text, output_path)
                play_audio(output_path)

if __name__ == "__main__":
    # 要监听的txt文件路径和保存音频的输出路径
    txt_file_path = r"C:\Users\17905\Desktop\acdemic\deepseek-catgirlfriend\assistant_reply2.txt"  # 你的txt文件路径
    output_dir = "response_test"  # 保存音频文件的目录

    print("开始检测文件变化...")  # 显示开始检测的提示信息

    # 创建并启动文件监听
    event_handler = TxtFileHandler(txt_file_path, output_dir)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(txt_file_path), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)  # 程序持续运行，监听文件变化
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
