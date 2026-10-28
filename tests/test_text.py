"""Browser test of the participant text (participant-text.md, read by shared/text.js).

Checks that participant-text.md has every heading the tasks use and nothing they can't use,
that the preview page shows every screen, that an edited file changes what the participant
sees (and is recorded in the data), that mistakes in the file are reported on the setup screen
and the preview page, and that the tasks fall back to the last downloaded copy, then to the
built-in text, when the file can't be downloaded.

    python tests/test_text.py
"""
import asyncio, sys
from playwright.async_api import async_playwright
from common import REPO, serve_repo, Checks

MD = (REPO / 'participant-text.md').read_text()


async def route_text(ctx, body=None, status=200):
    """Serve participant-text.md with this content (or an error status) from now on."""
    await ctx.unroute('**/participant-text.md')
    async def handler(route):
        if status != 200:
            await route.fulfill(status=status, body='not found')
        else:
            await route.fulfill(status=200, body=body, headers={'content-type': 'text/markdown; charset=utf-8'})
    await ctx.route('**/participant-text.md', handler)


async def gonogo_instructions(page, base):
    """Open the go/no-go task, start it, and return (setup warning, instructions screen text, recorded text)."""
    await page.goto(base + '/gonogo/')
    await page.wait_for_function('window.__gng')
    await page.fill('#pid', 'TXT01')
    await page.click('#startBtn')
    await page.wait_for_function("!document.getElementById('msg').classList.contains('hidden')")
    warn = await page.evaluate("document.getElementById('textLine').classList.contains('hidden') ? '' : document.getElementById('textLine').textContent")
    shown = await page.inner_text('#msg')
    recorded = await page.evaluate("[window.__gng.S.meta.text_source, window.__gng.S.meta.participant_text['Go/no-go: instructions']]")
    return warn, shown, recorded


async def main():
    chk = Checks()
    with serve_repo() as base:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            ctx = await browser.new_context(viewport={'width': 1180, 'height': 820})
            page = await ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))

            # the file in the repository
            await page.goto(base + '/preview.html')
            await page.wait_for_selector('#status .box')
            chk(await page.get_attribute('#status .box', 'class') == 'box ok', 'participant-text.md: every heading is there and usable (preview page says so)')
            n = await page.evaluate("document.querySelectorAll('figure').length")
            chk(n == 16, f'preview page shows all {n} participant screens')
            keys = await page.evaluate("window.ParticipantText.SECTIONS.map(s => s.key)")
            chk(all(f'## {k}\n' in MD for k in keys), f'all {len(keys)} headings are in participant-text.md')

            # an edited file
            edited = MD.replace('Keep your finger on the start mark.', 'Rest your finger on the **start mark**.')
            edited = edited.replace('## Storytelling: before a story\n', '## Storytelling: befor a story\n')          # typo in a heading
            edited = edited.replace('Tap {go letter} fast.', 'Tap {go leter} fast.')                                # typo in a word to fill in
            await route_text(ctx, edited)
            warn, shown, recorded = await gonogo_instructions(page, base)
            chk('Rest your finger on the start mark.' in shown, 'an edited line shows on the participant screen')
            chk(recorded == ['file', 'Rest your finger on the **start mark**.'], f'the wording used is recorded in the data {recorded}')
            chk('{go leter}' in warn, 'setup screen reports a misspelled {word}')
            await page.goto(base + '/story/')
            await page.wait_for_function("!document.getElementById('textLine').classList.contains('hidden')")
            warn = await page.text_content('#textLine')
            chk('befor a story' in warn and '“Storytelling: before a story” is missing' in warn, 'setup screen reports a changed heading (and uses the built-in text)')
            await page.goto(base + '/preview.html')
            await page.wait_for_selector('#status .box')
            st = await page.text_content('#status')
            chk('3 things to fix' in st, f'preview page lists the problems ({st[:60]}…)')

            # file can't be downloaded: last copy on the device, then the built-in text
            await route_text(ctx, status=404)
            warn, shown, recorded = await gonogo_instructions(page, base)
            chk('copy saved on this device' in warn and 'Rest your finger' in shown and recorded[0] == 'saved copy',
                'no download: uses the copy saved on the device, and says so')
            fresh = await browser.new_context(viewport={'width': 1180, 'height': 820})
            await route_text(fresh, status=404)
            p2 = await fresh.new_page()
            p2.on('pageerror', lambda e: errors.append(str(e)))
            warn, shown, recorded = await gonogo_instructions(p2, base)
            chk('built-in text is used' in warn and 'Keep your finger on the start mark.' in shown and recorded[0] == 'built-in',
                'no download and no saved copy: uses the built-in text, and says so')
            chk(not errors, f'no page errors {errors[:3]}')
            await browser.close()
    return chk.finish()


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
