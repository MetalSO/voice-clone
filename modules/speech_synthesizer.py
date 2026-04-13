import os
import traceback

gtts_available = False
pyttsx3_available = False
coqui_tts_available = False
azure_tts_available = False

try:
    from gtts import gTTS
    gtts_available = True
except ImportError:
    print("gTTS not available")

try:
    import pyttsx3
    pyttsx3_available = True
except ImportError:
    print("pyttsx3 not available")

try:
    from TTS.api import TTS
    coqui_tts_available = True
except ImportError:
    print("Coqui TTS not available")

try:
    import azure.cognitiveservices.speech as speechsdk
    azure_tts_available = True
    azure_speech_key = os.environ.get("AZURE_SPEECH_KEY")
    azure_speech_region = os.environ.get("AZURE_SPEECH_REGION")
    if not azure_speech_key or not azure_speech_region:
        azure_tts_available = False
        print("Azure credentials not set")
except ImportError:
    print("Azure Speech SDK not available")

print(f"Module init: gTTS={gtts_available}, pyttsx3={pyttsx3_available}, Coqui={coqui_tts_available}, Azure={azure_tts_available}")

def get_available_models():
    models = {}

    if gtts_available:
        models["gtts"] = {
            "name": "gTTS",
            "description": "Google Text-to-Speech",
            "available": True,
            "features": ["云端", "高质量", "需要网络"]
        }
    else:
        models["gtts"] = {
            "name": "gTTS",
            "description": "Google Text-to-Speech",
            "available": False,
            "features": ["云端", "高质量", "需要网络"]
        }

    if pyttsx3_available:
        models["pyttsx3"] = {
            "name": "pyttsx3",
            "description": "本地语音合成",
            "available": True,
            "features": ["本地", "离线可用", "快速"]
        }
    else:
        models["pyttsx3"] = {
            "name": "pyttsx3",
            "description": "本地语音合成",
            "available": False,
            "features": ["本地", "离线可用", "快速"]
        }

    if coqui_tts_available:
        models["coqui"] = {
            "name": "Coqui TTS",
            "description": "开源神经网络语音合成",
            "available": True,
            "features": ["高质量", "开源", "模型较大"]
        }
    else:
        models["coqui"] = {
            "name": "Coqui TTS",
            "description": "开源神经网络语音合成",
            "available": False,
            "features": ["高质量", "开源", "模型较大"]
        }

    if azure_tts_available:
        models["azure"] = {
            "name": "Azure Speech Service",
            "description": "微软云服务语音合成",
            "available": True,
            "features": ["云端", "最高质量", "需要API密钥"]
        }
    else:
        models["azure"] = {
            "name": "Azure Speech Service",
            "description": "微软云服务语音合成",
            "available": False,
            "features": ["云端", "最高质量", "需要API密钥"]
        }

    return models

def synthesize_speech(text, model="pyttsx3", language="zh-CN", gender="female"):
    if not text or not isinstance(text, str):
        raise ValueError("Text cannot be empty")

    if model not in ["gtts", "pyttsx3", "coqui", "azure"]:
        raise ValueError(f"Unsupported model: {model}")

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    import uuid
    file_name = f"{uuid.uuid4()}.mp3"
    output_path = os.path.join(output_dir, file_name)

    lang_code = language.split("-")[0]

    try:
        if model == "gtts":
            return _synthesize_gtts(text, lang_code, output_path)
        elif model == "pyttsx3":
            return _synthesize_pyttsx3(text, lang_code, output_path, gender)
        elif model == "coqui":
            if not coqui_tts_available:
                raise Exception("Coqui TTS not available")
            return _synthesize_coqui(text, lang_code, output_path, gender)
        elif model == "azure":
            if not azure_tts_available:
                raise Exception("Azure Speech Service not available")
            return _synthesize_azure(text, language, output_path, gender)
    except Exception as e:
        print(f"Model {model} failed: {str(e)}")
        if model != "pyttsx3" and pyttsx3_available:
            print("Falling back to pyttsx3...")
            return _synthesize_pyttsx3(text, lang_code, output_path, gender)
        raise

def _synthesize_gtts(text, lang_code, output_path):
    if not gtts_available:
        raise Exception("gTTS not available")
    tts = gTTS(text=text, lang=lang_code, slow=False)
    tts.save(output_path)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        return output_path
    raise Exception("gTTS file not created")

