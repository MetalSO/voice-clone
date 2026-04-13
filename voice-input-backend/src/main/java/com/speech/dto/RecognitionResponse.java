package com.speech.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RecognitionResponse {
    private Integer errNo;
    private String errMsg;
    private String result;
    private Long sn;
}
