package com.example.dementiaassistant

data class ChatRequest(
    val message: String,
    val history: List<String>
)