# Bug Fixes

This document outlines the 10 specific bugs identified and fixed to make the application production-ready.

## 1. frontend/app.js
- **Line(s)**: 6
- **Problem**: The API URL was permanently hardcoded to `http://localhost:8000`, causing connections to fail when running inside a Docker network.
- **Fix**: Replaced hardcoded URL with dynamic environment variable fallback: `const API_URL = process.env.API_URL || "http://localhost:8000";`.

## 2. frontend/app.js
- **Line(s)**: 10
- **Problem**: No dedicated healthcheck endpoint existed for Docker to reliably poll the backend.
- **Fix**: Added new GET endpoint `app.get('/health', (req, res) => { res.status(200).json({ message: 'healthy' }); });`.

## 3. frontend/package.json
- **Line(s)**: 12-14
- **Problem**: The pipeline validation mandates ESLint, but `eslint` was entirely missing from `package.json`, causing CI lint failures.
- **Fix**: Appended `"eslint": "^8.50.0"` to `"devDependencies"`.

## 4. api/main.py
- **Line(s)**: 1-14
- **Problem**: CORS configuration middleware was absent, preventing proper cross-origin protections and headers.
- **Fix**: Imported `from fastapi.middleware.cors import CORSMiddleware` and attached `app.add_middleware(CORSMiddleware...)`.

## 5. api/main.py
- **Line(s)**: 16-20
- **Problem**: The Redis connection failed to coherently map all three properties (host, port, password) robustly via environment variables together, leading to failures depending on container context.
- **Fix**: Added `host=os.getenv("REDIS_HOST", "redis")`, `port=int(os.getenv("REDIS_PORT", 6379))`, and `password=os.getenv("REDIS_PASSWORD", None)`.

## 6. worker/worker.py
- **Line(s)**: 7
- **Problem**: Redis connection was rigidly hardcoded to `host="localhost"` breaking worker connectivity isolated in containers.
- **Fix**: Integrated exact same environment mappings logic from API: `r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=int(os.getenv("REDIS_PORT", 6379)), password=os.getenv('REDIS_PASSWORD', None))`.

## 7. worker/worker.py
- **Line(s)**: 12-19
- **Problem**: Worker processes lacked graceful termination routines, meaning docker SIGTERM signals would abruptly sever in-flight work.
- **Fix**: Bound the imported `signal` module to a custom `graceful_shutdown` loop handler using `signal.signal(signal.SIGTERM...)`.

## 8. api/requirements.txt
- **Line(s)**: 1-3
- **Problem**: Dependencies (`fastapi`, `uvicorn`, `redis`) floated on generic versions risking unanticipated breaking changes breaking production container builds.
- **Fix**: Enforced exact strict requirements pinning via `==` logic (`fastapi==0.103.1`, etc).

## 9. worker/requirements.txt
- **Line(s)**: 1
- **Problem**: Worker dependencies (`redis`) floated without explicitly pinned versions.
- **Fix**: Explicitly enforced exact `redis==5.0.1` pinning.

## 10. api/.env (Git History)
- **Problem**: An environment variables file `.env` intrinsically designed for secrets was maliciously/accidentally committed into origin repository timeline.
- **Fix**: Completely scraped the Git index aggressively forcing historical deletion running `git filter-branch --force --index-filter "git rm --cached --ignore-unmatch api/.env" --prune-empty --tag-name-filter cat -- --all`.
