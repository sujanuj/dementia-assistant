package com.example.dementiaassistant

import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import android.speech.RecognizerIntent
import android.content.Intent
import android.Manifest
import android.content.pm.PackageManager
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import android.speech.tts.TextToSpeech
import java.util.*
import android.content.Context
import android.view.Gravity
import android.view.ViewGroup
import android.app.AlarmManager
import android.app.PendingIntent
import android.os.Build
import android.provider.Settings
import java.util.regex.Pattern

class MainActivity : AppCompatActivity() {

    lateinit var input: EditText
    lateinit var button: Button
    lateinit var micButton: Button
    lateinit var chatLayout: LinearLayout
    lateinit var scrollView: ScrollView

    lateinit var tts: TextToSpeech
    lateinit var prefs: android.content.SharedPreferences

    var isContinuousMode = false
    var isProcessing = false

    val chatHistory = mutableListOf<String>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // 🎤 Permission
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
            != PackageManager.PERMISSION_GRANTED) {

            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.RECORD_AUDIO), 1
            )
        }

        // 🔔 Alarm Permission
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            val alarmManager = getSystemService(ALARM_SERVICE) as AlarmManager
            if (!alarmManager.canScheduleExactAlarms()) {
                startActivity(Intent(Settings.ACTION_REQUEST_SCHEDULE_EXACT_ALARM))
            }
        }

        input = findViewById(R.id.inputText)
        button = findViewById(R.id.sendButton)
        micButton = findViewById(R.id.micButton)
        chatLayout = findViewById(R.id.chatLayout)
        scrollView = findViewById(R.id.scrollView)

        prefs = getSharedPreferences("Memory", Context.MODE_PRIVATE)

        // 🔊 TTS
        tts = TextToSpeech(this) {
            if (it == TextToSpeech.SUCCESS) {
                tts.language = Locale.US
            }
        }

        button.setOnClickListener {

            if (isProcessing) return@setOnClickListener
            isProcessing = true

            val message = input.text.toString()
            if (message.isEmpty()) {
                isProcessing = false
                return@setOnClickListener
            }

            addMessage(message, true)
            input.setText("")
            chatHistory.add("User: $message")

            val lower = message.lowercase()

            // 🎵 PLAY SONG
            if (lower.startsWith("play")) {
                val song = message.replace("play", "", ignoreCase = true).trim()
                addMessage("Playing $song 🎵", false)
                tts.speak("Playing $song", TextToSpeech.QUEUE_FLUSH, null, null)
                playSong(song)
                isProcessing = false
                return@setOnClickListener
            }

            // 🧠 MEMORY SAVE
            if (lower.startsWith("i like")) {
                saveMemory(message)
                addMessage("Got it! I'll remember that 😊", false)
                tts.speak("Got it! I'll remember that", TextToSpeech.QUEUE_FLUSH, null, null)
                isProcessing = false
                return@setOnClickListener
            }

            // 🧠 MEMORY RECALL
            if (lower.contains("what do i like")) {
                val memory = getMemory()
                addMessage(memory, false)
                tts.speak(memory, TextToSpeech.QUEUE_FLUSH, null, null)
                isProcessing = false
                return@setOnClickListener
            }

            // 🧠 MEMORY ASSISTANT (NEW)
            if (lower.contains("who am i") || lower.contains("where am i")) {

                val call = RetrofitClient.instance.memoryAssistant(
                    mapOf("query" to message)
                )

                call.enqueue(object : Callback<ChatResponse> {
                    override fun onResponse(call: Call<ChatResponse>, response: Response<ChatResponse>) {
                        isProcessing = false
                        val reply = response.body()?.response ?: "I’m here to help 😊"
                        addMessage(reply, false)
                        tts.speak(reply, TextToSpeech.QUEUE_FLUSH, null, null)
                    }

                    override fun onFailure(call: Call<ChatResponse>, t: Throwable) {
                        isProcessing = false
                        addMessage("Error", false)
                    }
                })

                return@setOnClickListener
            }

            // 🚨 INCIDENT (NEW)
            if (lower.contains("help") || lower.contains("emergency")) {

                val call = RetrofitClient.instance.logIncident(
                    mapOf("description" to message)
                )

                call.enqueue(object : Callback<ChatResponse> {
                    override fun onResponse(call: Call<ChatResponse>, response: Response<ChatResponse>) {
                        isProcessing = false
                        val reply = "Emergency alert sent 🚨"
                        addMessage(reply, false)
                        tts.speak(reply, TextToSpeech.QUEUE_FLUSH, null, null)
                    }

                    override fun onFailure(call: Call<ChatResponse>, t: Throwable) {
                        isProcessing = false
                        addMessage("Error sending alert", false)
                    }
                })

                return@setOnClickListener
            }

            // ⏰ REMINDER (UPDATED WITH API)
            if (lower.contains("remind me")) {

                val success = setReminder(message)

                val call = RetrofitClient.instance.smartReminder(
                    mapOf("taken" to false)
                )

                call.enqueue(object : Callback<ChatResponse> {
                    override fun onResponse(call: Call<ChatResponse>, response: Response<ChatResponse>) {
                        isProcessing = false
                        val reply = response.body()?.response ?: "Reminder set ⏰"
                        addMessage(reply, false)
                        tts.speak(reply, TextToSpeech.QUEUE_FLUSH, null, null)
                    }

                    override fun onFailure(call: Call<ChatResponse>, t: Throwable) {
                        isProcessing = false
                        addMessage("Reminder set ⏰", false)
                    }
                })

                return@setOnClickListener
            }

            // 🤖 NORMAL CHAT
            val call = RetrofitClient.instance.sendMessage(
                ChatRequest(message, chatHistory)
            )

            call.enqueue(object : Callback<ChatResponse> {

                override fun onResponse(
                    call: Call<ChatResponse>,
                    response: Response<ChatResponse>
                ) {
                    isProcessing = false

                    if (response.isSuccessful) {
                        val reply = response.body()?.response ?: "No reply"
                        addMessage(reply, false)
                        chatHistory.add("Bot: $reply")
                        tts.speak(reply, TextToSpeech.QUEUE_FLUSH, null, null)
                    }
                }

                override fun onFailure(call: Call<ChatResponse>, t: Throwable) {
                    isProcessing = false
                    addMessage("Error: ${t.message}", false)
                }
            })
        }

        micButton.setOnClickListener {
            isContinuousMode = true
            startListening()
        }
    }

    // ================= REMINDER LOGIC =================

    private fun setReminder(input: String): Boolean {
        try {
            val calendar = Calendar.getInstance()

            val minutes = Pattern.compile("in (\\d+) minutes?").matcher(input.lowercase())
            if (minutes.find()) {
                calendar.add(Calendar.MINUTE, minutes.group(1).toInt())
                scheduleAlarm(calendar, input)
                return true
            }

            val hours = Pattern.compile("after (\\d+) hours?").matcher(input.lowercase())
            if (hours.find()) {
                calendar.add(Calendar.HOUR_OF_DAY, hours.group(1).toInt())
                scheduleAlarm(calendar, input)
                return true
            }

            return false

        } catch (e: Exception) {
            return false
        }
    }

    private fun scheduleAlarm(calendar: Calendar, message: String) {

        val intent = Intent(this, ReminderReceiver::class.java)
        intent.putExtra("message", message)

        val pendingIntent = PendingIntent.getBroadcast(
            this,
            System.currentTimeMillis().toInt(),
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val alarmManager = getSystemService(ALARM_SERVICE) as AlarmManager

        alarmManager.setExactAndAllowWhileIdle(
            AlarmManager.RTC_WAKEUP,
            calendar.timeInMillis,
            pendingIntent
        )
    }

    // ================= EXISTING =================

    private fun playSong(songName: String) {
        val intent = Intent(Intent.ACTION_SEARCH)
        intent.setPackage("com.google.android.youtube")
        intent.putExtra("query", songName)

        try {
            startActivity(intent)
        } catch (e: Exception) {
            Toast.makeText(this, "YouTube not installed", Toast.LENGTH_SHORT).show()
        }
    }

    private fun addMessage(text: String, isUser: Boolean) {
        val textView = TextView(this)
        textView.text = text
        textView.textSize = 16f
        textView.setPadding(20, 10, 20, 10)

        val params = LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.WRAP_CONTENT,
            ViewGroup.LayoutParams.WRAP_CONTENT
        )

        params.setMargins(10, 10, 10, 10)

        if (isUser) {
            params.gravity = Gravity.END
            textView.setBackgroundColor(0xFFD1C4E9.toInt())
        } else {
            params.gravity = Gravity.START
            textView.setBackgroundColor(0xFFE0E0E0.toInt())
        }

        textView.layoutParams = params
        chatLayout.addView(textView)

        scrollView.post {
            scrollView.fullScroll(ScrollView.FOCUS_DOWN)
        }
    }

    private fun saveMemory(text: String) {
        val existing = prefs.getStringSet("likes", mutableSetOf()) ?: mutableSetOf()
        val newSet = existing.toMutableSet()
        newSet.add(text)
        prefs.edit().putStringSet("likes", newSet).apply()
    }

    private fun getMemory(): String {
        val memories = prefs.getStringSet("likes", null)
        if (memories.isNullOrEmpty()) {
            return "I don’t know yet 😊"
        }
        val cleaned = memories.map {
            it.replace("i like", "", ignoreCase = true).trim()
        }
        return "You like ${cleaned.joinToString(", ")} 🎉"
    }

    fun startListening() {
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        startActivityForResult(intent, 1)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == 1 && resultCode == RESULT_OK) {
            val result = data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
            val spokenText = result?.get(0)

            input.setText(spokenText)

            if (!isProcessing) {
                button.performClick()
            }
        }
    }

    override fun onDestroy() {
        tts.stop()
        tts.shutdown()
        super.onDestroy()
    }
}