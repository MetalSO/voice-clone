import speech_recognition as sr

def process_audio(audio_path):
    """
    处理语音文件，返回识别结果
    
    Args:
        audio_path: 语音文件路径
        
    Returns:
        str: 识别出的文本
    """
    # 初始化识别器
    r = sr.Recognizer()
    
    # 读取语音文件
    with sr.AudioFile(audio_path) as source:
        # 读取音频数据
        audio_data = r.record(source)
        
        try:
            # 使用Google Web Speech API进行识别
            # 注意：此API需要互联网连接
            text = r.recognize_google(audio_data, language="zh-CN")
            return text
        except sr.UnknownValueError:
            return "无法识别语音"
        except sr.RequestError as e:
            return f"API请求失败: {str(e)}"
