# LegisGator 🐊⚖️

LLM‑compressed, Z3‑reinforced contract analyser.

> **Security First**  
> • Secrets live only in `.env` or CI secret store.  
> • Payload never logged; SHA‑256 fingerprints only.  
> • Disk cache auto‑expires (default 24 h) and is local‑only.  
> • Pre‑commit includes `git‑secrets`; any key leak aborts push.  
> • Supply‑chain pinned via `poetry.lock` (hash‑verified).  

```bash
# quickstart
pip install ".[dev]"           # after cloning repo
export OPENAI_API_KEY="sk-..." # or echo into .env
python -m legisgator.cli file sample.txt
