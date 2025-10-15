#!/usr/bin/env python3
import sys, re, pathlib
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "db/migrations")
bad=[]
rules=[(r"\bdrop\s+table\b","DROP TABLE"),
       (r"\balter\s+table\s+\w+\s+drop\s+column\b","ALTER DROP COLUMN"),
       (r"\bdrop\s+(procedure|function|trigger|view)\b","DROP objeto")]
for p in ROOT.rglob("*.sql"):
    t=p.read_text(encoding="utf-8",errors="ignore")
    for rx,label in rules:
        if re.search(rx,t,re.I): bad.append((p,label))
if bad:
    for f,l in bad: print(f"- {f}: {l}")
    sys.exit(1)
print("Riesgos: OK")
