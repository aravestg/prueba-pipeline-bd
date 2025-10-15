#!/usr/bin/env python3
import sys, re, pathlib

RAIZ = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "db/migrations")
errores = []

for sql in RAIZ.rglob("*.sql"):
    texto = sql.read_text(encoding="utf-8", errors="ignore")
    ruta  = str(sql).lower()
    es_rollback = ("/rollback/" in ruta) or bool(re.search(r"\.down\.sql$", sql.name, re.I))

    # TRUNCATE: siempre exige comentario explícito
    if re.search(r"\btruncate\s+table\b", texto, re.I):
        if "/* approved-truncate */" not in texto.lower():
            errores.append((sql, "TRUNCATE sin '/* approved-truncate */'"))

    # DROP: permitido SOLO en rollback
    reglas_drop = [
        (r"\bdrop\s+table\b",     "DROP TABLE"),
        (r"\bdrop\s+index\b",     "DROP INDEX"),
        (r"\bdrop\s+procedure\b", "DROP PROCEDURE"),
        (r"\bdrop\s+function\b",  "DROP FUNCTION"),
        (r"\bdrop\s+trigger\b",   "DROP TRIGGER"),
        (r"\bdrop\s+view\b",      "DROP VIEW"),
    ]
    for rx, etiqueta in reglas_drop:
        if re.search(rx, texto, re.I) and not es_rollback:
            errores.append((sql, f"{etiqueta} solo permitido en rollback/"))

    # ALTER ... DROP COLUMN: incluso en rollback requiere comentario
    if re.search(r"\balter\s+table\s+\w+\s+drop\s+column\b", texto, re.I):
        if not es_rollback or "/* approved-alter-drop */" not in texto.lower():
            errores.append((sql, "ALTER DROP COLUMN requiere rollback y '/* approved-alter-drop */'"))

if errores:
    print("Statements de riesgo detectados:")
    for f, msg in errores:
        print(f"- {f}: {msg}")
    sys.exit(1)
else:
    print("Cheques de riesgo: OK")
