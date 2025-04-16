import tensorflow as tf

# 获取所有可用的GPU设备
physical_devices = tf.config.list_physical_devices('GPU')

# 打印GPU信息
if physical_devices:
    print(f"可用的GPU设备数量: {len(physical_devices)}")
    for idx, device in enumerate(physical_devices):
        print(f"GPU {idx}: {device}")
else:
    print("没有找到可用的GPU设备")
