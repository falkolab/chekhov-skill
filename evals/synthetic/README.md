# Synthetic eval

Six cases with the facts given in the prompt. Fast, but far from real use - see ../../METHODOLOGY.md.

Run two subagents on `cases.md`: one plain, one told to read `../../skill/SKILL.md` first. Each writes its replies to a file, separated by `=== N ===`. Compare against `expected.md` and count words per case.
