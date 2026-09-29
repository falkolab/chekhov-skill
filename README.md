# chekhov-skill

A Claude Code skill that makes the agent write its chat messages the way Chekhov edited prose: the answer first, only details that matter, the next step last, no filler. It changes how the agent writes, not what it does. Replies stay in the user's language.

Triggered by asking for replies "like Chekhov" or "Chekhov-style", in any language.

## Install

```bash
git clone https://github.com/falkolab/chekhov-skill.git
ln -s "$(pwd)/chekhov-skill/skill" ~/.claude/skills/chekhov
```

Only `skill/` is linked, so the evals never reach an agent's context.

## Keep it on

By default the skill loads when asked. Two ways to make it permanent:

**CLAUDE.md line** - simplest. Add to `./CLAUDE.md` for one project or `~/.claude/CLAUDE.md` for the whole machine:

```
Reply like Chekhov in every message: load the chekhov skill at the start of the session.
```

The skill loads at the start of each session (3/3 in a test). CLAUDE.md survives compaction; the skill text itself may be summarized away in a very long session.

**Output style** - strongest. The text goes into the system prompt of every request and survives compaction. Generate it from the skill (for one project use `.claude/output-styles/` instead):

```bash
mkdir -p ~/.claude/output-styles
{ printf -- '---\nname: Chekhov\ndescription: Terse replies the way Chekhov edited prose\nkeep-coding-instructions: true\n---\n'
  awk 'f>=2{print} /^---$/{f++}' skill/SKILL.md; } > ~/.claude/output-styles/chekhov.md
```

Turn it on with `/config` -> Output style -> Chekhov, or `"outputStyle": "Chekhov"` in `~/.claude/settings.json` (project: `.claude/settings.local.json`). It replaces any other output style, and it is a copy: rerun the command after updating the skill.

## Layout

- `skill/SKILL.md` - the skill.
- `evals/synthetic/` - facts-in, reply-out cases for quick wording checks.
- `evals/live/` - a sandbox repo and scripts that run real headless Claude Code sessions.
- `METHODOLOGY.md` - how to test a change.

## Measured behaviour

Sonnet, English. Claude Code: headless sessions on `evals/live`, 3 with the skill and 2 without, 4 messages each. Plain chat: the six `evals/synthetic` cases, one run each way.

| | skill | baseline |
|---|---|---|
| skill loads from the first message | 9/10 en, 10/10 ru | - |
| edits files without being asked | 0/12 replies | 5/8 |
| ends with the next step as a question | 10/12 | 4/8 |
| words per session, Claude Code | 187-264, mean 218 | 300-427, mean 364 |
| words for six cases, plain chat | 259 | 810 |

Replies are about 1.7x shorter inside Claude Code, whose system prompt already keeps baseline replies brief, and about 3x shorter in a plain chat setting.

## Changing the skill

1. The scope is brevity. Add a rule only when a brevity rule causes a degradation, and then fix that rule instead of adding a new one.
2. Examples drive behaviour more than rules. When behaviour is wrong, check the examples first.
3. Examples must not overlap any test case.
4. Check a change on new cases, with the live harness, several sessions, and a baseline. See `METHODOLOGY.md`.

## You might also like

[agent-mail-skill](https://github.com/falkolab/agent-mail-skill) — a Claude Code skill for file-based mail between agents across repositories, worktrees and sessions.

## License

MIT

## Author

Andrei Tkachenko, Telegram channel "Automate It" (Rus): [@aitomateit](https://t.me/aitomateit)
