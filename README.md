# Dementia Care Assistant (AI-Based)

This project is an Android-based application designed to help dementia patients with their daily activities. The system uses AI along with voice interaction to provide reminders, basic memory support, and simple conversations.

The goal of this project is to create a supportive and easy-to-use system for patients who may forget important tasks or personal details.

---

## Features

- Voice interaction using speech-to-text and text-to-speech  
- AI-based chat assistant for simple conversations  
- Memory feature to store and recall user preferences  
- Reminder system using natural language input  
- Emergency detection (e.g., when user says "help")  
- Basic memory assistant (answers questions like "Who am I?")

---

## Technologies Used

### Android App
- Kotlin  
- Android Studio  
- Speech Recognition API  
- Text-to-Speech  
- Retrofit for API calls  

### Backend
- Python  
- Flask  
- PostgreSQL with pgvector  
- OpenAI API (for embeddings and chat)  
- SQLAlchemy  

---

## Project Structure

dementia-assistant/
│
├── android-app/
│ └── DementiaAssistant/
│
├── backend/
│ ├── app/
│ ├── run.py
│
└── README.md

---

## How to Run

### Backend
```bash
cd backend
python run.py
```

The backend will run on:
http://localhost:5001


---

### Android App

1. Open the project in Android Studio  
2. Run an emulator  
3. Click Run  

---

## Sample Inputs

You can try the following commands in the app:

- I like music  
- What do I like?  
- Who am I?  
- Remind me in 1 minute  
- Help me  
- I feel sad  

---

## Purpose of the Project

Dementia patients often face difficulty remembering daily tasks, personal preferences, and sometimes even their surroundings. This project attempts to provide a simple assistant that can support them through reminders, conversation, and basic guidance.

---

## Future Improvements

- Add caregiver dashboard  
- Deploy backend to cloud  
- Add login system  
- Improve UI for better accessibility  
- Extend emotion detection  

---

## Author

Sujan U J  
MS Software Engineering  
Arizona State University