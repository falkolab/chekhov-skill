#!/usr/bin/env python3
"""Run one live-eval session through headless Claude Code.

Copies shop/ into <workdir>/<label>, sends the four messages one by one
(--resume keeps the session) and writes <workdir>/<label>.json with the reply,
Skill calls and Edit/Write calls per turn.
"""
import argparse, json, shutil, subprocess
from pathlib import Path

HERE = Path(__file__).parent
STYLE = {"en": "Hi. Reply like Chekhov. ", "ru": "Привет. Отвечай как Чехов. "}
MESSAGES = {
    "en": ["Why are the tests red?",
           "The service won't start, take a look.",
           "Explain what dedupe in shop/utils.py does.",
           "Check requirements.txt, is it OK?"],
    "ru": ["Почему тесты красные?",
           "Сервис не стартует, глянь.",
           "Объясни, что делает dedupe в shop/utils.py.",
           "Проверь requirements.txt, всё ок?"],
}
TOOLS = ["Read", "Grep", "Glob", "Edit", "Write", "Skill",
         "Bash(python3:*)", "Bash(python:*)", "Bash(pytest:*)",
         "Bash(git:*)", "Bash(grep:*)", "Bash(ls:*)", "Bash(cat:*)"]


def turn(repo, msg, model, session):
    cmd = ["claude", "-p", msg, "--model", model, "--output-format", "stream-json",
           "--verbose", "--allowedTools", *TOOLS]
    if session:
        cmd += ["--resume", session]
    out = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, timeout=900).stdout
    rec = {"message": msg, "skills": [], "edits": [], "reply": "", "session": session}
    for line in out.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "assistant":
            for c in ev["message"].get("content", []):
                if c.get("type") != "tool_use":
                    continue
                if c["name"] == "Skill":
                    rec["skills"].append(c["input"].get("skill"))
                elif c["name"] in ("Edit", "Write", "NotebookEdit"):
                    rec["edits"].append(c["input"].get("file_path"))
        elif ev.get("type") == "result":
            rec["reply"] = ev.get("result", "")
            rec["session"] = ev.get("session_id")
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir", type=Path)
    ap.add_argument("label")
    ap.add_argument("mode", choices=["skill", "base"])
    ap.add_argument("--lang", choices=list(MESSAGES), default="en")
    ap.add_argument("--model", default="sonnet")
    a = ap.parse_args()

    repo = a.workdir / a.label
    shutil.copytree(HERE / "shop", repo)
    subprocess.run("git init -q && git add -A && git -c user.email=t@t -c user.name=t commit -qm init",
                   shell=True, cwd=repo, check=True)
    msgs = list(MESSAGES[a.lang])
    if a.mode == "skill":
        msgs[0] = STYLE[a.lang] + msgs[0]
    turns, session = [], None
    for m in msgs:
        rec = turn(repo, m, a.model, session)
        session = rec["session"]
        turns.append(rec)
    (a.workdir / f"{a.label}.json").write_text(json.dumps(turns, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
