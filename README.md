# Dementia Care Assistant — AI-Based Mobile Application

**Course:** MS Software Engineering  
**Institution:** Arizona State University  
**Author:** Sujan U J  

---

## Abstract

This project presents an AI-powered Android application designed to assist dementia patients with daily activities, memory support, and caregiver communication. The system integrates a conversational AI backend with a mobile interface, providing voice interaction, personalized memory storage, and real-time reminders. The goal is to reduce cognitive load for patients and provide a scalable, cloud-deployed solution accessible from any Android device.

---

## 1. Project Overview

Dementia patients often experience difficulty remembering daily tasks, personal preferences, and sometimes even their identities. Existing solutions are either too complex for patients to navigate or lack personalization. This project addresses these gaps by building a lightweight, voice-enabled assistant that learns from conversations and adapts to individual patient needs.

The system consists of two main components:
- An **Android application** (Kotlin) serving as the patient-facing interface
- A **Python/Flask REST API backend** deployed on Railway with PostgreSQL for persistent memory storage using vector embeddings

---

## 2. Features

| Feature | Description |
|--------|-------------|
| Voice Interaction | Speech-to-text and text-to-speech using Android Speech Recognition API |
| AI Chat Assistant | Conversational AI powered by OpenAI GPT for context-aware responses |
| Memory System | Stores and retrieves user preferences using pgvector semantic search |
| Reminder System | Natural language reminder parsing (e.g., "Remind me in 10 minutes") |
| Emergency Detection | Detects keywords like "help" and triggers emergency response |
| Identity Support | Answers personal questions like "Who am I?" using stored context |

---

## 3. System Architecture

```
┌─────────────────────────────┐
│      Android App (Kotlin)   │
│  - MainActivity.kt          │
│  - RetrofitClient.kt        │
│  - ApiService.kt            │
│  - ReminderReceiver.kt      │
└────────────┬────────────────┘
             │ HTTPS (Retrofit)
             ▼
┌─────────────────────────────┐
│   Flask REST API (Python)   │
│   Deployed on Railway       │
│  - /chat endpoint           │
│  - /memory endpoint         │
│  - /remind endpoint         │
└────────────┬────────────────┘
             │ SQLAlchemy ORM
             ▼
┌─────────────────────────────┐
│  PostgreSQL + pgvector      │
│  (Railway managed DB)       │
│  - Vector embeddings        │
│  - User memory storage      │
└─────────────────────────────┘
```

---

## 4. Technologies Used

### Android Application
| Technology | Purpose |
|------------|---------|
| Kotlin | Primary programming language |
| Android Studio | IDE and build environment |
| Retrofit 2 | HTTP client for API communication |
| Speech Recognition API | Voice input processing |
| TextToSpeech API | Voice output |
| Android AlarmManager | Reminder scheduling |

### Backend
| Technology | Purpose |
|------------|---------|
| Python 3.13 | Backend language |
| Flask 3.1 | Web framework |
| SQLAlchemy | ORM for database interaction |
| PostgreSQL | Relational database |
| pgvector | Vector similarity search for memory |
| OpenAI API | GPT-based chat and embeddings |
| Gunicorn | WSGI production server |
| Railway | Cloud deployment platform |

---

## 5. Project Structure

```
dementia-assistant/
│
├── android-app/
│   └── AndroidStudioProjects/
│       └── DementiaAssistant/
│           ├── app/
│           │   └── src/main/java/com/example/dementiaassistant/
│           │       ├── MainActivity.kt         # Main UI and chat logic
│           │       ├── ApiService.kt           # Retrofit API interface
│           │       ├── RetrofitClient.kt       # HTTP client configuration
│           │       ├── ChatRequest.kt          # Request data class
│           │       ├── ChatResponse.kt         # Response data class
│           │       └── ReminderReceiver.kt     # Alarm/reminder handler
│           └── build.gradle.kts
│
├── backend/
│   └── ai-memory-system/
│       ├── app/
│       │   ├── __init__.py                     # Flask app factory
│       │   ├── routes.py                       # API route definitions
│       │   ├── models.py                       # SQLAlchemy data models
│       │   └── embedding.py                    # Vector embedding logic
│       ├── run.py                              # Application entry point
│       ├── requirements.txt                    # Python dependencies
│       └── Procfile                            # Railway deployment config
│
└── README.md
```

