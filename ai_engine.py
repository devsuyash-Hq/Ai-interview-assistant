"""
AI Engine
=========
Wraps every call to the Google Gemini API used by the Interview Assistant:

  1. summarize_resume()   -> structured JSON summary of the candidate
  2. generate_questions() -> role/difficulty-specific interview questions
  3. evaluate_answer()    -> per-answer scoring + feedback
  4. generate_final_report() -> overall performance summary

Uses Google's free Gemini API tier (no cost, no credit card required).
Keeping all API calls in one class makes the assistant easy to test,
swap models, or point at a different provider later.
"""

import json
from google import genai
from google.genai import types
from config import Config


class AIInterviewEngine:
    def __init__(self):
        Config.validate()
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model = Config.GEMINI_MODEL

    def _chat(self, system_prompt: str, user_prompt: str, json_mode: bool = True) -> str:
        """Single helper so every call shares the same error handling."""
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.4,
            response_mime_type="application/json" if json_mode else "text/plain",
        )
        response = self.client.models.generate_content(
            model=self.model,
            contents=user_prompt,
            config=config,
        )
        return response.text.strip()

    def summarize_resume(self, resume_text: str) -> dict:
        """Turn raw resume text into a structured skills/experience summary."""
        system_prompt = (
            "You are a technical recruiter. Extract a structured summary "
            "from the resume text below. Respond ONLY with valid JSON in "
            "exactly this schema, no extra commentary: "
            '{"role_fit": str, "skills": [str], "projects": [str], '
            '"experience_level": str}'
        )
        # Truncate to keep prompt size sane for long resumes
        raw = self._chat(system_prompt, resume_text[:6000])
        return self._safe_json(raw)

    def generate_questions(self, role: str, difficulty: str,
                            num_questions: int, resume_summary: dict = None) -> list:
        """Generate a list of {question, topic} objects tailored to the role."""
        context = (
            f"Candidate resume summary: {json.dumps(resume_summary)}"
            if resume_summary else "No resume was provided."
        )
        system_prompt = (
            "You are a senior technical interviewer. Generate interview "
            "questions tailored to the given role and difficulty level. "
            "Mix conceptual and practical/project-based questions. "
            "Respond ONLY with valid JSON: a list of objects shaped like "
            '{"question": str, "topic": str}.'
        )
        user_prompt = (
            f"Role: {role}\n"
            f"Difficulty: {difficulty}\n"
            f"Number of questions: {num_questions}\n"
            f"{context}"
        )
        raw = self._chat(system_prompt, user_prompt)
        questions = self._safe_json(raw)
        return questions if isinstance(questions, list) else []

    def evaluate_answer(self, question: str, answer: str) -> dict:
        """Score a single answer and produce actionable feedback."""
        system_prompt = (
            "You are a strict but fair technical interviewer grading a "
            "candidate's spoken answer. Respond ONLY with valid JSON: "
            '{"score": int (0-10), "strengths": [str], '
            '"improvements": [str], "ideal_answer_tip": str}'
        )
        user_prompt = f"Question: {question}\nCandidate answer: {answer}"
        raw = self._chat(system_prompt, user_prompt)
        return self._safe_json(raw)

    def generate_final_report(self, qa_records: list) -> str:
        """Produce a short overall performance summary across all answers."""
        system_prompt = (
            "You are an interview coach. Given a full mock interview "
            "transcript with per-question scores, write a concise, honest, "
            "encouraging overall performance summary (150-200 words) "
            "covering strengths, weak areas, and 2-3 concrete next steps. "
            "Respond with plain text, not JSON."
        )
        return self._chat(system_prompt, json.dumps(qa_records), json_mode=False)

    @staticmethod
    def _safe_json(raw: str):
        """Strip markdown code fences and parse JSON defensively."""
        cleaned = raw.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {}
