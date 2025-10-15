#!/usr/bin/env python3
import sys, pathlib
root = pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "db/migrations")

errors = []
for change in root.iterdir():
    if not change.is_dir():
        continue
    inst = change / "install"
    roll = change / "rollback"
    if not inst.is_dir():
        errors.append(f"{change}: falta carpeta install/")
    if not roll.is_dir():
        errors.append(f"{change}: falta carpeta rollback/")
    # al menos un .sql en install
    if inst.is_dir() and not any(inst.glob("*.sql")):
        errors.append(f"{change}: install/ sin .sql")
    if roll.is_dir() and not any(roll.glob("*.sql")):
        errors.append(f"{change}: rollback/ sin .sql")
if errors:
    print("Errores de estructura:")
    for e in errors: print("-", e)
    sys.exit(1)
print("Estructura install/rollback OK")
