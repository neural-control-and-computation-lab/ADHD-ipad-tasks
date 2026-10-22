"""Shared helpers for the browser tests: serve the repo locally and report checks."""
import contextlib, csv, functools, http.server, io, pathlib, socketserver, threading

REPO = pathlib.Path(__file__).resolve().parent.parent


@contextlib.contextmanager
def serve_repo():
    """Serve the repository root on a free localhost port; yields the base URL."""
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    handler = functools.partial(Quiet, directory=str(REPO))
    with socketserver.TCPServer(('127.0.0.1', 0), handler) as httpd:
        t = threading.Thread(target=httpd.serve_forever, daemon=True)
        t.start()
        try:
            yield f'http://127.0.0.1:{httpd.server_address[1]}'
        finally:
            httpd.shutdown()


def parse_csv(text):
    """Read a task CSV, skipping the '#' header lines."""
    return list(csv.DictReader(io.StringIO('\n'.join(l for l in text.splitlines() if not l.startswith('#')))))


class Checks:
    def __init__(self):
        self.failed = 0

    def __call__(self, cond, msg):
        print(('PASS ' if cond else 'FAIL ') + msg)
        if not cond:
            self.failed += 1

    def finish(self):
        print('OVERALL', 'PASS' if not self.failed else f'FAIL ({self.failed} failed)')
        return 0 if not self.failed else 1
