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
    return "Backend running!"

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

    new_memory = Memory(
        user_id=user_id,
        message=message,
        embedding=embedding
    )

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
            SELECT message
            FROM conversation_memory
            ORDER BY embedding <-> CAST(:query_embedding AS vector)
            LIMIT 3;
        """),
        {"query_embedding": query_embedding}
    ).fetchall()

    messages = [r[0] for r in results]

    return jsonify({
        "query": query,
        "similar_messages": messages
    })


# ================= MEMORY ASSISTANT =================
@main.route("/memory-assistant", methods=["POST"])
def memory_assistant():
    query = request.json.get("query", "").lower()

    if "who am i" in query:
        return jsonify({
            "response": "You are a patient using the Dementia Care Assistant. Your caregiver is here to help you."
        })

    if "where am i" in query:
        return jsonify({
            "response": "You are safe. You are at your home."
        })

    return jsonify({
        "response": "I'm here to help you 😊"
    })


# ================= INCIDENT LOGGING =================
@main.route("/incident", methods=["POST"])
def incident():
    data = request.json
    description = data.get("description", "No details")

    # (You can later store in DB)
    print(f"🚨 INCIDENT: {description} at {datetime.now()}")

    return jsonify({
        "status": "Incident logged successfully",
        "time": str(datetime.now())
    })


# ================= SMART REMINDER =================
@main.route("/smart-reminder", methods=["POST"])
def smart_reminder():
    data = request.json
    taken = data.get("taken")

    if taken is False:
        return jsonify({
            "response": "You missed your medicine. I will remind you again in 10 minutes."
        })

    return jsonify({
        "response": "Great job taking your medicine! 😊"
    })


# ================= CHAT (MAIN FEATURE - UPGRADED) =================
@main.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("message")

    if not query:
        return jsonify({"error": "message is required"}), 400

    # STEP 1 — embedding
    try:
        query_embedding = get_embedding(query)
    except Exception as e:
        return jsonify({"error": "embedding failed", "details": str(e)}), 500

    # STEP 2 — retrieve memory
    results = db.session.execute(
        text("""
            SELECT message
            FROM conversation_memory
            ORDER BY embedding <-> CAST(:query_embedding AS vector)
            LIMIT 5;
        """),
        {"query_embedding": query_embedding}
    ).fetchall()

    memory_context = [r[0] for r in results]
    context_text = "\n".join(memory_context)

    # STEP 3 — SMART PROMPT (UPGRADED)
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

    # STEP 4 — OpenAI
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

    # STEP 5 — store memory
    new_memory = Memory(
        user_id="default",
        message=query,
        embedding=query_embedding
    )

    db.session.add(new_memory)
    db.session.commit()

    return jsonify({
        "query": query,
        "response": answer,
        "memory_used": memory_context
    })