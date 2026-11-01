package com.cynbit.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Getter;
import java.time.Instant;

@Getter
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ApiResponse<T> {
    private final boolean success;
    private final int statusCode;
    private final String message;
    private final T data;
    private final ApiError error;
    private final String timestamp;

    public static <T> ApiResponse<T> success(T data, String message) {
        return ApiResponse.<T>builder()
                .success(true)
                .statusCode(200)
                .message(message)
                .data(data)
                .timestamp(Instant.now().toString())
                .build();
    }

    public static <T> ApiResponse<T> failure(int statusCode, String errorCode, String errorMessage) {
        return ApiResponse.<T>builder()
                .success(false)
                .statusCode(statusCode)
                .message("Request processing failed")
                .error(new ApiError(errorCode, errorMessage))
                .timestamp(Instant.now().toString())
                .build();
    }

    @Getter
    public static class ApiError {
        private final String code;
        private final String detail;

        public ApiError(String code, String detail) {
            this.code = code;
            this.detail = detail;
        }
    }
}