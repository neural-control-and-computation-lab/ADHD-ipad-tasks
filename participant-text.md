# Participant text

Everything participants read on the iPad. You can change it here without any coding.

### How to make a change

1. Click the pencil icon at the top right of this file.
2. Change the wording (see "What to change" below).
3. Click the green **Commit changes…** button, then **Commit changes** in the box that opens. This saves it.
4. Wait about 2 minutes, then open the [preview page](https://neural-control-and-computation-lab.github.io/ADHD-ipad-tasks/preview.html) to see your change on every screen. If it still shows the old wording, wait a minute and press Reload.

The iPads show the new wording the next time a task is opened (with internet).

### What to change

Each piece of text below looks like this:

```
  ## Storytelling: before a film        ← heading: leave it exactly as it is
  > Before each film, in large text.    ← grey note for you: participants don't see it

  Next, you'll watch a short film.      ← what participants see: change this
```

- Change only the text under the grey notes.
- Leave a blank line between paragraphs.
- To make words bold, put two stars on each side: `**like this**`.
- To show nothing, delete the text but keep the heading. Buttons always need some text.

### Words in curly brackets

The app fills these in, so keep them spelled exactly as they are. You can move them or delete them. The grey note under a heading lists the ones that work there.

| Word | Becomes |
|---|---|
| `{retell time}` | the time to retell that film or story, set in [retell-times.md](retell-times.md), e.g. "80 seconds". On the first screen, if the times differ: "between 60 and 90 seconds" |
| `{go letter}`, `{no-go letter}` | the two letters (X and A) |
| `{parts}` | the number of parts in the go/no-go task (4) |
| `{part}`, `{next part}` | the part just finished, and the next one |
| `{average tap time}`, `{missed}`, `{no-go tapped}`, `{no-go total}` | the participant's scores in the part just finished |

### If something goes wrong

- If the app can't use a piece of text (for example because a heading was changed), it shows the original wording for that piece. The preview page says what to fix.
- Every saved version of this file is kept. **History** (top right of the file) lists them. To undo a change, ask Jonathan, or open the earlier version from History and copy its text back in.
- Each data file records the exact wording that participant saw.

# Go/no-go reach task

## Go/no-go: instructions title
> Title of the first screen.

Instructions

## Go/no-go: instructions
> First screen, above the two letters.

Keep your finger on the start mark.

## Go/no-go: next to the go letter
> First screen, next to the go letter (the app shows the letter).

tap the circle as fast as you can

## Go/no-go: next to the no-go letter
> First screen, next to the no-go letter (the app shows the letter).

don't move

## Go/no-go: instructions, below the letters
> First screen, below the two letters, in smaller text.
>
> Words the app fills in here: {go letter}, {no-go letter}

Go back to the mark after each tap. Don't wait to see if an {no-go letter} is coming.

## Go/no-go: button to start the practice
> Button on the first screen.

Start practice

## Go/no-go: practice message, too slow
> Practice only: shown after a go letter if they did not tap in time.

Too slow

## Go/no-go: practice message, moved for the no-go letter
> Practice only: shown if they tap for the no-go letter.
>
> Words the app fills in here: {go letter}, {no-go letter}

Don't move for {no-go letter}

## Go/no-go: practice message, too early
> Practice only: shown if they tap before the letter appears.

Too early

## Go/no-go: after the practice, title
> Title of the screen after the practice.

Practice

## Go/no-go: after the practice
> Screen after the practice, above the scores.
>
> Words the app fills in here: {go letter}, {no-go letter}

Practice done. From now on there are no messages after each letter.

## Go/no-go: scores
> Scores shown after the practice and at each break. Each line break is kept.
>
> Words the app fills in here: {go letter}, {no-go letter}, {average tap time}, {missed}, {no-go tapped}, {no-go total}

Average tap time: **{average tap time}**
Missed {go letter}'s: **{missed}** (aim for 0)
{no-go letter}'s tapped: **{no-go tapped}** of {no-go total}

## Go/no-go: button to practise again
> Button after the practice.

Practice again

## Go/no-go: button to start the task
> Button after the practice.
>
> Words the app fills in here: {parts}

Start part 1 of {parts}

## Go/no-go: break, title
> Title of the break screen between parts.

Break

## Go/no-go: break
> Break screen between parts, above the scores.
>
> Words the app fills in here: {part}, {parts}, {go letter}, {no-go letter}

Part {part} of {parts} done.

## Go/no-go: reminder at each break
> Break screen, below the scores.
>
> Words the app fills in here: {go letter}, {no-go letter}

Tap {go letter} fast. Don't wait for {no-go letter}.

## Go/no-go: button to start the next part
> Button on the break screen (it can be pressed once the 15 s break is over).
>
> Words the app fills in here: {next part}, {parts}

Start part {next part}

## Go/no-go: end
> Last screen.

All done. Thank you!

# Storytelling task

## Storytelling: introduction
> First screen. If the films and stories have different retell times, {retell time} says "between 60 and 90 seconds".
>
> Words the app fills in here: {retell time}

You'll watch **2 short films** and listen to **2 short stories**, one at a time.

After each one, summarize what happened and share one key takeaway. You'll have {retell time}, and a timer will count down.

## Storytelling: button after the introduction
> Button on the first screen.

Continue

## Storytelling: before a film
> Before each film, in large text.
>
> Words the app fills in here: {retell time}

Next, you'll watch a short film. 

## Storytelling: before a story
> Before each story, in large text.
>
> Words the app fills in here: {retell time}

Next, you'll listen to a story.  

## Storytelling: before a film or story, second line
> Before each film or story, below the large text.
>
> Words the app fills in here: {retell time}

Tap Start when you're ready.

## Storytelling: start button
> Button before each film or story.

Start

## Storytelling: while a story plays
> On screen while a story plays (films fill the screen).

Listen to the story

## Storytelling: retell after a film
> Retell screen after a film, above the timer.
>
> Words the app fills in here: {retell time}

Briefly retell what happened in your own words and share one key thought or takeaway about it.

## Storytelling: retell after a story
> Retell screen after a story, above the timer.
>
> Words the app fills in here: {retell time}

Briefly retell what happened in your own words and share one key thought or takeaway about it.

## Storytelling: retell, second line
> Retell screen, below the first line, in smaller text.
>
> Words the app fills in here: {retell time}

Keep going until the timer runs out.

## Storytelling: when the time is up
> Shown for 2 s when the timer runs out.

Time's up. Thank you!

## Storytelling: end
> Last screen.

All done. Thank you!

## Storytelling: if a film or story won't play
> Only if a film or story fails to play.

Sorry, that didn't play.

Please tell the researcher.
