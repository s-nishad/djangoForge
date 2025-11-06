# contextiq/rag_llm.py
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

def llm_pipeline():
    """
    Initialize a lightweight instruction-tuned pipeline for QA.
    Uses fallback-friendly model for slow machines.
    """
    try:
        pipe = pipeline("text2text-generation", model="google/flan-t5-small")
        return pipe
    except Exception as e:
        logger.error(f"Failed to initialize LLM pipeline: {e}")
        return None

def generate_answer(context: str, question: str):
    """
    Generate a concise answer given a context and question.
    If model or inference fails, returns the full context as fallback.
    """
    if not context.strip():
        return "No relevant content found."

    prompt = f"Context: {context}\nQuestion: {question}\nAnswer concisely:"

    pipe = llm_pipeline()
    if pipe is None:
        logger.warning("Using fallback answer (full context) due to pipeline failure.")
        return context  # Fallback: return full context text

    try:
        result = pipe(prompt, max_length=300, do_sample=False)
        answer = result[0]['generated_text']
    except Exception as e:
        logger.error(f"Failed during answer generation: {e}")
        logger.warning("Using fallback answer (full context) due to runtime error.")
        answer = context  # Fallback: full text

    return answer
