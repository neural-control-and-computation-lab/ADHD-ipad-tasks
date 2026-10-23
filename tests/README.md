# Tests

Automated checks that run each task in a headless browser with a simulated participant and check the exported data. Run them after changing a task, before pushing.

## Setup (once)

- Python 3.9 or later
- `pip install playwright`, then `python -m playwright install chromium`
- `ffmpeg` (for the storytelling test's clips): `brew install ffmpeg` on a Mac

## Running

From the repository root:

- `python tests/test_gonogo.py`: a shortened go/no-go session (about 1 min). It checks trial and no-go counts, that the order and fixation times match the participant's seed, the sync flashes and timing, and that every outcome and RT matches what the simulated participant did.
- `python tests/test_session.py`: the session page with both tasks (about 30 s). It checks that the participant's details reach each task and are locked, the counterbalanced order, the task statuses, and that "Save all" exports both CSVs with the same visit ID.
- `python tests/test_story.py`: a full storytelling session with short generated clips (about 30 s). It checks that the files persist, the order, the 3 flashes at playback and retell start, the retell length, and the experimenter-menu actions.

Each test prints PASS/FAIL lines and ends with OVERALL PASS or FAIL. Timings from a headless browser can occasionally be off by a frame; rerun once before assuming a real problem.
