package com.speech.dto;

import lombok.Data;

@Data
public class RecognitionRequest {
    private String format;
    private Integer rate;
    private String language;
    private Integer devPid;
}
