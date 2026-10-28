/* Shared session (participant) information for the ADHD iPad tasks.

   The session page (index.html) sets the current participant once per visit. Each task reads
   it, fills in its participant fields and saves its data under the same visit ID, so one
   participant can be run through both tasks without re-entering anything. The participant is
   also passed in the task link (?pid=...), which works even if the browser storage differs.

   Saved task data (one record per task run) live in this browser's localStorage under each
   task's prefix. Each record holds the finished CSV text, so the session page can list and
   export everything for a participant.
*/
(function () {
  'use strict';
  const KEY = 'adhdTasks:currentSession';
  const TASKS = [
    {id: 'gonogo', name: 'Go/no-go reach task', short: 'Go/no-go', path: 'gonogo/', prefix: 'gngReach:session:'},
    {id: 'story', name: 'Storytelling task', short: 'Storytelling', path: 'story/', prefix: 'storyTask:session:'}
  ];

  const lsGet = k => { try { return localStorage.getItem(k); } catch (e) { return null; } };
  const lsSet = (k, v) => { try { localStorage.setItem(k, v); return true; } catch (e) { return false; } };
  const lsDel = k => { try { localStorage.removeItem(k); } catch (e) {} };
  const lsKeys = () => { try { return Object.keys(localStorage); } catch (e) { return []; } };
  const pad = n => String(n).padStart(2, '0');
  const stamp = d => `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}-${pad(d.getHours())}${pad(d.getMinutes())}`;
  const validId = id => /^[A-Za-z0-9_\-]+$/.test(id || '');

  /* The current participant: link parameters first, then the stored session. */
  function current() {
    const q = new URLSearchParams(location.search);
    const pid = q.get('pid');
    let stored = null;
    try { stored = JSON.parse(lsGet(KEY) || 'null'); } catch (e) {}
    if (pid && validId(pid)) {
      const same = stored && stored.participant === pid ? stored : {};
      return {participant: pid, hand: q.get('hand') || same.hand || 'right',
              visit: q.get('visit') || same.visit || '', started_iso: same.started_iso || ''};
    }
    return stored && validId(stored.participant) ? stored : null;
  }
  function start(info) {
    const now = new Date();
    const s = {participant: info.participant, hand: info.hand || 'right',
               visit: stamp(now), started_iso: now.toISOString(), started_local: now.toLocaleString()};
    lsSet(KEY, JSON.stringify(s));
    return s;
  }
  function update(fields) { const s = current(); if (!s) return null; Object.assign(s, fields); lsSet(KEY, JSON.stringify(s)); return s; }
  function end() { lsDel(KEY); }
  function taskLink(task, s, base) {
    const q = new URLSearchParams({pid: s.participant, hand: s.hand || 'right', visit: s.visit || ''});
    return (base || '') + task.path + '?' + q.toString();
  }

  /* All saved task runs on this iPad, newest first. */
  function records() {
    const out = [];
    for (const t of TASKS) {
      for (const k of lsKeys().filter(k => k.startsWith(t.prefix))) {
        let d = null;
        try { d = JSON.parse(lsGet(k)); } catch (e) {}
        if (!d || !d.csv) continue;           // older test records without CSV text are ignored here
        out.push(Object.assign({key: k, taskId: t.id, taskName: t.short}, d));
      }
    }
    return out.sort((a, b) => String(b.session).localeCompare(String(a.session)));
  }
  function markExported(keys) {
    for (const k of keys) { try { const d = JSON.parse(lsGet(k)); if (d) { d.exported = true; lsSet(k, JSON.stringify(d)); } } catch (e) {} }
  }
  function storageUsed() {               // characters held by the tasks in localStorage (≈ bytes)
    let n = 0;
    for (const k of lsKeys()) if (TASKS.some(t => k.startsWith(t.prefix))) n += (lsGet(k) || '').length;
    return n;
  }
  /* Share (or download) one or more CSV files. Returns true if the share sheet or download ran. */
  async function exportFiles(files) {
    try {
      const fs = files.map(f => new File([f.text], f.name, {type: 'text/csv'}));
      if (navigator.canShare && navigator.canShare({files: fs})) { await navigator.share({files: fs, title: files.length === 1 ? files[0].name : 'Task data'}); return true; }
    } catch (e) { if (e && e.name === 'AbortError') return false; }
    for (const f of files) {
      const a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([f.text], {type: 'text/csv'})); a.download = f.name;
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(a.href), 10000);
    }
    return true;
  }

  window.Session = {KEY, TASKS, current, start, update, end, taskLink, records, markExported, storageUsed, exportFiles, validId, stamp,
                    lsGet, lsSet, lsDel};
})();
