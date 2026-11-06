# Talking Points: AI Interview Assistant

Use these if an interviewer asks about this project.

## 30-second pitch

"I built a voice-enabled mock interview simulator in Python. It parses a
candidate's resume, generates tailored technical questions using the OpenAI
API, listens to spoken answers via speech recognition, scores them in real
time, and produces a full feedback report. I built it to practice structured
prompt design and to have a reusable tool for my own interview prep."

## STAR story: designing reliable AI output

- **Situation:** The AI engine needed to return structured data (questions,
  scores, feedback) that the rest of the app could parse reliably.
- **Task:** Get consistent, parseable JSON out of a language model instead of
  free-form text that could break the app.
- **Action:** I wrote strict system prompts instructing the model to respond
  ONLY with JSON in a fixed schema, then added a `_safe_json()` helper that
  strips markdown code fences and falls back to an empty result instead of
  crashing on a malformed response.
- **Result:** The app never crashes on a bad AI response — it degrades
  gracefully, which matters a lot for a live demo.

## STAR story: handling hardware dependency (microphone)

- **Situation:** Speech-to-text depends on a working microphone, which isn't
  guaranteed on every machine (e.g. in a demo environment or over remote
  desktop).
- **Task:** Make sure the app is still usable if the mic isn't available.
- **Action:** I added a `mic_available` check at startup and had `listen()`
  fall back to typed input automatically, with the same for text-to-speech.
- **Result:** The same codebase runs identically whether or not audio
  hardware is present — no separate "demo mode" needed.

## Likely follow-up questions & how to answer

**"Why OpenAI instead of a local/offline model?"**
→ Talk about needing reliable structured JSON output at low latency, and
that the architecture (isolated `ai_engine.py`) makes swapping providers
straightforward later.

**"How would you scale this to many concurrent users?"**
→ Move from CLI to a Flask/FastAPI backend, queue OpenAI calls, cache
resume summaries, and store sessions in a database instead of local files.

**"What was the hardest part?"**
→ Getting the model to reliably return valid JSON every time, and handling
audio hardware differences across environments.

**"What would you add next?"**
→ Behavioral/STAR-format question sets, a Tkinter or web UI, and PDF export
of the report.