---

## 6. Setup and Installation

### Prerequisites
- Python 3.9+
- Android Studio (latest stable)
- PostgreSQL with pgvector extension
- OpenAI API key

### Backend Setup (Local)

```bash
# Clone the repository
git clone https://github.com/sujanuj/dementia-assistant.git
cd dementia-assistant/backend/ai-memory-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env
echo "DATABASE_URL=postgresql://localhost/ai_memory" >> .env

# Run the application
python run.py
```

Backend will start at: `http://localhost:5001`

### Android App Setup

1. Open `android-app/AndroidStudioProjects/DementiaAssistant` in Android Studio
2. Wait for Gradle sync to complete
3. Update `BASE_URL` in `RetrofitClient.kt` to your backend URL
4. Run on emulator or physical device

---

## 7. Deployment

### Backend — Railway

The backend is deployed on [Railway](https://railway.app) with a managed PostgreSQL database.

**Live URL:** `https://dementia-assistant-production.up.railway.app`

**Environment Variables Required:**
```
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...  (auto-set by Railway)
```

**Database Setup:**
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### Android App — APK Build

```bash
cd android-app/AndroidStudioProjects/DementiaAssistant
./gradlew assembleDebug
# Output: app/build/outputs/apk/debug/app-debug.apk
```

---

## 8. API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check — returns "Backend running!" |
| POST | `/chat` | Send a message and receive AI response |
| POST | `/memory` | Store a user preference or fact |
| GET | `/memory` | Retrieve stored memories for a user |

### Example Request

```json
POST /chat
{
  "user_id": "patient_001",
  "message": "Who am I?"
}
```

### Example Response

```json
{
  "response": "You are a patient using the Dementia Care Assistant. Your caregiver is here to help you."
}
```

---

## 9. Sample Interactions

| User Input | System Response |
|------------|----------------|
| "Who am I?" | Provides patient identity information |
| "I like music" | Stores preference, confirms with acknowledgment |
| "What do I like?" | Retrieves stored preferences from memory |
| "Remind me in 5 minutes" | Sets a timed reminder notification |
| "Help me" | Triggers emergency detection response |
| "I feel sad" | Provides empathetic conversational support |

---

## 10. Known Limitations

- Voice recognition accuracy depends on device microphone quality and ambient noise
- OpenAI API usage is subject to rate limits and token costs
- Reminder system currently supports minute-based intervals only
- No caregiver dashboard implemented in current version
- App-to-app integration (e.g., opening YouTube) not yet implemented

---

## 11. Future Work

- [ ] Caregiver dashboard with patient activity monitoring
- [ ] Multi-user support with secure authentication (JWT)
- [ ] Improved emotion detection using sentiment analysis
- [ ] Integration with calendar and health apps
- [ ] Offline mode with local LLM support
- [ ] Google Play Store release
- [ ] Extended language support for non-English speakers

---

## 12. References

1. World Health Organization. (2023). *Dementia Fact Sheet*. WHO.
2. Brown, T., et al. (2020). Language Models are Few-Shot Learners. *NeurIPS*.
3. Johnson, J., Douze, M., & Jégou, H. (2021). Billion-scale similarity search with GPUs. *IEEE Transactions on Big Data*.
4. Android Developers Documentation. https://developer.android.com
5. OpenAI API Documentation. https://platform.openai.com/docs
6. Railway Documentation. https://docs.railway.app

---

## License

This project was developed for academic purposes as part of the MS Software Engineering program at Arizona State University. All rights reserved © 2026 Sujan U J.
