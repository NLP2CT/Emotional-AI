import time
import sounddevice as sd
import numpy as np
import keyboard
from scipy.io.wavfile import write
import tempfile

def record_audio(duration=30, fs=16000):
    print("按下空格键开始录音...")

    # 等待按下空格键开始录音
    while not keyboard.is_pressed('space'):
        time.sleep(0.1)  # 检查空格键状态

    print("录音开始...")
    audio_data = []

    # 设置录音流
    stream = sd.InputStream(callback=lambda indata, frames, time, status: audio_data.append(indata.copy()), channels=1, samplerate=fs)
    stream.start()

    start_time = time.time()

    # 延迟2秒再开始检测空格键
    time.sleep(2)

    while True:
        if keyboard.is_pressed('space'):  # 录音过程中检查空格键
            print("录音结束，开始识别...")
            stream.stop()  # 停止录音流
            stream.close()  # 关闭流
            break  # 按下空格键结束录音

        if time.time() - start_time > duration:  # 设置最大录音时长（避免长时间无响应）
            print("达到最大录音时长，自动停止...")
            stream.stop()  # 停止录音流
            stream.close()  # 关闭流
            break  # 如果达到最大时长自动停止录音

    # 将录音数据拼接成一个长的音频
    audio_data = np.concatenate(audio_data, axis=0)

    # 临时保存音频数据
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file_path = tmp_file.name
        # 使用 scipy.io.wavfile.write 保存音频数据
        write(tmp_file_path, fs, audio_data)
        return tmp_file_path
