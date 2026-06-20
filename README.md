# 🧠 OpenAI Debug CRUD API

A Flask-based REST API demonstrating CRUD operations with in-memory storage, enhanced by OpenAI-powered auto-debugging. Unexpected exceptions are sent to OpenAI for an explanation/fix suggestion; routine client errors (400/404) are not.

## ✅ Features

- CRUD operations for user management, backed by an in-memory store (thread-safe via a lock)
- OpenAI-powered error analysis on unexpected exceptions only - routine `abort()` errors (400/404) are passed through untouched, so they don't burn API calls
- Reusable `auto_debug_with_openai` decorator for consistent error handling across endpoints
- Structured logging via the `logging` module
- Input validation (name must be a non-empty string)
- Unit tests (pytest) covering CRUD routes and the decorator's error-handling paths

## 🛠️ Getting Started

### Prerequisites

- Python 3.9+
- An OpenAI API key

### Installation

```bash
git clone https://github.com/raj264/openai_debug_crud_api.git
cd openai_debug_crud_api
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configure

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_DEBUG=false   # defaults to false; only set true for local debugging
```

## 🚀 Running the Application

```bash
python main.py
```

The API is accessible at `http://127.0.0.1:5000/`.

## 🧪 Running Tests

```bash
pytest
```

## 📬 API Endpoints

| Method | Path | Body | Description |
|---|---|---|---|
| POST | `/users` | `{"name": "Alice"}` | Create a user |
| GET | `/users` | - | List all users |
| GET | `/users/<user_id>` | - | Get a user by ID |
| PUT | `/users/<user_id>` | `{"name": "Bob"}` | Update a user's name |
| DELETE | `/users/<user_id>` | - | Delete a user |

## 🤖 OpenAI Debug Decorator

`auto_debug_with_openai` wraps each route. On an **unexpected** exception, it:

1. Captures the full traceback.
2. Sends it to OpenAI (`gpt-3.5-turbo`) for an explanation/fix suggestion.
3. Logs the suggestion via `logging`.
4. Re-raises the original exception.

Flask's `HTTPException` (raised by `abort(400)`/`abort(404)`) is re-raised immediately, without involving OpenAI - those are expected client errors, not bugs.

## 📄 License

MIT License.

## 🙌 Acknowledgments

- [OpenAI](https://openai.com/) for the API used for error analysis.
- [Flask](https://flask.palletsprojects.com/) for the web framework.
