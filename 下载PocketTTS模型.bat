@echo off
chcp 65001 >nul
title Pocket-TTS 模型下载工具

echo ========================================
echo   Pocket-TTS 模型下载工具
echo ========================================
echo.
echo 官方模型仓库: https://huggingface.co/kyutai/pocket-tts-without-voice-cloning
echo.
echo 注意: 模型文件较大(约500MB)，请确保网络稳定
echo.

cd /d "d:\trea speech synthesis"

echo [1/5] 检查 Python 环境...
"d:\trea speech synthesis\venv\Scripts\python.exe" --version
echo.

echo [2/5] 安装 huggingface-hub...
"d:\trea speech synthesis\venv\Scripts\pip.exe install huggingface-hub --quiet
echo.

echo [3/5] 创建模型目录...
mkdir "C:\Users\Administrator\.cache\huggingface\hub\models--kyutai--pocket-tts-without-voice-cloning\snapshots" 2>nul
echo.

echo [4/5] 设置环境变量...
set HF_HTTPS_VERIFY=0
set HF_ENDPOINT=https://hf-mirror.com
echo.

echo [5/5] 开始下载模型...
echo 首次运行可能需要5-10分钟，请耐心等待...
echo.

"d:\trea speech synthesis\venv\Scripts\python.exe" -c "
import os
import ssl
os.environ['HF_HTTPS_VERIFY'] = '0'
os.environ['SSL_CERT_FILE'] = ''
ssl._create_default_https_context = ssl._create_unverified_context

from huggingface_hub import snapshot_download

print('开始下载 Pocket-TTS 模型...')
print('模型仓库: kyutai/pocket-tts-without-voice-cloning')
print()

try:
    local_dir = snapshot_download(
        'kyutai/pocket-tts-without-voice-cloning',
        local_dir_use_symlinks=False,
        resume_download=True
    )
    print()
    print('=' * 50)
    print('模型下载成功!')
    print(f'下载目录: {local_dir}')
    print('=' * 50)
except Exception as e:
    print()
    print('=' * 50)
    print('下载失败!')
    print(f'错误: {str(e)}')
    print('=' * 50)
    print()
    print('备选方案:')
    print('1. 访问 https://huggingface.co/kyutai/pocket-tts-without-voice-cloning')
    print('2. 手动下载所有 .safetensors 和 .model 文件')
    print('3. 创建目录并放入下载的文件')
"

echo.
echo 下载完成！
echo.
pause
