"""Detect objects in an image using Google Gemini and draw bounding boxes."""

from __future__ import annotations

import json
import os
import re
import sys

from google import genai
from google.genai import types
from PIL import Image, ImageDraw, ImageFont


PROMPT = (
    "Detect all of the prominent items in the image. "
    "Return a JSON array of objects, each with a \"label\" (string) and "
    "\"box_2d\" ([ymin, xmin, ymax, xmax]) normalized to 0-1000."
)

PALETTE = [
    "#FF3838", "#FF9D97", "#FF701F", "#FFB21D", "#CFD231",
    "#48F90A", "#92CC17", "#3DDB86", "#1A9334", "#00D4BB",
    "#2C99A8", "#00C2FF", "#344593", "#6473FF", "#0018EC",
    "#8438FF", "#520085", "#CB38FF", "#FF95C8", "#FF37C7",
]


def load_image(path: str) -> Image.Image:
    img = Image.open(path).convert("RGB")
    return img


def parse_json_response(text: str) -> list[dict]:
    """Parse JSON from Gemini, handling markdown fencing and trailing commas."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)
    return json.loads(cleaned)


def detect_objects(image: Image.Image) -> list[dict]:
    client = genai.Client()
    config = types.GenerateContentConfig(response_mime_type="application/json")

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[image, PROMPT],
        config=config,
    )

    return parse_json_response(response.text)


def draw_detections(image: Image.Image, detections: list[dict]) -> Image.Image:
    annotated = image.copy()
    draw = ImageDraw.Draw(annotated)
    width, height = image.size

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except OSError:
        font = ImageFont.load_default()

    for i, det in enumerate(detections):
        box = det["box_2d"]
        label = det.get("label", "object")

        y1 = int(box[0] / 1000 * height)
        x1 = int(box[1] / 1000 * width)
        y2 = int(box[2] / 1000 * height)
        x2 = int(box[3] / 1000 * width)

        color = PALETTE[i % len(PALETTE)]
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)

        text_bbox = draw.textbbox((0, 0), label, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        text_bg = [x1, y1 - text_h - 6, x1 + text_w + 8, y1]
        if text_bg[1] < 0:
            text_bg = [x1, y2, x1 + text_w + 8, y2 + text_h + 6]
            text_origin = (x1 + 4, y2 + 2)
        else:
            text_origin = (x1 + 4, y1 - text_h - 4)

        draw.rectangle(text_bg, fill=color)
        draw.text(text_origin, label, fill="white", font=font)

    return annotated


DEFAULT_IMAGE_CANDIDATES = ["image.png", "image.jpeg", "image.jpg"]


def resolve_image_path() -> str:
    explicit = os.environ.get("IMAGE_PATH")
    if explicit:
        if os.path.isfile(explicit):
            return explicit
        print(f"Error: image not found at '{explicit}'", file=sys.stderr)
        sys.exit(1)

    for candidate in DEFAULT_IMAGE_CANDIDATES:
        if os.path.isfile(candidate):
            return candidate

    tried = ", ".join(DEFAULT_IMAGE_CANDIDATES)
    print(f"Error: no image found (tried {tried})", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    image_path = resolve_image_path()

    print(f"Loading image from {image_path} ...")
    image = load_image(image_path)
    print(f"Image size: {image.size[0]}x{image.size[1]}")

    print("Sending image to Gemini for object detection ...")
    detections = detect_objects(image)
    print(f"Detected {len(detections)} object(s):")
    for det in detections:
        print(f"  - {det.get('label', '?')}: {det['box_2d']}")

    print("Drawing bounding boxes ...")
    annotated = draw_detections(image, detections)

    output_path = os.environ.get("OUTPUT_PATH", "output_annotated.png")
    annotated.save(output_path)
    print(f"Annotated image saved to {output_path}")


if __name__ == "__main__":
    main()
