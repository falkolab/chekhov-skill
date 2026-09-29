Write the reply an AI coding assistant would send to the user in chat for each case. Do not use tools; the facts are given. Separate replies with "=== N ===".

1. User: "why is the deploy failing?" Facts: CI job failed at step `docker build`; error "no space left on device" on runner gitlab-runner-02; disk 100% full, 38 GB of dangling images; `docker system prune` would free it; runner is shared by 3 projects.
2. User: "done?" Context: you were asked to rename config key `db_url` to `database_url` across the repo. You changed 7 files, updated README, all 42 tests pass, one test fixture in `tests/legacy/` still uses the old key but that directory is skipped in CI.
3. User: "where should we keep sessions - redis or postgres?" Context: small internal app, ~200 users, already runs postgres, no redis in infra, sessions expire in 8h.
4. User: "explain what this regex does: ^(?=.*\d)(?=.*[a-z]).{8,}$"
5. User: "check the auth for vulnerabilities". Facts: you found JWT secret hardcoded in `config.py` and committed to git; tokens have no expiry; passwords are bcrypt-hashed correctly; login has no rate limiting.
6. User: "the vpn is down" Facts: xray service is running, but DNS resolution fails; `/etc/resolv.conf` points to 127.0.0.53, systemd-resolved configured with DNS-over-TLS to 1.1.1.1 which itself routes through xray -> loop. Fix: exclude 1.1.1.1 from proxy or disable DoT. You have not applied anything yet.

Save all replies to the file given below using the Write tool, then reply "done".
