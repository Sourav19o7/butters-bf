# Butter's BF (Butter's Behavior Finder)

A real-time dog behavior analysis system that watches your Golden Retriever through a webcam and uses a local vision AI model to describe what she's doing — then learns from your corrections over time.

---

## What it does

Every few seconds, the system:

1. Captures a frame from your webcam
2. Sends it to a local [Moondream](https://github.com/vikhyat/moondream) vision model (via Ollama)
3. Gets a one-sentence behavioral description: what Butter is doing and what she wants right now
4. Lets you correct the guess — corrections are saved and fed back as context for future observations

The model analyzes eyes, ears, nose, tail, posture, and overall body language to form its guess. Past corrections are injected into the prompt so the model adapts to Butter's specific patterns over time.

---

## Project structure

```
.
├── analyze.py         # Main loop: capture → analyze → feedback
├── feedback.py        # SQLite helpers: init DB, save, and retrieve past corrections
├── view_feedback.py   # CLI viewer for all stored feedback entries
├── find_camera.py     # Utility to discover available camera indices
├── data/
│   └── frames/        # Saved captured frames (timestamped JPEGs)
└── .env               # Config (camera index, model name, Ollama URL, DB name)
```

---

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally with Moondream pulled (`ollama pull moondream`)
- A webcam

Install Python dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install opencv-python requests python-dotenv
```

---

## Configuration

Create a `.env` file in the project root:

```env
CAMERA=0
MODEL=moondream
OLLAMA_URL=http://localhost:11434/api/chat
DATABASE_NAME=butter.db
```

If you're not sure which camera index to use, run:

```bash
python find_camera.py
```

This saves test shots (`camera_0.jpeg`, `camera_1.jpeg`, …) for each detected camera so you can identify the right one.

---

## Usage

**Start the analysis loop:**

```bash
python analyze.py
```

The model will describe what Butter is doing. Press Enter to skip, or type a correction to teach it the right answer.

**View past feedback:**

```bash
python view_feedback.py
```

---

## How the feedback loop works

Corrections are stored in a local SQLite database (`butter.db`). Before each new analysis, the system pulls all past corrections and appends them to the prompt:

```
From past observation:
- Butter was actually: asking for food
- Butter was actually: sleeping, not watching the door
```

This gives the model personalized context about Butter's habits without any fine-tuning.

---

## Built with

- [OpenCV](https://opencv.org) — webcam capture
- [Moondream](https://github.com/vikhyat/moondream) — lightweight local vision model
- [Ollama](https://ollama.com) — local model serving
- SQLite — feedback storage
