/* Participant text for the ADHD iPad tasks.

   Everything a participant reads during a task comes from participant-text.md at the top of
   the repository, so it can be changed on GitHub without touching the code. Each "## heading"
   in that file is one piece of text; the text under it (until the next heading) is what is shown.

   When a task opens it downloads participant-text.md and keeps a copy on the device. If the
   download fails it uses that copy, and if there is none, the built-in text below. The built-in
   text is only a fallback: change the wording in participant-text.md, not here.

   Formatting understood in the file: a blank line starts a new paragraph, a single line break
   is kept, **two stars** make bold, lines starting with ">" are notes for the editor (not
   shown), and {names in curly brackets} are filled in by the app (see `fill` below).
*/
(function () {
  'use strict';
  const FILE = 'participant-text.md';
  const CACHE_KEY = 'adhdTasks:participantText';

  /* Every piece of participant text, in the order it appears in participant-text.md.
     task: which task uses it; where: the note shown under the heading in the file;
     text: built-in wording; fill: the {names} the app can fill in for this one;
     button: must not be empty. */
  const SECTIONS = [
    {key: 'Go/no-go: instructions title', task: 'gonogo', where: 'Title of the first screen.', text: 'Instructions'},
    {key: 'Go/no-go: instructions', task: 'gonogo', where: 'First screen, above the two letters.', text: 'Keep your finger on the start mark.'},
    {key: 'Go/no-go: next to the go letter', task: 'gonogo', where: 'First screen, next to the go letter (the app shows the letter).', text: 'tap the circle as fast as you can'},
    {key: 'Go/no-go: next to the no-go letter', task: 'gonogo', where: 'First screen, next to the no-go letter (the app shows the letter).', text: "don't move"},
    {key: 'Go/no-go: instructions, below the letters', task: 'gonogo', where: 'First screen, below the two letters, in smaller text.',
     text: "Go back to the mark after each tap. Don't wait to see if an {no-go letter} is coming.", fill: ['go letter', 'no-go letter']},
    {key: 'Go/no-go: button to start the practice', task: 'gonogo', where: 'Button on the first screen.', text: 'Start practice', button: true},
    {key: 'Go/no-go: practice message, too slow', task: 'gonogo', where: 'Practice only: shown after a go letter if they did not tap in time.', text: 'Too slow'},
    {key: 'Go/no-go: practice message, moved for the no-go letter', task: 'gonogo', where: 'Practice only: shown if they tap for the no-go letter.',
     text: "Don't move for {no-go letter}", fill: ['go letter', 'no-go letter']},
    {key: 'Go/no-go: practice message, too early', task: 'gonogo', where: 'Practice only: shown if they tap before the letter appears.', text: 'Too early'},
    {key: 'Go/no-go: after the practice, title', task: 'gonogo', where: 'Title of the screen after the practice.', text: 'Practice'},
    {key: 'Go/no-go: after the practice', task: 'gonogo', where: 'Screen after the practice, above the scores.',
     text: 'Practice done. From now on there are no messages after each letter.', fill: ['go letter', 'no-go letter']},
    {key: 'Go/no-go: scores', task: 'gonogo', where: 'Scores shown after the practice and at each break. Each line break is kept.',
     text: "Average tap time: **{average tap time}**\nMissed {go letter}'s: **{missed}** (aim for 0)\n{no-go letter}'s tapped: **{no-go tapped}** of {no-go total}",
     fill: ['go letter', 'no-go letter', 'average tap time', 'missed', 'no-go tapped', 'no-go total']},
    {key: 'Go/no-go: button to practise again', task: 'gonogo', where: 'Button after the practice.', text: 'Practice again', button: true},
    {key: 'Go/no-go: button to start the task', task: 'gonogo', where: 'Button after the practice.', text: 'Start part 1 of {parts}', fill: ['parts'], button: true},
    {key: 'Go/no-go: break, title', task: 'gonogo', where: 'Title of the break screen between parts.', text: 'Break'},
    {key: 'Go/no-go: break', task: 'gonogo', where: 'Break screen between parts, above the scores.', text: 'Part {part} of {parts} done.', fill: ['part', 'parts', 'go letter', 'no-go letter']},
    {key: 'Go/no-go: reminder at each break', task: 'gonogo', where: 'Break screen, below the scores.', text: "Tap {go letter} fast. Don't wait for {no-go letter}.", fill: ['go letter', 'no-go letter']},
    {key: 'Go/no-go: button to start the next part', task: 'gonogo', where: 'Button on the break screen (it can be pressed once the 15 s break is over).', text: 'Start part {next part}', fill: ['next part', 'parts'], button: true},
    {key: 'Go/no-go: end', task: 'gonogo', where: 'Last screen.', text: 'All done. Thank you!'},

    {key: 'Storytelling: introduction', task: 'story', where: 'First screen.',
     text: "You'll watch **2 short films** and listen to **2 short stories**, one at a time.\n\nAfter each one, tell us what happened. You'll have {retell time}, and a timer will count down.",
     fill: ['retell time']},
    {key: 'Storytelling: button after the introduction', task: 'story', where: 'Button on the first screen.', text: 'Continue', button: true},
    {key: 'Storytelling: before a film', task: 'story', where: 'Before each film, in large text.', text: "Next, you'll watch a short film."},
    {key: 'Storytelling: before a story', task: 'story', where: 'Before each story, in large text.', text: "Next, you'll listen to a story."},
    {key: 'Storytelling: before a film or story, second line', task: 'story', where: 'Before each film or story, below the large text.', text: "Tap Start when you're ready."},
    {key: 'Storytelling: start button', task: 'story', where: 'Button before each film or story.', text: 'Start', button: true},
    {key: 'Storytelling: while a story plays', task: 'story', where: 'On screen while a story plays (films fill the screen).', text: 'Listen to the story'},
    {key: 'Storytelling: retell after a film', task: 'story', where: 'Retell screen after a film, above the timer.', text: 'Tell us what happened in the film.', fill: ['retell time']},
    {key: 'Storytelling: retell after a story', task: 'story', where: 'Retell screen after a story, above the timer.', text: 'Tell us what happened in the story.', fill: ['retell time']},
    {key: 'Storytelling: retell, second line', task: 'story', where: 'Retell screen, below the first line, in smaller text.', text: 'Keep going until the timer runs out.', fill: ['retell time']},
    {key: 'Storytelling: when the time is up', task: 'story', where: 'Shown for 2 s when the timer runs out.', text: "Time's up. Thank you!"},
    {key: 'Storytelling: end', task: 'story', where: 'Last screen.', text: 'All done. Thank you!'},
    {key: "Storytelling: if a film or story won't play", task: 'story', where: 'Only if a film or story fails to play.', text: "Sorry, that didn't play.\n\nPlease tell the researcher."}
  ];
  const norm = h => String(h).trim().replace(/\s+/g, ' ').replace(/[’‘]/g, "'").toLowerCase();
  const TASK_PREFIX = {gonogo: 'go/no-go:', story: 'storytelling:'};

  /* participant-text.md -> {normalised heading: {heading, text}} */
  function parse(md) {
    const out = {};
    let cur = null, lines = [];
    const flush = () => { if (cur) out[norm(cur)] = {heading: cur, text: lines.join('\n').replace(/<!--[\s\S]*?-->/g, '').trim()}; };
    for (const raw of String(md).replace(/\r/g, '').split('\n')) {
      const h2 = raw.match(/^##\s+(.+?)\s*#*\s*$/);
      if (h2) { flush(); cur = h2[1]; lines = []; continue; }
      if (/^#(\s|$)/.test(raw)) { flush(); cur = null; continue; }     // a top-level heading ends a section
      if (!cur || /^\s*>/.test(raw)) continue;                         // notes for the editor
      lines.push(raw);
    }
    flush();
    return out;
  }
  const names = text => [...String(text).matchAll(/\{([^{}]+)\}/g)].map(m => m[1].trim());

  /* The text as participant-text.md (used to create the file; the file is the copy people edit). */
  function toMarkdown(intro) {
    let md = intro || '';
    let task = null;
    for (const s of SECTIONS) {
      if (s.task !== task) { task = s.task; md += `\n# ${task === 'gonogo' ? 'Go/no-go reach task' : 'Storytelling task'}\n`; }
      const can = (s.fill || []).length ? `\n>\n> Words the app fills in here: ${s.fill.map(n => '{' + n + '}').join(', ')}` : '';
      md += `\n## ${s.key}\n> ${s.where}${can}\n\n${s.text}\n`;
    }
    return md;
  }

  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  function fillIn(text, vars) {
    return String(text).replace(/\{([^{}]+)\}/g, (m, n) => {
      const k = n.trim().toLowerCase();
      return vars && Object.prototype.hasOwnProperty.call(vars, k) ? String(vars[k]) : m;
    });
  }
  const inlineHtml = s => esc(s).replace(/\*\*([\s\S]+?)\*\*/g, '<b>$1</b>').replace(/\n/g, '<br>');

  /* Build the text object a task uses, plus a list of problems for the setup screen. */
  function build(task, fileMap, source) {
    const problems = [];
    if (source === 'saved copy') problems.push(`Couldn't download ${FILE}, so the copy saved on this device earlier is used.`);
    if (source === 'built-in') problems.push(`Couldn't download ${FILE}, so the built-in text is used.`);
    const mine = SECTIONS.filter(s => task === 'all' || s.task === task);
    const text = {};
    for (const s of mine) {
      const f = fileMap && fileMap[norm(s.key)];
      let t = s.text;
      if (fileMap && !f) problems.push(`“${s.key}” is missing from ${FILE}, so the built-in text is used for it. Check the heading is spelled exactly as before.`);
      else if (f && !f.text && s.button) problems.push(`“${s.key}” is empty, so the built-in text is used for it (a button needs a label).`);
      else if (f) t = f.text;
      const bad = names(t).filter(n => !(s.fill || []).includes(n.toLowerCase()));
      if (bad.length) problems.push(`“${s.key}”: ${bad.map(n => '{' + n + '}').join(', ')} can't be filled in here, so ${bad.length > 1 ? 'they show' : 'it shows'} exactly as typed.` +
        ((s.fill || []).length ? ` Available here: ${s.fill.map(n => '{' + n + '}').join(', ')}.` : ''));
      text[s.key] = t;
    }
    if (fileMap) {
      const known = new Set(SECTIONS.map(s => norm(s.key)));
      const prefixes = task === 'all' ? Object.values(TASK_PREFIX) : [TASK_PREFIX[task]];
      for (const [k, f] of Object.entries(fileMap))
        if (!known.has(k) && prefixes.some(p => k.startsWith(p)))
          problems.push(`“${f.heading}” in ${FILE} isn't a heading the app knows, so its text isn't used. Check the spelling.`);
    }
    const get = key => { if (!(key in text)) throw new Error('unknown participant text: ' + key); return text[key]; };
    return {
      source, problems, text,
      plain: (key, vars) => fillIn(get(key), vars).replace(/\*\*/g, '').replace(/\s*\n\s*/g, ' ').trim(),   // buttons and titles
      line: (key, vars) => inlineHtml(fillIn(get(key), vars).trim()),                                       // one block, line breaks kept
      paras: (key, vars, cls) => fillIn(get(key), vars).split(/\n\s*\n/).map(p => p.trim()).filter(Boolean)  // paragraphs
        .map(p => `<p${cls ? ` class="${cls}"` : ''}>${inlineHtml(p)}</p>`).join('')
    };
  }

  /* Load the text for one task ('gonogo', 'story' or 'all'). base = path to the repository root. */
  async function load(task, base) {
    let md = null, source = 'built-in';
    try {
      const ctl = new AbortController(), timer = setTimeout(() => ctl.abort(), 6000);
      const res = await fetch((base || '') + FILE, {cache: 'no-cache', signal: ctl.signal});
      clearTimeout(timer);
      if (res.ok) { md = await res.text(); source = 'file'; try { localStorage.setItem(CACHE_KEY, md); } catch (e) {} }
    } catch (e) {}
    if (md === null) { try { md = localStorage.getItem(CACHE_KEY); } catch (e) {} if (md) source = 'saved copy'; }
    return build(task, md ? parse(md) : null, source);
  }

  window.ParticipantText = {FILE, SECTIONS, parse, build, load, toMarkdown, fillIn};
})();
