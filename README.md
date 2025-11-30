# OpenAI Chat App

A simple command-line chat application using the OpenAI API.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) - Python package and project manager
  - Install via curl:
    ```bash
    curl -sSL https://install.astral.sh | python3 -
    ```
- An OpenAI API key

## Setup

1. **Clone the repository and navigate to the project directory**

2. **Set your OpenAI API key as an environment variable:**

   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

3. **Install dependencies:**

   ```bash
   uv sync
   ```

## Running the App

```bash
uv run main.py
```

Type your messages and press Enter to chat with the AI. Type `quit` to exit.
