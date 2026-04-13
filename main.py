from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from modules.speech_processor import process_audio
from modules.speech_synthesizer import synthesize_speech

# 加载环境变量
load_dotenv()

# 创建FastAPI应用
app = FastAPI(
    title="语音处理服务",
    description="提供语音输入处理和语音合成功能的RESTful API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 语音合成请求模型
class SynthesisRequest(BaseModel):
    text: str
    model: str = "pyttsx3"
    language: str = "zh-CN"
    gender: str = "female"

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "服务运行正常"}

# 获取模型可用性状态
@app.get("/api/speech/models")
async def get_available_models():
    """
    获取可用的语音合成模型
    """
    # 尝试导入Coqui TTS
    try:
        from TTS.api import TTS
        coqui_available = True
    except ImportError:
        coqui_available = False
    
    # 尝试导入Azure Speech SDK
    try:
        import azure.cognitiveservices.speech as speechsdk
        import os
        azure_available = True
        # 检查环境变量是否设置
        azure_speech_key = os.environ.get("AZURE_SPEECH_KEY")
        azure_speech_region = os.environ.get("AZURE_SPEECH_REGION")
        if not azure_speech_key or not azure_speech_region:
            azure_available = False
    except ImportError:
        azure_available = False
    
    # pyttsx3通常是可用的
    try:
        import pyttsx3
        pyttsx3_available = True
    except ImportError:
        pyttsx3_available = False
    
    # gTTS通常是可用的，但我们在代码中禁用了它
    try:
        from gtts import gTTS
        gtts_available = True
    except ImportError:
        gtts_available = False
    
    return {
        "models": {
            "azure": {
                "available": azure_available,
                "name": "Azure Speech Service",
                "description": "高质量云服务语音合成"
            },
            "coqui": {
                "available": coqui_available,
                "name": "Coqui TTS",
                "description": "开源高质量语音合成"
            },
            "pyttsx3": {
                "available": pyttsx3_available,
                "name": "pyttsx3",
                "description": "本地语音合成"
            },
            "gtts": {
                "available": gtts_available,
                "name": "gTTS",
                "description": "Google Text-to-Speech"
            }
        }
    }

# 语音输入处理端点
@app.post("/api/speech/process")
async def speech_process(file: UploadFile = File(...)):
    """
    处理语音输入文件，返回识别结果
    """
    try:
        # 保存上传的文件
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # 处理语音文件
        result = process_audio(file_path)
        
        # 删除临时文件
        os.remove(file_path)
        
        return {"status": "success", "text": result}
    except Exception as e:
        # 确保临时文件被删除
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"处理语音文件失败: {str(e)}")

# 语音合成端点
@app.post("/api/speech/synthesize")
async def speech_synthesize(request: SynthesisRequest):
    """
    将文本转换为语音，返回语音文件路径
    """
    import threading
    import concurrent.futures
    try:
        # 使用线程池执行语音合成，避免阻塞事件循环
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(synthesize_speech,
                text=request.text,
                model=request.model,
                language=request.language,
                gender=request.gender
            )
            audio_path = future.result()
        return {"status": "success", "audio_path": audio_path}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"语音合成失败: {str(e)}")

# ==================== 语音克隆 API ====================

# 语音克隆状态端点
@app.get("/api/voice-clone/status")
async def voice_clone_status():
    """获取语音克隆服务状态"""
    try:
        from services.voice_clone.voice_clone_service import get_clone_status
        status = get_clone_status()
        return {"status": "ok", **status}
    except ImportError:
        return {"status": "error", "message": "语音克隆模块未安装"}

# 语音克隆合成端点
@app.post("/api/voice-clone/synthesize")
async def voice_clone_synthesize(
    audio: UploadFile = File(...),
    text: str = Form(""),
    speed: float = Form(1.0),
    pitch: float = Form(0.0),
    volume: float = Form(1.0),
    model: str = Form("pyttsx3")
):
    """
    语音克隆合成接口
    
    参数:
    - audio: 参考声音文件 (wav, mp3, webm)
    - text: 要合成的文本
    - speed: 语速 (0.5-2.0)
    - pitch: 音调 (-12 到 +12)
    - volume: 音量 (0-1)
    - model: 模型选择 (kittentts, pyttsx3)
    """
    import concurrent.futures
    import traceback

    print(f"Received request - text: '{text}', model: '{model}', audio filename: {audio.filename}")

    if not text or not text.strip():
        print("Error: text is empty or whitespace")
        raise HTTPException(status_code=400, detail="文本内容不能为空")
    
    try:
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        audio_filename = f"ref_{audio.filename}"
        audio_path = os.path.join(temp_dir, audio_filename)
        
        with open(audio_path, "wb") as f:
            f.write(await audio.read())
        
        def run_clone():
            from services.voice_clone.voice_clone_service import (
                clone_voice_with_pockettts,
                clone_voice_with_kittentts,
                clone_voice_with_pyttsx3
            )

            if model == "pockettts":
                result = clone_voice_with_pockettts(
                    text=text.strip(),
                    reference_audio_path=audio_path,
                    speed=speed,
                    pitch=pitch,
                    volume=volume
                )
            elif model == "kittentts":
                result = clone_voice_with_kittentts(
                    text=text.strip(),
                    reference_audio_path=audio_path,
                    speed=speed,
                    pitch=pitch,
                    volume=volume
                )
            else:
                result = clone_voice_with_pyttsx3(
                    text=text.strip(),
                    speed=speed,
                    pitch=pitch,
                    volume=volume
                )
            
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            return result
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_clone)
            audio_output_path = future.result(timeout=120)
        
        if audio_output_path and os.path.exists(audio_output_path):
            relative_path = audio_output_path.replace("\\", "/")
            return {
                "status": "success",
                "audio_path": relative_path,
                "model_used": model
            }
        
        raise HTTPException(status_code=500, detail="语音克隆失败，未生成音频文件")
        
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)
        raise HTTPException(
            status_code=500, 
            detail=f"语音克隆失败: {str(e)}"
        )

# 音频上传端点（预处理）
@app.post("/api/voice-clone/upload")
async def voice_clone_upload(audio: UploadFile = File(...)):
    """上传参考音频并返回处理信息"""
    import uuid
    
    try:
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        file_ext = os.path.splitext(audio.filename)[1] or ".webm"
        filename = f"{uuid.uuid4()}{file_ext}"
        filepath = os.path.join(temp_dir, filename)
        
        with open(filepath, "wb") as f:
            content = await audio.read()
            f.write(content)
        
        from services.voice_clone.voice_clone_service import VoiceCloneProcessor
        processor = VoiceCloneProcessor()
        
        wav_path = processor.convert_to_wav(filepath)
        audio_info = processor.process_audio_file(wav_path)
        
        features = processor.extract_audio_features(audio_info["data"])
        
        return {
            "status": "success",
            "filename": filename,
            "duration": audio_info["duration"],
            "samplerate": audio_info["samplerate"],
            "features": features
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"音频上传处理失败: {str(e)}")

# 挂载静态文件目录
# 注意：必须在API路由之后挂载，否则API请求会被静态文件路由拦截
app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
