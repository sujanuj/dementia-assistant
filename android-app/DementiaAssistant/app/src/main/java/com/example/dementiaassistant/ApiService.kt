package com.example.dementiaassistant

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST


interface ApiService {
    @POST("/chat")
    fun sendMessage(@Body request: ChatRequest): Call<ChatResponse>
    @POST("/memory-assistant")
    fun memoryAssistant(@Body request: Map<String, String>): Call<ChatResponse>

    @POST("/smart-reminder")
    fun smartReminder(@Body request: Map<String, Boolean>): Call<ChatResponse>

    @POST("/incident")
    fun logIncident(@Body request: Map<String, String>): Call<ChatResponse>
}