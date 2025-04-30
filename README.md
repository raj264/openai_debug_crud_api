# 🧠 OpenAI Debug CRUD API

A Flask-based REST API demonstrating CRUD operations with in-memory storage, enhanced by OpenAI-powered auto-debugging via ChatGPT. This project is designed for rapid prototyping and testing, featuring reusable error-handling decorators and a developer-friendly architecture.

## ✅ Features

- Simple CRUD operations for user management
- In-memory data storage (no external database required)
- OpenAI integration for real-time error analysis and debugging suggestions
- Reusable decorator for consistent error handling across endpoints
- Modular codebase for easy integration into existing projects
- JSON-formatted error responses
- Environment variable management using `.env` files
- Logging for monitoring application behavior
- Interactive API documentation with Swagger UI
- Unit tests for ensuring code reliability

## 🛠️ Getting Started

### Prerequisites

- Python 3.7 or higher
- OpenAI API key

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/raj264/openai_debug_crud_api.git
   cd openai_debug_crud_api
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   Create a `.env` file in the project root with the following content:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🚀 Running the Application

Start the Flask development server:

```bash
python main.py
```

The API will be accessible at `http://127.0.0.1:5000/`.

## 🧪 Running Tests

To run the unit tests:

```bash
pytest
```

## 📬 API Endpoints

### Create a New User

- **Endpoint**: `POST /users`
- **Request Body**:

  ```json
  {
    "name": "Alice"
  }
  ```

- **Response**: Returns the created user object with a unique ID.

### Retrieve All Users

- **Endpoint**: `GET /users`
- **Response**: Returns a list of all user objects.

### Retrieve a User by ID

- **Endpoint**: `GET /users/<user_id>`
- **Response**: Returns the user object with the specified ID.

### Update a User's Name

- **Endpoint**: `PUT /users/<user_id>`
- **Request Body**:

  ```json
  {
    "name": "Bob"
  }
  ```

- **Response**: Returns the updated user object.

### Delete a User

- **Endpoint**: `DELETE /users/<user_id>`
- **Response**: Returns the deleted user object.

## 🤖 OpenAI Debug Decorator

The `auto_debug_with_openai` decorator enhances error handling by:

1. Catching exceptions in the decorated function.
2. Capturing the full traceback.
3. Sending the traceback to OpenAI's API with a prompt for analysis.
4. Logging the AI's suggested fix to the console.

This provides immediate, AI-driven insights into errors, streamlining the debugging process.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙌 Acknowledgments

- [OpenAI](https://openai.com/) for providing the API used for error analysis.
- [Flask](https://flask.palletsprojects.com/) for the web framework.
