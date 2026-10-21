# Go/No-Go reach task (iPad)

A go/no-go task for the ATHENA ADHD study. It runs in Safari on the lab iPad. The participant reaches from a start mark on the table and taps the circle on the iPad when they see **X**. They keep still when they see **A**.

**Live version:** https://neural-control-and-computation-lab.github.io/gonogo-reach/

Everything is in one file, `index.html`. It needs no internet once it has loaded, and it sends no data anywhere. Data stay on the iPad until you export them.

## Design (follows Verbruggen et al., 2019 and STOP-IT where it applies)

- **Stimuli:** X = go, A = no-go, 25% no-go. This is the proportion the consensus guide recommends.
- **Practice:** 1 block of 32 trials (24 X, 8 A). Feedback after errors ("Too slow", "Don't move for A", "Too early"), the same as STOP-IT's practice feedback (750 ms).
- **Test:** 3 blocks of 72 trials = 216 trials in total, 54 of them no-go. This is the block layout of the consensus guide's Inquisit version. Order is fully randomised within each block.
- **Each trial:**
  - 250 ms fixation cross (as in STOP-IT)
  - the letter stays up until a tap, or for 1500 ms
  - a new trial starts every 2500 ms, whatever the response
- **Why the timing is longer than STOP-IT:** STOP-IT uses a 1250 ms response window and 2000 ms trials for key presses. We added 250 ms for the reach and 500 ms so there's time to get back to the start mark. A fixed trial length also keeps the event rate the same for everyone, which matters when RT variability is a main measure.
- **Between blocks:** 15 s break showing average tap time, missed X's ("try to keep this at 0") and A's tapped. The consensus guide recommends this to stop people slowing down.
- **Instructions:** one short screen. Finger on the start mark; X = tap the circle as fast as you can; A = don't move; go back to the mark after each tap, and don't wait to see if an A is coming. The last point is the guide's key instruction, adapted for go/no-go.
- **Session length:** about 1.5 min of practice plus 10 min of test, not counting instructions. If that's too long, setting the trial length to 2250 ms (`soaMs`) brings the test down to about 9 min.
- **Order of trials:** set by the participant ID, so the same ID always gives the same order and the sequence can be rebuilt without the data file.

## Video synchronisation

- **Corner patches:** the two squares at the far corners of the screen turn white for 200 ms at every letter onset. Line the video up to the first frame where they go white.
- **Block start:** both patches flash 3 times (200 ms on, 200 ms off) at the start of each block, and again after a pause.
- **Trial code:** the grey strip along the top edge is the trial number in binary. The outer two cells are always on and mark the ends. The 9 cells between them are the trial number, most significant bit first. The trial number is also printed underneath.
- **Placement:** the code, number and patches sit at the edge furthest from the participant, so the reaching hand shouldn't cover them. Check this in the camera views during piloting.

## Setting up the iPad

- **Open the task:** go to https://neural-control-and-computation-lab.github.io/gonogo-reach/ in Safari, tap Share, then Add to Home Screen. Open it from the home-screen icon so it runs full screen with no browser bars.
- **Rotation:** turn on rotation lock (Control Centre). A flat iPad will otherwise flip orientation on its own. Landscape is the default layout.
- **Screen:** set Auto-Lock to Never and turn on Do Not Disturb. Set the brightness to a fixed level (turn off auto-brightness) so the patches look the same in every session.
- **Guided Access** (Settings → Accessibility): turn it on and start it once the task is open. This stops home-gestures and notifications from interrupting the task.
- **Positioning:** put the iPad on the pedestal with the bottom of the screen facing the participant.
- **Start mark:** tape it on the table and use the same spot for everyone. Write down the distance.
- **Size check:** press "Check layout & size" on the setup screen. The white bar should measure 10 cm. If it doesn't, change "px per cm" in Advanced settings (52 is right for most iPads, 64 for an iPad mini).

