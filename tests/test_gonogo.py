"""Browser test of the go/no-go task (gonogo/index.html).

Runs a shortened session in headless Chromium with a simulated participant that taps most
go letters, misses some, taps some no-go letters and occasionally touches too early, pauses
and resumes mid-block, then checks the exported CSV against what the simulated participant did.

    python tests/test_gonogo.py
"""
import asyncio, sys
from playwright.async_api import async_playwright
from common import serve_repo, parse_csv, Checks

FAST = ('?practiceTrials=8&blocks=2&trialsPerBlock=16&postMs=600&fixMinMs=100&fixMaxMs=500'
        '&maxRtMs=550&breakSec=1&countdownSec=1&leadMs=200&syncFlashMs=100&feedbackMs=200')

ROBOT_JS = r"""
(() => {
  let seed = 12345; const rnd = () => (seed = (seed*1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;
  window.__robot = [];
  const st = document.getElementById('stage'), L = window.__gng.L;
  const tap = (x, y) => { const o = {clientX:x, clientY:y, bubbles:true, cancelable:true, pointerId:1, pointerType:'touch'};
    st.dispatchEvent(new PointerEvent('pointerdown', o)); setTimeout(() => st.dispatchEvent(new PointerEvent('pointerup', o)), 80); };
  const letter = document.getElementById('letter'), fix = document.getElementById('fix');
  new MutationObserver(() => {                     // occasional touch during fixation
    if (!fix.classList.contains('hidden') && window.__gng.B && rnd() < 0.06) {
      setTimeout(() => tap(L.cx + 5, L.cy + 5), 20);
      window.__robot.push({code: window.__gng.B.cur && window.__gng.B.cur.code, act: 'premature'});
    }
  }).observe(fix, {attributes: true, attributeFilter: ['class']});
  new MutationObserver(() => {                     // respond to each letter
    if (letter.classList.contains('hidden') || letter.classList.contains('count')) return;
    const B = window.__gng.B; if (!B || !B.cur) return;
    const c = B.cur, act = c.type === 'go' ? (rnd() < 0.1 ? 'miss' : 'tap') : (rnd() < 0.3 ? 'tap' : 'withhold');
    const delay = 150 + Math.floor(rnd()*250);
    window.__robot.push({code: c.code, type: c.type, act, delay});
    if (act === 'tap') { const off = rnd() < 0.15 ? 300 : 0; setTimeout(() => tap(L.cx + off, L.cy + off/3), delay); }
  }).observe(letter, {attributes: true, attributeFilter: ['class']});
})();
"""


async def click_text(page, text, timeout=60000):
    await page.wait_for_function(
        "t => [...document.querySelectorAll('#msgBtns button')].some(b => b.textContent.startsWith(t) && !b.disabled)",
        arg=text, timeout=timeout)
    await page.locator('#msgBtns button', has_text=text).first.click()


async def wait_msg(page, timeout=120000):
    await page.wait_for_function("() => !document.getElementById('msg').classList.contains('hidden')", timeout=timeout)


