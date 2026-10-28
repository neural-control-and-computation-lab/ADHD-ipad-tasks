# ADHD study iPad tasks

iPad tasks for the ATHENA ADHD study (NCC Lab, York University). Participants do both tasks in one session, while markerless cameras record their movement. Every task flashes white patches in the far corners of the screen, so its events can be lined up with the camera video, and saves a CSV log on the iPad.

**Live site (session page):** https://neural-control-and-computation-lab.github.io/ADHD-ipad-tasks/

| Page | What it does | Details |
|---|---|---|
| Session page (`index.html`) | Enter the participant once, open each task, see what's done, export all of a participant's data | this file |
| Go/no-go reach task (`gonogo/`) | Reach and tap the circle for X, don't move for A; practice + 4 test blocks | [gonogo/README.md](gonogo/README.md) |
| Storytelling task (`story/`) | Two short films and two spoken stories in random order, each followed by a 1-minute retell | [story/README.md](story/README.md) |

## Running a session

1. **Session page:** enter the participant ID and the hand they'll use, then press Start session.
2. **Tasks:** the page suggests the task order (counterbalanced: go/no-go first for odd-numbered IDs, storytelling first for even). Press Open on a task.
   - The task fills in the participant's details and locks them.
   - Its data are saved under this session's visit ID.
3. **Back to the session page:** when a task ends, press the small "Back to session page" button under "All done. Thank you!". That task now shows as Done.
4. **Save the data:** after both tasks, press Save data. The share sheet saves both files (AirDrop, Save to Files or Dropbox).
5. **End the session:** press End session before the next participant.

## Setting up an iPad

- **Add one icon:** open the session page in Safari, tap Share, then Add to Home Screen. Add only this page, not the individual tasks.
  - The tasks open inside the session page's app.
  - Each home-screen icon on an iPad has its own separate storage, so separate task icons wouldn't see the participant or each other's data.
- **Run everything from that icon.** It runs full screen with no browser bars.
- **Download the films and stories:** on Wi-Fi, open the storytelling task once from that icon. It downloads them (about 75 MB) and keeps them on the iPad. Press Test on each to check the sound. The session page warns if they're missing. See [story/README.md](story/README.md).
- **Screen:** set Auto-Lock to Never, turn on Do Not Disturb, and fix the screen brightness.
- **Rotation:** lock rotation in landscape.
- **Guided Access** (Settings → Accessibility): use it to stop gestures and notifications from interrupting a session.
- **Data:** nothing is sent over the network. Data stay on the iPad until saved and deleted.
  - The only downloads are the app itself and the storytelling task's films and stories.
  - "All data on this iPad" at the bottom of the session page lists every run, shows how much storage is used, and can delete runs that have been saved.

## Shared conventions

- **Sync patches:** 3 cm white squares in the two top corners of the screen (the edge away from the participant). Line the video up to the first frame where they turn white.
- **Event markers:** both patches flash 3 times (150 ms on, 150 ms off) at the start of each block or event. Flash 1 is the event.
- **Experimenter menu inside a task:** press and hold the top centre of the screen for 1 s (Esc on a keyboard).
- **Data files:** `GNG_<ID>_<date-time>.csv` and `STORY_<ID>_<date-time>.csv`.
  - The `#` header lines include `visit=`, which is the same in both files from one session.
  - They also include the hand and all settings.
- **Order:** trial orders within each task are set by the participant ID, so they can be rebuilt without the data file.
- **Setup screens:** each task's setup screen shows the participant and a Start button. Everything else (design, settings, checks, saved runs, and the storytelling films) is folded away under "Settings and checks".
- **Settings:** change them there, or put any setting in the link (e.g. `.../gonogo/?blocks=3`). A yellow line above Start shows when anything differs from the defaults.
- **Participant screens:** once a task starts, every screen is written for the participant. No titles, IDs or experimenter notes are shown.

## Updating a task

- **Files:**
  - Each task is one file, `<task>/index.html`.
  - The storytelling films and stories are in `story/media/`.
  - `session.js` holds the shared participant/session code used by all three pages.
- **Workflow:** edit, run the checks in [tests/](tests/README.md), then commit and push to `main`. GitHub Pages updates within a few minutes.
- **On the iPad:** close and reopen the home-screen app to get the new version.
- **Versions:** each task's version number is saved in every data file. Bump it when you change anything that affects the data.
