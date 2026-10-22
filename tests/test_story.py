"""Browser test of the storytelling task (story/index.html).

Makes four short test clips with ffmpeg (two videos, two tones), loads them into the app,
checks they survive a page reload, then runs a full session with a 3 s retell. Trial 2 is
paused and resumed during playback and trial 3 skips to the retell early. Checks the order,
the sync flashes and the retell timing in the event log.

    python tests/test_story.py
"""
import asyncio, subprocess, sys, tempfile, pathlib
from playwright.async_api import async_playwright
from common import serve_repo, parse_csv, Checks

CLIPS = {
    'film1': ('film_a.webm', ['-f', 'lavfi', '-i', 'testsrc=size=640x480:rate=30:duration=3', '-c:v', 'libvpx', '-b:v', '300k']),
    'film2': ('film_b.webm', ['-f', 'lavfi', '-i', 'smptebars=size=640x360:rate=30:duration=2.5', '-c:v', 'libvpx', '-b:v', '300k']),
    'story1': ('story_a.wav', ['-f', 'lavfi', '-i', 'sine=frequency=440:duration=2.5']),
    'story2': ('story_b.wav', ['-f', 'lavfi', '-i', 'sine=frequency=660:duration=2']),
}


def make_clips(folder):
    for name, args in CLIPS.values():
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', *args, str(folder / name)], check=True)


async def open_menu(page):
    await page.keyboard.press('Escape')
    await page.wait_for_function("!document.getElementById('menu').classList.contains('hidden')")


async def menu_click(page, label):
    await page.evaluate("l => [...document.querySelectorAll('#menuBtns button')].find(b => b.textContent.startsWith(l)).click()", label)


async def wait_flashes_done(page, trial, tag):
    await page.wait_for_function(
        "([n, tag]) => window.__story.S.rows.some(r => r.trial === n && r.event === 'sync_flash' && r.detail === tag + ' flash 3')",
        arg=[trial, tag])


async def main():
    chk = Checks()
    with tempfile.TemporaryDirectory() as tmp, serve_repo() as base:
        tmp = pathlib.Path(tmp)
        make_clips(tmp)
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
            page = await browser.new_page(viewport={'width': 1180, 'height': 820})
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            await page.goto(base + '/story/?retellSec=3&doneMs=300')
            await page.wait_for_function('window.__story && window.__story.ready')
            for slot, (name, _) in CLIPS.items():
                await page.set_input_files(f'input[data-slot={slot}]', str(tmp / name))
                await page.wait_for_function('s => !!window.__story.media[s]', arg=slot, timeout=15000)
            await page.reload()
            await page.wait_for_function('window.__story && window.__story.ready')
            listed = await page.inner_text('#slots')
            chk(all(name in listed for name, _ in CLIPS.values()), 'all four files still loaded after a page reload')

            await page.fill('#pid', 'TEST01')
            expected = await page.evaluate("window.__story.seededOrder('TEST01')")
            await page.click('#startBtn')
            await page.locator('#msgBtns button', has_text='Continue').click()
            for n in range(1, 5):
                await page.wait_for_function("n => document.getElementById('msgTitle').textContent === `Trial ${n} of 4`", arg=n, timeout=20000)
                await page.locator('#msgBtns button', has_text='Start').click()
                if n == 2:
                    await wait_flashes_done(page, 2, 'playback start')
                    await page.wait_for_timeout(300)
                    await open_menu(page)
                    await menu_click(page, 'Resume')
                if n == 3:
                    await wait_flashes_done(page, 3, 'playback start')
                    await page.wait_for_timeout(300)
                    await open_menu(page)
                    await menu_click(page, 'Skip to the retell')
                if n == 4:
                    await wait_flashes_done(page, 4, 'retell start')
                    await page.wait_for_timeout(500)
                    await open_menu(page)
                    await page.wait_for_timeout(500)
                    await menu_click(page, 'Continue the countdown')
            await page.wait_for_function("document.getElementById('msgTitle').textContent === 'Finished'", timeout=30000)
            text = await page.evaluate('window.__story.csvText({meta: window.__story.S.meta, rows: window.__story.S.rows})')
            await browser.close()

    rows = parse_csv(text)
    trials = {}
    for r in rows:
        if r['trial']:
            trials.setdefault(int(r['trial']), []).append(r)
    chk([trials[n][0]['slot'] for n in sorted(trials)] == expected, f'played in the order set by the ID {expected}')
    for n in sorted(trials):
        ev = trials[n]
        first = lambda e, d=None: next((r for r in ev if r['event'] == e and (d is None or r['detail'] == d)), None)
        pf = [r for r in ev if r['event'] == 'sync_flash' and r['detail'].startswith('playback start')]
        rf = [r for r in ev if r['event'] == 'sync_flash' and r['detail'].startswith('retell start')]
        lag = float(pf[0]['t_ms']) - float(first('media_playing')['t_ms'])
        dur = float(first('retell_end')['t_ms']) - float(first('retell_start')['t_ms'])
        chk(len(pf) == 3 and len(rf) == 3, f'trial {n} ({ev[0]["kind"]}): 3 flashes at playback start and 3 at retell start')
        chk(0 <= lag < 80, f'trial {n}: first flash {lag:.1f} ms after playback began')
        chk(first('retell_start')['t_ms'] == rf[0]['t_ms'], f'trial {n}: retell timer starts on retell flash 1')
        chk(2990 <= dur <= 3060, f'trial {n}: retell lasted {dur:.0f} ms (3000 planned)')
    chk(any(r['event'] == 'resumed' for r in trials[2]), 'trial 2: pause and resume during playback logged')
    chk(any(r['event'] == 'media_stopped_early' for r in trials[3]), 'trial 3: skip to the retell logged')
    chk(any(r['event'] == 'menu_opened' for r in trials[4]), 'trial 4: menu during the retell, countdown kept its time')
    chk(not errors, f'no page errors {errors[:3]}')
    return chk.finish()


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
