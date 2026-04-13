import os
import sys
import uuid
import traceback
import tempfile
import ssl
from typing import Optional, Dict, Any
from pathlib import Path

os.environ['HF_HTTPS_VERIFY'] = '0'
os.environ['SSL_CERT_FILE'] = ''
ssl._create_default_https_context = ssl._create_unverified_context

LOCAL_MODEL_DIR = Path(r'C:\Users\Administrator\.cache\huggingface\hub\models--kyutai--pocket-tts-without-voice-cloning\snapshots\075c0abfe7e41450521b0200b5168cfbc16bc77b')

from huggingface_hub import hf_hub_download as original_hf_hub_download

def patched_hf_hub_download(repo_id, filename, revision=None, **kwargs):
    local_file = LOCAL_MODEL_DIR / filename
    if local_file.exists():
        return str(local_file)
    try:
        return original_hf_hub_download(repo_id=repo_id, filename=filename, revision=revision, **kwargs)
    except Exception:
        if local_file.exists():
            return str(local_file)
        raise

import huggingface_hub
huggingface_hub.hf_hub_download = patched_hf_hub_download

PYTTSX3_AVAILABLE = False
POCKETTTS_AVAILABLE = False
KITTENTTS_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    print("pyttsx3 not available")

try:
    import pocket_tts
    POCKETTTS_AVAILABLE = True
    print("Pocket-TTS available")
except ImportError:
    print("Pocket-TTS not available")

try:
    from TTS.api import TTS
    TTS_AVAILABLE = True
    KITTENTTS_AVAILABLE = True
    print("Coqui TTS (KittenTTS) available")
except ImportError:
    print("TTS (Coqui) not available")


class VoiceCloneProcessor:
    def __init__(self):
        self.output_dir = "output"
        self.temp_dir = "temp"

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def process_audio_file(self, audio_path: str) -> Dict[str, Any]:
        try:
            import soundfile as sf
            data, samplerate = sf.read(audio_path)
            return {
                "samplerate": samplerate,
                "duration": len(data) / samplerate if len(data.shape) == 1 else len(data) / samplerate,
                "channels": data.shape[1] if len(data.shape) > 1 else 1
            }
        except Exception as e:
            return {"error": str(e), "samplerate": 16000, "duration": 0}

    def extract_audio_features(self, audio_path: str) -> Dict[str, Any]:
        return {"status": "placeholder"}

    def convert_to_wav(self, input_path: str) -> str:
        return input_path


class PocketTTSEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized') and self.initialized:
            return
        self.model = None
        self.initialized = False
        self.sample_rate = 24000

    def initialize(self, model_path: Optional[str] = None) -> bool:
        if not POCKETTTS_AVAILABLE:
            print("Pocket-TTS not available")
            return False

        try:
            print("Initializing Pocket-TTS model...")
            self.model = pocket_tts.TTSModel.load_model()
            self.sample_rate = self.model.sample_rate
            self.initialized = True
            print(f"Pocket-TTS initialized successfully (sample_rate: {self.sample_rate})")
            return True
        except Exception as e:
            error_msg = str(e)
            print(f"Pocket-TTS init error: {error_msg}")
            if "SSL" in error_msg or "certificate" in error_msg.lower():
                print("SSL Certificate error - check network connection to HuggingFace")
            return False

    def synthesize(self, text: str, reference_audio_path: str, speed: float = 1.0, language: str = "zh") -> Optional[str]:
        if not self.initialized or self.model is None:
            raise Exception("Pocket-TTS model not initialized")

        try:
            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # 转换非 WAV 格式到 WAV
            audio_ext = os.path.splitext(reference_audio_path)[1].lower()
            if audio_ext in ['.webm', '.mp3', '.ogg', '.m4a', '.aac']:
                print(f"Converting {audio_ext} audio to WAV format...")
                from pydub import AudioSegment
                audio = AudioSegment.from_file(reference_audio_path)
                # 转换为 24kHz 单声道 WAV
                audio = audio.set_frame_rate(24000).set_channels(1)
                temp_wav = os.path.join(output_dir, f"temp_{uuid.uuid4()}.wav")
                audio.export(temp_wav, format="wav")
                reference_audio_path = temp_wav

            output_path = os.path.join(output_dir, f"pockettts_{uuid.uuid4()}.wav")

            model_state = self.model.get_state_for_audio_prompt(reference_audio_path)

            audio_tensor = self.model.generate_audio(
                model_state,
                text,
                max_tokens=50
            )

            import torch
            import scipy.io.wavfile as wavfile

            audio_data = audio_tensor.cpu().numpy()

            if audio_data.ndim == 2:
                audio_data = audio_data.T

            audio_data = audio_data / torch.max(torch.abs(torch.tensor(audio_data))).item() * 0.95

            wavfile.write(output_path, self.sample_rate, audio_data)

            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return output_path

            raise Exception("Pocket-TTS output file is empty")
        except Exception as e:
            raise Exception(f"Pocket-TTS synthesis failed: {str(e)}")


class KittenTTSEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return
        self.model = None
        self.initialized = False

    def initialize(self, model_path: Optional[str] = None) -> bool:
        if TTS_AVAILABLE:
            try:
                self.model = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
                self.initialized = True
                print("KittenTTS (XTTS v2) initialized successfully")
                return True
            except Exception as e:
                print(f"KittenTTS init error: {e}")
        return False

    def synthesize(self, text: str, reference_audio_path: str, speed: float = 1.0, language: str = "zh") -> Optional[str]:
        if not self.initialized or self.model is None:
            raise Exception("KittenTTS model not initialized")

        try:
            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            output_path = os.path.join(output_dir, f"kittentts_{uuid.uuid4()}.wav")

            self.model.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav=reference_audio_path,
                language=language,
                speed=speed
            )

            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return output_path

            raise Exception("KittenTTS output file is empty")
        except Exception as e:
            raise Exception(f"KittenTTS synthesis failed: {str(e)}")


def clone_voice_with_pockettts(
    text: str,
    reference_audio_path: str,
    speed: float = 1.0,
    pitch: float = 0.0,
    volume: float = 1.0,
    language: str = "zh"
) -> str:
    engine = PocketTTSEngine()

    if not engine.initialize():
        raise Exception("Pocket-TTS引擎初始化失败，请检查网络连接")

    return engine.synthesize(
        text=text,
        reference_audio_path=reference_audio_path,
        speed=speed,
        language=language
    )


def clone_voice_with_kittentts(
    text: str,
    reference_audio_path: str,
    speed: float = 1.0,
    pitch: float = 0.0,
    volume: float = 1.0,
    language: str = "zh"
) -> str:
    engine = KittenTTSEngine()

    if not engine.initialize():
        raise Exception("KittenTTS引擎初始化失败，Coqui TTS未正确安装")

    return engine.synthesize(
        text=text,
        reference_audio_path=reference_audio_path,
        speed=speed,
        language=language
    )


def clone_voice_with_pyttsx3(
    text: str,
    speed: float = 1.0,
    pitch: float = 0.0,
    volume: float = 1.0,
    gender: str = "female"
) -> str:
    if not PYTTSX3_AVAILABLE:
        raise Exception("pyttsx3不可用，请安装: pip install pyttsx3")

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, f"pyttsx3_{uuid.uuid4()}.mp3")

    try:
        engine = pyttsx3.init()

        rate = int(150 * speed)
        engine.setProperty('rate', rate)

        vol = max(0, min(1, volume))
        engine.setProperty('volume', vol)

        voices = engine.getProperty('voices')
        if voices:
            for voice in voices:
                voice_name_lower = voice.name.lower()
                if 'chinese' in voice_name_lower or 'zh' in voice_name_lower:
                    engine.setProperty('voice', voice.id)
                    break

        engine.save_to_file(text, output_path)
        engine.runAndWait()

        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return output_path

        raise Exception("pyttsx3合成文件为空")

    except Exception as e:
        raise Exception(f"pyttsx3合成失败: {str(e)}")
    finally:
        try:
            engine.stop()
        except:
            pass


def get_clone_status() -> Dict[str, Any]:
    return {
        "pockettts": {
            "available": POCKETTTS_AVAILABLE,
            "model": "Pocket-TTS (Kyutai)",
            "description": "轻量级高质量语音克隆模型"
        },
        "kittentts": {
            "available": KITTENTTS_AVAILABLE,
            "model": "Coqui XTTS v2",
            "description": "高质量语音克隆模型"
        },
        "pyttsx3": {
            "available": PYTTSX3_AVAILABLE,
            "model": "SAPI5",
            "description": "系统基础语音合成"
        }
    }


processor = VoiceCloneProcessor()