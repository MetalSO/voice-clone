package com.speech.exception;

import lombok.Getter;

@Getter
public class SpeechException extends RuntimeException {

    private final Integer errorCode;

    public SpeechException(String message) {
        super(message);
        this.errorCode = 500;
    }

    public SpeechException(Integer errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }

    public SpeechException(String message, Throwable cause) {
        super(message, cause);
        this.errorCode = 500;
    }
}
