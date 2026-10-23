# Go/No-Go reach task (iPad)

A go/no-go task for the ATHENA ADHD study. It runs in Safari on the lab iPad. The participant reaches from a start mark on the table and taps the circle on the iPad when they see **X**. They keep still when they see **A**.

**Live version:** https://neural-control-and-computation-lab.github.io/ADHD-ipad-tasks/gonogo/ (normally opened from the [session page](../README.md))

Everything is in one file, `index.html`. It needs no internet once it has loaded, and it sends no data anywhere. Data stay on the iPad until you export them.

## Design (follows Verbruggen et al., 2019 and STOP-IT where it applies)

- **Stimuli:** X = go, A = no-go, 25% no-go. This is the proportion the consensus guide recommends.
- **Practice:** 1 block of 32 trials (24 X, 8 A). After an error, a message ("Too slow", "Don't move for A" or "Too early") shows for 750 ms, as in STOP-IT.
- **Test:** 4 blocks of 72 trials = 288 trials in total, 72 of them no-go. The consensus guide's Inquisit version uses 3 blocks of 72; we added a fourth for more trials. Order is fully randomised within each block.
- **Each trial:**
  - a fixation cross for a random 500–2000 ms (uniform, so 1250 ms on average)
  - the letter stays up until a tap, or for 1500 ms
  - the next fixation cross appears 2000 ms after the letter, whatever the response
- **Why the fixation time is random:** we don't track whether the hand is on the start mark, so the letter onset must not be predictable, or people will start moving early. Each trial's fixation time is drawn at random from 500–2000 ms, all values equally likely. Advanced settings also offer an exponential distribution, which makes late onsets harder to anticipate; the data file records which one was used.
- **Why the timing is longer than STOP-IT:** STOP-IT uses a 1250 ms response window for key presses. We added 250 ms for the reach. The 2000 ms from one letter to the next fixation, plus at least 500 ms of fixation, leaves time to get back to the start mark.
- **Between blocks:** 15 s break showing average tap time, missed X's ("aim for 0") and A's tapped. The consensus guide recommends this to stop people slowing down.
- **Instructions:** one short screen. Finger on the start mark; X = tap the circle as fast as you can; A = don't move; go back to the mark after each tap, and don't wait to see if an A is coming. The last point is the guide's key instruction, adapted for go/no-go.
- **Session length:** about 2 min of practice plus 17 min of test, not counting instructions. Dropping to 3 blocks (`blocks=3`) brings the test down to about 12.5 min.
- **Order of trials and fixation times:** set by the participant ID, so the same ID always gives the same sequence and it can be rebuilt without the data file.

## Video synchronisation

- **Corner patches:** the two 3 cm squares at the far corners of the screen turn white for 150 ms at every letter onset. Line the video up to the first frame where they go white.
- **Block start:** both patches flash 3 times (150 ms on, 150 ms off) at the start of each block, and again after a pause.
- **Trial code:** the grey strip along the top edge is the trial number in binary. The outer two cells are always on and mark the ends. The 9 cells between them are the trial number, most significant bit first. A printed trial number can be turned on in Advanced settings (off by default).
- **Placement:** the code strip and patches sit at the edge furthest from the participant, so the reaching hand shouldn't cover them. Check this in the camera views during piloting.

## Setting up the iPad

