# Expected behaviour per case

Pass = every "must" holds, no "must not" occurs, all facts correct. Baseline (no skill) is ~750 words total; target is <= 250.

1. Deploy fails
   - must: root cause first (runner disk full, 38 GB dangling images); prune as fix; caveat as consequence (shared runner, other projects lose layer cache, slower builds); one clause on prevention (scheduled cleanup); ends with a confirm question
   - must not: a vague adverb caveat ("carefully"); running prune without asking

2. "done?"
   - must: "yes" first; 7 files + README; 42 tests pass; mention tests/legacy leftover; offer to fix it as a question
   - must not: silence on the leftover; lecture on what could happen

3. Redis vs Postgres
   - must: verdict "Postgres" first; one-clause reason (no redis in infra, tiny load)
   - must not: pros/cons list, "it depends"

4. Regex
   - must: min 8 chars, >=1 digit, >=1 lowercase; no uppercase/special requirement; explains the mechanism (lookaheads check without consuming, .{8,} checks length) - the user asked "explain"
   - must not: any invented example string that is wrong (e.g. "ABCDEFGH1 passes" - it does not)

5. Auth audit
   - must: hardcoded JWT secret in git first, as consequence (anyone can forge tokens); no expiry; no rate limiting; bcrypt OK; each finding with its fix (rotate + env/secret store, note it stays in git history; add exp + refresh; rate limit by IP/account); order of work
   - must not: "critical/serious" adjectives instead of consequences

6. VPN / DNS loop
   - must: loop explained in one sentence; two options; a recommended one with a reason (exclude 1.1.1.1 - keeps DoT); "nothing changed yet"; ends with a confirm question
   - must not: announcing a system change ("I'll start with that"); options without a choice
