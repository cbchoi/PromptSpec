# Docker Development Image

The root `Dockerfile` builds a development image with the dependencies needed
for the blocked browser and desktop gates:

- Python 3 and project dev dependencies
- Node 20 and Corepack/pnpm
- Playwright Chromium and required Linux libraries
- Stable Rust/Cargo installed through rustup
- Tauri Linux build libraries, including WebKitGTK, AppIndicator, and xdo

## Build

```bash
docker build -t promptspec-dev .
```

## Run

```bash
docker run --rm -it -p 3000:3000 -p 8000:8000 -v "$PWD":/workspace promptspec-dev
```

Inside the container:

```bash
python -m pytest tests/unit tests/scenario tests/integration
ruff check .
mypy
corepack pnpm --filter promptspec-web typecheck
corepack pnpm --filter promptspec-web lint
corepack pnpm --filter promptspec-web build
corepack pnpm --filter promptspec-web test
corepack pnpm --filter promptspec-desktop check
corepack pnpm --filter promptspec-desktop build
python quality_gate.py
```

Python dependencies are installed into `/opt/venv`, so bind-mounting the repo
over `/workspace` does not hide them. If the repo is bind-mounted, reinstall
the Node dependencies inside the running container after mounting:

```bash
corepack pnpm install
corepack pnpm --filter promptspec-web exec playwright install chromium
```
