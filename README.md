# OpenAI Chat App

A simple command-line chat application using the OpenAI API.

## How to scan for AI-BOM

Use the Snyk CLI with an AI-BOM command:

```sh
snyk aibom --experimental --json
```

Pipe the Snyk CLI output of AI-BOM findings to `jq` to easily find and match your results:

```sh
snyk aibom --experimental --json  | jq '.components[] | select(."bom-ref" | startswith("model:")) | ."bom-ref"'
```

Get a fancy visual view of the AI-BOM findings using `ai-bom-visualizer` npm package:

```sh
snyk aibom --experimental --json  | npx ai-bom-visualizer --open
```

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

### OpenAI Chat

```bash
uv run main.py
```

Type your messages and press Enter to chat with the AI. Type `quit` to exit.

### Whisper Speech-to-Text

```bash
uv run whisper.py
```

This script demonstrates **speech-to-text transcription and translation** using OpenAI's Whisper model:

- Loads a fine-tuned Whisper model (`whisper-medium-fleurs-lang-id`) for language identification
- Streams French audio samples from the Common Voice dataset
- Translates the French speech into English text
- Uses the Hugging Face `transformers` and `datasets` libraries

**Note:** The first run will download the model (~1.5GB) and stream audio samples.

### BLIP Visual Question Answering

```bash
uv run blip.py
```

This script demonstrates **visual question answering (VQA)** using Salesforce's BLIP model:

- Loads the BLIP VQA model (`blip-vqa-base`) from Hugging Face
- Downloads a sample image from the web
- Asks a question about the image ("how many men are in the picture?")
- Returns a natural language answer based on the image content

**Note:** The first run will download the model (~1GB).

## Examples

Other example projects you can clone and scan for AI-BOM findings:
- https://github.com/snyk-labs/ai-buffet/
- https://github.com/aws-samples/generative-ai-on-amazon-sagemaker/
- https://github.com/aws-samples/amazon-bedrock-workshop
