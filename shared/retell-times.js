/* Retell time for each film and story in the storytelling task.

   The times are in retell-times.md at the top of the repository, so they can be changed on
   GitHub without touching the code. Each "## Film 1 …" / "## Story 2 …" heading has a line
   "Retell time: 80 seconds" under it. The task downloads the file and keeps a copy on the
   device; if the download fails it uses that copy, and if there is none, the built-in time
   for each film and story (retellSec in SLOTS in story/index.html).

   Times can be written as "80", "80 seconds", "80 s", "1 minute", "1.5 minutes" or "1:20".
*/
(function () {
  'use strict';
  const FILE = 'retell-times.md';
  const MIN = 1, MAX = 600;
  const norm = s => String(s).trim().replace(/\s+/g, ' ').toLowerCase();

  /* "80", "80 seconds", "1 minute", "1.5 min", "1:20" -> seconds, or null if it can't be read. */
  function parseTime(v) {
    const s = norm(v).replace(/\.$/, '');
    let m;
    if ((m = s.match(/^(\d+)\s*(s|sec|secs|second|seconds)?$/))) return Number(m[1]);
    if ((m = s.match(/^(\d+(?:\.\d+)?)\s*(m|min|mins|minute|minutes)$/))) return Math.round(Number(m[1]) * 60);
    if ((m = s.match(/^(\d+):([0-5]\d)$/))) return Number(m[1]) * 60 + Number(m[2]);
    return null;
  }

  /* slots: [{id, name: 'Film 1', label: 'The Book Witch', retellSec: built-in time}] */
  function parse(md, slots) {
    const found = {}, problems = [], noted = new Set();
    let cur = null, fence = false;
    for (const raw of String(md).replace(/\r/g, '').split('\n')) {
      if (/^\s*```/.test(raw)) { fence = !fence; continue; }          // examples in ``` boxes are ignored
      if (fence) continue;
      const h = raw.match(/^##\s+(.+?)\s*#*\s*$/);
      if (h) {
        cur = slots.find(s => norm(h[1]).startsWith(norm(s.name))) || null;
        if (!cur) problems.push(`“${h[1]}” in ${FILE} doesn't start with ${slots.map(s => s.name).join(', ')}, so it isn't used.`);
        continue;
      }
      if (/^#(\s|$)/.test(raw)) { cur = null; continue; }
      const t = cur && raw.match(/^\s*retell time\s*:\s*(.*?)\s*$/i);
      if (!t) continue;
      const sec = parseTime(t[1]);
      if (sec === null) { problems.push(`${cur.name}: “${t[1]}” isn't a time the app can read (write e.g. 80 seconds or 1:20), so ${cur.retellSec} seconds is used.`); noted.add(cur.id); }
      else if (sec < MIN || sec > MAX) { problems.push(`${cur.name}: ${sec} seconds is outside ${MIN}–${MAX} seconds, so ${cur.retellSec} seconds is used.`); noted.add(cur.id); }
      else found[cur.id] = sec;
    }
    for (const s of slots)
      if (!(s.id in found) && !noted.has(s.id))
        problems.push(`No retell time found for ${s.name} (${s.label}) in ${FILE}, so ${s.retellSec} seconds is used. It needs a heading starting with "${s.name}" and a line "Retell time: …".`);
    return {times: Object.fromEntries(slots.map(s => [s.id, s.id in found ? found[s.id] : s.retellSec])), problems};
  }

  /* -> {times: {slot id: seconds}, source: 'file' | 'saved copy' | 'built-in', problems: [...]} */
  async function load(base, slots) {
    const {text, source} = await ParticipantText.fetchFile(FILE, base);
    const problems = [];
    if (source === 'saved copy') problems.push(`Couldn't download ${FILE}, so the copy saved on this device earlier is used.`);
    if (source === 'built-in') problems.push(`Couldn't download ${FILE}, so the built-in retell times are used.`);
    const r = text ? parse(text, slots) : {times: Object.fromEntries(slots.map(s => [s.id, s.retellSec])), problems: []};
    return {times: r.times, source, problems: problems.concat(r.problems)};
  }

  window.RetellTimes = {FILE, parse, parseTime, load};
})();
