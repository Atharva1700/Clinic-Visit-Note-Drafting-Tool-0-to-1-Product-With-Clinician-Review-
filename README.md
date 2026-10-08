# Clinic Visit-Note Drafting Tool

Turns a simulated visit transcript into a draft clinical note. Sentences the model is unsure about are flagged `[CONFIRM]` so a clinician reviews them before saving. Uses synthetic transcripts only.

## Run

    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=your-key
    python draft_note.py data/transcripts/sample_01.txt

Writes the draft to `drafts/` and appends every run to `edit_log.jsonl`.

## Files

- `draft_note.py` - sends transcript to the Claude API, saves draft, logs the run
- `data/transcripts/` - synthetic transcripts only
- `EVALUATION.md` - TODO: results and failure list across synthetic transcripts (to be filled in from real runs)
- `frontend/` - TODO: React review screen (not started)

## Human in the loop

The tool never saves a note as final. Every draft needs clinician review, and any `[CONFIRM]` marker must be resolved before the note is used.
