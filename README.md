# ADHD study iPad tasks

iPad tasks for the ATHENA ADHD study (NCC Lab, York University). Each participant does two tasks in one session while markerless cameras record their movement:

- **Go/no-go reach task:** reach and tap a circle when an X appears; don't move for an A.
- **Storytelling task:** two short films and two spoken stories in random order, each followed by a 1-minute retell.

| Link | What it is |
|---|---|
| [Session page](https://neural-control-and-computation-lab.github.io/ADHD-ipad-tasks/) | The app. Open it on the iPad. |
| [Preview of the participant screens](https://neural-control-and-computation-lab.github.io/ADHD-ipad-tasks/preview.html) | Every screen participants see, with the current wording. |
| [participant-text.md](participant-text.md) | The wording itself. Edit it here on GitHub. |

## Changing what participants read (no coding)

Everything participants read during the tasks is in **[participant-text.md](participant-text.md)**.

1. Open [participant-text.md](participant-text.md) and click the pencil icon ("Edit this file") at the top right.
2. Change the text under a heading. Keep the headings (the lines starting with `##`) as they are.
3. Click **Commit changes…**, then **Commit changes** again.
4. After about 2 minutes, check the [preview page](https://neural-control-and-computation-lab.github.io/ADHD-ipad-tasks/preview.html). It also says if anything in the file can't be used.

Each iPad picks up the new wording the next time a task is opened with internet. Every data file records the exact wording that participant saw. The top of [participant-text.md](participant-text.md) explains paragraphs, bold and the words in curly brackets. Editing needs a GitHub account with write access to this repository: ask Jonathan.

## Running a session

1. **Session page:** enter the participant ID and the hand they'll use, then press Start session.
2. **Tasks:** the page lists the two tasks in order (go/no-go first for odd-numbered IDs, storytelling first for even). Press Open on the first one.
3. **Back to the session page:** when a task ends, press the small "Back to session page" button under "All done. Thank you!". The task now shows as Done. Open the next one.
4. **Save the data:** after both tasks, press Save data. The share sheet saves both CSV files (AirDrop, Save to Files or Dropbox).
5. **End the session:** press End session before the next participant.

## Setting up an iPad

- **One home-screen icon:** open the [session page](https://neural-control-and-computation-lab.github.io/ADHD-ipad-tasks/) in Safari, tap Share, then Add to Home Screen. Add only this page, not the tasks: each icon has its own storage, and the tasks open inside this one.
- **Run everything from that icon.** It runs full screen, without browser bars.
- **Films and stories:** on Wi-Fi, open the storytelling task once from that icon. It downloads them (about 75 MB) and keeps them. Under "Films, settings and checks", press Test on each to check the sound.
- **Screen:** set Auto-Lock to Never, turn on Do Not Disturb, fix the brightness, and lock rotation in landscape.
- **Guided Access** (Settings → Accessibility) stops gestures and notifications from interrupting a session.
- **Data:** nothing is sent anywhere. Data stay on the iPad until saved with Save data. "All data on this iPad" at the bottom of the session page lists every run and can delete runs that have been saved.

## What's in this repository

| File or folder | What it holds |
|---|---|
| [participant-text.md](participant-text.md) | Everything participants read. The one file to edit for wording. |
| `index.html` | The session page |
| `preview.html` | The preview of the participant screens |
| [gonogo/](gonogo/README.md) | The go/no-go reach task. Its README describes the design and the data file. |
| [story/](story/README.md) | The storytelling task. Its README describes the design and the data file. `story/media/` holds the films and stories. |
| `shared/` | Code used by every page: the participant/session details (`session.js`) and the participant text (`text.js`) |
| [tests/](tests/README.md) | Automated checks, run after changing the code |
| `manifest.json`, `icon.png` | Home-screen app name and icon |

## For whoever changes the code

- **Video sync:** 3 cm white patches in the two top corners of the screen (the edge away from the participant). Both flash 3 times (150 ms on, 150 ms off) at the start of each block or event, and flash 1 is the event. Line the video up to the first frame where they turn white.
- **Experimenter menu inside a task:** press and hold the top centre of the screen for 1 s (Esc on a keyboard).
- **Data files:** `GNG_<ID>_<date-time>.csv` and `STORY_<ID>_<date-time>.csv`. The `#` header lines hold the app version, `visit=` (the same in both files from one session), the hand, all settings and the participant text used.
- **Order:** trial orders are set by the participant ID, so they can be rebuilt without the data file.
- **Settings:** under "Settings and checks" on each task's setup screen, or in the link (e.g. `.../gonogo/?blocks=3`). A yellow line above Start shows when anything differs from the defaults.
- **Each task is one file,** `<task>/index.html`. The wording lives in `participant-text.md`; the built-in copy in `shared/text.js` is only used if that file can't be downloaded.
- **Workflow:** edit, run the checks in [tests/](tests/README.md), then commit and push to `main`. GitHub Pages updates within a few minutes; close and reopen the home-screen app on the iPad to get the new version.
- **Versions:** each task's version number is saved in every data file. Bump it when you change anything that affects the data.
