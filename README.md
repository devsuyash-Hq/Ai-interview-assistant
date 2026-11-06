# AI Interview Assistant 🎙️

A voice-enabled mock interview simulator powered by the OpenAI API. It generates
role-specific technical interview questions (optionally tailored to your resume),
listens to your spoken answers, scores them in real time, and produces a full
performance report at the end of the session.

## Features

- **Resume-aware questioning** — parses a PDF resume and tailors questions to your actual skills/projects
- **Role & difficulty targeting** — e.g. "Java Backend Developer Intern", easy/medium/hard
- **Voice interaction** — asks questions aloud (TTS) and transcribes your spoken answers (speech-to-text)
- **Real-time AI evaluation** — each answer is scored 0–10 with strengths, gaps, and an ideal-answer tip
- **Automatic report generation** — a timestamped `.txt` report with per-question feedback and an overall summary
- **Graceful fallbacks** — works via typed input if no microphone/speaker is detected

## Tech Stack

| Component            | Technology                          |
|-----------------------|--------------------------------------|
| Core language          | Python 3.10+                        |
| AI / question generation & scoring | OpenAI API (Chat Completions) |
| Resume parsing          | `pdfplumber`                        |
| Speech-to-text          | `SpeechRecognition` (Google Web Speech API) |
| Text-to-speech          | `pyttsx3`                            |
| Config management       | `python-dotenv`                      |

## Project Structure

```
ai_interview_assistant/
├── main.py               # Entry point — orchestrates the interview flow
├── config.py              # Loads API key & settings from .env
├── ai_engine.py            # All OpenAI calls: summarize, generate, evaluate
├── voice_engine.py          # Text-to-speech + speech-to-text
├── resume_parser.py         # PDF text extraction
├── report_generator.py       # Builds & saves the final report
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

1. **Clone/copy the project folder** onto your machine.
2. **Create a virtual environment** (recommended):
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```
3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
   > **Windows note:** `PyAudio` sometimes fails to install directly via pip.
   > If it fails, run: `pip install pipwin` then `pipwin install pyaudio`.
4. **Set up your API key:**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key: `OPENAI_API_KEY=sk-...`
5. **Run it:**
   ```
   python main.py
   ```

## How It Works (Flow)

1. You provide a resume path (optional), target role, difficulty, and number of questions.
2. If a resume is provided, `ai_engine.summarize_resume()` extracts a structured JSON summary of skills/projects.
3. `ai_engine.generate_questions()` uses that context to generate tailored questions via the OpenAI API.
4. For each question:
   - `voice_engine.speak()` reads it aloud
   - `voice_engine.listen()` records and transcribes your spoken answer
   - `ai_engine.evaluate_answer()` scores it and gives feedback
5. After all questions, `ai_engine.generate_final_report()` produces an overall summary.
6. `report_generator.save_report()` writes everything to a timestamped `.txt` file in `/reports`.

## Sample Session (excerpt)

```
🎤 Interviewer: Question 1: Can you explain how you resolved the race
condition in your testcontainers-java MongoDBContainer fix?

🎙️  Listening... (speak now)
You said: I added a wait strategy that checks for a specific log
message before the container is considered ready...

→ Score: 8/10
→ Improve: Mention how you verified the fix under load / CI
```

## Possible Extensions

- Swap the CLI for a Tkinter or web (Flask) front end
- Add sentiment/confidence analysis on tone of voice
- Support behavioral (STAR-format) question sets alongside technical ones
- Export the report as a formatted PDF instead of plain text

## Author

Built by Suyash as a portfolio project demonstrating integration of LLM APIs,
speech processing, and structured AI-output design in a real, usable tool.
