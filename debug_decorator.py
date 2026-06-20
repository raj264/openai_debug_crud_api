import functools
import logging
import os
import traceback

from openai import OpenAI
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


def auto_debug_with_openai(func):
    """
    A decorator to catch unexpected exceptions, send the traceback to OpenAI,
    and log the suggested fix. Routine HTTP errors raised via Flask's abort()
    (HTTPException) are re-raised untouched, since they're expected client
    errors, not bugs worth spending an API call to diagnose.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception:
            tb = traceback.format_exc()
            prompt = (
                f"I encountered this error in a Flask API function.\n\n"
                f"Traceback:\n{tb}\n"
                f"Can you explain the error and suggest a fix?"
            )

            try:
                response = _get_client().chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                )
                suggestion = response.choices[0].message.content
            except Exception as openai_error:
                suggestion = f"(Failed to get suggestion from OpenAI: {openai_error})"

            logger.error("Unhandled exception in %s\n[OpenAI Debug Suggestion]:\n%s", func.__name__, suggestion)
            raise  # Re-raise the original exception

    return wrapper
