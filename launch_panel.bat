@echo off
chcp 65001 >nul
cd /d "C:\GPT-SoVITS_WorkSpace\GPT-SoVITS-v3lora-20250228"
:: 启动 WebUI
echo 正在启动 GPT-SoVITS WebUI... >> output_log.txt
runtime\python.exe GPT_SoVITS\inference_webui.py
if errorlevel 1 (
    echo ❌ WebUI 启动失败，请检查模型路径或依赖是否完整 >> output_log.txt
    pause
    exit /b
)

pause
