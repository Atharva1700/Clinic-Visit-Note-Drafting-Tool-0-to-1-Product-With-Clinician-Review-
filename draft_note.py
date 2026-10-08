"""Draft a visit note from a synthetic transcript; flag uncertain sentences for clinician review.

Usage:
    python draft_note.py data/transcripts/sample_01.txt
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic

MODEL = "claude-haiku-5-5"
SYSTEM = (
    "You draft clinical visit notes from a visit transcript. Use only facts stated in the "
    "transcript; do not add diagnoses or values that were not said. If a sentence in the note "
    "is inferred or unclear from the transcript, append the tag [CONFIRM] to that sentence. "
    "Output only the note."
)
OUT_DIR = Path("drafts")
LOG = Path("edit_log.jsonl")


def draft(transcript: str) -> str:
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": transcript}],
    )
    return msg.content[0].text


def main() -> None:
    src = Path(sys.argv[1])
    note = draft(src.read_text())

    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / f"{src.stem}.draft.md"
    out.write_text(note)

    entry = {
        "time": datetime.now(timezone.utc).isoformat(),
        "source": str(src),
        "draft": str(out),
        "needs_confirm": note.count("[CONFIRM]"),
        "status": "draft_pending_clinician_review",
    }
    with LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"Draft saved to {out}; {entry['needs_confirm']} sentence(s) flagged [CONFIRM].")


if __name__ == "__main__":
    main()
