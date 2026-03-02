# Gemini Image Object Detection

Detect objects in images using Google Gemini's multimodal vision API and draw annotated bounding boxes on the output image. 

Note: supporting docs from Google on the Gemini model usage for object detection: https://ai.google.dev/gemini-api/docs/image-understanding


This project uses [uv](https://docs.astral.sh/uv/) for dependency management and [1Password CLI (`op`)](https://developer.1password.com/docs/cli/) to inject the Gemini API key at runtime.

## Prerequisites

- [uv](https://docs.astral.sh/uv/installation/) installed
- [1Password CLI (`op`)](https://developer.1password.com/docs/cli/get-started/) installed and signed in
- A Gemini API key stored in 1Password (the secret reference is configured in `.env`)

## Project layout

```
├── .env                # 1Password secret reference for GEMINI_API_KEY
├── detect.py           # Main detection script
├── run.sh              # One-command runner (wraps op + uv)
├── image.png           # Input image (place your image here)
├── pyproject.toml      # Project metadata and dependencies
└── README.md
```

## Setup

The `.env` file contains a 1Password secret reference:

```
GEMINI_API_KEY=op://Private/Gemini API Key/credential
```

Edit the vault, item, and field names to match your 1Password setup.

## Running

The quickest way — just run the wrapper script:

```bash
./run.sh
```

This is equivalent to the full command:

```bash
op run --env-file=.env -- uv run python detect.py
```

Either way, this will:

1. Use `op run` to resolve the 1Password secret reference in `.env` and inject `GEMINI_API_KEY` as a real environment variable
2. Use `uv run` to create the virtual environment (if needed), install dependencies, and execute the script
3. Load `image.png` from the current directory, send it to Gemini for object detection, draw bounding boxes, and save the result as `output_annotated.png`

### Custom image path

Override the input or output paths with environment variables:

```bash
IMAGE_PATH=./my-photo.jpg OUTPUT_PATH=./result.png ./run.sh
```

## How it works

1. The image is loaded and sent to the Gemini API with a prompt requesting object detection
2. Gemini returns a JSON array of detected objects, each with a `label` and a `box_2d` bounding box (`[ymin, xmin, ymax, xmax]` normalized to 0–1000)
3. The script converts the normalized coordinates to pixel values and draws labeled, color-coded bounding boxes using Pillow
4. The annotated image is saved to disk
