# Testing methodology

## Harnesses

**Synthetic** (`evals/synthetic/`). Facts are given in the prompt; a subagent writes one reply per case, with and without the skill. Use it for quick wording checks and ablations. It does not reflect real use: the agent writes with the rules in front of it, in one focused pass.

**Live** (`evals/live/`). Real headless Claude Code sessions: `claude -p`, follow-ups via `--resume`. The style is requested only in the first message, so triggering is tested too. Use it to accept a change.

```bash
cd evals/live
python3 run_cli.py <workdir> s1 skill            # style requested in message 1
python3 run_cli.py <workdir> b1 base             # baseline
python3 run_cli.py <workdir> s2 skill --lang ru  # non-English conversation
python3 trigger_cli.py <workdir> 10 --lang en    # trigger rate over 10 fresh sessions
```

Each `<label>.json` holds, per turn, the reply, Skill calls and Edit/Write calls. Edits are allowed on purpose, so an unasked edit shows up in the log. Sessions use your normal Claude Code config.

On a subscription the runs consume usage limits. `total_cost_usd` in the CLI output is an API-price estimate.

## What to check

Against `evals/live/expected.md`, per reply:

- the first sentence is the answer, and the cause is stated;
- nothing is changed without being asked;
- the reply ends with the next step as a question;
- the mechanism is kept when the user asked to explain;
- each finding has its fix, with an order of work when there are several;
- no invented dates, versions or tool behaviour;
- no recap of earlier tasks;
- word count, skill vs baseline.

## Rules

- Run at least 3 sessions with the skill and 1-2 without. A single difference is noise.
- Keep tuning cases and checking cases separate. The cases here have been used for tuning; write new ones to check a change.
- Keep examples in `SKILL.md` disjoint from every test case, or the agent copies them and passes.
- Rules must say how to open, what to include and how to close. The reply is generated in one pass, so "delete X afterwards" does nothing.
- If rewording a rule twice does not move a result, the wording is not the lever.
- Brevity rules can cause fabrication. A hedge on an unchecked fact is not filler.
- Validate a harness against real use before trusting its numbers. Subagent-based live runs showed recaps and flaky triggering that real sessions do not.
