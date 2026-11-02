# Installation Guide

## Requirements

- Python 3.10 or newer
- Windows, macOS, or Linux
- Internet connection only for initial package installation

## Windows Installation

1. Extract `AI_Flashcard_Quiz_Engine.zip`.
2. Open Command Prompt or PowerShell.
3. Navigate to the project folder:

```bat
cd AI_Flashcard_Quiz_Engine
```

4. Create a virtual environment:

```bat
python -m venv venv
```

5. Activate it:

```bat
venv\Scripts\activate
```

6. Install dependencies:

```bat
pip install -r requirements.txt
```

7. Run the application:

```bat
python app.py
```

8. Open the browser at:

```text
http://127.0.0.1:5000
```

## Optional AI Configuration

Create a file named `.env` in the project root:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

The application works without this file.
