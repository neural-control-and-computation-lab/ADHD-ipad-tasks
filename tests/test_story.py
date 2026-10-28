"""Browser test of the storytelling task (story/index.html).

1. Opens the task and checks that it downloads the four films and stories in story/media/,
   keeps them after a reload (only a size check goes to the server), and shows their lengths.
2. Swaps in four short test clips made with ffmpeg (as if the files had changed on the server)
   and checks that the task downloads them again.
3. Runs a full session with the short clips and a 3 s retell. Trial 2 is paused and resumed
   during playback and trial 3 skips to the retell early. Checks the order, the sync flashes
   and the retell timing in the event log.

    python tests/test_story.py

Playwright's Chromium can't decode H.264, so it can't read the films' lengths; the test says so
and checks their sizes only. Safari on the iPad plays them.
"""
import asyncio, subprocess, sys, tempfile, pathlib
from playwright.async_api import async_playwright
from common import REPO, serve_repo, parse_csv, Checks

CLIPS = {
    'film1': ('film_a.webm', ['-f', 'lavfi', '-i', 'testsrc=size=640x480:rate=30:duration=3', '-c:v', 'libvpx', '-b:v', '300k']),
    'film2': ('film_b.webm', ['-f', 'lavfi', '-i', 'smptebars=size=640x360:rate=30:duration=2.5', '-c:v', 'libvpx', '-b:v', '300k']),
    'story1': ('story_a.wav', ['-f', 'lavfi', '-i', 'sine=frequency=440:duration=2.5']),
    'story2': ('story_b.wav', ['-f', 'lavfi', '-i', 'sine=frequency=660:duration=2']),
}


ALL_HERE = "['film1','film2','story1','story2'].every(s => window.__story.media[s]) && !window.__story.syncing"


def make_clips(folder):
    for name, args in CLIPS.values():
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', *args, str(folder / name)], check=True)


def clip_router(folder):
    """Playwright route handler that answers requests for story/media/<slot>-*.* with the test clips."""
    async def handler(route):
        slot = route.request.url.split('?')[0].rsplit('/', 1)[-1].split('-')[0]
        name = CLIPS[slot][0]
        body = (folder / name).read_bytes()
        ctype = 'video/webm' if name.endswith('.webm') else 'audio/wav'
        await route.fulfill(status=200, body=body, headers={'content-type': ctype, 'content-length': str(len(body))})
    return handler


def media_duration(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out)


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
            reqs = []
            page.on('request', lambda r: reqs.append((r.method, r.url.rsplit('/', 1)[-1])) if '/story/media/' in r.url else None)

            # 1. the files that come with the app
            real = {slot: next((REPO / 'story' / 'media').glob(slot + '-*')) for slot in CLIPS}
            await page.goto(base + '/story/?retellSec=3&doneMs=300')
            await page.wait_for_function('window.__story && window.__story.ready')
            await page.wait_for_function(ALL_HERE, timeout=180000)
            got = await page.evaluate("Object.fromEntries(Object.entries(window.__story.media).map(([k, m]) => [k, [m.name, m.size, m.duration]]))")
            chk(all(got[s][0] == real[s].name and got[s][1] == real[s].stat().st_size for s in CLIPS),
                'downloaded all four files in story/media/ (names and sizes match)')
            h264 = await page.evaluate("""document.createElement('video').canPlayType('video/mp4; codecs="avc1.640029, mp4a.40.2"') !== ''""")
            for s in CLIPS:
                if s.startswith('film') and not h264:
                    print(f'NOTE {s}: this browser has no H.264 decoder, so only the download was checked')
                    continue
                want = media_duration(real[s])
                chk(abs(got[s][2] - want) < 0.3, f'{s}: plays in this browser, length {got[s][2]:.1f} s (file: {want:.1f} s)')
            listed = await page.inner_text('#slots')
            chk(all(t in listed for t in ['The Book Witch', 'Live a Little', 'The Straw', 'The Wolf and the Kid']), 'setup screen lists the four titles')
            chk(await page.evaluate("JSON.parse(localStorage.getItem('storyTask:media')).ready"), 'tells the session page the files are on this device')
            reqs.clear()
            await page.reload()
            await page.wait_for_function('window.__story && window.__story.ready')
            await page.wait_for_function(ALL_HERE, timeout=30000)
            chk(not [r for r in reqs if r[0] == 'GET'] and len([r for r in reqs if r[0] == 'HEAD']) == 4,
                f'after a reload the files come from the device; only 4 size checks go to the server ({len(reqs)} requests)')

            # 2. files changed on the server: swap in the short test clips
            await page.context.route('**/story/media/*', clip_router(tmp))
            reqs.clear()
            await page.reload()
            await page.wait_for_function('window.__story && window.__story.ready')
            await page.wait_for_function(ALL_HERE + " && Object.values(window.__story.media).every(m => m.duration < 5)", timeout=30000)
            chk(sorted(r[1].split('-')[0] for r in reqs if r[0] == 'GET') == sorted(CLIPS), 'files that changed on the server are downloaded again')

            # 3. a full session with the short clips
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
    chk(all(f.name in text for f in real.values()) and 'version=1.2' in text.replace(' ', ''), 'data file header lists the file names and app version')
    chk(not errors, f'no page errors {errors[:3]}')
    return chk.finish()


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
