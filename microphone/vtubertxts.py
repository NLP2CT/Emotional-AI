import sounddevice as sd
import numpy as np
from pydub import AudioSegment

# 设置设备ID为 CABLE Input（模拟麦克风）
virtual_mic_device_id = 18  # CABLE Input (VB-Audio Virtual Cable)

# 查看设备的采样率
device_info = sd.query_devices(virtual_mic_device_id)
device_sample_rate = device_info['default_samplerate']

# 加载 MP3 文件
file_path = r"..\gptsovits-r-solution\response_audio.wav"
audio = AudioSegment.from_wav(file_path)

# 如果需要，将音频采样率转换为设备支持的采样率
if audio.frame_rate != device_sample_rate:
    audio = audio.set_frame_rate(int(device_sample_rate))

# 转换为 numpy 数组
samples = np.array(audio.get_array_of_samples())

# 如果是立体声，转换成2列（左/右声道）
if audio.channels == 2:
    samples = samples.reshape((-1, 2))

# 获取采样率
sample_rate = audio.frame_rate

# 播放音频并打印成功信息
def play_audio(samples, sample_rate):
    try:
        sd.play(samples, samplerate=sample_rate, device=virtual_mic_device_id)
        sd.wait()  # 等待播放完成
        print("音频已成功播放到虚拟麦克风！")  # 成功信息
    except Exception as e:
        print(f"播放音频时发生错误: {e}")  # 错误信息

# 开始播放音频
play_audio(samples, sample_rate)
