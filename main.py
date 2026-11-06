"""
AI Interview Assistant — Entry Point
=====================================
A voice-enabled mock interview tool that:
  1. Optionally parses a candidate's resume (PDF)
  2. Generates role-specific interview questions via OpenAI
  3. Asks questions aloud and listens to spoken answers
  4. Scores each answer and gives real-time feedback
  5. Produces a final performance report

Run:
    python main.py
"""

from ai_engine import AIInterviewEngine
from voice_engine import VoiceEngine
from resume_parser import extract_text_from_pdf
from report_generator import save_report
from config import Config


def get_setup_inputs():
    print("=" * 60)
    print(" AI INTERVIEW ASSISTANT")
    print("=" * 60)

    resume_path = input("Path to resume PDF (leave blank to skip): ").strip()
    role = input("Target role (e.g., 'Java Backend Developer Intern'): ").strip()
    difficulty = input("Difficulty [easy/medium/hard] (default medium): ").strip() or "medium"
    num_q_raw = input(f"Number of questions (default {Config.DEFAULT_NUM_QUESTIONS}): ").strip()
    num_q = int(num_q_raw) if num_q_raw.isdigit() else Config.DEFAULT_NUM_QUESTIONS

    return resume_path, role, difficulty, num_q


def main():
    resume_path, role, difficulty, num_q = get_setup_inputs()

    engine = AIInterviewEngine()
    voice = VoiceEngine(rate=Config.VOICE_RATE)

    resume_summary = None
    if resume_path:
        try:
            resume_text = extract_text_from_pdf(resume_path)
            print("Analyzing resume...")
            resume_summary = engine.summarize_resume(resume_text)
        except Exception as e:
            print(f"Could not read resume ({e}). Continuing without it.")

    print("\nGenerating interview questions...")
    questions = engine.generate_questions(role, difficulty, num_q, resume_summary)

    if not questions:
        print("Failed to generate questions. Check your API key and internet connection.")
        return

    qa_records = []
    voice.speak(
        f"Let's begin your mock interview for the {role} role. "
        f"I'll ask you {len(questions)} questions."
    )

    for i, q in enumerate(questions, 1):
        voice.speak(f"Question {i}: {q['question']}")
        answer = voice.listen()

        print("Evaluating your answer...")
        evaluation = engine.evaluate_answer(q["question"], answer)

        print(f"→ Score: {evaluation.get('score', 'N/A')}/10")
        if evaluation.get("improvements"):
            print(f"→ Improve: {', '.join(evaluation['improvements'])}")

        qa_records.append({
            "question": q["question"],
            "topic": q.get("topic", ""),
            "answer": answer,
            "evaluation": evaluation,
        })

    print("\nGenerating overall feedback...")
    overall_summary = engine.generate_final_report(qa_records)
    voice.speak("Here's your overall feedback.")
    print(f"\n{overall_summary}\n")

    filepath = save_report(qa_records, overall_summary)
    print(f"Full report saved to: {filepath}")


if __name__ == "__main__":
    main()
