"""Browser test of the session page (index.html) with both tasks.

Starts a session for participant P007 on the session page, opens each task from there, checks
that the participant's details arrive and are locked, runs a very short version of each task,
then checks the statuses on the session page and that "Save all CSVs" exports both files with
the same visit ID.

    python tests/test_session.py
"""
import asyncio, sys, tempfile, pathlib
from playwright.async_api import async_playwright
from common import serve_repo, Checks
from test_story import make_clips, clip_router, ALL_HERE

GNG_FAST = 'practiceTrials=0&blocks=1&trialsPerBlock=8&postMs=500&fixMinMs=100&fixMaxMs=300&maxRtMs=400&countdownSec=1&leadMs=100&syncFlashMs=80'
STORY_FAST = 'retellSec=1&doneMs=200'


async def main():
    chk = Checks()
    with tempfile.TemporaryDirectory() as tmp, serve_repo() as base:
        tmp = pathlib.Path(tmp)
        make_clips(tmp)
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
            ctx = await browser.new_context(viewport={'width': 1180, 'height': 820}, accept_downloads=True)
            page = await ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('dialog', lambda d: asyncio.ensure_future(d.accept()))

            # the storytelling task downloads its files the first time it opens (short test clips here)
            await ctx.route('**/story/media/*', clip_router(tmp))
            await page.goto(base + '/')
            chk('not on this iPad yet' in await page.inner_text('#storeMeta'), 'session page warns that the films and stories are not downloaded yet')
            await page.goto(base + '/story/')
            await page.wait_for_function('window.__story && window.__story.ready')
            await page.wait_for_function(ALL_HERE, timeout=30000)

            # start a session
            await page.goto(base + '/')
            chk('stories for the storytelling task: on this iPad' in await page.inner_text('#storeMeta'), 'session page shows the films and stories are on this iPad')
            await page.fill('#pid', 'P007')
            await page.select_option('#hand', 'left')
            await page.fill('#notes', 'test run')
            await page.click('#startBtn')
            chk(await page.inner_text('#who') == 'P007', 'session page shows the current participant')
            order = await page.eval_on_selector_all('#taskList .task b', 'els => els.map(e => e.textContent)')
            chk('Go/no-go' in order[0], f'odd ID: go/no-go suggested first ({order})')
            visit = await page.evaluate("JSON.parse(localStorage.getItem('adhdTasks:currentSession')).visit")

            # go/no-go from the session page
            await page.locator('#taskList .task', has_text='Go/no-go').locator('button').click()
            await page.wait_for_url('**/gonogo/**')
            chk('pid=P007' in page.url and 'hand=left' in page.url, 'task link carries the participant')
            await page.goto(page.url + '&' + GNG_FAST)
            vals = await page.evaluate("[document.getElementById('pid').value, document.getElementById('pid').readOnly, document.getElementById('hand').value, document.getElementById('hand').disabled, document.getElementById('notes').value]")
            chk(vals == ['P007', True, 'left', True, 'test run'], f'go/no-go: participant details filled in and locked {vals}')
            await page.click('#startBtn')
            await page.locator('#msgBtns button', has_text='Start').click()
            await page.wait_for_function("document.getElementById('msgTitle').textContent === 'Finished'", timeout=60000)
            chk(await page.locator('#msgExtra button', has_text='Back to session page').count() == 1, 'go/no-go end screen offers "Back to session page"')
            await page.locator('#msgExtra button', has_text='Back to session page').click()
            await page.wait_for_function("document.getElementById('who') && document.getElementById('who').textContent === 'P007'")

            # storytelling from the session page
            await page.locator('#taskList .task', has_text='Storytelling').locator('button').click()
            await page.wait_for_url('**/story/**')
            await page.goto(page.url + '&' + STORY_FAST)
            await page.wait_for_function('window.__story && window.__story.ready')
            vals = await page.evaluate("[document.getElementById('pid').value, document.getElementById('pid').readOnly]")
            chk(vals == ['P007', True], 'storytelling: participant filled in and locked')
            await page.click('#startBtn')
            await page.locator('#msgBtns button', has_text='Continue').click()
            for n in range(1, 5):
                await page.wait_for_function("n => document.getElementById('msgTitle').textContent === `Trial ${n} of 4`", arg=n, timeout=20000)
                await page.locator('#msgBtns button', has_text='Start').click()
            await page.wait_for_function("document.getElementById('msgTitle').textContent === 'Finished'", timeout=30000)
            await page.locator('#msgExtra button', has_text='Back to session page').click()
            await page.wait_for_function("document.getElementById('who') && document.getElementById('who').textContent === 'P007'")

            # statuses and combined export
            st = await page.eval_on_selector_all('#taskList .st', 'els => els.map(e => e.textContent)')
            chk(all(s.startswith('Finished') for s in st), f'both tasks show as finished ({st})')
            names = []
            async def grab(d):
                names.append(d.suggested_filename)
                texts.append(open(await d.path()).read())
            texts = []
            page.on('download', lambda d: asyncio.ensure_future(grab(d)))
            await page.click('#saveAllBtn')
            await page.wait_for_timeout(1500)
            chk(sorted(n.split('_')[0] for n in names) == ['GNG', 'STORY'] and all('_P007_' in n for n in names), f'"Save all" exports both CSVs ({names})')
            chk(len(texts) == 2 and all(f'visit={visit}' in t for t in texts), f'both CSVs carry the same visit ID ({visit})')
            chk(any('hand=left' in t for t in texts) and all('notes=test run' in t for t in texts), 'hand and notes from the session page are in the data')
            await page.wait_for_function("document.querySelectorAll('#taskList .st')[0].textContent.includes('exported')")
            chk(True, 'runs marked as exported')
            await page.click('#endBtn')
            chk(await page.is_visible('#newCard'), 'ending the session returns to the new-participant form')
            chk(not errors, f'no page errors {errors[:3]}')
            await browser.close()
    return chk.finish()


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
