#!/usr/bin/env python3
"""Count how often the skill loads from the first message alone, over n fresh sessions."""
import argparse, json, subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from run_cli import HERE, MESSAGES, STYLE


def one(i, workdir, msg, model):
    repo = workdir / f"t{i}"
    if not repo.exists():
        subprocess.run(["cp", "-R", str(HERE / "shop"), str(repo)], check=True)
    out = subprocess.run(["claude", "-p", msg, "--model", model, "--output-format", "stream-json",
                          "--verbose", "--max-turns", "3", "--allowedTools", "Read", "Glob", "Grep", "Skill"],
                         cwd=repo, capture_output=True, text=True, timeout=600).stdout
    skills = []
    for line in out.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "assistant":
            skills += [c["input"].get("skill") for c in ev["message"].get("content", [])
                       if c.get("type") == "tool_use" and c["name"] == "Skill"]
    return skills


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir", type=Path)
    ap.add_argument("n", type=int)
    ap.add_argument("--lang", choices=list(MESSAGES), default="en")
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--parallel", type=int, default=5)
    a = ap.parse_args()

    a.workdir.mkdir(parents=True, exist_ok=True)
    msg = STYLE[a.lang] + MESSAGES[a.lang][0]
    with ThreadPoolExecutor(a.parallel) as ex:
        runs = list(ex.map(lambda i: one(i, a.workdir, msg, a.model), range(a.n)))
    print(json.dumps({"n": a.n, "lang": a.lang, "loaded": sum("chekhov" in r for r in runs)}))


if __name__ == "__main__":
    main()
