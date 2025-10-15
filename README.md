# Monorepo DB — Esqueleto alineado al *Manual Oficial de Políticas de Gestión de Cambios en Bases de Datos*

## Estructura
```
/db/schema/OWNER/{tablas|vistas|sps|funciones|triggers|indices|grants|sinonimos}
/db/migrations/<US-XXXX-nombre>/{install,rollback}
/db/metadata/           # datos inmutables (catálogos/config)
```

### Política
- `/db/schema`: **fuente de verdad** (estado final). 1 archivo CREATE (o REPLACE si el motor lo soporta) por objeto.
- `/db/migrations/<US-XXXX>`: cambio atómico con **carpetas `install` y `rollback`**.
- `/db/metadata`: scripts de datos **inmutables**. Para instalación inicial, también se incluyen en `/db/migrations/<US-XXXX>/install`.

## Flujos
- **feature/** → PR a **staging** (Squash & Merge). CI valida (lint, pares install/rollback, detecta riesgos).
- Al **merge en staging** se crea un **tag**: `PAP-<rama>-<sha7>`.
- En **rama `PAP-XXXX`**, un workflow empaqueta la carpeta del cambio en `.zip` (install + rollback) como *artifact*.
- El responsable hace `git cherry-pick <tag>` hacia `PAP-XXXX` y distribuye el paquete.

> Este esqueleto incluye Workflows y scripts *stub* para automatizar lo anterior.
