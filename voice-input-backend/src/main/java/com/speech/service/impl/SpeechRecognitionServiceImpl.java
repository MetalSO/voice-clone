package com.speech.service.impl;

import com.speech.dto.RecognitionResult;
import com.speech.service.SpeechRecognitionService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.UUID;

@Service
@Slf4j
public class SpeechRecognitionServiceImpl implements SpeechRecognitionService {

    @Override
    public RecognitionResult recognize(MultipartFile audio, String language) throws Exception {
        log.info("Received audio file for recognition: name={}, size={}, language={}",
                audio.getOriginalFilename(), audio.getSize(), language);

        Path tempFile = null;
        try {
            tempFile = Files.createTempFile("speech-", ".webm");
            Files.write(tempFile, audio.getBytes());
            log.info("Audio file saved to: {}", tempFile.toAbsolutePath());
        } catch (IOException e) {
            log.error("Failed to save audio file", e);
            throw new RuntimeException("Failed to save audio file: " + e.getMessage());
        }

        String apiKey = System.getenv("BAIDU_API_KEY");
        String secretKey = System.getenv("BAIDU_SECRET_KEY");

        if (apiKey == null || secretKey == null || apiKey.isEmpty() || secretKey.isEmpty()) {
            log.warn("Baidu API credentials not configured, returning placeholder result");
            return RecognitionResult.builder()
                    .text("【提示】语音识别服务已连接，但由于未配置百度语音API密钥，暂返回占位结果。请在系统环境变量中配置 BAIDU_API_KEY 和 BAIDU_SECRET_KEY。")
                    .duration((double) audio.getSize() / 16000.0)
                    .language(language)
                    .build();
        }

        log.info("Baidu API credentials configured, proceeding with recognition");
        return RecognitionResult.builder()
                .text("百度语音识别功能已配置，但需要完整的SDK集成")
                .duration((double) audio.getSize() / 16000.0)
                .language(language)
                .build();
    }
}
