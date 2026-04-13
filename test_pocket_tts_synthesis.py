import os
import ssl
import time

print('=== Pocket-TTS 语音合成完整测试 ===')
print()

os.environ['HF_HTTPS_VERIFY'] = '0'
os.environ['SSL_CERT_FILE'] = ''
ssl._create_default_https_context = ssl._create_unverified_context

LOCAL_MODEL_DIR = r'C:\Users\Administrator\.cache\huggingface\hub\models--kyutai--pocket-tts-without-voice-cloning\snapshots\075c0abfe7e41450521b0200b5168cfbc16bc77b'

from huggingface_hub import hf_hub_download as original_hf_hub_download
from pathlib import Path

def patched_hf_hub_download(repo_id, filename, revision=None, **kwargs):
    local_file = Path(LOCAL_MODEL_DIR) / filename
    if local_file.exists():
        print(f'  [本地] {filename}')
        return str(local_file)
    print(f'  [下载] {filename}...')
    try:
        return original_hf_hub_download(repo_id=repo_id, filename=filename, revision=revision, **kwargs)
    except Exception:
        if local_file.exists():
            return str(local_file)
        raise

import huggingface_hub
huggingface_hub.hf_hub_download = patched_hf_hub_download

print('1. 加载 Pocket-TTS 模型...')
import pocket_tts

start_time = time.time()
model = pocket_tts.TTSModel.load_model()
load_time = time.time() - start_time
print(f'   模型加载完成，耗时: {load_time:.2f} 秒')
print(f'   采样率: {model.sample_rate} Hz')

print()
print('2. 加载参考音频（用于语音克隆）...')
# 使用预定义的语音
voice_name = "alba"  # 使用预定义语音
print(f'   使用预定义语音: {voice_name}')

print()
print('3. 测试语音合成...')
test_text = "Hello, this is a test of the Pocket-TTS voice cloning system."

start_time = time.time()

try:
    # 使用预定义语音进行合成
    audio = model.generate_audio(
        model.get_state_for_audio_prompt(voice_name),
        test_text,
        max_tokens=50
    )
    synthesis_time = time.time() - start_time

    print(f'   合成成功!')
    print(f'   合成耗时: {synthesis_time:.2f} 秒')
    print(f'   输出音频形状: {audio.shape}')
    print(f'   音频时长: {audio.shape[-1] / model.sample_rate:.2f} 秒')

    # 计算实时率 (RTF)
    audio_duration = audio.shape[-1] / model.sample_rate
    rtf = audio_duration / synthesis_time
    print(f'   实时率 (RTF): {rtf:.2f}x')

    # 保存测试音频
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'pockettts_test.wav')

    import scipy.io.wavfile as wavfile
    audio_data = audio.cpu().numpy()
    if audio_data.ndim == 2:
        audio_data = audio_data.T
    wavfile.write(output_path, model.sample_rate, audio_data)
    print(f'   测试音频已保存: {output_path}')

    print()
    print('=' * 50)
    print('Pocket-TTS 语音合成测试完成!')
    print('=' * 50)

except Exception as e:
    print()
    print('=' * 50)
    print('语音合成测试失败!')
    print('=' * 50)
    print(f'错误: {e}')
    import traceback
    traceback.print_exc()