def _synthesize_pyttsx3(text, lang_code, output_path, gender="female"):
    if not pyttsx3_available:
        raise Exception("pyttsx3 not available")

    import platform
    print(f"Platform: {platform.system()}")

    engine = None
    errors = []

    init_methods = []
    if platform.system() == "Windows":
        init_methods.append(('sapi5', lambda: pyttsx3.init('sapi5')))
    init_methods.append(('default', lambda: pyttsx3.init()))

    for method_name, init_func in init_methods:
        try:
            print(f"Trying pyttsx3 init method: {method_name}")
            engine = init_func()
            print(f"pyttsx3 init ({method_name}) succeeded")
            break
        except Exception as e:
            print(f"pyttsx3 init ({method_name}) failed: {str(e)}")
            errors.append(f"{method_name}: {str(e)}")

    if engine is None:
        raise Exception(f"pyttsx3 init failed. Errors: {'; '.join(errors)}")

    try:
        voices = engine.getProperty('voices')
        print(f"Found {len(voices)} voices")

        target_voice_id = None
        for voice in voices:
            print(f"Voice: {voice.name}, ID: {voice.id}, Languages: {voice.languages}")

        voice_female = None
        voice_male = None

        for voice in voices:
            try:
                voice_langs = str(voice.languages).lower()
                voice_name = voice.name.lower()

                if 'zh' in voice_langs or 'chinese' in voice_name:
                    if 'female' in voice_name or '女' in voice_name:
                        voice_female = voice.id
                    elif 'male' in voice_name or '男' in voice_name:
                        voice_male = voice.id

                if lang_code == "en":
                    if 'en' in voice_langs:
                        if 'female' in voice_name:
                            voice_female = voice.id
                        elif 'male' in voice_name:
                            voice_male = voice.id
            except:
                pass

        if gender == "female" and voice_female:
            target_voice_id = voice_female
        elif gender == "male" and voice_male:
            target_voice_id = voice_male
        else:
            for voice in voices:
                try:
                    if 'zh' in str(voice.languages).lower():
                        target_voice_id = voice.id
                        break
                except:
                    pass

        if target_voice_id:
            print(f"Setting voice: {target_voice_id}")
            engine.setProperty('voice', target_voice_id)

        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)

        print(f"Synthesizing to: {output_path}")
        engine.save_to_file(text, output_path)
        engine.runAndWait()

        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"File created: {output_path}, size: {file_size} bytes")
            if file_size > 0:
                return output_path

        raise Exception("Output file not created or empty")

    except Exception as e:
        raise Exception(f"pyttsx3 synthesis failed: {str(e)}")
    finally:
        if engine:
            try:
                engine.stop()
            except:
                pass

def _synthesize_coqui(text, lang_code, output_path, gender="female"):
    if not coqui_tts_available:
        raise Exception("Coqui TTS not available")

    try:
        if lang_code == "zh":
            model_name = "tts_models/zh-CN/baker/tacotron2-DDC-GST"
        else:
            model_name = "tts_models/en/ljspeech/tacotron2-DDC"

        print(f"Using Coqui model: {model_name}")
        tts = TTS(model_name=model_name)
        tts.tts_to_file(text=text, file_path=output_path)

        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return output_path
        raise Exception("Coqui TTS file not created")
    except Exception as e:
        raise Exception(f"Coqui TTS failed: {str(e)}")

def _synthesize_azure(text, language, output_path, gender="female"):
    if not azure_tts_available:
        raise Exception("Azure not available")

    try:
        speech_key = os.environ.get("AZURE_SPEECH_KEY")
        service_region = os.environ.get("AZURE_SPEECH_REGION")

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

        if language == "zh-CN":
            speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural" if gender == "female" else "zh-CN-YunxiNeural"
        elif language == "en-US":
            speech_config.speech_synthesis_voice_name = "en-US-AriaNeural" if gender == "female" else "en-US-ChristopherNeural"
        else:
            speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"

        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return output_path
            raise Exception("Azure file not created")
        else:
            raise Exception(f"Azure synthesis failed: {result.error_details}")
    except Exception as e:
        raise Exception(f"Azure TTS failed: {str(e)}")
