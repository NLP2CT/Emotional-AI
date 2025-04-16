import time
import sounddevice as sd
import numpy as np
import keyboard
from gradio_client import Client, handle_file
import tempfile
from scipy.io.wavfile import write  # 使用 scipy.io.wavfile.write 来保存音频数据

# 设置Gradio客户端
client = Client("http://127.0.0.1:7860/")  # 假设Gradio应用在本地运行

# 设置录音参数
fs = 16000  # 采样率
duration = 30  # 最大录音时长，单位：秒

# 录音函数
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

# 语音识别函数
def speech_to_text(audio_path):
    try:
        print(f"正在进行语音识别，音频路径: {audio_path}")
        # 调用Gradio的API进行语音识别
        result = client.predict(
            input_wav=handle_file(audio_path),
            language="auto",  # 使用自动语言检测
            api_name="/model_inference"  # 使用模型推理API
        )
        print(f"识别结果: {result}")
        return result
    except Exception as e:
        print(f"语音识别过程中出现错误: {e}")
        return ""

def main():
    try:
        print("开始录音，按下空格键开始录音，按下空格键结束录音并进行识别...")

        # 录音并获取音频文件路径
        audio_path = record_audio(duration=30, fs=fs)

        # 调用语音识别API
        text = speech_to_text(audio_path)

        # 输出识别结果
        print(f"识别结果: {text}")
    except Exception as e:
        print(f"程序运行中出现错误: {e}")

if __name__ == "__main__":
    main()
  