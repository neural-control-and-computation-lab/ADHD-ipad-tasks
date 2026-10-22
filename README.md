# NCC Lab iPad tasks

Tasks for markerless motion-tracking experiments (ATHENA). Each task is a single web page that runs in Safari on an iPad. It flashes white patches in the far corners of the screen so the iPad's events can be lined up with the camera video, and it saves a CSV log on the iPad.

**Live site:** https://neural-control-and-computation-lab.github.io/ipad-tasks/

| Task | Link | Details |
|---|---|---|
| Go/no-go reach task | https://neural-control-and-computation-lab.github.io/ipad-tasks/gonogo/ | [gonogo/README.md](gonogo/README.md) |
| Storytelling task | https://neural-control-and-computation-lab.github.io/ipad-tasks/story/ | [story/README.md](story/README.md) |

## Using a task on the iPad

- Open the task's link in Safari, tap Share, then Add to Home Screen. Do this for each task you need; each gets its own icon.
- Run the task from its home-screen icon, so it fills the screen with no browser bars.
- Set Auto-Lock to Never, turn on Do Not Disturb, and fix the screen brightness.
- Turn on rotation lock in landscape, and use Guided Access (Settings → Accessibility) to stop gestures and notifications interrupting a session.
- Data stay on the iPad until you export them from the end screen (Save CSV…). Nothing is sent over the network.

## Shared conventions

- **Sync patches:** 3 cm white squares in the two top corners of the screen (the edge away from the participant). Line the video up to the first frame where they turn white.
- **Event markers:** both patches flash 3 times (150 ms on, 150 ms off) at the start of each block or event; flash 1 is the event.
- **Experimenter menu:** press and hold the top centre of the screen for 1 s (Esc on a keyboard).
- **Order:** trial orders are set by the participant ID, so they can be rebuilt without the data file.
- **Settings:** each task has Advanced settings on its setup screen, and any setting can go in the link (e.g. `.../gonogo/?blocks=3`). A yellow badge shows when anything differs from the defaults.

## Updating a task

- Each task is one file: `<task>/index.html`. Edit it, run the checks in [tests/](tests/README.md), then commit and push to `main`; GitHub Pages updates within a few minutes.
- On the iPad, reload the page (or close and reopen the home-screen app) to get the new version.
- Each task has a version number that is saved in every data file. Bump it when you change anything that affects the data.
