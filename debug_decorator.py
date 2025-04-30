import openai
import os
import functools
import traceback

# Set your OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def auto_debug_with_openai(func):
    """
    A decorator to catch exceptions, send the traceback to OpenAI,
    and print out the suggested fix from ChatGPT.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            tb = traceback.format_exc()
            prompt = (
                f"I encountered this error in a Flask API function.\n\n"
                f"Traceback:\n{tb}\n"
                f"Can you explain the error and suggest a fix?"
            )

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                suggestion = response.choices[0].message.content
            except Exception as openai_error:
                suggestion = f"(Failed to get suggestion from OpenAI: {openai_error})"

            print("\n[OpenAI Debug Suggestion]:\n" + suggestion)
            raise  # Re-raise the original exception

    return wrapper