- **Home screen:** see the [main README](../README.md#setting-up-an-ipad). Add only the session page to the home screen and open this task from there.
- **Rotation:** hold the iPad in landscape and turn on rotation lock (Control Centre). A flat iPad will otherwise flip orientation on its own. The layout also works in portrait, but use the same orientation for everyone.
- **Screen:** set Auto-Lock to Never and turn on Do Not Disturb. Set the brightness to a fixed level (turn off auto-brightness) so the patches look the same in every session.
- **Guided Access** (Settings → Accessibility): turn it on and start it once the task is open. This stops home-gestures and notifications from interrupting the task.
- **Positioning:** put the iPad on the pedestal with the bottom of the screen facing the participant.
- **Start mark:** tape it on the table and use the same spot for everyone. Write down the distance.
- **Size check:** press "Check layout & size" on the setup screen. The white bar should measure 10 cm. If it doesn't, change "Screen scale (px per cm)" in Advanced settings (52 is right for most iPads, 64 for an iPad mini).

## Running a session

- **Start:** open the task from the session page. The participant ID, hand and notes are filled in from there. Press Start session.
  - Opened on its own, the task asks for the ID and hand instead.
- **Instructions:** read the single instruction screen out loud, then press Start practice.
- **After practice:** choose Repeat practice or Start part 1. Repeat it if the participant clearly didn't follow the instructions.
- **Each part:** a part starts as soon as its Start button is pressed. A 3-second countdown gives the participant time to put their finger on the start mark. On break screens, the button unlocks after 15 s.
- **Pausing:** press and hold the grey code strip at the top centre of the screen for 1 s. From the pause screen you can resume (the interrupted trial is re-run), restart the block, or end and save. The task also pauses on its own if the screen locks or someone switches apps.
- **Saving:** at the end you can press Save CSV… right away, or go back to the session page and save both tasks' files together. Download CSV is a fallback.
- **Backup copy:** every run stays on the iPad until deleted. Runs are listed on the session page, and on this task's setup screen.

## Data file (backup to the video)

- **File name:** `GNG_<ID>_<date-time>.csv`. The lines starting with `#` hold the visit ID (shared with the storytelling file from the same session), hand, notes, settings and device info. Read the file with `comment='#'` in pandas or `comment.char='#'` in R.
- **Rows:** one per trial. There are also `sync` rows for the block-start flashes.
- **Main columns:**
  - `block` (0 = practice), `trial_in_block`, `code` (the trial number in the binary strip)
  - `type` (go/nogo), `outcome` (hit, omission, commission, correct_withhold, aborted)
- **Timing columns:**
  - `fix_ms`: when the fixation cross appeared
  - `foreperiod_ms`: how long the fixation cross was planned to stay up on that trial
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
- **Other columns:** `block_label` (P1 = practice, B1–B4 = test parts), `block_run` (goes up if a block is restarted), `fix_sched_ms` (planned fixation time), `frame_ms` (screen refresh interval when the letter appeared).
- **Timing accuracy:** the iPad's times are accurate to about one screen refresh (about 17 ms at 60 Hz). The corner patches in the video are the reference.

## Settings

- **Advanced settings:** every value can be changed on the setup screen. A yellow "non-default settings" badge appears when anything differs from the defaults above.
- **Settings in the link:** values can also go in the URL, e.g. `.../index.html?blocks=3`. A bookmarked link then always starts with the same settings.
- **Testing on a laptop:** the space bar works as a tap on the circle, and Esc pauses.

## Things to settle while piloting

- **Timing:** check that the 1500 ms window and the time between trials are comfortable for the reach. Look for missed X's caused by slow returns to the start mark, and check in the video whether people still start moving before the letter.
- **Visibility:** check whether the corner patches and code strip are visible in every camera view, and readable at the cameras' frame rate.
- **Feedback:** decide whether to keep between-block feedback. Verbruggen recommends it, but it is one more thing that differs between participants.
- **Letter size:** check that the letter (4 cm in a 7 cm circle) is easy to read at the participant's viewing angle.

## Updating the task

- The live page is served by GitHub Pages from the `main` branch of the [ADHD-ipad-tasks](../README.md) repo.
- Edit `gonogo/index.html`, commit and push to `main`. The live page updates within a few minutes.
- On the iPad, reload the page (or close and reopen the home-screen app) to get the new version.
- Record which version was used for each participant. The version number is saved in every data file.

## References

- Verbruggen, F., et al. (2019). A consensus guide to capturing the ability to inhibit actions and impulsive behaviors in the stop-signal task. *eLife*, 8, e46323. https://doi.org/10.7554/eLife.46323
- STOP-IT (jsPsych version): https://github.com/fredvbrug/STOP-IT
- Lamp, G., et al. (2022). Kinematic studies of the go/no-go task as a dynamic sensorimotor inhibition task. *Brain Sciences*, 12(11), 1581. https://doi.org/10.3390/brainsci12111581
