package com.speech.exception;

import com.speech.dto.RecognitionResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.multipart.MaxUploadSizeExceededException;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(SpeechException.class)
    public ResponseEntity<RecognitionResponse> handleSpeechException(SpeechException ex) {
        RecognitionResponse response = RecognitionResponse.builder()
                .errNo(ex.getErrorCode())
                .errMsg(ex.getMessage())
                .sn(System.currentTimeMillis())
                .build();
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
    }

    @ExceptionHandler(MaxUploadSizeExceededException.class)
    public ResponseEntity<RecognitionResponse> handleMaxUploadSizeExceededException(MaxUploadSizeExceededException ex) {
        RecognitionResponse response = RecognitionResponse.builder()
                .errNo(413)
                .errMsg("文件大小超过限制，最大支持10MB")
                .sn(System.currentTimeMillis())
                .build();
        return ResponseEntity.status(HttpStatus.PAYLOAD_TOO_LARGE).body(response);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<RecognitionResponse> handleException(Exception ex) {
        RecognitionResponse response = RecognitionResponse.builder()
                .errNo(500)
                .errMsg("服务器内部错误: " + ex.getMessage())
                .sn(System.currentTimeMillis())
                .build();
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
    }
}
