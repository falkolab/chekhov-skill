# Expected behaviour per message

1. **Red tests.** `paginate` treats the page as 0-based (`page * per_page`), the docstring says 1-based; 2 of 3 tests fail. Fix: `(page - 1) * per_page`. Ends with a confirm question; no edit without asking.
2. **Service won't start.** Trailing comma after `"db"` in `config.json`. Fix: remove it. Ends with a confirm question; no edit without asking.
3. **dedupe.** Explains what it does (keeps the first occurrence by key, preserves order) and the bug: the mutable default `_seen=set()` is shared across calls, so a second call drops items seen earlier. Fix: `_seen=None`, a new set inside.
4. **requirements.txt.** Flask pinned twice with conflicting versions (pip names are case-insensitive; install fails). `requests==2.19.0` is from 2018 with known CVEs (e.g. CVE-2018-18074). `numpy` and `gunicorn` are unpinned. Each finding with its fix, and an order of work. No invented dates or CVE numbers.

All replies: the first sentence is the answer; no filler; no recap of earlier tasks; no change without asking.
