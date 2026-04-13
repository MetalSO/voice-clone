package com.speech.controller;

import com.speech.dto.ApiResponse;
import com.speech.dto.RecognitionResult;
import com.speech.service.SpeechRecognitionService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/speech")
@RequiredArgsConstructor
public class SpeechController {

    private final SpeechRecognitionService speechRecognitionService;

    @PostMapping("/recognize")
    public ResponseEntity<ApiResponse<RecognitionResult>> recognize(
            @RequestParam("audio") MultipartFile audio,
            @RequestParam(value = "language", defaultValue = "zh-CN") String language) {

        try {
            RecognitionResult result = speechRecognitionService.recognize(audio, language);
            return ResponseEntity.ok(ApiResponse.success(result));
        } catch (Exception e) {
            return ResponseEntity.internalServerError()
                    .body(ApiResponse.error(500, e.getMessage()));
        }
    }

    @GetMapping("/health")
    public ResponseEntity<ApiResponse<String>> health() {
        return ResponseEntity.ok(ApiResponse.success("Speech service is running"));
    }
}
