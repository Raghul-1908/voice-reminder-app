import os
import json
import re
import datetime
import requests

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, util
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app)

REMINDERS_FILE = "reminders.json"

# --------------------------
# Embedding model (for similarity removal)
# --------------------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# --------------------------
# Scheduler
# --------------------------
scheduler = BackgroundScheduler()
scheduler.start()

# --------------------------
# Storage Helpers
# --------------------------

def load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return []
    with open(REMINDERS_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=4)

# --------------------------
# Time Parser
# --------------------------

def parse_time_from_text(text):
    text = text.lower()
    match = re.search(r'(\d+)\s*(second|seconds|minute|minutes|hour|hours)', text)
    if not match:
        return None

    value = int(match.group(1))
    unit = match.group(2)

    if "second" in unit:
        delta = datetime.timedelta(seconds=value)
    elif "minute" in unit:
        delta = datetime.timedelta(minutes=value)
    elif "hour" in unit:
        delta = datetime.timedelta(hours=value)
    else:
        return None

    return datetime.datetime.now() + delta

# --------------------------
# Mark reminder as due
# --------------------------

def mark_due(reminder_id):
    reminders = load_reminders()
    for r in reminders:
        if r["id"] == reminder_id:
            r["status"] = "due"
    save_reminders(reminders)

# --------------------------
# llama.cpp (TinyLlama) Optimized Logic
# --------------------------

def process_with_model(user_text):
    # TinyLlama performs best with ChatML or Llama-2 template
    # This prompt tells it to be a helpful assistant first, but use JSON for tools
    prompt = f"""<|system|>
You are a helpful voice assistant.
- If the user wants to set a reminder, answer ONLY: ["add", "task description"]
- If the user wants to delete a reminder, answer ONLY: ["remove", "task description"]
- For any other question, provide a short, conversational answer.</s>
<|user|>
{user_text}</s>
<|assistant|>
"""

    try:
        response = requests.post(
            "http://127.0.0.1:8080/completion",
            json={
                "prompt": prompt,
                "n_predict": 128,      # Enough for conversational answers
                "temperature": 0.7,    # Balanced creativity
                "top_k": 40,
                "top_p": 0.9,
                "stop": ["</s>", "<|user|>", "User:"] # Crucial for CPU efficiency
            },
            timeout=30
        )

        result = response.json()
        text = result.get("content", "").strip()

        # Check for Reminder Command in the output
        match = re.search(r'\[\s*"(add|remove)"\s*,\s*"(.*?)"\s*\]', text)
        if match:
            return match.group(1), match.group(2)

        # If it's just text, treat it as a 'chat' intent
        return "chat", text

    except Exception as e:
        print("Local LLM Error:", e)
        return "chat", "I can't reach the model right now. Is llama.cpp running on port 8080?"

# --------------------------
# Remove Most Similar Reminder
# --------------------------

def remove_most_similar(text):
    reminders = load_reminders()
    if not reminders:
        return None

    texts = [r["text"] for r in reminders]
    embeddings = embedding_model.encode(texts, convert_to_tensor=True)
    query_embedding = embedding_model.encode(text, convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, embeddings)
    best_index = scores.argmax().item()

    removed = reminders.pop(best_index)
    save_reminders(reminders)
    return removed

# --------------------------
# Routes
# --------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/list")
def list_reminders():
    return jsonify(load_reminders())

@app.route("/acknowledge", methods=["POST"])
def acknowledge():
    rid = request.json.get("id")
    reminders = load_reminders()
    reminders = [r for r in reminders if r["id"] != rid]
    save_reminders(reminders)
    return jsonify({"status": "cleared"})

@app.route("/personal-ai", methods=["POST"])
def personal_ai():
    user_text = request.json.get("text", "")
    
    # Process intent using TinyLlama
    intent, content = process_with_model(user_text)

    # ---------------- ADD ----------------
    if intent == "add":
        trigger_time = parse_time_from_text(user_text)
        if not trigger_time:
            return jsonify({"reply": "I heard you want a reminder, but I need a time, like 'in 5 minutes'."})

        reminders = load_reminders()
        reminder_id = f"rem_{int(datetime.datetime.now().timestamp())}"
        
        new_reminder = {
            "id": reminder_id,
            "text": content,
            "time": trigger_time.isoformat(),
            "status": "pending"
        }
        reminders.append(new_reminder)
        save_reminders(reminders)

        scheduler.add_job(
            func=mark_due,
            trigger="date",
            run_date=trigger_time,
            args=[reminder_id],
            id=reminder_id
        )
        return jsonify({"reply": f"Alright, I'll remind you to {content}."})

    # ---------------- REMOVE ----------------
    elif intent == "remove":
        removed = remove_most_similar(content)
        if removed:
            return jsonify({"reply": f"Deleted the reminder for {removed['text']}."})
        else:
            return jsonify({"reply": "I couldn't find a matching reminder to remove."})

    # ---------------- CHAT / ANSWERS ----------------
    else:
        # If intent is 'chat', the content is the LLM's direct answer
        return jsonify({"reply": content})

if __name__ == "__main__":
    app.run(debug=True, port=5000)