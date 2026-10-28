# Storytelling task (iPad)

Part of the ATHENA ADHD study. The participant watches two short films and listens to two short spoken stories, one at a time. After each one they retell it while a timer counts down. There are no motor instructions; the cameras record incidental movement while they watch, listen and talk.

**Live version:** https://neural-control-and-computation-lab.github.io/ADHD-ipad-tasks/story/ (normally opened from the [session page](../README.md))

## Design

- **Stimuli:** 2 films (video) and 2 stories (audio), in a random order set by the participant ID. The same ID always gives the same order (listed under "Films, settings and checks" on the setup screen).
- **Each trial:**
  - the screen says only "Next, you'll watch a short film" or "Next, you'll listen to a story", with a Start button
  - the film plays on screen, or the story plays with a "Listen to the story" screen
  - when it ends, the screen goes blank for 2 s
  - then the retell screen appears ("Tell us what happened in the film/story") with a 1-minute countdown
  - "Time's up. Thank you!" for 2 s, then the next one
- **What the participant sees:** every screen during the task is written for the participant. Titles, file names, the participant ID and trial numbers are never shown. The end screen just says "All done. Thank you!", with a small button to go back to the session page.
- **Session length:** about 9 min of films and stories plus 4 × 1 min of retelling, so about 13–14 min with the instructions.

## Video synchronisation

- **Playback start:** both corner patches flash 3 times when playback actually starts. For films, this waits for the first video frame to be shown. Flash 1 is the playback start.
- **Retell start:** both patches flash 3 times when the retell screen appears and the countdown starts (after the 2 s pause). Flash 1 is the start of the retell.
- **Clear corners:** the film is drawn below the strip holding the patches, so the corners stay black except during the flashes.

## Films and stories

| Slot | Title | File in `media/` | Length |
|---|---|---|---|
| Film 1 | The Book Witch | `film1-the-book-witch.mp4` | 1:39 |
| Film 2 | Live a Little | `film2-live-a-little.mp4` | 1:53 |
| Story 1 | The Straw, the Coal and the Bean | `story1-the-straw-the-coal-and-the-bean.mp3` | 3:14 |
| Story 2 | The Wolf and the Kid | `story2-the-wolf-and-the-kid.mp3` | 2:00 |

- **They come with the app.** The first time the task opens on an iPad it downloads all four (about 75 MB, so use Wi-Fi). The setup screen shows the progress.
- **They stay on the iPad.** After that they play from the iPad, so a session doesn't need the internet.
  - Each time the task opens with a connection, it checks that the files still match the ones here and downloads any that have changed.
  - If the iPad ever clears them, they download again the next time the task opens on Wi-Fi.
- **Check once per iPad:** press Test on each one to check it plays and the volume is right.
- **Safari and the home-screen app keep separate storage.** Open the task from the session page's home-screen icon, which is how it will be run, so the files are downloaded there.
- **Public:** the files are in this public repository, so anyone with the link can download them.
- **The videos were compressed** from the originals (1920×1080, H.264, about 2–3 Mbit/s, sound kept as AAC 128 kbit/s) to keep them under GitHub's file-size limit. The stories are the original MP3s.
- **Changing a film or story:**
  - Add the new file to `media/` under a new name.
  - Update its line in `SLOTS` near the top of `index.html` (title and file name).
  - Keep each file under 50 MB (GitHub refuses files over 100 MB).
  - iPads pick up the change the next time the task opens on Wi-Fi.

## Running a session

- **Start:** open the task from the session page. It shows the participant ID and "Films and stories: ready on this iPad" in green. Press Start.
  - Opened on its own, the task asks for the ID instead.
  - The order, the Test buttons for the films and stories, the settings and the layout check are under "Films, settings and checks".
- **Introduction:** the participant reads it (or you read it to them), then presses Continue.
- **Each trial:** the participant (or you) presses Start when ready. Nothing else is needed until the next one.
- **Experimenter menu:** press and hold the top centre of the screen for 1 s (Esc on a keyboard). During playback you can resume, skip to the retell, restart the trial, or end the session. During the retell you can let the countdown continue (it keeps running in the background) or end it early.
- **Saving:** at the end, go back to the session page and press Save data there, which saves both tasks' files together. Every run stays on the iPad until deleted (session page, or this task's "Films, settings and checks").

## Data file

- **File name:** `STORY_<ID>_<date-time>.csv`. Lines starting with `#` hold the app version, the visit ID (shared with the go/no-go file from the same session), the order, the file names, sizes and durations, hand, settings and device info. Read the file with `comment='#'` in pandas or `comment.char='#'` in R.
- **Rows:** one row per event, with `trial`, `slot`, `label`, `kind` (video/audio) and `file`.
- **Events:**
  - `start_pressed`
  - `media_playing`
  - `sync_flash` (detail says playback/retell start and flash 1–3)
  - `media_ended`
  - `retell_start`
  - `retell_end`
  - menu actions (`menu_opened`, `resumed`, `media_stopped_early`, `trial_restarted`, `trial_skipped`)
  - `media_problem` if a film or story fails to play
  - `app_hidden` / `app_visible`
- **Times:** `t_ms` is the iPad clock (ms since the page loaded) and `epoch_ms` is wall-clock time. `media_time_s` is the position in the film or story at that moment.

## Settings

- **Change settings** (under "Films, settings and checks"): retell time (default 60 s), the blank pause before the retell (default 2 s), how long "Time's up" shows, patch size and flash timing, screen scale, and the order seed. A yellow line on the setup screen shows when anything differs from the defaults.
- **Settings in the link:** e.g. `.../story/?retellSec=45`. The order seed defaults to the participant ID.
- **Instruction wording:** edit the `TEXT` block near the top of `index.html`. It holds every line the participant sees.

## Things to settle while piloting

- Check that the patch flashes are visible in every camera view while a film is playing.
- Check the volume of the stories at the participant's position.
- Decide whether participants should be told in advance that they will retell each one (the introduction screen currently says so).
