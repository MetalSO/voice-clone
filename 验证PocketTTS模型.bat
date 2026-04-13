@echo off
chcp 65001 >nul
title Pocket-TTS 模型验证工具

echo ========================================
echo   Pocket-TTS 模型验证工具
echo ========================================
echo.

cd /d "d:\trea speech synthesis"

echo 正在检查模型文件...
echo.

"d:\trea speech synthesis\venv\Scripts\python.exe" -c "
import os
import glob

base_dir = r'C:\Users\Administrator\.cache\huggingface\hub\models--kyutai--pocket-tts-without-voice-cloning'

# 查找实际快照目录
snapshots = glob.glob(os.path.join(base_dir, 'snapshots', '*'))
if snapshots:
    model_dir = snapshots[0]
else:
    model_dir = base_dir

print(f'模型目录: {model_dir}')
print()

required_files = [
    'tokenizer.model',
    'flow_lm/model.safetensors',
    'mimi/model.safetensors'
]

all_present = True
for f in required_files:
    path = os.path.join(model_dir, f)
    if os.path.exists(path):
        size = os.path.getsize(path) / (1024*1024)
        print(f'  ✓ {f} ({size:.1f} MB)')
    else:
        print(f'  ✗ {f} 缺失')
        all_present = False

print()
if all_present:
    print('=' * 50)
    print('所有模型文件已就绪!')
    print('=' * 50)

    # 测试加载
    print()
    print('正在测试 Pocket-TTS 模型加载...')
    try:
        import pocket_tts
        model = pocket_tts.TTSModel.load_model()
        print(f'  ✓ 模型加载成功!')
        print(f'  ✓ 采样率: {model.sample_rate} Hz')
        print()
        print('Pocket-TTS 已准备就绪，可以使用语音克隆功能!')
    except Exception as e:
        print(f'  ✗ 模型加载失败: {e}')
else:
    print('=' * 50)
    print('模型文件不完整，请重新下载')
    print('=' * 50)
    print()
    print('下载链接:')
    print('  https://huggingface.co/kyutai/pocket-tts-without-voice-cloning/tree/main')
"

echo.
pause