## Running a session

- **Start:** enter the participant ID and the hand used, then press Start session.
- **Instructions:** read the single instruction screen out loud, then press Start practice.
- **After practice:** choose Repeat practice or Start part 1. Repeat it if the participant clearly didn't follow the instructions.
- **Each block:** a block starts straight from the button, with a 3-second countdown so the participant can put their finger on the start mark. After each break, the Start button unlocks after 15 s.
- **Pausing:** press and hold the trial number at the top of the screen for 1 s. From the pause screen you can resume (the interrupted trial is re-run), restart the block, or end and save. The task also pauses on its own if the screen locks or someone switches apps.
- **Saving:** at the end, press Save CSV… and pick AirDrop, Save to Files, or Dropbox. Download CSV is a fallback.
- **Backup copy:** sessions also stay on the iPad (listed on the setup screen) until you delete them.

## Data file (backup to the video)

- **File name:** `GNG_<ID>_<date-time>.csv`. The lines starting with `#` hold the settings and device info. Read the file with `comment='#'` in pandas or `comment.char='#'` in R.
- **Rows:** one per trial. There are also `sync` rows for the block-start flashes.
- **Main columns:**
  - `block` (0 = practice), `trial_in_block`, `code` (the number shown on screen)
  - `type` (go/nogo), `outcome` (hit, omission, commission, correct_withhold, aborted)
- **Timing columns:**
  - `onset_ms`: when the letter was drawn
  - `onset_epoch_ms`: the same moment as wall-clock time, for rough matching to camera timestamps
  - `rt_ms`: from letter onset to touching the screen. This includes movement time; reach onset has to come from ATHENA.
- **Touch columns:**
  - `touch_x_cm` and `touch_y_cm`: where the tap landed, relative to the circle centre
  - `in_target`
  - `premature_n`: touches before the letter appeared
  - `late_rt_ms`: taps after the response window closed
  - `extra_n`: any other touches
  - `aborted`: 1 for trials interrupted by a pause (these are re-run)
- **Timing accuracy:** the iPad's times are accurate to about one screen refresh (about 17 ms at 60 Hz). The corner patches in the video are the reference.

## Settings

- **Advanced settings:** every value can be changed on the setup screen. A yellow "non-default settings" badge appears when anything differs from the defaults above.
- **Settings in the link:** values can also go in the URL, e.g. `.../index.html?soaMs=2250`. A bookmarked link then always starts with the same settings.
- **Testing on a laptop:** the space bar works as a tap on the circle, and Esc pauses.

## Things to settle while piloting

- **Trial length:** check that 2500 ms trials and a 1500 ms window are comfortable for the reach. Look for missed X's caused by slow returns to the start mark.
- **Visibility:** check whether the corner patches and code strip are visible in every camera view, and readable at the cameras' frame rate.
- **Feedback:** decide whether to keep between-block feedback. Verbruggen recommends it, but it is one more thing that differs between participants.
- **Letter size:** check that the letter (4 cm in a 7 cm circle) is easy to read at the participant's viewing angle.

## Updating the task

- The live page is served by GitHub Pages from the `main` branch of this repo.
- Edit `index.html`, commit and push to `main`. The live page updates within a few minutes.
- On the iPad, reload the page (or close and reopen the home-screen app) to get the new version.
- Record which version was used for each participant. The version number is saved in every data file.

## References

- Verbruggen, F., et al. (2019). A consensus guide to capturing the ability to inhibit actions and impulsive behaviors in the stop-signal task. *eLife*, 8, e46323. https://doi.org/10.7554/eLife.46323
- STOP-IT (jsPsych version): https://github.com/fredvbrug/STOP-IT
- Lamp, G., et al. (2022). Kinematic studies of the go/no-go task as a dynamic sensorimotor inhibition task. *Brain Sciences*, 12(11), 1581. https://doi.org/10.3390/brainsci12111581
