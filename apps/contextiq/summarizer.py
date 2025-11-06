# contextiq/summarizer.py
from langdetect import detect
from transformers import pipeline, Pipeline
import logging

logger = logging.getLogger(__name__)

def summarize_pipe() -> Pipeline | None:
    """
    Initialize summarization pipeline.
    Returns None if initialization fails.
    """
    try:
        return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    except Exception as e:
        logger.error(f"Failed to initialize summarization pipeline: {e}")
        return None


def summarize_document(text: str):
    """
    Detect language and generate a short summary using HuggingFace model.
    Returns tuple: (language_code, summary_text)
    If summarization fails, returns (language_code, "").
    """
    if not text.strip():
        raise ValueError("Cannot summarize empty text")

    # Detect language (fallback to 'unknown' if detection fails)
    try:
        language = detect(text)
    except Exception:
        language = "unknown"

    # for now 
    return language, ""

    # summarizer_pipeline = summarize_pipe()
    # if summarizer_pipeline is None:
    #     logger.warning("Summarizer not initialized; returning empty summary.")
    #     return language, ""

    # try:
    #     summary = summarizer_pipeline(
    #         text[:5000],
    #         max_length=150,
    #         min_length=50,
    #         do_sample=False
    #     )
    #     summary_text = summary[0].get("summary_text", "").strip()
    # except Exception as e:
    #     logger.error(f"Error during summarization: {e}")
    #     summary_text = ""

    # return language, summary_text
