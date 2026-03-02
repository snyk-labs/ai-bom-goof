# image-detection-project

Use Ultralytics YOLO and the Supervision library to detect and annotate objects in images.

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and running.

## Prerequisites

- [uv](https://docs.astral.sh/uv/installation/) installed (e.g. `curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Optional: system dependencies (Debian/Ubuntu)

OpenCV requires `libGL`, which may not be present in minimal or containerised environments. Install it with:

```bash
sudo apt-get update && sudo apt-get install -y libgl1-mesa-glx
```

## Setup

From the project root:

```bash
cd image-detection-project
```

You don't have to run `uv sync` yourself: **`uv run` will create the environment and install dependencies automatically** the first time you run something (e.g. `uv run python src/main.py`). If you want to install everything upfront (e.g. for your IDE), run once:

```bash
uv sync
```

To include dev dependencies (e.g. pytest):

```bash
uv sync --all-extras
```

## Running the app

```bash
uv run python src/main.py
```

`uv run` uses the project's `.venv` and ensures dependencies are synced, so you don't need to activate the venv yourself.

**Note:** The script expects example images under `~/image_detection_examples/` (e.g. `~/image_detection_examples/liran-at-devopsdays-tlv.jpg`). Create that directory and add an image, or change `IMAGE_PATH` in `src/main.py` to point to your image. The annotated output is written to `annotated_image.jpg` in the current directory.

## Project layout (uv)

- **`pyproject.toml`** – Project metadata and dependencies.
- **`uv.lock`** – Lockfile of resolved versions; commit this for reproducible installs.
- **`.venv/`** – Virtual environment created by uv (git-ignored).

## Useful uv commands

| Command | Purpose |
|--------|---------|
| `uv sync` | Install/update dependencies from lockfile |
| `uv run python src/main.py` | Run the app in the project environment |
| `uv add <package>` | Add a dependency and update lockfile |
| `uv add --dev <package>` | Add a dev dependency |
| `uv lock` | Refresh lockfile without installing |
