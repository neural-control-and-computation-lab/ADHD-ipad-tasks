# ADHD study iPad tasks

iPad tasks for the ATHENA ADHD study (NCC Lab, York University). Each participant does two tasks in one session while markerless cameras record their movement:

- **Go/no-go reach task:** reach and tap a circle when an X appears; don't move for an A.
- **Storytelling task:** two short films and two spoken stories in random order, each followed by a timed retell.

| Link | What it is |
|---|---|
| [Session page](https://neural-control-and-computation-lab.github.io/ADHD-ipad-tasks/) | The app. Open it on the iPad. |
| [Preview page](https://neural-control-and-computation-lab.github.io/ADHD-ipad-tasks/preview.html) | Every screen participants see, with the current wording and retell times. |
| [participant-text.md](participant-text.md) | What participants read. You can edit it. |
| [retell-times.md](retell-times.md) | How long participants have to retell each film and story. You can edit it. |

## Changing the wording or the retell times (no coding)

Two files hold everything you're likely to change:

- **What participants read:** [participant-text.md](participant-text.md)
- **How long they have to retell each film and story:** [retell-times.md](retell-times.md)

To make a change:

1. Open the file (click its name above) and click the pencil icon at the top right.
2. Make your change. The top of each file shows which parts to change.
3. Click the green **Commit changes…** button, then **Commit changes** in the box that opens. This saves it.
4. Wait about 2 minutes, then check the [preview page](https://neural-control-and-computation-lab.github.io/ADHD-ipad-tasks/preview.html). It shows every screen with your change, and a yellow box if something in either file needs fixing.

The iPads pick up the change the next time a task is opened (with internet).

Good to know:

- Each data file records the exact wording and retell times that participant had.
- Every saved version is kept. **History** (top right of a file) lists them. To undo a change, ask Jonathan, or open the earlier version from History and copy its text back in.
- All the other files are code. To change anything else, such as the 2-second pause before each retell or the text size, ask Jonathan.

## Running a session

1. **Session page:** enter the participant ID and the hand they'll use, then press Start session. This is the only place the ID is typed.
2. **Consent and questionnaire:** press Open next to "Consent and questionnaire". The consent form opens in Safari with the participant ID already attached. When the participant finishes it, it goes straight on to the questionnaire. When both are done, switch back to the ADHD tasks app (swipe up from the bottom edge and tap it).
3. **Tasks:** the page lists the two tasks in order (go/no-go first for odd-numbered IDs, storytelling first for even). Press Open on the first one.
4. **Back to the session page:** when a task ends, press the small "Back to session page" button under "All done. Thank you!". The task now shows as Done. Open the next one.
5. **Save the data:** after both tasks, press Save data. The share sheet saves both CSV files (AirDrop, Save to Files or Dropbox).
6. **End the session:** press End session before the next participant.

In QuestionPro, the participant ID is in the **Custom 1** column of both surveys' data. Email and URPP/KURE ID are only in the consent survey.

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
| [retell-times.md](retell-times.md) | The retell time for each film and story |
| `index.html` | The session page |
| `preview.html` | The preview of the participant screens |
| [gonogo/](gonogo/README.md) | The go/no-go reach task. Its README describes the design and the data file. |
| [story/](story/README.md) | The storytelling task. Its README describes the design and the data file. `story/media/` holds the films and stories. |
| `shared/` | Code used by every page: the participant/session details (`session.js`), the participant text (`text.js`) and the retell times (`retell-times.js`) |
| [tests/](tests/README.md) | Automated checks, run after changing the code |
| `manifest.json`, `icon.png` | Home-screen app name and icon |

## For whoever changes the code

- **Video sync:** 3 cm white patches in the two top corners of the screen (the edge away from the participant). Both flash 3 times (150 ms on, 150 ms off) at the start of each block or event, and flash 1 is the event. Line the video up to the first frame where they turn white.
- **Consent and questionnaire link:** `FORMS_LINK` near the top of the script in `index.html` is the consent survey's QuestionPro link. The session page adds `?custom1=<participant ID>`; the consent survey's finish option redirects to the questionnaire with `?custom1=${custom1}`, so both surveys store the ID.
- **Experimenter menu inside a task:** press and hold the top centre of the screen for 1 s (Esc on a keyboard).
- **Data files:** `GNG_<ID>_<date-time>.csv` and `STORY_<ID>_<date-time>.csv`. The `#` header lines hold the app version, `visit=` (the same in both files from one session), the hand, all settings and the participant text used.
- **Order:** trial orders are set by the participant ID, so they can be rebuilt without the data file.
- **Settings:** under "Settings and checks" on each task's setup screen, or in the link (e.g. `.../gonogo/?blocks=3`). A yellow line above Start shows when anything differs from the defaults.
- **Each task is one file,** `<task>/index.html`. The wording lives in `participant-text.md`; the built-in copy in `shared/text.js` is only used if that file can't be downloaded.
- **Workflow:** edit, run the checks in [tests/](tests/README.md), then commit and push to `main`. GitHub Pages updates within a few minutes; close and reopen the home-screen app on the iPad to get the new version.
- **Versions:** each task's version number is saved in every data file. Bump it when you change anything that affects the data.

### Changing a setting in the code

Other settings are numbers near the top of each task's file, [story/index.html](story/index.html) and [gonogo/index.html](gonogo/index.html), in the block that starts `const DEFAULTS = {`. Each line has a note saying what it is (e.g. `retellDelayMs: 2000,` is the pause before each retell, in milliseconds). Change only the number, raise the last number of `const VERSION` just above it by one (e.g. `'1.6.0'` to `'1.6.1'`) so the data files show the change, commit, and check the preview page.
