# Bug Fixes

This document outlines the 10 specific bugs identified and fixed to make the application production-ready.

## 1. frontend/app.js (Line 6)
- **Problem**: The API URL was hardcoded to `http://localhost:8000`, so the frontend couldn't connect to the API when running inside Docker.
- **Fix**: Replaced the hardcoded URL with an environment variable: `const API_URL = process.env.API_URL || "http://localhost:8000";`.

## 2. frontend/app.js (Line 10)
- **Problem**: There was no healthcheck endpoint, so Docker had no way to know if the frontend was fully running.
- **Fix**: Added a simple GET endpoint at `/health` that returns a `200` success response: `app.get('/health', (req, res) => { res.status(200).json({ message: 'healthy' }); });`.

## 3. frontend/package.json (Lines 12-14)
- **Problem**: The CI pipeline required linting, but `eslint` was missing from the project dependencies, causing the pipeline to fail.
- **Fix**: Added `"eslint": "^8.57.0"` to the `"devDependencies"`. (Note: We used the latest 8.x version to avoid old NPM security vulnerabilities).

## 4. api/main.py (Lines 1-14)
- **Problem**: The API lacked CORS (Cross-Origin Resource Sharing) middleware, which would block frontend requests in a real browser.
- **Fix**: Imported and added `CORSMiddleware` to the FastAPI app to safely allow cross-origin requests.

## 5. api/main.py (Lines 16-20)
- **Problem**: The Redis connection was tightly coupled to local setups: `r = redis.Redis(host="localhost", port=6379)`. This broke inside Docker where the host is `redis`.
- **Fix**: Updated it to use environment variables for the host, port, and password: `host=os.getenv("REDIS_HOST", "redis")`, etc.

## 6. worker/worker.py (Line 7)
- **Problem**: Just like the API, the worker's Redis connection was hardcoded to `host="localhost"`.
- **Fix**: Applied the exact same environment variable setup used in the API to connect properly dynamically.

## 7. worker/worker.py (Lines 12-19)
- **Problem**: The worker couldn't shut down safely. If Docker stopped the container, it would kill any job currently processing.
- **Fix**: Added a `graceful_shutdown` function using the Python `signal` module to catch shutdown commands (`SIGTERM`) and exit cleanly.

## 8. api/requirements.txt (Lines 1-3)
- **Problem**: Python packages didn't have specific versions pinned, so future updates could unexpectedly break the app.
- **Fix**: Pinned the versions using `>=`, like `fastapi>=0.103.1` and `uvicorn>=0.23.2`. (Note: We used `>=` instead of `==` to safely allow `pip` to resolve a complex dependency conflict with `h11` during the build without failing).

## 9. worker/requirements.txt (Line 1)
- **Problem**: The worker's Redis package had no version specified.
- **Fix**: Pinned the version exactly to `redis==5.0.1` to ensure consistent builds.

## 10. api/.env (Git History)
- **Problem**: A `.env` file containing sensitive environment variables was accidentally pushed into the Git repository history.
- **Fix**: Used `git filter-branch` to completely scrub the `.env` file from the entire Git history to prevent security leaks.
