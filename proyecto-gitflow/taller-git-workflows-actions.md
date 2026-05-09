# 🚀 Taller Avanzado: Git Workflows, Branch Policies, Environments y GitHub Actions

**Institución:** IU Digital de Antioquia  
**Instructora:** Darkanita  
**Nivel:** Básico–Intermedio  
**Duración estimada:** 4–5 horas  
**Prerrequisitos:** Haber completado el Taller de Git y GitHub (o tener conocimientos equivalentes)

---

## 📋 Tabla de Contenidos

1. [Git Workflows: Estrategias de ramificación](#1-git-workflows-estrategias-de-ramificación)
2. [Gitflow en la práctica](#2-gitflow-en-la-práctica)
3. [GitHub Flow: El flujo simplificado](#3-github-flow-el-flujo-simplificado)
4. [Trunk-Based Development](#4-trunk-based-development)
5. [Branch Policies y protección de ramas](#5-branch-policies-y-protección-de-ramas)
6. [Environments: Dev, Staging y Producción](#6-environments-dev-staging-y-producción)
7. [GitHub Actions: Introducción a CI/CD](#7-github-actions-introducción-a-cicd)
8. [Primer workflow: Lint y Tests automáticos](#8-primer-workflow-lint-y-tests-automáticos)
9. [Deploy automático a ambientes](#9-deploy-automático-a-ambientes)
10. [Workflows avanzados: Matrix, Secrets y Artifacts](#10-workflows-avanzados-matrix-secrets-y-artifacts)
11. [Ejercicio integrador final](#11-ejercicio-integrador-final)
12. [Cheat Sheet de Workflows y Actions](#12-cheat-sheet-de-workflows-y-actions)

---

## 1. Git Workflows: Estrategias de ramificación

### Teoría

Un **Git Workflow** es un conjunto de reglas y convenciones que define cómo un equipo usa ramas para organizar el desarrollo. No hay un workflow "perfecto"; cada uno se adapta a distintos contextos.

### Los tres workflows más populares

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  GITFLOW               GITHUB FLOW           TRUNK-BASED               │
│                                                                         │
│  main ─────────────    main ─────────────    main ─────────────         │
│    │                     │                     │                         │
│  develop ──────────      │                     │                         │
│    │    \    /           │                     │                         │
│  feature  release      feature               feature (corta)           │
│    │        │            │                     │                         │
│  hotfix     │            └── PR → main         └── PR → main            │
│             │                                                           │
│                                                                         │
│  Equipos grandes       Equipos medianos      Equipos con CI/CD          │
│  Releases planificados Deploy continuo       Deploy continuo            │
│  Múltiples versiones   Simplicidad           Feature flags              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

| Workflow | Ramas principales | Mejor para | Complejidad |
|---|---|---|---|
| **Gitflow** | `main`, `develop`, `feature/*`, `release/*`, `hotfix/*` | Releases planificados, versiones múltiples | Alta |
| **GitHub Flow** | `main`, `feature/*` | Deploy continuo, equipos medianos | Baja |
| **Trunk-Based** | `main`, ramas muy cortas | CI/CD maduro, feature flags | Muy baja |

---

## 2. Gitflow en la práctica

### Teoría

Gitflow usa dos ramas permanentes (`main` y `develop`) y tres tipos de ramas temporales:

```
main:     v1.0 ──────────────────────── v1.1 ──────── v1.2
            │                             ▲               ▲
            │                             │               │
develop:    └── A ── B ── C ── D ── E ── F ── G ── H ── I
                      \       /       \       /
feature/login:         X ── Y         │      │
                                      │      │
release/1.1:                          R₁ ── R₂
                                               \
hotfix/1.2:                                     H₁ (fix urgente en main)
```

- **main:** solo contiene código en producción. Cada commit es una versión.
- **develop:** rama de integración donde se juntan las features.
- **feature/\*:** una por funcionalidad, nace de `develop`, se fusiona a `develop`.
- **release/\*:** preparación para producción (últimos ajustes, docs, versión).
- **hotfix/\*:** correcciones urgentes en producción, nacen de `main`.

### 🧪 Ejercicio 1: Simular Gitflow completo

```bash
# ══════════════════════════════════════════════
# PASO 1: Crear el proyecto e inicializar Gitflow
# ══════════════════════════════════════════════
mkdir proyecto-gitflow
cd proyecto-gitflow
git init

# Crear archivo inicial en main
cat > app.py << 'EOF'
"""
Mi Aplicación - v1.0
IU Digital de Antioquia
"""

def main():
    print("Bienvenido a Mi Aplicación v1.0")

if __name__ == "__main__":
    main()
EOF

cat > README.md << 'EOF'
# Mi Aplicación

Proyecto de ejemplo para aprender Gitflow.

## Versión actual: 1.0
EOF

git add .
git commit -m "feat: crear proyecto inicial v1.0"

# Etiquetar la versión 1.0
git tag -a v1.0 -m "Release v1.0 - versión inicial"

# ══════════════════════════════════════════════
# PASO 2: Crear la rama develop
# ══════════════════════════════════════════════
git checkout -b develop

# ══════════════════════════════════════════════
# PASO 3: Trabajar en una feature (desde develop)
# ══════════════════════════════════════════════
git checkout -b feature/modulo-usuarios

cat > usuarios.py << 'EOF'
"""Módulo de gestión de usuarios."""

class Usuario:
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo

    def __str__(self):
        return f"{self.nombre} ({self.correo})"

def listar_usuarios(usuarios):
    """Muestra la lista de usuarios registrados."""
    for i, u in enumerate(usuarios, 1):
        print(f"  {i}. {u}")
EOF

git add usuarios.py
git commit -m "feat: agregar módulo de gestión de usuarios"

# Agregar integración en app.py
cat > app.py << 'EOF'
"""
Mi Aplicación - v1.0
IU Digital de Antioquia
"""
from usuarios import Usuario, listar_usuarios

def main():
    print("Bienvenido a Mi Aplicación")
    usuarios = [
        Usuario("Ana", "ana@correo.com"),
        Usuario("Carlos", "carlos@correo.com"),
    ]
    print("\nUsuarios registrados:")
    listar_usuarios(usuarios)

if __name__ == "__main__":
    main()
EOF

git add app.py
git commit -m "feat: integrar módulo de usuarios en app principal"

# ══════════════════════════════════════════════
# PASO 4: Fusionar feature a develop
# ══════════════════════════════════════════════
git checkout develop
git merge --no-ff feature/modulo-usuarios -m "merge: integrar feature/modulo-usuarios a develop"
git branch -d feature/modulo-usuarios

# ══════════════════════════════════════════════
# PASO 5: Crear una release (desde develop)
# ══════════════════════════════════════════════
git checkout -b release/1.1

# Ajustes finales de la release
cat > CHANGELOG.md << 'EOF'
# Changelog

## v1.1 - $(date +%Y-%m-%d)
### Nuevas funcionalidades
- Módulo de gestión de usuarios
- Listado de usuarios registrados

## v1.0
- Versión inicial de la aplicación
EOF

# Actualizar versión en README
sed -i 's/Versión actual: 1.0/Versión actual: 1.1/' README.md 2>/dev/null || \
  sed 's/Versión actual: 1.0/Versión actual: 1.1/' README.md > README.tmp && mv README.tmp README.md

git add .
git commit -m "chore: preparar release 1.1"

# ══════════════════════════════════════════════
# PASO 6: Fusionar release a main Y a develop
# ══════════════════════════════════════════════

# Fusionar a main
git checkout main
git merge --no-ff release/1.1 -m "merge: release 1.1 a main"
git tag -a v1.1 -m "Release v1.1 - módulo de usuarios"

# Fusionar a develop también
git checkout develop
git merge --no-ff release/1.1 -m "merge: release 1.1 a develop"

# Eliminar la rama de release
git branch -d release/1.1

# ══════════════════════════════════════════════
# PASO 7: Simular un Hotfix (desde main)
# ══════════════════════════════════════════════
git checkout main
git checkout -b hotfix/fix-saludo

# Corregir un "bug" en producción
sed -i 's/Bienvenido a Mi Aplicación/Bienvenido a Mi Aplicación v1.1/' app.py 2>/dev/null || \
  sed 's/Bienvenido a Mi Aplicación/Bienvenido a Mi Aplicación v1.1/' app.py > app.tmp && mv app.tmp app.py

git add app.py
git commit -m "fix: corregir mensaje de bienvenida con versión"

# Fusionar hotfix a main
git checkout main
git merge --no-ff hotfix/fix-saludo -m "merge: hotfix fix-saludo a main"
git tag -a v1.1.1 -m "Hotfix v1.1.1 - corregir saludo"

# Fusionar hotfix a develop también
git checkout develop
git merge --no-ff hotfix/fix-saludo -m "merge: hotfix fix-saludo a develop"

git branch -d hotfix/fix-saludo

# ══════════════════════════════════════════════
# PASO 8: Ver el resultado final
# ══════════════════════════════════════════════
echo ""
echo "═══ Historial completo ═══"
git log --oneline --graph --all

echo ""
echo "═══ Tags (versiones) ═══"
git tag -l
```

### 🤔 Reflexión

Después de ejecutar el ejercicio, responde:

1. ¿De qué rama nace una feature? ¿A cuál se fusiona?
2. ¿Por qué el hotfix se fusiona tanto a `main` como a `develop`?
3. ¿Qué pasaría si olvidas fusionar el hotfix a `develop`?

---

## 3. GitHub Flow: El flujo simplificado

### Teoría

GitHub Flow es mucho más sencillo: solo hay una rama permanente (`main`) y ramas temporales por feature. Cada cambio pasa por un Pull Request antes de llegar a `main`.

```
main:         A ── B ── C ────── D (merge PR) ── E ────── F (merge PR)
                          \     ▲                  \     ▲
feature/login:             X ── Y                   │    │
                                                    │    │
fix/bug-404:                                        Z ── W
```

**Reglas de GitHub Flow:**

1. `main` siempre está en estado desplegable (deployable).
2. Para cualquier cambio, crea una rama descriptiva desde `main`.
3. Haz commits frecuentes y haz push a tu rama.
4. Abre un Pull Request para discusión y revisión.
5. Después de la revisión, fusiona a `main`.
6. Despliega inmediatamente después del merge.

### 🧪 Ejercicio 2: Practicar GitHub Flow

```bash
# ══════════════════════════════════════════════
# PASO 1: Crear un nuevo proyecto
# ══════════════════════════════════════════════
mkdir proyecto-github-flow
cd proyecto-github-flow
git init

cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Mi App</title>
</head>
<body>
    <h1>Bienvenido</h1>
    <p>Aplicación de ejemplo - GitHub Flow</p>
</body>
</html>
EOF

git add .
git commit -m "feat: crear página inicial"

# ══════════════════════════════════════════════
# PASO 2: Feature 1 - Agregar navegación
# ══════════════════════════════════════════════
git checkout -b feature/agregar-nav

cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Mi App</title>
</head>
<body>
    <nav>
        <a href="/">Inicio</a>
        <a href="/about">Acerca de</a>
        <a href="/contact">Contacto</a>
    </nav>
    <h1>Bienvenido</h1>
    <p>Aplicación de ejemplo - GitHub Flow</p>
</body>
</html>
EOF

git add .
git commit -m "feat: agregar barra de navegación"

# Simular el merge vía PR (en real sería desde GitHub)
git checkout main
git merge --no-ff feature/agregar-nav -m "merge: PR #1 - agregar navegación"
git branch -d feature/agregar-nav

# ══════════════════════════════════════════════
# PASO 3: Feature 2 - Agregar footer
# ══════════════════════════════════════════════
git checkout -b feature/agregar-footer

cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Mi App</title>
</head>
<body>
    <nav>
        <a href="/">Inicio</a>
        <a href="/about">Acerca de</a>
        <a href="/contact">Contacto</a>
    </nav>
    <h1>Bienvenido</h1>
    <p>Aplicación de ejemplo - GitHub Flow</p>
    <footer>
        <p>&copy; 2026 - IU Digital de Antioquia</p>
    </footer>
</body>
</html>
EOF

git add .
git commit -m "feat: agregar footer con copyright"

git checkout main
git merge --no-ff feature/agregar-footer -m "merge: PR #2 - agregar footer"
git branch -d feature/agregar-footer

# Ver resultado
git log --oneline --graph --all
```

---

## 4. Trunk-Based Development

### Teoría

En Trunk-Based Development el equipo trabaja directamente sobre `main` (el "trunk") o con ramas extremadamente cortas (máximo 1–2 días). Se apoya fuertemente en **CI/CD** y **feature flags** para controlar qué funcionalidades están activas.

```
main:    A ── B ── C ── D ── E ── F ── G ── H     (todos los commits)
               \  /         \  /
short-lived:    X             Y                     (ramas de horas, no días)
```

**¿Cuándo usarlo?**

- Equipos con CI/CD maduro y buena cobertura de tests.
- Deploy múltiples veces al día.
- Se usan feature flags para activar/desactivar funcionalidades.

### Feature Flags: El concepto

```python
# Ejemplo simple de feature flag
FEATURE_FLAGS = {
    "nuevo_dashboard": False,   # Desactivado en producción
    "exportar_pdf": True,       # Activo para todos
}

def mostrar_dashboard():
    if FEATURE_FLAGS["nuevo_dashboard"]:
        return render_nuevo_dashboard()
    else:
        return render_dashboard_clasico()
```

Esto permite hacer merge a `main` sin que los usuarios vean funcionalidades incompletas.

### 🤔 Reflexión

¿Cuál workflow elegirías para cada escenario?

| Escenario | Tu respuesta |
|---|---|
| App móvil con releases cada 2 semanas | |
| Sitio web que se actualiza 5 veces al día | |
| Librería open-source con versiones 1.x, 2.x y 3.x | |
| Proyecto universitario de 3 personas | |

---

## 5. Branch Policies y protección de ramas

### Teoría

Las **Branch Policies** (políticas de rama) son reglas que se configuran en GitHub para proteger ramas importantes, especialmente `main`. Evitan que alguien pueda hacer push directamente sin revisión.

### Políticas más comunes

| Política | Qué hace | ¿Para qué sirve? |
|---|---|---|
| **Require pull request** | Obliga a pasar por PR antes de merge | Asegurar revisión de código |
| **Require approvals** | Necesita N aprobaciones de revisores | Validación por pares |
| **Require status checks** | Los tests/CI deben pasar antes de merge | No romper el código |
| **Require signed commits** | Solo commits firmados | Verificar autoría |
| **Restrict push access** | Solo ciertos usuarios pueden hacer push | Control de acceso |
| **Require linear history** | No se permiten merge commits | Historial limpio |
| **Lock branch** | Rama de solo lectura | Proteger releases |

### 🧪 Ejercicio 3: Configurar Branch Protection en GitHub

**Este ejercicio se realiza en la interfaz web de GitHub:**

1. Ve a tu repositorio en GitHub.
2. Haz clic en **Settings** → **Branches** (menú lateral).
3. En "Branch protection rules", haz clic en **"Add branch protection rule"**.
4. En "Branch name pattern", escribe: `main`
5. Activa las siguientes opciones:

```
☑ Require a pull request before merging
    ☑ Require approvals (1)
    ☑ Dismiss stale pull request approvals when new commits are pushed

☑ Require status checks to pass before merging
    ☑ Require branches to be up to date before merging

☑ Do not allow bypassing the above settings
```

6. Haz clic en **"Create"**.

### Verificar que funciona

```bash
# Intenta hacer push directo a main (debería fallar)
echo "cambio directo" >> README.md
git add .
git commit -m "test: intentar push directo"
git push origin main
# ❌ Error: protected branch - changes must be made through a pull request
```

### El flujo correcto con protecciones activas

```bash
# 1. Crear rama
git checkout -b feature/mi-cambio

# 2. Hacer cambios y commits
echo "nuevo contenido" >> archivo.txt
git add .
git commit -m "feat: agregar nuevo contenido"

# 3. Push de la rama (NO de main)
git push origin feature/mi-cambio

# 4. Ir a GitHub y abrir Pull Request
# 5. Esperar aprobación y que pasen los checks
# 6. Merge desde la interfaz de GitHub

# 7. Actualizar tu main local
git checkout main
git pull origin main
```

---

## 6. Environments: Dev, Staging y Producción

### Teoría

Los **Environments** (ambientes) son etapas por las que pasa tu código antes de llegar a los usuarios finales. Cada ambiente tiene un propósito diferente:

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│   LOCAL          DEV            STAGING         PRODUCCIÓN         │
│   (tu PC)       (compartido)   (pre-prod)      (usuarios)         │
│                                                                    │
│   Desarrollo    Integración    Pruebas          Release            │
│   individual    del equipo     finales          al público         │
│                                                                    │
│   feature/*  →  develop     →  release/*     →  main               │
│                                                                    │
│   Tu código     ¿Funciona      ¿Funciona        ¡En vivo!          │
│   funciona?     con todo?      como en prod?                       │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

| Ambiente | Rama asociada | Propósito | ¿Quién lo usa? |
|---|---|---|---|
| **Development** | `develop` o `feature/*` | Integración temprana, pruebas rápidas | Desarrolladores |
| **Staging** | `release/*` o `staging` | Réplica de producción para pruebas finales | QA, Product Owner |
| **Production** | `main` | La versión que ven los usuarios reales | Usuarios finales |

### Configurar Environments en GitHub

**En la interfaz de GitHub:**

1. Ve a **Settings** → **Environments**.
2. Haz clic en **"New environment"**.
3. Crea tres ambientes:

| Nombre | Configuración recomendada |
|---|---|
| `development` | Sin restricciones (deploy libre) |
| `staging` | Require reviewers: 1 persona |
| `production` | Require reviewers: 2 personas + Wait timer: 5 min |

4. Para `production`, también puedes restringir qué ramas pueden hacer deploy:
   - En "Deployment branches" → selecciona "Selected branches" → agrega `main`.

### 🧪 Ejercicio 4: Estructura de ramas por ambiente

```bash
# ══════════════════════════════════════════════
# Crear un proyecto con ramas por ambiente
# ══════════════════════════════════════════════
mkdir proyecto-environments
cd proyecto-environments
git init

cat > app.py << 'EOF'
"""Aplicación con manejo de ambientes."""
import os

ENV = os.getenv("APP_ENV", "development")

def get_config():
    configs = {
        "development": {"debug": True, "db": "localhost:5432/dev_db"},
        "staging":     {"debug": True, "db": "staging-server:5432/staging_db"},
        "production":  {"debug": False, "db": "prod-server:5432/prod_db"},
    }
    return configs.get(ENV, configs["development"])

def main():
    config = get_config()
    print(f"Ambiente: {ENV}")
    print(f"Debug: {config['debug']}")
    print(f"Base de datos: {config['db']}")

if __name__ == "__main__":
    main()
EOF

git add .
git commit -m "feat: crear app con configuración por ambiente"

# Crear ramas para cada ambiente
git checkout -b develop
git checkout -b staging
git checkout main

# Probar cada ambiente
echo ""
echo "═══ Probando Development ═══"
APP_ENV=development python3 app.py

echo ""
echo "═══ Probando Staging ═══"
APP_ENV=staging python3 app.py

echo ""
echo "═══ Probando Production ═══"
APP_ENV=production python3 app.py

# Ver todas las ramas
echo ""
echo "═══ Ramas creadas ═══"
git branch -a
```

---

## 7. GitHub Actions: Introducción a CI/CD

### Teoría

**GitHub Actions** es la herramienta de CI/CD integrada en GitHub. Permite automatizar tareas cuando ocurren eventos en tu repositorio.

```
┌──────────────────────────────────────────────────┐
│              GitHub Actions                       │
│                                                   │
│  EVENTO          WORKFLOW          RESULTADO       │
│  (trigger)       (automatización)  (output)        │
│                                                   │
│  push        →   Ejecutar tests  →  ✅ Pass       │
│  pull_request →  Lint + Tests    →  ❌ Fail       │
│  release     →   Build + Deploy  →  🚀 Deployed   │
│  schedule    →   Backup diario   →  📦 Stored     │
│                                                   │
└──────────────────────────────────────────────────┘
```

### Anatomía de un Workflow

Los workflows viven en `.github/workflows/` como archivos YAML:

```yaml
# .github/workflows/mi-workflow.yml

name: Nombre del Workflow         # Nombre visible en GitHub

on:                                # ¿Cuándo se ejecuta?
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:                              # ¿Qué tareas ejecutar?
  nombre-del-job:
    runs-on: ubuntu-latest         # ¿En qué máquina?
    steps:                         # Pasos secuenciales
      - name: Paso 1
        uses: actions/checkout@v4  # Acción predefinida
      - name: Paso 2
        run: echo "Hola mundo"     # Comando de terminal
```

### Conceptos clave

| Concepto | Descripción |
|---|---|
| **Workflow** | Proceso automatizado definido en YAML |
| **Event (on)** | Evento que dispara el workflow (push, PR, schedule, etc.) |
| **Job** | Conjunto de pasos que se ejecutan en la misma máquina virtual |
| **Step** | Una tarea individual dentro de un job |
| **Action** | Componente reutilizable (ej: `actions/checkout@v4`) |
| **Runner** | La máquina virtual donde se ejecuta el job |
| **Artifact** | Archivo generado durante un workflow que se puede descargar |
| **Secret** | Variable sensible almacenada de forma segura |

---

## 8. Primer workflow: Lint y Tests automáticos

### 🧪 Ejercicio 5: CI con Python

```bash
# ══════════════════════════════════════════════
# PASO 1: Crear estructura del proyecto
# ══════════════════════════════════════════════
mkdir proyecto-ci-cd
cd proyecto-ci-cd
git init

# Crear la app
cat > calculadora.py << 'EOF'
"""Calculadora simple para demostrar CI/CD."""


def sumar(a, b):
    """Suma dos números."""
    return a + b


def restar(a, b):
    """Resta dos números."""
    return a - b


def multiplicar(a, b):
    """Multiplica dos números."""
    return a * b


def dividir(a, b):
    """Divide dos números. Lanza ValueError si b es 0."""
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b
EOF

# Crear los tests
cat > test_calculadora.py << 'EOF'
"""Tests para la calculadora."""
import pytest
from calculadora import sumar, restar, multiplicar, dividir


def test_sumar():
    assert sumar(2, 3) == 5
    assert sumar(-1, 1) == 0
    assert sumar(0, 0) == 0


def test_restar():
    assert restar(5, 3) == 2
    assert restar(1, 1) == 0


def test_multiplicar():
    assert multiplicar(3, 4) == 12
    assert multiplicar(0, 100) == 0


def test_dividir():
    assert dividir(10, 2) == 5
    assert dividir(7, 2) == 3.5


def test_dividir_entre_cero():
    with pytest.raises(ValueError):
        dividir(10, 0)
EOF

# Crear requirements
cat > requirements.txt << 'EOF'
pytest==8.3.4
flake8==7.1.1
EOF

# ══════════════════════════════════════════════
# PASO 2: Crear el workflow de CI
# ══════════════════════════════════════════════
mkdir -p .github/workflows

cat > .github/workflows/ci.yml << 'EOF'
name: CI - Lint y Tests

# ¿Cuándo se ejecuta?
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    name: 🔍 Verificar estilo de código
    runs-on: ubuntu-latest
    steps:
      # Paso 1: Descargar el código del repo
      - name: Checkout del código
        uses: actions/checkout@v4

      # Paso 2: Instalar Python
      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      # Paso 3: Instalar dependencias
      - name: Instalar dependencias
        run: pip install -r requirements.txt

      # Paso 4: Ejecutar linter
      - name: Ejecutar flake8
        run: flake8 calculadora.py --max-line-length=100

  test:
    name: 🧪 Ejecutar tests
    runs-on: ubuntu-latest
    needs: lint                    # Solo corre si lint pasa
    steps:
      - name: Checkout del código
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Instalar dependencias
        run: pip install -r requirements.txt

      # Ejecutar tests con reporte de cobertura
      - name: Ejecutar pytest
        run: pytest test_calculadora.py -v --tb=short
EOF

# ══════════════════════════════════════════════
# PASO 3: Commit y push
# ══════════════════════════════════════════════

cat > .gitignore << 'EOF'
__pycache__/
*.pyc
.pytest_cache/
.venv/
venv/
.env
EOF

git add .
git commit -m "feat: agregar calculadora con CI (lint + tests)"

# Verificar localmente antes de hacer push
echo ""
echo "═══ Verificación local ═══"
echo "--- Lint ---"
pip install flake8 pytest --quiet 2>/dev/null
flake8 calculadora.py --max-line-length=100 && echo "✅ Lint OK" || echo "❌ Lint falló"

echo "--- Tests ---"
pytest test_calculadora.py -v --tb=short
```

Después de hacer push a GitHub, ve a la pestaña **Actions** de tu repositorio para ver el workflow ejecutándose.

---

## 9. Deploy automático a ambientes

### 🧪 Ejercicio 6: Workflow con múltiples ambientes

```bash
# ══════════════════════════════════════════════
# Crear workflow de deploy por ambientes
# ══════════════════════════════════════════════

cat > .github/workflows/deploy.yml << 'EOF'
name: Deploy por Ambientes

on:
  push:
    branches:
      - develop        # Trigger para Dev
      - staging        # Trigger para Staging
      - main           # Trigger para Producción

jobs:
  # ──────────────────────────────────────────
  # JOB 1: Tests (siempre corren primero)
  # ──────────────────────────────────────────
  tests:
    name: 🧪 Ejecutar tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest test_calculadora.py -v

  # ──────────────────────────────────────────
  # JOB 2: Deploy a Development
  # ──────────────────────────────────────────
  deploy-dev:
    name: 🔧 Deploy a Development
    needs: tests
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment:
      name: development
      url: https://dev.mi-app.com
    steps:
      - uses: actions/checkout@v4
      - name: Deploy a Dev
        run: |
          echo "🔧 Desplegando a DEVELOPMENT..."
          echo "Rama: ${{ github.ref_name }}"
          echo "Commit: ${{ github.sha }}"
          echo "Autor: ${{ github.actor }}"
          # Aquí irían los comandos reales de deploy
          # Ejemplo: aws s3 sync ./build s3://dev-bucket
          echo "✅ Deploy a Development exitoso"

  # ──────────────────────────────────────────
  # JOB 3: Deploy a Staging
  # ──────────────────────────────────────────
  deploy-staging:
    name: 🔎 Deploy a Staging
    needs: tests
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/staging'
    environment:
      name: staging
      url: https://staging.mi-app.com
    steps:
      - uses: actions/checkout@v4
      - name: Deploy a Staging
        run: |
          echo "🔎 Desplegando a STAGING..."
          echo "Rama: ${{ github.ref_name }}"
          echo "✅ Deploy a Staging exitoso"

  # ──────────────────────────────────────────
  # JOB 4: Deploy a Producción
  # ──────────────────────────────────────────
  deploy-prod:
    name: 🚀 Deploy a Producción
    needs: tests
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://mi-app.com
    steps:
      - uses: actions/checkout@v4
      - name: Deploy a Producción
        run: |
          echo "🚀 Desplegando a PRODUCCIÓN..."
          echo "Rama: ${{ github.ref_name }}"
          echo "Commit: ${{ github.sha }}"
          echo "✅ Deploy a Producción exitoso"
          echo ""
          echo "📊 Resumen del deploy:"
          echo "  Fecha: $(date)"
          echo "  Versión: $(git describe --tags --always)"
EOF

git add .
git commit -m "ci: agregar workflow de deploy por ambientes"
```

### Diagrama del flujo completo

```
  Desarrollador hace push a:

  develop  ──→  Tests ──→ ✅ ──→ Deploy Dev      (automático)
  staging  ──→  Tests ──→ ✅ ──→ Deploy Staging   (requiere aprobación)
  main     ──→  Tests ──→ ✅ ──→ Deploy Producción (requiere 2 aprobaciones + wait)
```

---

## 10. Workflows avanzados: Matrix, Secrets y Artifacts

### Matrix Strategy: Probar en múltiples versiones

```yaml
# .github/workflows/ci-matrix.yml
name: CI Matrix

on: [push, pull_request]

jobs:
  test:
    name: Python ${{ matrix.python-version }} en ${{ matrix.os }}
    runs-on: ${{ matrix.os }}

    # Ejecuta el job en TODAS las combinaciones
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']
        os: [ubuntu-latest, windows-latest, macos-latest]

    steps:
      - uses: actions/checkout@v4
      - name: Configurar Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: pytest test_calculadora.py -v
```

Esto genera **12 jobs** (4 versiones × 3 sistemas operativos).

### Secrets: Variables sensibles

Los secrets se configuran en **Settings → Secrets and variables → Actions**:

```yaml
# Usar un secret en un workflow
steps:
  - name: Deploy con credenciales
    run: |
      echo "Desplegando..."
      # El secret se inyecta como variable de entorno
      curl -X POST https://api.deploy.com \
        -H "Authorization: Bearer ${{ secrets.DEPLOY_TOKEN }}"
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

> ⚠️ **Nunca** pongas tokens, contraseñas o API keys directamente en el código YAML. Siempre usa secrets.

### Artifacts: Guardar archivos generados

```yaml
# Generar y guardar un reporte de tests
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt

      # Generar reporte en formato HTML
      - name: Ejecutar tests con reporte
        run: pytest test_calculadora.py -v --html=reporte.html --self-contained-html
        continue-on-error: true

      # Guardar el reporte como artifact
      - name: Subir reporte de tests
        uses: actions/upload-artifact@v4
        with:
          name: reporte-tests
          path: reporte.html
          retention-days: 30      # Se guarda por 30 días
```

Los artifacts se pueden descargar desde la pestaña **Actions** → seleccionar el workflow run → sección "Artifacts".

### 🧪 Ejercicio 7: Workflow con notificación

```bash
# Crear un workflow que notifique el resultado
cat > .github/workflows/notify.yml << 'EOF'
name: CI con Resumen

on:
  pull_request:
    branches: [main]

jobs:
  ci-completo:
    name: 🔄 Pipeline Completo
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Instalar dependencias
        run: pip install -r requirements.txt

      - name: Lint
        run: flake8 calculadora.py --max-line-length=100

      - name: Tests
        run: pytest test_calculadora.py -v

      # Agregar comentario automático al PR con el resumen
      - name: Comentar en el PR
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            const status = '${{ job.status }}';
            const emoji = status === 'success' ? '✅' : '❌';
            const body = `## ${emoji} Resultado del CI

            | Check | Estado |
            |-------|--------|
            | Lint (flake8) | ${status === 'success' ? '✅ Pasó' : '❌ Falló'} |
            | Tests (pytest) | ${status === 'success' ? '✅ Pasó' : '❌ Falló'} |

            **Commit:** \`${{ github.sha }}\`
            **Rama:** \`${{ github.head_ref }}\``;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
EOF

git add .
git commit -m "ci: agregar workflow con notificación en PRs"
```

---

## 11. Ejercicio integrador final

### Proyecto: "Data Pipeline con CI/CD"

Construir un repositorio completo que integre Gitflow, Branch Policies, Environments y GitHub Actions.

```bash
# ══════════════════════════════════════════════════════
# PASO 1: Crear el proyecto
# ══════════════════════════════════════════════════════
mkdir data-pipeline-cicd
cd data-pipeline-cicd
git init

# ── Estructura de carpetas ──
mkdir -p src tests .github/workflows

# ── Código principal ──
cat > src/pipeline.py << 'PYEOF'
"""
Data Pipeline - Proyecto Integrador
IU Digital de Antioquia
"""
import csv
import os
from io import StringIO


def extraer_datos(texto_csv):
    """Extrae datos desde un texto CSV."""
    reader = csv.DictReader(StringIO(texto_csv))
    return list(reader)


def transformar_datos(datos):
    """Limpia y transforma los datos."""
    transformados = []
    for registro in datos:
        limpio = {
            "nombre": registro.get("nombre", "").strip().title(),
            "edad": int(registro.get("edad", 0)),
            "ciudad": registro.get("ciudad", "").strip().title(),
        }
        if limpio["edad"] > 0:
            transformados.append(limpio)
    return transformados


def cargar_datos(datos, formato="texto"):
    """Genera la salida de los datos procesados."""
    if formato == "texto":
        lineas = []
        for d in datos:
            lineas.append(f"{d['nombre']}, {d['edad']} años, {d['ciudad']}")
        return "\n".join(lineas)
    elif formato == "csv":
        if not datos:
            return "nombre,edad,ciudad"
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=datos[0].keys())
        writer.writeheader()
        writer.writerows(datos)
        return output.getvalue().strip()


def ejecutar_pipeline(texto_csv):
    """Ejecuta el pipeline ETL completo."""
    env = os.getenv("APP_ENV", "development")
    print(f"🔄 Ejecutando pipeline en ambiente: {env}")

    datos_crudos = extraer_datos(texto_csv)
    print(f"📥 Extraídos: {len(datos_crudos)} registros")

    datos_limpios = transformar_datos(datos_crudos)
    print(f"🔧 Transformados: {len(datos_limpios)} registros válidos")

    resultado = cargar_datos(datos_limpios)
    print(f"📤 Cargados exitosamente")

    return datos_limpios
PYEOF

# ── Tests ──
cat > tests/test_pipeline.py << 'PYEOF'
"""Tests del Data Pipeline."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pipeline import extraer_datos, transformar_datos, cargar_datos, ejecutar_pipeline


CSV_EJEMPLO = """nombre,edad,ciudad
Ana,25,medellín
Carlos,30,bogotá
,0,
Diana,28, cali """


def test_extraer_datos():
    datos = extraer_datos(CSV_EJEMPLO)
    assert len(datos) == 4
    assert datos[0]["nombre"] == "Ana"


def test_transformar_datos():
    datos = extraer_datos(CSV_EJEMPLO)
    resultado = transformar_datos(datos)
    assert len(resultado) == 3  # El registro vacío se filtra
    assert resultado[0]["nombre"] == "Ana"
    assert resultado[0]["ciudad"] == "Medellín"  # .title()
    assert resultado[2]["ciudad"] == "Cali"       # strip + title


def test_cargar_texto():
    datos = [{"nombre": "Ana", "edad": 25, "ciudad": "Medellín"}]
    texto = cargar_datos(datos, formato="texto")
    assert "Ana" in texto
    assert "25 años" in texto


def test_cargar_csv():
    datos = [{"nombre": "Ana", "edad": 25, "ciudad": "Medellín"}]
    csv_out = cargar_datos(datos, formato="csv")
    assert "nombre,edad,ciudad" in csv_out
    assert "Ana" in csv_out


def test_pipeline_completo():
    resultado = ejecutar_pipeline(CSV_EJEMPLO)
    assert len(resultado) == 3
    assert all(r["edad"] > 0 for r in resultado)
PYEOF

# ── Requirements ──
cat > requirements.txt << 'EOF'
pytest==8.3.4
flake8==7.1.1
EOF

# ── Workflow de CI/CD ──
cat > .github/workflows/pipeline-ci-cd.yml << 'EOF'
name: Data Pipeline CI/CD

on:
  push:
    branches: [main, develop, staging]
  pull_request:
    branches: [main, develop]

jobs:
  # ── Calidad de código ──
  lint:
    name: 🔍 Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install flake8
      - run: flake8 src/ --max-line-length=100

  # ── Tests ──
  test:
    name: 🧪 Tests
    needs: lint
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --tb=short

  # ── Deploy Dev ──
  deploy-dev:
    name: 🔧 Deploy Dev
    needs: test
    if: github.ref == 'refs/heads/develop' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment:
      name: development
    steps:
      - uses: actions/checkout@v4
      - run: echo "🔧 Desplegado en Development - $(date)"

  # ── Deploy Staging ──
  deploy-staging:
    name: 🔎 Deploy Staging
    needs: test
    if: github.ref == 'refs/heads/staging' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment:
      name: staging
    steps:
      - uses: actions/checkout@v4
      - run: echo "🔎 Desplegado en Staging - $(date)"

  # ── Deploy Production ──
  deploy-prod:
    name: 🚀 Deploy Production
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment:
      name: production
    steps:
      - uses: actions/checkout@v4
      - run: echo "🚀 Desplegado en Producción - $(date)"
EOF

# ── README ──
cat > README.md << 'EOF'
# 📊 Data Pipeline con CI/CD

Proyecto integrador del Taller de Git Workflows, Environments y GitHub Actions.

## Estructura

```
data-pipeline-cicd/
├── src/
│   └── pipeline.py           # Pipeline ETL
├── tests/
│   └── test_pipeline.py      # Tests automatizados
├── .github/
│   └── workflows/
│       └── pipeline-ci-cd.yml # CI/CD con GitHub Actions
├── requirements.txt
├── .gitignore
└── README.md
```

## Pipeline

El pipeline ejecuta tres etapas:
1. **Extraer** → Lee datos desde CSV
2. **Transformar** → Limpia nombres, valida edades, normaliza ciudades
3. **Cargar** → Genera salida en texto o CSV

## CI/CD

| Rama | Ambiente | Aprobación |
|------|----------|------------|
| `develop` | Development | Automático |
| `staging` | Staging | 1 reviewer |
| `main` | Production | 2 reviewers |

## Ejecutar localmente

```bash
pip install -r requirements.txt
pytest tests/ -v
```
EOF

# ── .gitignore ──
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
.pytest_cache/
.venv/
venv/
.env
EOF

# ══════════════════════════════════════════════════════
# PASO 2: Commits iniciales con Gitflow
# ══════════════════════════════════════════════════════
git add .
git commit -m "feat: crear data pipeline con CI/CD completo"
git tag -a v1.0 -m "Release v1.0 - pipeline inicial"

# Crear ramas de ambientes
git checkout -b develop
git checkout -b staging
git checkout main

# ══════════════════════════════════════════════════════
# PASO 3: Verificar todo localmente
# ══════════════════════════════════════════════════════
echo ""
echo "═══════════════════════════════════════"
echo "  Verificación local del proyecto"
echo "═══════════════════════════════════════"
echo ""
echo "--- Lint ---"
flake8 src/ --max-line-length=100 && echo "✅ Lint OK"
echo ""
echo "--- Tests ---"
pytest tests/ -v --tb=short
echo ""
echo "--- Ramas ---"
git branch -a
echo ""
echo "--- Historial ---"
git log --oneline --graph --all
```

### ✅ Criterios de evaluación

| Criterio | Puntos |
|---|---|
| Repositorio con estructura correcta (src/, tests/, .github/) | 15 |
| Al menos 5 commits con Conventional Commits | 15 |
| Uso de al menos 2 ramas (feature + develop) fusionadas | 15 |
| Archivo `.gitignore` apropiado | 5 |
| Tests que pasen (`pytest`) | 15 |
| Workflow de CI que ejecute lint + tests | 15 |
| Workflow con deploy a al menos 2 ambientes | 10 |
| Branch protection configurada en `main` | 5 |
| README claro con instrucciones | 5 |
| **Total** | **100** |

---

## 12. Cheat Sheet de Workflows y Actions

### Gitflow

```bash
git checkout -b develop                        # Crear develop
git checkout -b feature/nombre develop         # Feature desde develop
git checkout develop && git merge --no-ff feature/nombre  # Merge feature
git checkout -b release/1.0 develop            # Preparar release
git checkout main && git merge --no-ff release/1.0        # Release a main
git tag -a v1.0 -m "Release 1.0"              # Etiquetar versión
git checkout -b hotfix/nombre main             # Hotfix desde main
```

### GitHub Flow

```bash
git checkout -b feature/nombre main            # Feature desde main
git push origin feature/nombre                 # Push de la rama
# → Abrir PR en GitHub → Review → Merge
git checkout main && git pull                  # Actualizar local
```

### Branch Protection

```
Settings → Branches → Add rule → main
  ☑ Require pull request
  ☑ Require approvals
  ☑ Require status checks
```

### GitHub Actions (sintaxis esencial)

```yaml
name: Nombre
on: [push, pull_request]                       # Eventos
on:
  push:
    branches: [main]                           # Solo en main
  schedule:
    - cron: '0 9 * * 1'                        # Lunes a las 9am UTC

jobs:
  mi-job:
    runs-on: ubuntu-latest                     # Runner
    needs: otro-job                            # Dependencia
    if: github.ref == 'refs/heads/main'        # Condicional
    environment: production                    # Ambiente
    steps:
      - uses: actions/checkout@v4              # Acción
      - run: comando                           # Shell
      - run: |                                 # Multi-línea
          comando1
          comando2
    env:
      MI_VAR: valor                            # Variable de entorno
      SECRET: ${{ secrets.MI_SECRET }}         # Secret
```

### Environments

```
Settings → Environments → New environment
  development  → Sin restricciones
  staging      → 1 reviewer requerido
  production   → 2 reviewers + wait timer + solo rama main
```

---

> 💡 **Recursos adicionales:**
> - [Documentación de GitHub Actions](https://docs.github.com/es/actions)
> - [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
> - [Gitflow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)
> - [Entender el YAML de Actions](https://docs.github.com/es/actions/writing-workflows)

---

*Taller diseñado para la IU Digital de Antioquia por Darkanita* 🐧
