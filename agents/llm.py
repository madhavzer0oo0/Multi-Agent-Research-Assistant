import os
import re
import time

from dotenv import load_dotenv
from langchain_groq import ChatGroq


DEFAULT_MODEL = "llama-3.1-8b-instant"


def build_llm(
    model_name: str = DEFAULT_MODEL,
    temperature: float = 0.2,
    max_tokens: int = 900,
) -> ChatGroq:
    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("Set GROQ_API_KEY in your .env file before running the app.")
    return ChatGroq(model=model_name, temperature=temperature, max_tokens=max_tokens)


def invoke_with_retry(chain, payload, retries: int = 2):
    for attempt in range(retries + 1):
        try:
            return chain.invoke(payload)
        except Exception as exc:
            message = str(exc)
            if "rate_limit" not in message.lower() and "rate limit" not in message.lower():
                raise
            if attempt == retries:
                raise RuntimeError(
                    "Groq rate limit reached. Please wait a few seconds and run again."
                ) from exc
            wait_seconds = _rate_limit_wait_seconds(message)
            time.sleep(wait_seconds)


def _rate_limit_wait_seconds(message: str) -> float:
    match = re.search(r"try again in ([0-9.]+)s", message, re.IGNORECASE)
    if match:
        return float(match.group(1)) + 1
    return 8
