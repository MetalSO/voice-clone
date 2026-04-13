package com.speech.service;

import com.speech.dto.RecognitionResult;
import org.springframework.web.multipart.MultipartFile;

public interface SpeechRecognitionService {

    RecognitionResult recognize(MultipartFile audio, String language) throws Exception;
}
