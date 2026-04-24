from flask import Blueprint, request, jsonify
from sqlalchemy import text
from app import db
from app.models import Memory
from app.embedding import get_embedding
from openai import OpenAI
from datetime import datetime

client = OpenAI()

main = Blueprint("main", __name__)

# ================= HOME =================
@main.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dementia Care Assistant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #f0f4f8; color: #333; }
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; text-align: center; padding: 80px 20px;
        }
        .hero h1 { font-size: 2.8em; margin-bottom: 15px; }
        .hero p { font-size: 1.2em; opacity: 0.9; max-width: 600px; margin: 0 auto 30px; }
        .badge {
            display: inline-block; background: rgba(255,255,255,0.2);
            padding: 8px 20px; border-radius: 20px; font-size: 0.9em; margin: 5px;
        }
        .container { max-width: 1000px; margin: 0 auto; padding: 50px 20px; }
        .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; margin: 40px 0; }
        .card {
            background: white; border-radius: 12px; padding: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }
        .card .icon { font-size: 2.5em; margin-bottom: 15px; }
        .card h3 { font-size: 1.2em; margin-bottom: 10px; color: #667eea; }
        .card p { color: #666; line-height: 1.6; }
        .endpoints { background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); }
        .endpoints h2 { margin-bottom: 20px; color: #333; }
        .endpoint { display: flex; align-items: center; padding: 12px 0; border-bottom: 1px solid #f0f0f0; }
        .endpoint:last-child { border-bottom: none; }
        .method { background: #667eea; color: white; padding: 4px 10px; border-radius: 5px; font-size: 0.8em; font-weight: bold; margin-right: 15px; min-width: 50px; text-align: center; }
        .method.get { background: #48bb78; }
        .url { font-family: monospace; font-weight: bold; margin-right: 15px; }
        .desc { color: #666; font-size: 0.9em; }
        .status { text-align: center; padding: 30px; }
        .status-dot { display: inline-block; width: 12px; height: 12px; background: #48bb78; border-radius: 50%; margin-right: 8px; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        .footer { text-align: center; padding: 30px; color: #999; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="hero">
        <h1>🧠 Dementia Care Assistant</h1>
        <p>An AI-powered mobile application helping dementia patients with daily activities, memory support, and reminders.</p>
        <span class="badge">🎓 Arizona State University</span>
        <span class="badge">📱 Android App</span>
        <span class="badge">🤖 OpenAI GPT</span>
        <span class="badge">🗄️ PostgreSQL + pgvector</span>
    </div>

    <div class="container">
        <div class="status">
            <span class="status-dot"></span>
            <strong>All Systems Operational</strong> — Backend is live and running
        </div>

        <div class="cards">
            <div class="card">
                <div class="icon">🎙️</div>
                <h3>Voice Interaction</h3>
                <p>Speech-to-text and text-to-speech for hands-free patient interaction using Android Speech Recognition API.</p>
            </div>
            <div class="card">
                <div class="icon">🧠</div>
                <h3>AI Memory System</h3>
                <p>Stores and retrieves patient preferences using vector embeddings and semantic similarity search with pgvector.</p>
            </div>
            <div class="card">
                <div class="icon">⏰</div>
                <h3>Smart Reminders</h3>
                <p>Natural language reminder parsing — patients can say "Remind me in 5 minutes" and the system handles the rest.</p>
            </div>
            <div class="card">
                <div class="icon">🚨</div>
                <h3>Emergency Detection</h3>
                <p>Detects emergency keywords like "help" and triggers immediate caregiver alerts and response protocols.</p>
            </div>
            <div class="card">
                <div class="icon">💬</div>
                <h3>Conversational AI</h3>
                <p>GPT-4o-mini powered conversations tailored for dementia patients — simple, calm, and supportive responses.</p>
            </div>
            <div class="card">
                <div class="icon">🔒</div>
                <h3>Persistent Memory</h3>
                <p>Every conversation is stored and used to personalize future interactions for each individual patient.</p>
            </div>
        </div>

        <div class="endpoints">
            <h2>📡 API Endpoints</h2>
            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="url">/</span>
                <span class="desc">Landing page — system status</span>
            </div>
            <div class="endpoint">
                <span class="method">POST</span>
                <span class="url">/chat</span>
                <span class="desc">Main AI chat endpoint with memory retrieval</span>
            </div>
            <div class="endpoint">
                <span class="method">POST</span>
                <span class="url">/store</span>
                <span class="desc">Store a new memory or conversation</span>
            </div>
            <div class="endpoint">
                <span class="method">POST</span>
                <span class="url">/search</span>
                <span class="desc">Semantic search through stored memories</span>
            </div>
            <div class="endpoint">
                <span class="method">POST</span>
                <span class="url">/memory-assistant</span>
                <span class="desc">Answer identity questions (Who am I?)</span>
            </div>
            <div class="endpoint">
                <span class="method">POST</span>
                <span class="url">/smart-reminder</span>
                <span class="desc">Medicine and task reminder system</span>
            </div>
            <div class="endpoint">
                <span class="method">POST</span>
                <span class="url">/incident</span>
                <span class="desc">Log emergency incidents with timestamp</span>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>Built by <strong>Sujan U J</strong> — MS Software Engineering, Arizona State University © 2026</p>
        <p style="margin-top:8px;">Deployed on Railway · Powered by OpenAI · Android + Flask + PostgreSQL</p>
    </div>
</body>
</html>
"""

# ================= STORE MEMORY =================
@main.route("/store", methods=["POST"])
def store():
    data = request.json
    message = data.get("message")
    user_id = data.get("user_id", "default")
    if not message:
        return jsonify({"error": "message required"}), 400
    try:
        embedding = get_embedding(message)
    except Exception as e:
        print("Embedding failed:", e)
        embedding = None
    new_memory = Memory(user_id=user_id, message=message, embedding=embedding)
    db.session.add(new_memory)
    db.session.commit()
    return jsonify({"status": "stored"})


# ================= SEARCH MEMORY =================
@main.route("/search", methods=["POST"])
def search():
    data = request.json
    query = data.get("query")
    if not query:
        return jsonify({"error": "query required"}), 400
    try:
        query_embedding = get_embedding(query)
    except Exception as e:
        return jsonify({"error": "embedding failed"}), 500
    results = db.session.execute(
        text("""
            SELECT message FROM conversation_memory
            ORDER BY embedding <-> CAST(:query_embedding AS vector)
            LIMIT 3;
        """),
        {"query_embedding": query_embedding}
    ).fetchall()
    return jsonify({"query": query, "similar_messages": [r[0] for r in results]})


# ================= MEMORY ASSISTANT =================
@main.route("/memory-assistant", methods=["POST"])
def memory_assistant():
    query = request.json.get("query", "").lower()
    if "who am i" in query:
        return jsonify({"response": "You are a patient using the Dementia Care Assistant. Your caregiver is here to help you."})
    if "where am i" in query:
        return jsonify({"response": "You are safe. You are at your home."})
    return jsonify({"response": "I'm here to help you 😊"})


# ================= INCIDENT LOGGING =================
@main.route("/incident", methods=["POST"])
def incident():
    data = request.json
    description = data.get("description", "No details")
    print(f"🚨 INCIDENT: {description} at {datetime.now()}")
    return jsonify({"status": "Incident logged successfully", "time": str(datetime.now())})


# ================= SMART REMINDER =================
@main.route("/smart-reminder", methods=["POST"])
def smart_reminder():
    data = request.json
    taken = data.get("taken")
    if taken is False:
        return jsonify({"response": "You missed your medicine. I will remind you again in 10 minutes."})
    return jsonify({"response": "Great job taking your medicine! 😊"})


# ================= CHAT =================
@main.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("message")
    if not query:
        return jsonify({"error": "message is required"}), 400
    try:
        query_embedding = get_embedding(query)
    except Exception as e:
        return jsonify({"error": "embedding failed", "details": str(e)}), 500
    results = db.session.execute(
        text("""
            SELECT message FROM conversation_memory
            ORDER BY embedding <-> CAST(:query_embedding AS vector)
            LIMIT 5;
        """),
        {"query_embedding": query_embedding}
    ).fetchall()
    memory_context = [r[0] for r in results]
    context_text = "\n".join(memory_context)
    prompt = f"""
You are a calm, friendly assistant helping a dementia patient.
Rules:
- Keep responses short and simple.
- Be supportive and reassuring.
- Use patient-friendly language.
- If memory is useful, use it.

Relevant memory:
{context_text}

User: {query}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful healthcare assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        return jsonify({"error": "chat failed", "details": str(e)}), 500
    new_memory = Memory(user_id="default", message=query, embedding=query_embedding)
    db.session.add(new_memory)
    db.session.commit()
    return jsonify({"query": query, "response": answer, "memory_used": memory_context})