async def main():
    chk = Checks()
    with serve_repo() as base:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            ctx = await browser.new_context(viewport={'width': 1180, 'height': 820}, has_touch=True, accept_downloads=True)
            page = await ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))

            # --- shortened session with a simulated participant ---
            await page.goto(base + '/gonogo/' + FAST)
            await page.fill('#pid', 'TEST01')
            await page.evaluate(ROBOT_JS)
            await page.click('#startBtn')
            await click_text(page, 'Start practice')
            await wait_msg(page)
            await click_text(page, 'Start part 1')
            await page.wait_for_timeout(4500)
            await page.keyboard.press('Escape')
            await page.wait_for_timeout(300)
            chk(await page.is_visible('#pause'), 'pause screen opens mid-block')
            await page.click('#resumeBtn')
            await wait_msg(page)
            await click_text(page, 'Start part 2')
            await page.wait_for_function("window.__gng.S && window.__gng.S.status === 'finished'", timeout=120000)
            end_text = await page.inner_text('#msg')
            chk('All done' in end_text and 'TEST01' not in end_text and 'Experimenter' not in end_text,
                'end screen is for the participant (no ID, no experimenter table)')
            robot = await page.evaluate('window.__robot')
            lists = await page.evaluate('window.__gng.S.testLists')
            async with page.expect_download() as dl:
                await page.locator('#msgExtra button', has_text='Save data').click()   # no share sheet here, so it downloads
            text = open(await (await dl.value).path()).read()

            rows = parse_csv(text)
            trials = [r for r in rows if r['type'] != 'sync']
            syncs = [r for r in rows if r['type'] == 'sync']
            final = [r for r in trials if r['aborted'] == '0']
            by = {}
            for r in final:
                by.setdefault(r['block_label'], []).append(r)
            chk(sorted(by) == ['B1', 'B2', 'P1'], f'blocks present {sorted(by)}')
            chk(len(by['P1']) == 8 and sum(r['type'] == 'nogo' for r in by['P1']) == 2, 'practice: 8 trials, 2 no-go')
            for b in ['B1', 'B2']:
                chk(len(by[b]) == 16 and sum(r['type'] == 'nogo' for r in by[b]) == 4, f'{b}: 16 trials, 4 no-go')
            for i, b in enumerate(['B1', 'B2']):
                got = {int(r['trial_in_block']): r for r in by[b]}
                chk([got[k + 1]['type'] for k in range(16)] == [x['type'] for x in lists[i]], f'{b} trial order matches the seeded list')
                chk([int(got[k + 1]['foreperiod_ms']) for k in range(16)] == [x['fp'] for x in lists[i]], f'{b} fixation times match the seeded list')
            codes = [int(r['code']) for r in trials]
            chk(codes == sorted(set(codes)), 'trial codes unique and increasing')
            chk(len(syncs) == 3 * (len({r['block_run'] for r in trials}) + 1), f'3 sync flashes per block start or resume ({len(syncs)} logged)')
            d = [float(r['onset_ms']) - float(r['fix_ms']) - float(r['foreperiod_ms']) for r in final]
            chk(all(abs(x) <= 34 for x in d), f'fixation lasts its planned time (actual - planned {min(d):.1f} to {max(d):.1f} ms)')
            rr = sorted(by['B2'], key=lambda r: int(r['trial_in_block']))
            post = [float(rr[i + 1]['fix_ms']) - float(rr[i]['onset_ms']) for i in range(len(rr) - 1)]
            chk(all(583 <= x <= 650 for x in post), f'letter onset to next fixation {min(post):.0f}-{max(post):.0f} ms (600 planned)')

            plan = {a['code']: a for a in robot if 'type' in a}
            expect = {('go', 'tap'): 'hit', ('go', 'miss'): 'omission', ('nogo', 'tap'): 'commission', ('nogo', 'withhold'): 'correct_withhold'}
            mism, rterr = 0, []
            for r in final:
                a = plan.get(int(r['code']))
                if not a or r['outcome'] != expect[(a['type'], a['act'])]:
                    mism += 1
                elif r['outcome'] in ('hit', 'commission'):
                    rterr.append(float(r['rt_ms']) - a['delay'])
            chk(mism == 0, f'outcomes match the simulated responses ({len(final)} trials)')
            chk(rterr and all(-2 <= e <= 30 for e in rterr), f'logged RT matches tap time ({min(rterr):.1f} to {max(rterr):.1f} ms difference)')
            chk(any(r['in_target'] == '0' for r in final), 'taps outside the circle are flagged')

            # --- same ID gives the same order; different ID a different one ---
            orders = []
            for pid in ['TEST01', 'TEST01', 'TEST02']:
                await page.goto(base + '/gonogo/')
                await page.fill('#pid', pid)
                await page.click('#startBtn')
                orders.append(await page.evaluate('window.__gng.S.testLists'))
            chk(orders[0] == orders[1] and orders[0] != orders[2], 'order is reproducible from the participant ID')
            chk([len(x) for x in orders[0]] == [72] * 4 and all([t['type'] for t in x].count('nogo') == 18 for x in orders[0]),
                'defaults: 4 blocks of 72 with 18 no-go each')
            fps = [t['fp'] for x in orders[0] for t in x]
            chk(500 <= min(fps) and max(fps) <= 2000, f'default fixation times within 500-2000 ms ({min(fps)}-{max(fps)})')
            chk(not errors, f'no page errors {errors[:3]}')
            await browser.close()
    return chk.finish()


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
