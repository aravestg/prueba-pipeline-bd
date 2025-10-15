#!/usr/bin/env python3
import sys, re, pathlib
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "db")

viol = []
for p in ROOT.rglob("*.sql"):
    t = p.read_text(encoding="utf-8", errors="ignore")
    if re.search(r"\b(create|drop)\s+database\b", t, re.I):
        viol.append((p, "Evita CREATE/DROP DATABASE"))
    if re.search(r"\btruncate\s+table\b", t, re.I) and "/* approved-truncate */" not in t.lower():
        viol.append((p, "TRUNCATE requiere /* approved-truncate */"))
if viol:
    for p,m in viol:
        print(f"- {p}: {m}")
    sys.exit(1)
print("Lint OK")
