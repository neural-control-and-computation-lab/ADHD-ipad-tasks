# Storytelling task (iPad)

Part of the ATHENA ADHD study. The participant watches two short silent films and listens to two short spoken stories, one at a time. After each one they retell it while a timer counts down. There are no motor instructions; the cameras record incidental movement while they watch, listen and talk.

**Live version:** https://neural-control-and-computation-lab.github.io/ipad-tasks/story/

## Design

- **Stimuli:** 2 films (video) and 2 stories (audio), in a random order set by the participant ID. The same ID always gives the same order, and the setup screen shows it.
- **Each trial:**
  - the experimenter sees which film or story is next and presses Start
  - the film plays on screen, or the story plays with a "Listen to the story" screen
  - when it ends, the retell screen appears ("Tell us what happened in the film/story") with a 30 s countdown
  - "Time's up" for 2 s, then the experimenter sees the next one
- **Session length:** the four stimuli plus 4 × 30 s of retelling, about 6–8 min for 1–1.5 min stimuli.

## Video synchronisation

- **Playback start:** both corner patches flash 3 times when playback actually starts. For films, this waits for the first video frame to be shown. Flash 1 is the playback start.
- **Retell start:** both patches flash 3 times when the countdown starts. Flash 1 is the start of the retell.
- **Clear corners:** the film is drawn below the strip holding the patches, so the corners stay black except during the flashes.

## Loading the films and stories

- Put the four files somewhere the iPad can reach (e.g. Dropbox, which shows up in the Files app).
- On the setup screen, press Load file for each slot and pick the file. Videos: MP4 or MOV. Audio: MP3, M4A or WAV.
- The files stay on that iPad until removed, so this only needs doing once per iPad. They are not uploaded anywhere, and none are stored in this repository.
- Safari and the home-screen app keep separate storage, so load the files from the home-screen app if that's how you'll run the task.
- Rename each slot (e.g. "Fox and the Cat") so the experimenter preview and the data file use real names.
- Press Test on each slot to check it plays and the volume is right.
- The YouTube films need to be downloaded as MP4 files first. Check that the lab has permission to use them.

## Running a session

- **Start:** enter the participant ID (the order appears), then press Start session. All four files must be loaded.
- **Introduction:** read the introduction screen to the participant, then press Continue.
- **Each trial:** press Start when the participant is ready. Nothing else is needed until the next preview.
- **Experimenter menu:** press and hold the top centre of the screen for 1 s (Esc on a keyboard). During playback you can resume, skip to the retell, restart the trial, or end the session. During the retell you can let the countdown continue (it keeps running in the background) or end it early.
- **Saving:** at the end, press Save CSV… and pick AirDrop, Save to Files, or Dropbox. Sessions also stay on the iPad until deleted from the setup screen.

## Data file

- **File name:** `STORY_<ID>_<date-time>.csv`. Lines starting with `#` hold the order, file names and durations, settings and device info. Read the file with `comment='#'` in pandas or `comment.char='#'` in R.
- **Rows:** one row per event, with `trial`, `slot`, `label`, `kind` (video/audio) and `file`.
- **Events:**
  - `start_pressed`
  - `media_playing`
  - `sync_flash` (detail says playback/retell start and flash 1–3)
  - `media_ended`
  - `retell_start`
  - `retell_end`
  - menu actions (`menu_opened`, `resumed`, `media_stopped_early`, `trial_restarted`, `trial_skipped`)
  - `app_hidden` / `app_visible`
- **Times:** `t_ms` is the iPad clock (ms since the page loaded) and `epoch_ms` is wall-clock time. `media_time_s` is the position in the film or story at that moment.

## Settings

- **Advanced settings** on the setup screen: retell time (default 30 s), a gap before the retell timer (default 0), how long "Time's up" shows, patch size and flash timing, screen scale, and the order seed.
- **Settings in the link:** e.g. `.../story/?retellSec=45`. The order seed defaults to the participant ID.
- **Instruction wording:** edit the `TEXT` block near the top of `index.html`.

## Things to settle while piloting

- Check that the patch flashes are visible in every camera view while a film is playing.
- Check the volume of the stories at the participant's position.
- Decide whether participants should be told in advance that they will retell each one (the introduction screen currently says so).
