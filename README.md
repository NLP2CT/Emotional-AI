# Emotional-AI 部署过程

以下是 **Emotional-AI** 项目的详细部署步骤，包括从拉取仓库到启动项目以及后续的配置。

## 1. 拉取仓库

首先，拉取 `Emotional-AI` 项目的代码。

```bash
git clone https://github.com/<repo>/Emotional-AI.git
cd Emotional-AI
```

## 2. 安装 Conda

如果你尚未安装 Conda，可以根据操作系统下载并安装 [Miniconda](https://docs.conda.io/en/latest/miniconda.html) 或 [Anaconda](https://www.anaconda.com/products/individual)。

### 安装完 Conda 后，检查是否成功安装：

```bash
conda --version
```

## 3. 安装 GPT-SoVITS

B站的大佬做的项目，推荐直接下载 GPT-SoVITS 的最新安装包。记得保存解压的位置，因为未来配置时需要使用该路径。

1. **下载 GPT-SoVITS**：访问 GitHub 仓库，下载最新的安装包。
2. **解压**：解压到自己指定的目录，记住路径。

## 4. 启动项目

安装完依赖后，可以启动项目。运行以下命令：

```bash
python start_up.py
```

### 如果一切正常：

- 系统会自动为每个项目创建 Conda 环境并安装 `requirements.txt` 中的依赖。
  
### 可能会遇到的问题：

有时 `requirements.txt` 可能有一些问题，导致依赖没有完全安装。这时可以手动安装缺失的库：

```bash
conda activate <目标文件夹名>
pip install <缺少的依赖>
```

同时因为还没有配置GPT-SoVITS所以第一个弹窗会启动失败，不用管他继续执行程序就可以了

## 5. 安装 VTube Studio

1. **VTube Studio 本体**：去 [Steam](https://store.steampowered.com/) 搜索并下载 VTube Studio。
2. **虚拟麦克风**：下载 [VBCABLE_Driver_Pack45](https://www.vb-cable.com/) 并按照安装提示进行安装。安装完成后，配置麦克风为 VBCable 驱动。

## 6. 修改配置

完成上述步骤后，进行以下配置修改：

### 1. 修改 `launch_panel.bat` 中的路径

打开 `launch_panel.bat` 文件，将 `cd` 行的路径修改为你解压的 GPT-SoVITS 目录路径。

### 2. 配置 `weight.json`

可以创建一个 `weight.json` 文件放置在 GPT-SoVITS 的根目录下。这样在未来你训练完模型后，可以直接通过配置文件中的模型启动，不需要再点击浏览器（需要你训练好的模型路径）

### 3. 训练音频

如果需要训练音频或进行其他调整，可以参考 B站的教程。

### 4. DeepSeek API

去 `deepseek-catgirlfriend` 目录下修改 `conversation.py` 中的 API 配置。
当然你想要用别的AI的API只要稍微改一改就好了

## 启动过程

### 启动一系列必须的后台服务

#### 1. 手动启动

- 点击 GPT-SoVITS 的 `go-webui.bat`，可以进入网站（localhost:9874）开启 TTS 推理（即 `inference_webui.py`）。
- 进入 `SenseVoice-main` 目录：

  ```bash
  conda activate <之前创立好的或者你自己建的>
  python webui.py
  ```

- 进入 `gptsovits-r-solution` 目录，注意一定要启动 TTS 推理后才能启动这个服务：

  ```bash
  conda activate <之前创立好的或者你自己建的>
  python realtime.py
  ```

- 进入 `microphone` 目录：

  ```bash
  conda activate <之前创立好的或者你自己建的>
  python call.py
  ```

#### 2. 脚本启动

```bash
python start_up.py
```

正常情况下会启动四个终端，分别对应四个服务。如果所有服务都没有报错，部署就成功了。

### 启动对话服务

1. 进入 `deepseek-catgirlfriend` 目录：

   ```bash
   conda activate <之前创立好的或者你自己建的>
   python main.py
   ```
   
2. 启动 VTube Studio。

通过空格输入，如果流程没有报错，就表示成功了！

---


## Q&A
1. 为什么不使用GPT-SoVITE提供的API？
   没有研究过Gradio，我也不会改
2. 为什么没有配置SwinFace？
   我的电脑跑不动会死机（
   如果你硬要使用的话记得去仓库下载checkpoint_step_79999_gpu_0.pt模型捏
