import os
import ssl
import time

print('=== Pocket-TTS SSL 修复测试 ===')
print()

# 必须在任何网络请求之前设置环境变量
os.environ['HF_HTTPS_VERIFY'] = '0'
os.environ['SSL_CERT_FILE'] = ''

# 1. 修补 ssl 模块
ssl._create_default_https_context = ssl._create_unverified_context

# 2. 保存原始的 hf_hub_download
from huggingface_hub import hf_hub_download as original_hf_hub_download
from pathlib import Path

# 定义本地模型目录
LOCAL_MODEL_DIR = Path(r'C:\Users\Administrator\.cache\huggingface\hub\models--kyutai--pocket-tts-without-voice-cloning\snapshots\075c0abfe7e41450521b0200b5168cfbc16bc77b')

def patched_hf_hub_download(repo_id, filename, revision=None, **kwargs):
    """修补后的 hf_hub_download，优先使用本地文件"""
    # 检查本地是否有该文件
    local_file = LOCAL_MODEL_DIR / filename
    if local_file.exists():
        print(f'  [本地缓存] {filename}')
        return str(local_file)

    # 如果本地没有，则调用原始函数（但 SSL 已禁用）
    print(f'  [下载] {filename}...')
    try:
        return original_hf_hub_download(repo_id=repo_id, filename=filename, revision=revision, **kwargs)
    except Exception as e:
        # 如果下载失败但本地文件存在，尝试使用本地文件
        if local_file.exists():
            return str(local_file)
        raise e

# 替换 hf_hub_download
import sys
import huggingface_hub
huggingface_hub.hf_hub_download = patched_hf_hub_download

# 修补 requests 模块
import requests
original_get = requests.Session.get
def patched_get(self, url, **kwargs):
    kwargs['verify'] = False
    return original_get(self, url, **kwargs)
requests.Session.get = patched_get

print("SSL 修复已应用")
print("本地文件优先模式已启用")
print()

import pocket_tts

print('正在加载 Pocket-TTS 模型（首次可能需要1-3分钟）...')
start_time = time.time()

try:
    model = pocket_tts.TTSModel.load_model()
    load_time = time.time() - start_time

    print()
    print('=' * 50)
    print('模型加载成功!')
    print(f'加载耗时: {load_time:.2f} 秒')
    print(f'采样率: {model.sample_rate} Hz')
    print('=' * 50)

except Exception as e:
    print()
    print('=' * 50)
    print('模型加载失败!')
    print('=' * 50)
    print()
    print('错误信息:', str(e)[:500])

    import traceback
    traceback.print_exc()
