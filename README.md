# 🎤 Voice Reminder App

A simple and lightweight **Voice Reminder App** built using **Flask** that allows users to create and manage reminders through voice commands and a clean web interface. The application stores reminders in a JSON file, making it easy to deploy without requiring a database.

---

## ✨ Features

- 🎙️ Voice-based reminder creation
- 📝 Add reminders manually
- 📋 View all saved reminders
- 🗑️ Delete completed reminders
- 💾 JSON-based storage (No database required)
- 🌐 Simple Flask web interface
- ⚡ Lightweight and easy to run

---

## 📂 Project Structure

```
Voice-Reminder-App/
│
├── static/
│   ├── style.css
│   ├── script.js
│   └── assets/
│
├── templates/
│   └── index.html
│
├── app.py
├── reminders.json
├── requirements.txt
└── README.md
```

---

## 🛠 Technologies Used

- Python 3
- Flask
- HTML5
- CSS3
- JavaScript
- JSON

---

## 📁 File Description

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application |
| `reminders.json` | Stores all reminder data |
| `templates/` | HTML pages |
| `static/` | CSS, JavaScript, and assets |
| `requirements.txt` | Python dependencies |

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/Raghul_1908voice-reminder-app.git
```

Move into the project directory:

```bash
cd voice-reminder-app
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the Flask server:

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 🎙️ How It Works

1. Open the application in your browser.
2. Click the microphone button.
3. Speak your reminder naturally.
4. The reminder is processed and saved.
5. All reminders are stored in `reminders.json`.
6. View, manage, or delete reminders anytime.

---

## 📌 Example Voice Commands

```
Remind me to submit my assignment tomorrow.

Remind me to call Mom at 7 PM.

Remind me to attend the team meeting on Friday.

Remind me to drink water every hour.
```

---

## 🌟 Future Improvements

- 🔔 Desktop notifications
- 📱 Mobile-friendly interface
- ☁️ Cloud synchronization
- 📅 Google Calendar integration
- 🤖 AI-powered natural language understanding
- ⏰ Recurring reminders
- 📧 Email and SMS notifications
- 🔊 Text-to-Speech reminder playback

---

## 🎯 Applications

- Personal task management
- Daily scheduling
- Student assignment reminders
- Medication reminders
- Meeting notifications
- Productivity assistant

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests for improvements or bug fixes.

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Developed as a learning project to demonstrate voice recognition, Flask web development, and lightweight reminder management using JSON storage.
